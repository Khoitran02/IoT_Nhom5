#!/usr/bin/env python3
"""
setup_emqx_bridge.py - Thiết lập MQTT Bridge 2 chiều giữa local EMQX và public broker.emqx.io
Hỗ trợ Wokwi ESP32 chạy trên trình duyệt nối qua public broker về FIWARE stack local.

Topics trên broker.emqx.io (độc nhất để tránh xung đột):
  iot_nhom5_shrimp/pond001/attrs  -> Local /shrimpkey/pond001/attrs
  iot_nhom5_shrimp/pond001/cmdexe -> Local /shrimpkey/pond001/cmdexe
  Local /shrimpkey/pond001/cmd    -> Remote iot_nhom5_shrimp/pond001/cmd

  Tương tự cho pond002.
"""
import urllib.request
import json
import sys

EMQX_API = "http://127.0.0.1:18083/api/v5"
PUBLIC_BROKER = "broker.emqx.io:1883"
TOPIC_PREFIX = "iot_nhom5_shrimp_c8d2"

def get_token():
    req = urllib.request.Request(
        f"{EMQX_API}/login",
        data=json.dumps({"username": "admin", "password": "change-me-emqx"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())["token"]

def list_bridges(token):
    req = urllib.request.Request(f"{EMQX_API}/bridges", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def delete_bridge(token, bridge_id):
    req = urllib.request.Request(
        f"{EMQX_API}/bridges/{bridge_id}",
        headers={"Authorization": f"Bearer {token}"},
        method="DELETE"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Deleted bridge {bridge_id}: {resp.status}")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"Error deleting {bridge_id}: {e}")

def create_bridge(token, payload):
    name = payload["name"]
    req = urllib.request.Request(
        f"{EMQX_API}/bridges",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            status = data.get("status", "unknown")
            print(f"Created bridge {name}: status={status}")
            return True
    except urllib.error.HTTPError as e:
        print(f"Failed to create bridge {name}: {e.code} - {e.read().decode()}")
        return False

def main():
    print("1. Authenticating with local EMQX...")
    token = get_token()
    print("   Auth OK.")

    # Xóa các bridge cũ liên quan đến wokwi nếu có
    existing = list_bridges(token)
    for b in existing:
        bid = f"{b.get('type')}:{b.get('name')}"
        if "wokwi" in b.get("name", ""):
            print(f"Removing old bridge: {bid}")
            delete_bridge(token, bid)

    bridges_to_create = []

    PONDS = [f"pond{i:03d}" for i in range(1, 6)] # pond001 .. pond005 (Toan bo 5 ao Wokwi)

    for pond_id in PONDS:
        # 1. Ingress attrs: Remote -> Local
        bridges_to_create.append({
            "type": "mqtt",
            "name": f"wokwi_in_{pond_id}_attrs",
            "server": PUBLIC_BROKER,
            "proto_ver": "v4",
            "ingress": {
                "remote": {
                    "topic": f"{TOPIC_PREFIX}/{pond_id}/attrs",
                    "qos": 1
                },
                "local": {
                    "topic": f"/shrimpkey/{pond_id}/attrs",
                    "payload": "${payload}",
                    "qos": 1
                }
            }
        })

        # 2. Ingress cmdexe: Remote -> Local
        bridges_to_create.append({
            "type": "mqtt",
            "name": f"wokwi_in_{pond_id}_cmdexe",
            "server": PUBLIC_BROKER,
            "proto_ver": "v4",
            "ingress": {
                "remote": {
                    "topic": f"{TOPIC_PREFIX}/{pond_id}/cmdexe",
                    "qos": 1
                },
                "local": {
                    "topic": f"/shrimpkey/{pond_id}/cmdexe",
                    "payload": "${payload}",
                    "qos": 1
                }
            }
        })

        # 3. Egress cmd: Local -> Remote
        bridges_to_create.append({
            "type": "mqtt",
            "name": f"wokwi_out_{pond_id}_cmd",
            "server": PUBLIC_BROKER,
            "proto_ver": "v4",
            "egress": {
                "local": {
                    "topic": f"/shrimpkey/{pond_id}/cmd"
                },
                "remote": {
                    "topic": f"{TOPIC_PREFIX}/{pond_id}/cmd",
                    "payload": "${payload}",
                    "qos": 1
                }
            }
        })

    print(f"2. Creating {len(bridges_to_create)} MQTT bridges...")
    success_count = 0
    for b in bridges_to_create:
        if create_bridge(token, b):
            success_count += 1

    print(f"\nCompleted: {success_count}/{len(bridges_to_create)} bridges active.")
    if success_count == len(bridges_to_create):
        print("MQTT Bridge setup SUCCESSFUL!")
    else:
        print("Some bridges failed. Please check logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()

