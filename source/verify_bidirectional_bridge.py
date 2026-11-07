#!/usr/bin/env python3
"""
verify_bidirectional_bridge.py - Kiểm tra thông suốt cả 2 chiều giữa local EMQX và broker.emqx.io:
1. Ingress: broker.emqx.io (iot_nhom5_shrimp/pond001/attrs) -> local EMQX (/shrimpkey/pond001/attrs)
2. Egress: local EMQX (/shrimpkey/pond001/cmd) -> broker.emqx.io (iot_nhom5_shrimp/pond001/cmd)
3. Cmdexe: broker.emqx.io (iot_nhom5_shrimp/pond001/cmdexe) -> local EMQX (/shrimpkey/pond001/cmdexe)
"""
import paho.mqtt.client as mqtt
import time
import json
import sys

ingress_received = []
egress_received = []
cmdexe_received = []

def on_local_msg(client, userdata, msg):
    payload = msg.payload.decode(errors='ignore')
    if "test_bridge_ingress" in payload:
        print(f"[LOCAL] Nhan Ingress Attrs thanh cong: {msg.topic} -> {payload}")
        ingress_received.append((msg.topic, payload))
    elif "test_bridge_cmdexe" in payload:
        print(f"[LOCAL] Nhan Ingress Cmdexe thanh cong: {msg.topic} -> {payload}")
        cmdexe_received.append((msg.topic, payload))

def on_remote_msg(client, userdata, msg):
    payload = msg.payload.decode(errors='ignore')
    if "test_bridge_egress" in payload:
        print(f"[REMOTE broker.emqx.io] Nhan Egress Cmd thanh cong: {msg.topic} -> {payload}")
        egress_received.append((msg.topic, payload))

print("1. Ket noi MQTT Local va Remote...")
local_client = mqtt.Client()
local_client.on_message = on_local_msg
local_client.connect("127.0.0.1", 1883, 60)
local_client.subscribe("/shrimpkey/pond001/#")
local_client.loop_start()

remote_client = mqtt.Client()
remote_client.on_message = on_remote_msg
remote_client.connect("broker.emqx.io", 1883, 60)
remote_client.subscribe("iot_nhom5_shrimp_c8d2/pond001/#")
remote_client.loop_start()

time.sleep(2)

print("\n2. Test 1: Ingress (Remote -> Local)")
test_attrs = json.dumps({"test_bridge_ingress": True, "do": 5.2, "ph": 7.8, "t": 28.5, "s": 15.0, "a": "OFF"})
remote_client.publish("iot_nhom5_shrimp_c8d2/pond001/attrs", test_attrs)
time.sleep(2)

print("\n3. Test 2: Egress (Local -> Remote)")
test_cmd = json.dumps({"test_bridge_egress": True, "aerator": "ON"})
local_client.publish("/shrimpkey/pond001/cmd", test_cmd)
time.sleep(2)

print("\n4. Test 3: Cmdexe (Remote -> Local)")
test_cmdexe = json.dumps({"test_bridge_cmdexe": True, "aerator": "ON"})
remote_client.publish("iot_nhom5_shrimp_c8d2/pond001/cmdexe", test_cmdexe)
time.sleep(2)

local_client.loop_stop()
local_client.disconnect()
remote_client.loop_stop()
remote_client.disconnect()

print("\n--- KET QUA KIEM TRA ---")
print(f"Ingress Attrs:  {'PASS' if ingress_received else 'FAIL'}")
print(f"Egress Cmd:     {'PASS' if egress_received else 'FAIL'}")
print(f"Ingress Cmdexe: {'PASS' if cmdexe_received else 'FAIL'}")

if ingress_received and egress_received and cmdexe_received:
    print("\n>>> TAT CA 3 LUONG BRIDGE 2 CHIEU HOAT DONG HOAN HAO! <<<")
    sys.exit(0)
else:
    print("\n>>> CO LUONG CHUA THONG. KIEM TRA LAI! <<<")
    sys.exit(1)

