#!/usr/bin/env bash
# =============================================================================
# provision.sh - khởi tạo dữ liệu cấu hình cho hệ thống nuôi tôm (chạy 1 lần, chạy lại an toàn)
#   1. Service group trên IoT Agent (apikey -> entity type Pond)
#   2. N thiết bị ao (pond001..pondN) <-> entity urn:ngsi-ld:Pond:001..N
#   3. Subscription Orion -> QuantumLeap (ghi lịch sử vào CrateDB)
#
# Chạy (Git Bash / Linux / macOS):   bash source/provision.sh
# Đổi cấu hình bằng biến môi trường, ví dụ:  N_PONDS=10 bash source/provision.sh
# Dọn sạch thiết bị và entity cũ rồi khai báo lại:  RESET=1 bash source/provision.sh
#   (nên dừng simulator trước khi RESET, nếu không IoT Agent sẽ tự tạo lại thiết bị)
# =============================================================================
set -euo pipefail

ORION_URL="${ORION_URL:-http://localhost:1026}"          # gọi từ máy bạn
IOTA_URL="${IOTA_URL:-http://localhost:4041}"            # gọi từ máy bạn
FIWARE_SERVICE="${FIWARE_SERVICE:-shrimp}"
FIWARE_SERVICEPATH="${FIWARE_SERVICEPATH:-/}"
APIKEY="${APIKEY:-shrimpkey}"
N_PONDS="${N_PONDS:-5}"
# Địa chỉ BÊN TRONG mạng Docker (các container gọi nhau, không phải localhost)
CB_INTERNAL="${CB_INTERNAL:-http://orion:1026}"
QL_INTERNAL="${QL_INTERNAL:-http://quantumleap:8668/v2/notify}"
NR_INTERNAL="${NR_INTERNAL:-http://node-red:1880/notify}"

HDR_NOBODY=(-H "fiware-service: ${FIWARE_SERVICE}" -H "fiware-servicepath: ${FIWARE_SERVICEPATH}")
HDR=("${HDR_NOBODY[@]}" -H "Content-Type: application/json")
RESET="${RESET:-0}"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

wait_for() {  # url, tên
  local i
  for i in $(seq 1 30); do
    if curl -fs -o /dev/null "$1"; then echo "  sẵn sàng: $2"; return 0; fi
    sleep 2
  done
  echo "  KHÔNG kết nối được $2 ($1). Hãy kiểm tra 'docker compose ps'." >&2
  exit 1
}

post() {  # url, body, nhãn
  local code
  code="$(curl -s -o "$TMP" -w '%{http_code}' -X POST "$1" "${HDR[@]}" -d "$2" || true)"
  case "$code" in
    2??) echo "  OK    $3" ;;
    409) echo "  BỎ QUA $3 (đã tồn tại)" ;;
    *)   echo "  LỖI   $3 (HTTP $code)" >&2; cat "$TMP" >&2; echo >&2; exit 1 ;;
  esac
}

echo "== 0. Kiểm tra dịch vụ =="
wait_for "${ORION_URL}/version" "Orion"
wait_for "${IOTA_URL}/iot/about" "IoT Agent"

if [[ "${RESET}" == "1" ]]; then
  echo "== RESET: xoá thiết bị và entity cũ =="
  for i in $(seq 1 "${N_PONDS}"); do
    DEV="$(printf 'pond%03d' "$i")"
    ENT="$(printf 'urn:ngsi-ld:Pond:%03d' "$i")"
    # Có thể có nhiều thiết bị cùng device_id (khác apikey): xoá lặp tới khi hết
    for _ in 1 2 3; do
      code="$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "${IOTA_URL}/iot/devices/${DEV}" "${HDR_NOBODY[@]}" || true)"
      [[ "$code" == 2?? ]] || break
    done
    curl -s -o /dev/null -X DELETE "${ORION_URL}/v2/entities/${ENT}?type=Pond" "${HDR_NOBODY[@]}" || true
    curl -s -o /dev/null -X DELETE "${ORION_URL}/v2/entities/Pond:${DEV}?type=Pond" "${HDR_NOBODY[@]}" || true
    echo "  đã dọn ${DEV}"
  done
fi

echo "== 1. Service group (apikey=${APIKEY}) =="
post "${IOTA_URL}/iot/services" "{
  \"services\": [{
    \"apikey\": \"${APIKEY}\",
    \"cbroker\": \"${CB_INTERNAL}\",
    \"entity_type\": \"Pond\",
    \"resource\": \"/iot/json\"
  }]
}" "service group"

echo "== 2. Thiết bị ao (${N_PONDS}) =="
for i in $(seq 1 "${N_PONDS}"); do
  DEV="$(printf 'pond%03d' "$i")"
  ENT="$(printf 'urn:ngsi-ld:Pond:%03d' "$i")"
  post "${IOTA_URL}/iot/devices" "{
    \"devices\": [{
      \"device_id\": \"${DEV}\",
      \"apikey\": \"${APIKEY}\",
      \"entity_name\": \"${ENT}\",
      \"entity_type\": \"Pond\",
      \"protocol\": \"IoTA-JSON\",
      \"transport\": \"MQTT\",
      \"timezone\": \"Asia/Ho_Chi_Minh\",
      \"attributes\": [
        {\"object_id\": \"do\", \"name\": \"dissolvedOxygen\", \"type\": \"Number\"},
        {\"object_id\": \"ph\", \"name\": \"pH\",              \"type\": \"Number\"},
        {\"object_id\": \"t\",  \"name\": \"temperature\",     \"type\": \"Number\"},
        {\"object_id\": \"s\",  \"name\": \"salinity\",        \"type\": \"Number\"},
        {\"object_id\": \"a\",  \"name\": \"aeratorState\",    \"type\": \"Text\"}
      ],
      \"commands\": [
        {\"name\": \"aerator\", \"type\": \"command\"}
      ]
    }]
  }" "thiết bị ${DEV} -> ${ENT}"
done

echo "== 3. Subscription Orion -> QuantumLeap =="
if curl -s "${ORION_URL}/v2/subscriptions" "${HDR[@]}" | grep -q "Notify QuantumLeap"; then
  echo "  BỎ QUA subscription (đã tồn tại)"
else
  post "${ORION_URL}/v2/subscriptions" "{
    \"description\": \"Notify QuantumLeap of pond changes\",
    \"subject\": {
      \"entities\": [{\"idPattern\": \".*\", \"type\": \"Pond\"}],
      \"condition\": {\"attrs\": [\"dissolvedOxygen\", \"pH\", \"temperature\", \"salinity\"]}
    },
    \"notification\": {
      \"http\": {\"url\": \"${QL_INTERNAL}\"},
      \"metadata\": [\"dateCreated\", \"dateModified\"]
    }
  }" "subscription -> QuantumLeap"
fi

echo "== 4. Subscription Orion -> Node-RED (Rule Engine) =="
if curl -s "${ORION_URL}/v2/subscriptions" "${HDR[@]}" | grep -q "Notify Node-RED"; then
  echo "  BỎ QUA subscription Node-RED (đã tồn tại)"
else
  post "${ORION_URL}/v2/subscriptions" "{
    \"description\": \"Notify Node-RED of pond changes\",
    \"subject\": {
      \"entities\": [{\"idPattern\": \".*\", \"type\": \"Pond\"}],
      \"condition\": {\"attrs\": [\"dissolvedOxygen\", \"pH\", \"temperature\", \"salinity\"]}
    },
    \"notification\": {
      \"http\": {\"url\": \"${NR_INTERNAL}\"},
      \"attrsFormat\": \"keyValues\"
    }
  }" "subscription -> Node-RED"
fi

cat <<EOF

Xong. Kiểm tra:
  curl -s -H "fiware-service: ${FIWARE_SERVICE}" -H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \\
       "${ORION_URL}/v2/entities?type=Pond&options=keyValues"
Rồi chạy simulator:  python source/simulator.py --ponds ${N_PONDS} --apikey ${APIKEY}
EOF