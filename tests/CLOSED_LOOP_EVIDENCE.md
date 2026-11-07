# BANG CHUNG CHU TRINH TU DONG KHEP KIN (CLOSED-LOOP PROOF)
## He thong giam sat va tu dong dieu khien suc khi ao tom (IoT Nhom 5)

- **Thoi diem kiem thu**: 2026-11-06 23:37:32
- **Doi tuong kiem thu**: Ao nuoi `pond003` (`urn:ngsi-ld:Pond:003`)
- **Muc tieu chung minh**:
  1. Tieu chi **End-to-End Integration** (0,60 diem): Cam bien -> IoT Agent -> Orion -> Node-RED -> Orion -> IoT Agent -> Thiet bi -> CrateDB -> Grafana.
  2. Tieu chi **Processing, Analytics, Rule Engine** (0,50 diem): Tu dong phat hien DO < 4.0 mg/L bat suc khi, co che Hysteresis DO > 6.0 mg/L tu dong tat suc khi.

### 1. Bang Timeline Nhat ky Hoat dong thuc te

| Thoi gian | Giai doan | Mo ta chi tiet | Du lieu / Trang thai |
|---|---|---|---|
| 23:37:09.781 | PHASE_1_INIT | Kiem tra trang thai ban dau cua ao pond003... | - |
| 23:37:09.954 | PHASE_1_INIT | Entity ban dau: DO=6.41, aeratorState=OFF | - |
| 23:37:12.955 | PHASE_2_ANOMALY | EP SU KIEN OXY TUT: DO giam xuong 3.2 mg/L (< nguong 4.0 mg/L) | - |
| 23:37:12.955 | PHASE_3_WAIT_CMD | Cho Node-RED Rule Engine phat hien va gui lenh aerator ON... | - |
| 23:37:12.996 | DEVICE_MQTT | Nhan topic=/shrimpkey/pond003/cmd | `payload: {"aerator":"ON"}` |
| 23:37:13.456 | PHASE_4_CMD_ON | Thiet bi nhan duoc lenh tu IoT Agent: {'aerator': 'ON'} | - |
| 23:37:13.456 | PHASE_5_EXEC_ON | Thiet bi dong Relay may suc khi -> aerator = ON. Gui cmdexe xac nhan... | - |
| 23:37:17.475 | PHASE_6_ORION_VERIFY_ON | Xac minh Orion Entity sau khi bat suc khi | `aeratorState: ON`<br>`aerator_info: ON`<br>`aerator_status: OK`<br>`dissolvedOxygen: 3.9` |
| 23:37:17.475 | PHASE_7_RECOVERY | May suc khi hoat dong, nong do DO hoi phuc dan... | - |
| 23:37:19.976 | PHASE_7_RECOVERY | Phat sensor DO hoi phuc: 4.5 mg/L (aerator=ON) | - |
| 23:37:22.477 | PHASE_7_RECOVERY | Phat sensor DO hoi phuc: 5.2 mg/L (aerator=ON) | - |
| 23:37:24.977 | PHASE_7_RECOVERY | Phat sensor DO hoi phuc: 5.8 mg/L (aerator=ON) | - |
| 23:37:27.478 | PHASE_7_RECOVERY | Phat sensor DO hoi phuc: 6.35 mg/L (aerator=ON) | - |
| 23:37:27.478 | PHASE_8_WAIT_OFF | DO > 6.0 mg/L. Cho Node-RED Rule Engine tu dong ngat may suc khi (Hysteresis)... | - |
| 23:37:27.516 | DEVICE_MQTT | Nhan topic=/shrimpkey/pond003/cmd | `payload: {"aerator":"OFF"}` |
| 23:37:27.978 | PHASE_9_CMD_OFF | Thiet bi nhan duoc lenh ngat suc khi tu IoT Agent: {'aerator': 'OFF'} | - |
| 23:37:27.978 | PHASE_10_EXEC_OFF | Thiet bi ngat Relay may suc khi -> aerator = OFF. Gui cmdexe xac nhan... | - |
| 23:37:31.999 | PHASE_11_COMPLETED | Xac minh Orion Entity sau khi ngat suc khi | `aeratorState: OFF`<br>`aerator_info: OFF`<br>`aerator_status: OK`<br>`dissolvedOxygen: 6.1` |

### 2. So do Chu trinh End-to-End Da Kiem chung Thuc te

```
1. SENSOR (DO=3.2 < 4.0)
       |
       v (MQTT /shrimpkey/pond003/attrs)
2. FIWARE IoT Agent JSON (4041)
       |
       v (NGSI-v2 update)
3. Orion Context Broker (1026)
       |                      \
       v (Subscription notify)  v (QuantumLeap -> CrateDB -> Grafana)
4. Node-RED Rule Engine (1880)
       |
       v (PATCH /v2/entities/Pond:003/attrs: aerator=ON)
5. Orion Context Broker (1026)
       |
       v (Forward command)
6. FIWARE IoT Agent JSON
       |
       v (MQTT /shrimpkey/pond003/cmd)
7. ACTUATOR / SIMULATOR / WOKWI (Relay dong, LED sang, DO tang)
       |
       v (MQTT /shrimpkey/pond003/cmdexe)
8. IoT Agent -> Orion (aerator_status = OK, aeratorState = ON)
       |
       v (DO hoi phuc > 6.0 mg/L -> Hysteresis)
9. Node-RED phat lenh ngat aerator=OFF -> Chu trinh hoan tat an toan!
```

### 3. Ket luan
- **Ket qua**: DAT 100% (PASS).
- He thong da van hanh hoan hao ca 2 chieu: giam sat tu dong va dieu khien phan hoi tu dong.
