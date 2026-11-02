# DỰ ÁN IoT NHÓM 5 — HỆ THỐNG GIÁM SÁT CHẤT LƯỢNG NƯỚC AO NUÔI TÔM VÀ TỰ ĐỘNG ĐIỀU KHIỂN SỤC KHÍ

> **Nền tảng**: FIWARE (Orion Context Broker + IoT Agent JSON) kết hợp EMQX, Node-RED, QuantumLeap, CrateDB, Grafana và ESP32 (Wokwi Simulator).

---

## 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

Hệ thống được thiết kế theo kiến trúc IIAF và chuẩn Smart Data Models của FIWARE:

```
  ESP32 (Wokwi) / Python Simulator
         │  MQTT (attrs)
         ▼
  ┌─────────────┐     ┌────────────────────┐     ┌──────────────┐
  │    EMQX     │────▶│  IoT Agent JSON    │────▶│    Orion     │ ──▶ MongoDB
  │(MQTT Broker)│     │ (MQTT ↔ NGSI-v2)   │     │Context Broker│
  └─────────────┘     └────────────────────┘     └──────┬───────┘
        ▲                                               │
        │                                    ┌──────────┴──────────┐
        │                                    │ Subscription        │ Subscription
        │                                    ▼                     ▼
  ┌─────┴──────┐                     ┌──────────────┐     ┌──────────────┐
  │  Thiết bị  │◀── command ◀────────│   Node-RED   │     │ QuantumLeap  │
  │ (nhận lệnh)│     (MQTT)          │(Rule Engine) │     │ (Time-series)│
  └────────────┘                     └──────────────┘     └──────┬───────┘
                                                                 │
                                                                 ▼
                                                          ┌──────────────┐
                                                          │   CrateDB    │
                                                          └──────┬───────┘
                                                                 │
                                                                 ▼
                                                          ┌──────────────┐
                                                          │   Grafana    │
                                                          │ (Dashboard)  │
                                                          └──────────────┘
```

### Các thông số giám sát (cho mỗi ao)
- **DO (Oxy hòa tan)**: 0.0 – 12.0 mg/L (Quan trọng nhất).
- **pH**: 6.5 – 9.5 (Khoảng tối ưu: 7.5 – 8.5).
- **Nhiệt độ nước**: 20.0 – 35.0 °C (Cảnh báo > 33°C).
- **Độ mặn (Salinity)**: 5.0 – 35.0 ppt.
- **Trạng thái sục khí**: `ON` / `OFF` (Điều khiển máy sục khí qua rơ-le).

---

## 2. DANH SÁCH DỊCH VỤ VÀ CỔNG TRUY CẬP

| Dịch vụ | Container | Image | Cổng ngoài | Tài khoản / Ghi chú |
|:---|:---|:---|:---:|:---|
| **EMQX Broker** | `shrimp-emqx` | `emqx/emqx:5.8.0` | `1883` (MQTT)<br>`18083` (Web UI) | UI: `admin` / `.env` |
| **Orion Broker** | `shrimp-orion` | `telefonicaiot/fiware-orion:4.7.0` | `1026` | NGSI-v2 REST API |
| **IoT Agent JSON** | `shrimp-iot-agent` | `telefonicaiot/iotagent-json:3.13.0` | `4041` | Cổng cấu hình thiết bị |
| **Node-RED** | `shrimp-node-red` | `nodered/node-red:4.0.2` | `1880` | [http://localhost:1880](http://localhost:1880) |
| **Grafana** | `shrimp-grafana` | `grafana/grafana-oss:11.0.0` | `3000` | [http://localhost:3000](http://localhost:3000)<br>`admin` / `change-me-grafana` |
| **CrateDB** | `shrimp-crate` | `crate:4.6.7` | `4200` (HTTP)<br>`5432` (Postgres) | [http://localhost:4200](http://localhost:4200) |
| **QuantumLeap** | `shrimp-quantumleap` | `orchestracities/quantumleap:1.0.0` | `8668` | Lưu trữ dữ liệu lịch sử |
| **MongoDB** | `shrimp-mongo` | `mongo:8.0` | Internal | CSDL cho Orion & IoT Agent |

---

## 3. HƯỚNG DẪN KHỞI CHẠY HỆ THỐNG

### Bước 1: Khởi động 8 container Docker
```bash
docker compose --env-file .env -f docker/docker-compose.yml up -d
```

### Bước 2: Khởi tạo thiết bị và Subscription (Provisioning)
Chạy script tự động (tạo Service Group, 5 thiết bị ao, Subscriptions Orion ➔ QuantumLeap và Orion ➔ Node-RED):
```bash
bash source/provision.sh
```

### Bước 3: Nạp Flow Rule Engine vào Node-RED
```bash
curl -i -X POST -H "Content-Type: application/json" -H "Node-RED-Deployment-Type: full" --data-binary "@config/node-red/flows.json" http://localhost:1880/flows
```

### Bước 4: Chạy bộ giả lập dữ liệu ao nuôi (Simulator)
```bash
python source/simulator.py --ponds 5 --apikey shrimpkey
```

---

## 4. QUY TẮC ĐIỀU KHIỂN TỰ ĐỘNG (RULE ENGINE)

1. **Quy tắc Oxy hòa tan (DO)**:
   - `DO < 4.0 mg/L`: Tự động bật máy sục khí (`aerator: ON`).
   - `DO > 6.0 mg/L`: Tự động tắt máy sục khí (`aerator: OFF`) theo cơ chế **Hysteresis** để chống giật rơ-le và tiết kiệm điện.
   - `DO < 2.5 mg/L`: Kích hoạt cảnh báo khẩn cấp (`CRITICAL_LOW_DO`).
2. **Quy tắc pH**:
   - `pH < 7.5` hoặc `pH > 8.5`: Phát cảnh báo bất thường chất lượng nước.
3. **Quy tắc Nhiệt độ**:
   - `Nhiệt độ > 33.0 °C`: Cảnh báo nhiệt cao + tự động bật sục khí hỗ trợ làm mát và hòa tan oxy.

---

## 5. HỆ THỐNG DASHBOARD GIÁM SÁT (GRAFANA)

- Địa chỉ truy cập: **[http://localhost:3000/d/shrimp-pond-monitor](http://localhost:3000/d/shrimp-pond-monitor)**
- **Tính năng**:
  - Dropdown chọn từng ao nuôi (`urn:ngsi-ld:Pond:001` đến `005`).
  - Card chỉ số tức thời: DO, pH, Nhiệt độ, Độ mặn, Trạng thái Sục khí (BẬT/TẮT).
  - Biểu đồ thời gian thực kèm các đường kẻ ngưỡng an toàn trực quan.
  - Biểu đồ lịch sử đóng/ngắt sục khí (Step timeline).
  - Biểu đồ cột tổng hợp trung bình DO theo giờ (`Hourly Aggregation`).
  - Bảng tra cứu 50 bản ghi đo lường gần nhất của toàn bộ các ao.

---

## 6. KIỂM THỬ VÀ ĐÁNH GIÁ (TESTING & BENCHMARK)

Dự án cung cấp sẵn bộ script tự động hóa kiểm thử 100%:

### 1. Kiểm tra 5 Kịch bản hoạt động (5 Test Scenarios)
```bash
python source/test_scenarios.py
```
*(Báo cáo chi tiết xem tại [`tests/TEST_REPORT.md`](tests/TEST_REPORT.md))*.

### 2. Thử nghiệm mở rộng và đo hiệu năng (Scale Benchmark 5 -> 100 ao)
```bash
python source/benchmark_scale.py
```
*(Báo cáo chi tiết xem tại [`tests/BENCHMARK_REPORT.md`](tests/BENCHMARK_REPORT.md))*.

### 3. Kiểm tra độ tin cậy và phục hồi lỗi (Reliability Test)
```bash
python source/test_reliability.py
```
*(Báo cáo chi tiết xem tại [`tests/RELIABILITY_REPORT.md`](tests/RELIABILITY_REPORT.md))*.

### 4. Mô phỏng phần cứng ESP32 trên Wokwi
- Mã nguồn và sơ đồ mạch tại thư mục [`wokwi/`](wokwi/).
- Xem chi tiết tại [`wokwi/README_WOKWI.md`](wokwi/README_WOKWI.md).

