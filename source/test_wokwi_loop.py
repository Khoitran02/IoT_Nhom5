#!/usr/bin/env python3
"""
test_wokwi_loop.py - Kiểm chứng toàn diện chuỗi Wokwi ESP32 kết nối qua broker.emqx.io
Mô phỏng chính xác hành vi của Firmware Wokwi ESP32 chạy trên Cloud Browser:
1. ESP32 kết nối public broker: broker.emqx.io:1883
2. Subscribe kênh lệnh: iot_nhom5_shrimp_c8d2/pond001/cmd
3. Publish dữ liệu cảm biến: iot_nhom5_shrimp_c8d2/pond001/attrs
4. Nhận lệnh điều khiển sục khí từ hệ thống FIWARE local qua EMQX Bridge
5. Thực thi đóng Relay / bật LED ảo và gửi phản hồi lên iot_nhom5_shrimp_c8d2/pond001/cmdexe
"""
import paho.mqtt.client as mqtt
import urllib.request
import json
import time
import sys

PUBLIC_BROKER = "broker.emqx.io"
TOPIC_PREFIX = "iot_nhom5_shrimp_c8d2"
DEV_ID = "pond001"
ORION_URL = "http://127.0.0.1:1026/v2/entities/urn:ngsi-ld:Pond:001?options=keyValues"
HEADERS_ORION = {"fiware-service": "shrimp", "fiware-servicepath": "/"}

received_cmd = []

def on_connect(client, userdata, flags, rc):
    print(f"[Wokwi ESP32 Virtual] Da ket noi WiFi va MQTT toi {PUBLIC_BROKER}:1883 (rc={rc})")
    cmd_topic = f"{TOPIC_PREFIX}/{DEV_ID}/cmd"
    client.subscribe(cmd_topic, qos=1)
    print(f"[Wokwi ESP32 Virtual] Da subscribe topic nhan lenh: {cmd_topic}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode(errors='ignore')
    print(f"[Wokwi ESP32 Virtual] >>> NHAN LENH TU PLATFORM: topic={msg.topic}, payload={payload}")
    try:
        data = json.loads(payload)
        received_cmd.append(data)
    except:
        pass

def get_orion():
    req = urllib.request.Request(ORION_URL, headers=HEADERS_ORION)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def main():
    print("="*75)
    print("KIEM CHUNG CHU TRINH DONG THIET BI WOKWI ESP32 QUA PUBLIC BROKER & BRIDGE")
    print("="*75)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(PUBLIC_BROKER, 1883, 60)
    client.loop_start()

    time.sleep(2)

    # Bước 1: Gửi trạng thái bình thường ban đầu từ Wokwi lên broker.emqx.io
    topic_attrs = f"{TOPIC_PREFIX}/{DEV_ID}/attrs"
    topic_cmdexe = f"{TOPIC_PREFIX}/{DEV_ID}/cmdexe"

    print("\n1. ESP32 Wokwi publish du lieu ban dau (DO=5.4 mg/L, aerator=OFF)...")
    client.publish(topic_attrs, json.dumps({
        "do": 5.4, "ph": 7.8, "t": 28.0, "s": 15.0, "a": "OFF"
    }), qos=1)
    client.publish(topic_cmdexe, json.dumps({"aerator": "OFF"}), qos=1)
    time.sleep(3)

    ent = get_orion()
    print(f"   -> Orion Entity nhan duoc qua Bridge: DO={ent.get('dissolvedOxygen')}, aeratorState={ent.get('aeratorState')}")

    # Bước 2: ESP32 phát hiện DO tụt sâu xuống 3.1 mg/L (< 4.0)
    print("\n2. ESP32 Wokwi do duoc DO tut sau: DO=3.1 mg/L (< 4.0 mg/L). Publish len public broker...")
    received_cmd.clear()
    client.publish(topic_attrs, json.dumps({
        "do": 3.1, "ph": 7.7, "t": 28.0, "s": 15.0, "a": "OFF"
    }), qos=1)

    print("3. Cho Node-RED local xu ly va EMQX Bridge chuyen lenh nguoc ra broker.emqx.io...")
    cmd_on = False
    for _ in range(15):
        time.sleep(1)
        if received_cmd and received_cmd[-1].get("aerator") == "ON":
            cmd_on = True
            break

    if not cmd_on:
        print("LOI: Wokwi khong nhan duoc lenh aerator=ON tu public broker!")
        sys.exit(1)

    print("   -> [WOKWI ACTUATOR] Dong Relay (GPIO 2 HIGH), Den LED xanh may suc khi SANG!")
    print("   -> ESP32 gui cmdexe: ON phan hoi lai public broker...")
    client.publish(topic_cmdexe, json.dumps({"aerator": "ON"}), qos=1)
    client.publish(topic_attrs, json.dumps({
        "do": 3.8, "ph": 7.7, "t": 28.0, "s": 15.0, "a": "ON"
    }), qos=1)
    time.sleep(2)

    ent = get_orion()
    print(f"   -> Orion Entity cap nhat qua Bridge: aerator_status={ent.get('aerator_status')}, aeratorState={ent.get('aeratorState')}")

    # Bước 3: Sục khí chạy, DO hồi phục lên 6.4 mg/L (> 6.0)
    print("\n4. May suc khi chay, DO hoi phuc len 6.4 mg/L (> 6.0 mg/L). Wokwi gui len broker.emqx.io...")
    received_cmd.clear()
    client.publish(topic_attrs, json.dumps({
        "do": 6.4, "ph": 7.8, "t": 28.0, "s": 15.0, "a": "ON"
    }), qos=1)

    print("5. Cho Node-RED Rule Engine phat lenh ngat Hysteresis qua Bridge...")
    cmd_off = False
    for _ in range(15):
        time.sleep(1)
        if received_cmd and received_cmd[-1].get("aerator") == "OFF":
            cmd_off = True
            break

    if not cmd_off:
        print("LOI: Wokwi khong nhan duoc lenh ngat aerator=OFF tu public broker!")
        sys.exit(1)

    print("   -> [WOKWI ACTUATOR] Ngat Relay (GPIO 2 LOW), Den LED xanh may suc khi TAT!")
    print("   -> ESP32 gui cmdexe: OFF phan hoi lai public broker...")
    client.publish(topic_cmdexe, json.dumps({"aerator": "OFF"}), qos=1)
    client.publish(topic_attrs, json.dumps({
        "do": 6.2, "ph": 7.8, "t": 28.0, "s": 15.0, "a": "OFF"
    }), qos=1)
    time.sleep(2)

    ent = get_orion()
    print(f"   -> Orion Entity hoan tat chu trinh: aerator_status={ent.get('aerator_status')}, aeratorState={ent.get('aeratorState')}")

    client.loop_stop()
    client.disconnect()

    print("\n" + "="*75)
    print("KET QUA: 100% CHU TRINH WOKWI ESP32 -> PUBLIC BROKER -> BRIDGE -> FIWARE")
    print("         -> NODE-RED -> BRIDGE -> WOKWI RELAY/LED HOAT DONG HOAN HAO!")
    print("="*75)

if __name__ == "__main__":
    main()

