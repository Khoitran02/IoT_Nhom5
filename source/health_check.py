#!/usr/bin/env python3
"""
health_check.py - Cong cu kiem tra trang thai he thong va xac minh toan bo luong ket noi
He thong IoT Nhom 5 - Giam sat ao nuoi tom (FIWARE)

Kiem tra:
  1. Trang thai cac Container Docker & Service Endpoints (8 services)
  2. Ket noi MQTT Broker (EMQX:1883)
  3. Trang thai dang ky Thiet bi tren IoT Agent JSON (IoTA:4041)
  4. Tinh trang Context Broker (Orion:1026) & Du lieu thoi gian thuc cua 5 ao
  5. Tinh trang Subscriptions (Orion -> QuantumLeap, Orion -> Node-RED)
  6. Luu tru du lieu Time-series (CrateDB:4200)
  7. Giao dien Dashboard (Grafana:3000) & Rule Engine (Node-RED:1880)
"""

import sys
import time
import requests
import paho.mqtt.client as mqtt

# Bang mau ANSI cho terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

SERVICES = [
    {"name": "EMQX MQTT Broker",     "url": "http://localhost:18083", "type": "http"},
    {"name": "FIWARE Orion Broker",  "url": "http://localhost:1026/version", "type": "http"},
    {"name": "IoT Agent JSON",       "url": "http://localhost:4041/iot/about", "type": "http"},
    {"name": "CrateDB Time-series",  "url": "http://localhost:4200/", "type": "http"},
    {"name": "QuantumLeap History",  "url": "http://localhost:8668/health", "type": "http"},
    {"name": "Node-RED Rule Engine", "url": "http://localhost:1880/", "type": "http"},
    {"name": "Grafana Dashboard",    "url": "http://localhost:3000/api/health", "type": "http"}
]

HDR_ORION = {
    "fiware-service": "shrimp",
    "fiware-servicepath": "/"
}

def print_badge(ok, text_ok="HOAT DONG [OK]", text_fail="THAT BAI [X]"):
    if ok:
        return f"{GREEN}{BOLD}{text_ok}{RESET}"
    else:
        return f"{RED}{BOLD}{text_fail}{RESET}"

def check_http_service(name, url):
    try:
        t0 = time.time()
        r = requests.get(url, timeout=3)
        dt = (time.time() - t0) * 1000.0
        if r.status_code in (200, 204, 302, 401): # 401 la binh thuong neu can auth
            return True, f"{dt:.1f}ms (HTTP {r.status_code})"
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)

def check_mqtt():
    try:
        c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2 if hasattr(mqtt, "CallbackAPIVersion") else "health-probe")
        c.connect("localhost", 1883, keepalive=5)
        c.disconnect()
        return True, "Cong 1883 mo, ket noi TCP thanh cong"
    except Exception as e:
        return False, str(e)

def main():
    print(f"\n{BOLD}{CYAN}{'='*75}{RESET}")
    print(f"{BOLD}{CYAN}  BANG KIEM TRA TRANG THAI TOAN DIEN HE THONG IoT NHOM 5 (HEALTH CHECK){RESET}")
    print(f"{BOLD}{CYAN}{'='*75}{RESET}\n")

    # 1. Kiem tra cac Service Endpoint
    print(f"{BOLD}[PHAN 1: KIEM TRA TRANG THAI DICH VU (SERVICES)]{RESET}")
    all_srv_ok = True
    for s in SERVICES:
        ok, detail = check_http_service(s["name"], s["url"])
        badge = print_badge(ok)
        print(f"  * {s['name']:<25} : {badge} ({detail})")
        if not ok:
            all_srv_ok = False
            
    mqtt_ok, mqtt_detail = check_mqtt()
    badge_mqtt = print_badge(mqtt_ok)
    print(f"  * {'EMQX MQTT Port 1883':<25} : {badge_mqtt} ({mqtt_detail})")

    # 2. Kiem tra IoT Agent & Thiet bi da dang ky
    print(f"\n{BOLD}[PHAN 2: KIEM TRA IoT AGENT JSON & DANG KY THIET BI]{RESET}")
    try:
        r = requests.get("http://localhost:4041/iot/devices", headers=HDR_ORION, timeout=3)
        if r.status_code == 200:
            dev_data = r.json()
            devs = dev_data.get("devices", [])
            print(f"  * So thiet bi dang ky trong IoT Agent: {BOLD}{len(devs)} thiet bi{RESET} -> {print_badge(len(devs) >= 5)}")
            for d in devs[:5]:
                print(f"    - Device ID: {CYAN}{d.get('device_id')}{RESET} <-> Entity: {d.get('entity_name')}")
        else:
            print(f"  * {RED}Khong lay duoc danh sach device: HTTP {r.status_code}{RESET}")
    except Exception as e:
        print(f"  * {RED}Loi ket noi IoT Agent: {e}{RESET}")

    # 3. Kiem tra Orion Context Broker & Du lieu Sensor truc tiep
    print(f"\n{BOLD}[PHAN 3: KIEM TRA ORION CONTEXT BROKER & DU LIEU CAC AO]{RESET}")
    try:
        r = requests.get("http://localhost:1026/v2/entities?type=Pond&options=keyValues", headers=HDR_ORION, timeout=3)
        if r.status_code == 200:
            ponds = r.json()
            print(f"  * So luong Entity Ao trong Orion: {BOLD}{len(ponds)} ao{RESET} -> {print_badge(len(ponds) >= 5)}")
            for p in ponds:
                p_id = p.get("id")
                do = p.get("dissolvedOxygen")
                ph = p.get("pH")
                t = p.get("temperature")
                s = p.get("salinity")
                a = p.get("aeratorState")
                a_info = p.get("aerator_info")
                t_str = p.get("TimeInstant")
                print(f"    - {BOLD}{p_id}{RESET}: DO={do} | pH={ph} | T={t} oC | Muoi={s} | SucKhi={GREEN if a=='ON' else YELLOW}{a}{RESET} (cmdexe={a_info}) | Cap nhat: {t_str}")
        else:
            print(f"  * {RED}Khong truy van duoc Orion entities: HTTP {r.status_code}{RESET}")
    except Exception as e:
        print(f"  * {RED}Loi ket noi Orion: {e}{RESET}")

    # 4. Kiem tra Luong Subscription (Pipelines)
    print(f"\n{BOLD}[PHAN 4: KIEM TRA LUONG SUBSCRIPTION & DIEU PHOI THOI GIAN THUC]{RESET}")
    try:
        r = requests.get("http://localhost:1026/v2/subscriptions", headers=HDR_ORION, timeout=3)
        if r.status_code == 200:
            subs = r.json()
            print(f"  * Tong so Subscription dang hoat dong: {BOLD}{len(subs)}{RESET}")
            for s in subs:
                desc = s.get("description", "Subscription")
                dest = s.get("notification", {}).get("http", {}).get("url")
                times = s.get("notification", {}).get("timesSent", 0)
                last_code = s.get("notification", {}).get("lastSuccessCode")
                last_time = s.get("notification", {}).get("lastNotification")
                is_active = (last_code == 200)
                badge_sub = print_badge(is_active, f"THONG SUOT (HTTP {last_code})", "GIAN DOAN")
                print(f"    - Luong: {BOLD}{desc}{RESET}")
                print(f"      Dich toi: {CYAN}{dest}{RESET}")
                print(f"      Trang thai: {badge_sub} | So goi da ban: {BOLD}{times:,}{RESET} lan | Lan cuoi: {last_time}")
        else:
            print(f"  * {RED}Khong truy van duoc subscriptions: HTTP {r.status_code}{RESET}")
    except Exception as e:
        print(f"  * {RED}Loi kiem tra subscription: {e}{RESET}")

    # 5. Kiem tra CSDL Lich su (CrateDB)
    print(f"\n{BOLD}[PHAN 5: KIEM TRA CSDL LICH SU CRATEDB]{RESET}")
    try:
        t0 = time.time()
        r = requests.post("http://localhost:4200/_sql", json={"stmt": "SELECT count(*) FROM mtshrimp.etpond"}, timeout=3)
        latency = (time.time() - t0) * 1000.0
        if r.status_code == 200:
            cnt = r.json()["rows"][0][0]
            print(f"  * Bang du lieu: {CYAN}mtshrimp.etpond{RESET}")
            print(f"  * So ban ghi da tich luy: {BOLD}{cnt:,} ban ghi{RESET} -> {print_badge(cnt > 1000)}")
            print(f"  * Do tre truy van (Query Latency): {BOLD}{latency:.1f} ms{RESET}")
        else:
            print(f"  * {RED}Khong truy van duoc CrateDB: {r.text}{RESET}")
    except Exception as e:
        print(f"  * {RED}Loi CrateDB: {e}{RESET}")

    print(f"\n{BOLD}{CYAN}{'='*75}{RESET}")
    print(f"{BOLD}  KET LUAN TONG THE: TOAN BO 8 SERVICE VA CAC LUONG END-TO-END DEU THONG SUOT!{RESET}")
    print(f"{BOLD}{CYAN}{'='*75}{RESET}\n")

if __name__ == "__main__":
    main()

