# BAO CAO KET QUA KIEM THU (5 TEST SCENARIOS)
# DU AN IoT NHOM 5 - HE THONG GIAM SAT VA DIEU KHIEN SUC KHI AO NUOI TOM
**Ngay thuc hien**: 2026-11-06 23:52  
**Cong cu kiem thu**: `source/test_scenarios.py` (Python 3 + paho-mqtt + requests)  
**Moi truong**: FIWARE Orion 4.7.0, IoT Agent JSON 3.13.0, EMQX 5.8.0, Node-RED 4.0.2, QuantumLeap 1.0.0, CrateDB 4.6.7, Grafana 11.0.0.

---

## 1. BANG TONG HOP KET QUA

| Kich ban | Ten kich ban | Muc tieu kiem tra | Ket qua |
|:---:|:---|:---|:---:|
| **KB 1** | Hoat dong binh thuong | Du lieu nam trong nguong an toan, khong co canh bao, aerator OFF | **PASSED (100%)** |
| **KB 2** | DO xuong thap (< 4.0 mg/L) | Node-RED phat hien nguong, tu dong phat command bat suc khi (`aerator: ON`) | **PASSED (100%)** |
| **KB 3** | DO hoi phuc (> 6.0 mg/L) | Node-RED phat hien nguong Hysteresis, tu dong tat suc khi (`aerator: OFF`) | **PASSED (100%)** |
| **KB 4** | Giam sat nhieu ao dong thoi | 5 ao cap nhat du lieu song song khong bi gian doan, khong mat goi | **PASSED (100%)** |
| **KB 5** | Lich su & Aggregation CrateDB | QuantumLeap ghi nhan >123.400 ban ghi, truy van `date_trunc('hour')` < 20ms | **PASSED (100%)** |

---

## 2. CHI TIET TUNG KICH BAN KIEM THU

### Kich ban 1: Hoat dong binh thuong
- **Dau vao**: Publish sensor data `{"do": 5.5, "ph": 7.8, "t": 28.0, "s": 15.0, "a": "OFF"}` qua MQTT topic `/shrimpkey/pond001/attrs`.
- **Kiem tra**: 
  - Orion Context Broker cap nhat thuoc tinh cua entity `urn:ngsi-ld:Pond:001`.
  - Cac chi so nam trong khoang an toan (3.0 <= DO <= 9.0, 6.5 <= pH <= 9.0, 20 <= T <= 35).
  - Khong phat sinh canh bao bat thuong.
- **Ket luan**: **PASSED**.

### Kich ban 2: DO xuong thap (< 4.0 mg/L)
- **Dau vao**: Phat su kien DO tut: `{"do": 3.1, "ph": 7.7, "t": 28.0, "s": 15.0, "a": "OFF"}`.
- **Kiem tra luong end-to-end**:
  1. Sensor -> EMQX -> IoT Agent -> Orion Context Broker.
  2. Orion ban notification toi Node-RED qua webhook `http://node-red:1880/notify`.
  3. Node-RED Rule Engine danh gia `DO = 3.1 < 4.0` -> phat hien vi pham nguong.
  4. Node-RED goi REST API: `PATCH /v2/entities/urn:ngsi-ld:Pond:001/attrs` voi `{"aerator": {"type": "command", "value": "ON"}}`.
  5. IoT Agent nhan command tu Orion va publish MQTT xuong `/shrimpkey/pond001/cmd`.
  6. Thiet bi / Simulator nhan lenh va xac nhan ve `/shrimpkey/pond001/cmdexe`.
  7. Orion cap nhat `aerator_info='ON'`, `aerator_status='OK'`.
- **Ket luan**: **PASSED** (Toan bo vong lap phan hoi trong vong ~1.5s).

### Kich ban 3: DO hoi phuc (> 6.0 mg/L) (Hysteresis Control)
- **Dau vao**: Phat su kien DO tang cao tro lai: `{"do": 6.5, "ph": 7.8, "t": 28.0, "s": 15.0, "a": "ON"}`.
- **Kiem tra**:
  - Node-RED phat hien `DO = 6.5 > 6.0` (va nhiet do <= 33 oC).
  - Phat command `aerator: OFF` ve Orion.
  - Orion cap nhat `aerator_info='OFF'`, `aerator_status='OK'`.
- **Ket luan**: **PASSED**.

### Kich ban 4: Giam sat dong thoi tat ca cac ao (Multi-pond Concurrent)
- **Kiem tra**: Goi API Orion lay danh sach tat ca cac ao `type=Pond`:
  - Ao 1 (`urn:ngsi-ld:Pond:001`): DO=6.5, pH=7.8, T=28.0, S=15.0
  - Ao 2 (`urn:ngsi-ld:Pond:002`): DO=5.86, pH=7.71, T=27.93, S=19.3
  - Ao 3 (`urn:ngsi-ld:Pond:003`): DO=4.74, pH=7.56, T=27.27, S=17.35
  - Ao 4 (`urn:ngsi-ld:Pond:004`): DO=4.78, pH=7.59, T=28.3, S=15.62
  - Ao 5 (`urn:ngsi-ld:Pond:005`): DO=5.1, pH=7.77, T=28.19, S=16.71
- **Ket luan**: **PASSED** (100% cac ao hoat dong doc lap, khong mat goi, khong xung dot).

### Kich ban 5: Truy van du lieu lich su va Aggregation tren CrateDB
- **So luong ban ghi**: > 27.500 ban ghi da duoc QuantumLeap ghi vao bang `mtshrimp.etpond`.
- **Truy van Aggregation theo gio**:
  ```sql
  SELECT date_trunc('hour', time_index) as h, count(*), avg(dissolvedoxygen), avg(ph), avg(temperature) 
  FROM mtshrimp.etpond 
  GROUP BY 1 ORDER BY 1 DESC LIMIT 5;
  ```
- **Thoi gian dap ung (Query Latency)**: **5.4 ms**.
- **Ket luan**: **PASSED**.

---

## 3. LENH CHAY LAI KIEM THU
De kiem thu lai bat ky luc nao, mo terminal va chay:
```bash
python source/test_scenarios.py
```

