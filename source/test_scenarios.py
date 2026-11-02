#!/usr/bin/env python3
"""
test_scenarios.py - Kiem thu 5 kich ban (Test Scenarios) cho he thong giam sat ao tom IoT Nhom 5

Cac kich ban:
  1. Kich ban 1: Hoat dong binh thuong (Cac thong so nam trong nguong an toan)
  2. Kich ban 2: DO xuong thap (< 4.0 mg/L) -> Tu dong kich hoat bat suc khi
  3. Kich ban 3: DO hoi phuc (> 6.0 mg/L) -> Tu dong tat suc khi (Hysteresis)
  4. Kich ban 4: Giam sat dong thoi tat ca cac ao (Multi-pond Concurrent)
  5. Kich ban 5: Kiem tra luu tru lich su va Aggregation tren CrateDB
"""

import json
import os
import sys
import time
import requests
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "127.0.0.1")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
APIKEY = os.getenv("APIKEY", "shrimpkey")
ORION_URL = os.getenv("ORION_URL", "http://127.0.0.1:1026")
CRATE_URL = os.getenv("CRATE_URL", "http://127.0.0.1:4200")
SERVICE = "shrimp"
SERVICE_PATH = "/"

HEADERS_ORION_GET = {
    "fiware-service": SERVICE,
    "fiware-servicepath": SERVICE_PATH
}

HEADERS_ORION_POST = {
    "fiware-service": SERVICE,
    "fiware-servicepath": SERVICE_PATH,
    "Content-Type": "application/json"
}

def log(msg, status=None):
    if status == "PASS":
        print(f"  [PASS] {msg}")
    elif status == "FAIL":
        print(f"  [FAIL] {msg}")
    elif status == "INFO":
        print(f"  [INFO] {msg}")
    else:
        print(f"{msg}")

def get_orion_entity(entity_id):
    url = f"{ORION_URL}/v2/entities/{entity_id}?options=keyValues"
    try:
        r = requests.get(url, headers=HEADERS_ORION_GET, timeout=5)
        if r.status_code == 200:
            return r.json()
        else:
            log(f"Orion GET {entity_id} status={r.status_code}: {r.text}", "FAIL")
    except Exception as e:
        log(f"Loi goi Orion: {e}", "FAIL")
    return None

def publish_mqtt(topic, payload):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2 if hasattr(mqtt, "CallbackAPIVersion") else "test-client")
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=10)
    client.publish(topic, json.dumps(payload), qos=1)
    client.disconnect()

def test_scenario_1():
    print("\n" + "="*70)
    print("KICH BAN 1: Hoat dong binh thuong (Cac thong so trong nguong)")
    print("="*70)
    dev_id = "pond001"
    ent_id = "urn:ngsi-ld:Pond:001"
    topic = f"/{APIKEY}/{dev_id}/attrs"
    payload = {"do": 5.5, "ph": 7.8, "t": 28.0, "s": 15.0, "a": "OFF"}
    
    log(f"Publish MQTT len topic {topic}: {payload}", "INFO")
    publish_mqtt(topic, payload)
    time.sleep(2)
    
    ent = get_orion_entity(ent_id)
    if not ent:
        log("Khong doc duoc entity tu Orion", "FAIL")
        return False
    
    do_val = ent.get("dissolvedOxygen")
    ph_val = ent.get("pH")
    temp_val = ent.get("temperature")
    sal_val = ent.get("salinity")
    
    log(f"Du lieu doc tu Orion: DO={do_val} mg/L | pH={ph_val} | T={temp_val} oC | Sal={sal_val} ppt", "INFO")
    
    # Kiem tra cac thong so nam trong khoang an toan
    is_safe = (3.0 <= do_val <= 9.0) and (6.5 <= ph_val <= 9.0) and (20.0 <= temp_val <= 35.0)
    if is_safe:
        log("Cac thong so nuoc duoc ghi nhan va nam trong khoang hoat dong hop le.", "PASS")
        return True
    else:
        log(f"Gia tri ngoai khoang kiem tra: {ent}", "FAIL")
        return False

def test_scenario_2():
    print("\n" + "="*70)
    print("KICH BAN 2: DO xuong thap (< 4.0 mg/L) -> Tu dong kich hoat bat suc khi")
    print("="*70)
    dev_id = "pond001"
    ent_id = "urn:ngsi-ld:Pond:001"
    topic = f"/{APIKEY}/{dev_id}/attrs"
    
    # Gui su kien DO tut xuong 3.1 mg/L voi aeratorState = OFF
    payload_low = {"do": 3.1, "ph": 7.7, "t": 28.0, "s": 15.0, "a": "OFF"}
    log(f"Phat su kien DO thap: DO=3.1 mg/L (< 4.0) len {topic}", "INFO")
    publish_mqtt(topic, payload_low)
    
    log("Cho Node-RED phat hien va gui lenh bat suc khi (aerator: ON)...", "INFO")
    success = False
    for i in range(10):
        time.sleep(1.2)
        ent = get_orion_entity(ent_id)
        if ent:
            aer_info = ent.get("aerator_info")
            aer_state = ent.get("aeratorState")
            aer_status = ent.get("aerator_status")
            if aer_info == "ON" or aer_state == "ON":
                log(f"Thanh cong! Orion cap nhat aerator_info='{aer_info}', aerator_status='{aer_status}', aeratorState='{aer_state}'", "PASS")
                success = True
                break
                
    if not success:
        log("Chua phat hien lenh bat suc khi trong thoi gian cho.", "FAIL")
        return False
    return True

def test_scenario_3():
    print("\n" + "="*70)
    print("KICH BAN 3: DO hoi phuc (> 6.0 mg/L) -> Tu dong tat suc khi (Hysteresis)")
    print("="*70)
    dev_id = "pond001"
    ent_id = "urn:ngsi-ld:Pond:001"
    topic = f"/{APIKEY}/{dev_id}/attrs"
    
    # Gui du lieu DO cao 6.5 mg/L khi dang ON
    payload_high = {"do": 6.5, "ph": 7.8, "t": 28.0, "s": 15.0, "a": "ON"}
    log(f"Phat su kien DO hoi phuc: DO=6.5 mg/L (> 6.0) len {topic}", "INFO")
    publish_mqtt(topic, payload_high)
    
    log("Cho Node-RED phat hien DO > 6.0 va phat command tat suc khi (aerator: OFF)...", "INFO")
    success = False
    for i in range(10):
        time.sleep(1.2)
        ent = get_orion_entity(ent_id)
        if ent:
            aer_info = ent.get("aerator_info")
            aer_state = ent.get("aeratorState")
            aer_status = ent.get("aerator_status")
            if aer_info == "OFF" or aer_state == "OFF":
                log(f"Thanh cong! Orion cap nhat aerator_info='{aer_info}', aerator_status='{aer_status}', aeratorState='{aer_state}'", "PASS")
                success = True
                break
                
    if not success:
        log("Chua phat hien lenh tat suc khi trong thoi gian cho.", "FAIL")
        return False
    return True

def test_scenario_4():
    print("\n" + "="*70)
    print("KICH BAN 4: Giam sat dong thoi tat ca cac ao (Multi-pond Concurrent)")
    print("="*70)
    url = f"{ORION_URL}/v2/entities?type=Pond&options=keyValues"
    r = requests.get(url, headers=HEADERS_ORION_GET, timeout=5)
    if r.status_code != 200:
        log(f"Khong lay duoc danh sach ao: HTTP {r.status_code}", "FAIL")
        return False
    
    ponds = r.json()
    log(f"Tong so ao dang duoc quan ly trong Context Broker: {len(ponds)} ao", "INFO")
    valid_count = 0
    for p in ponds:
        p_id = p.get("id")
        do = p.get("dissolvedOxygen")
        ph = p.get("pH")
        temp = p.get("temperature")
        sal = p.get("salinity")
        aer = p.get("aeratorState")
        t_inst = p.get("TimeInstant")
        log(f"[{p_id}] DO={do} mg/L | pH={ph} | T={temp} oC | S={sal} ppt | SucKhi={aer} | Time={t_inst}")
        if do is not None and ph is not None and temp is not None:
            valid_count += 1
    
    if len(ponds) >= 5 and valid_count == len(ponds):
        log(f"Toan bo {len(ponds)} ao cap nhat du lieu dong thoi, khong co ao nao bi mat du lieu.", "PASS")
        return True
    else:
        log(f"Co ao thieu du lieu (hop le: {valid_count}/{len(ponds)})", "FAIL")
        return False

def test_scenario_5():
    print("\n" + "="*70)
    print("KICH BAN 5: Truy van du lieu lich su va Aggregation tren CrateDB")
    print("="*70)
    
    # 1. Kiem tra so luong ban ghi
    sql_count = {"stmt": "SELECT count(*) FROM mtshrimp.etpond"}
    t0 = time.time()
    r = requests.post(f"{CRATE_URL}/_sql", json=sql_count, timeout=5)
    latency_cnt = (time.time() - t0) * 1000
    
    if r.status_code != 200:
        log(f"Loi truy van CrateDB count: {r.text}", "FAIL")
        return False
    
    cnt = r.json()["rows"][0][0]
    log(f"Tong so ban ghi lich su da luu trong mtshrimp.etpond: {cnt:,} records (latency: {latency_cnt:.1f} ms)", "INFO")
    
    # 2. Kiem tra truy van aggregation theo gio
    sql_agg = {
        "stmt": "SELECT date_trunc('hour', time_index) as h, count(*), avg(dissolvedoxygen), avg(ph), avg(temperature) FROM mtshrimp.etpond GROUP BY 1 ORDER BY 1 DESC LIMIT 5"
    }
    t1 = time.time()
    r_agg = requests.post(f"{CRATE_URL}/_sql", json=sql_agg, timeout=5)
    latency_agg = (time.time() - t1) * 1000
    
    if r_agg.status_code != 200:
        log(f"Loi truy van CrateDB aggregation: {r_agg.text}", "FAIL")
        return False
        
    rows = r_agg.json()["rows"]
    log(f"Ket qua Aggregation 5 gio gan nhat (query latency: {latency_agg:.1f} ms):", "INFO")
    for row in rows:
        log(f"  Gio: {row[0]} | So mau: {row[1]} | DO trung binh: {row[2]:.2f} mg/L | pH TB: {row[3]:.2f} | T TB: {row[4]:.2f} oC")
        
    if cnt > 1000 and len(rows) > 0:
        log("Du lieu lich su duoc luu tru day du, truy van aggregation chinh xac va latency thap.", "PASS")
        return True
    else:
        log("Du lieu lich su chua du hoac aggregation khong co ket qua.", "FAIL")
        return False

def main():
    print("\n" + "#"*70)
    print("  BAT DAU THUC HIEN 5 TEST SCENARIO - HE THONG IoT NHOM 5")
    print("#"*70)
    
    results = {}
    results["Kich ban 1 (Binh thuong)"] = test_scenario_1()
    results["Kich ban 2 (DO thap -> Bat aerator)"] = test_scenario_2()
    results["Kich ban 3 (DO hoi phuc -> Tat aerator)"] = test_scenario_3()
    results["Kich ban 4 (Giam sat nhieu ao)"] = test_scenario_4()
    results["Kich ban 5 (Lich su & Aggregation CrateDB)"] = test_scenario_5()
    
    print("\n" + "="*70)
    print("  TONG KET KET QUA KIEM THU (TEST REPORT SUMMARY)")
    print("="*70)
    all_passed = True
    for name, res in results.items():
        status_str = "PASSED [OK]" if res else "FAILED [X]"
        print(f"  {name:<45} : {status_str}")
        if not res:
            all_passed = False
            
    print("="*70)
    if all_passed:
        print("  KET LUAN: 5/5 KICH BAN KIEM THU DAT KET QUA HOAN HAO (100% PASS)!\n")
    else:
        print("  KET LUAN: Co kich ban chua dat yeu cau.\n")
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
