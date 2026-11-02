# ============================================================================

# DỰ ÁN IoT NHÓM 5 — HỆ THỐNG GIÁM SÁT CHẤT LƯỢNG NƯỚC AO NUÔI TÔM

# Kết hợp: Bài nhóm FIWARE + Dự án nuôi tôm

# ============================================================================

# Ngày cập nhật : 2026-11-02

# Tác giả : Nhóm 5

# ============================================================================

# ╔══════════════════════════════════════════════════════════════════════════╗

# ║ PHẦN 1: TỔNG QUAN DỰ ÁN ║

# ╚══════════════════════════════════════════════════════════════════════════╝

## 1.1 MÔ TẢ BÀI TOÁN

────────────────────────────────────────────────────────────────────────────
Xây dựng hệ thống IoT giám sát chất lượng nước ao nuôi tôm và tự động điều
khiển sục khí, sử dụng nền tảng FIWARE làm lớp IoT Platform / Context
Management. Hệ thống thu thập dữ liệu cảm biến (DO, pH, nhiệt độ, độ mặn),
áp dụng rule engine để ra quyết định (bật/tắt sục khí, cảnh báo), lưu lịch
sử và hiển thị dashboard theo thời gian thực.

Stakeholder: Người nuôi tôm, kỹ thuật viên ao, chủ trại, cán bộ khuyến nông.

## 1.2 THÔNG SỐ GIÁM SÁT (MỖI AO)

────────────────────────────────────────────────────────────────────────────
┌──────────────────┬────────┬─────────────────────────┬──────────────────────────────────┐
│ Thông số │ Đơn vị │ Mô phỏng (Wokwi) │ Ghi chú │
├──────────────────┼────────┼─────────────────────────┼──────────────────────────────────┤
│ Oxy hòa tan (DO) │ mg/L │ Biến trở │ Quan trọng nhất, chu kỳ ngày/đêm │
│ pH │ - │ Biến trở │ Dao động theo ngày │
│ Nhiệt độ nước │ °C │ DS18B20 │ │
│ Độ mặn │ ppt │ Biến trở │ Thay đổi chậm │
│ Trạng thái sục │ ON/OFF │ Relay + LED │ Actuator │
└──────────────────┴────────┴─────────────────────────┴──────────────────────────────────┘

## 1.3 RULE ENGINE (CONDITION → DECISION → ACTION)

────────────────────────────────────────────────────────────────────────────
• DO < 4 mg/L → Bật sục khí
• DO > 6 mg/L → Tắt sục khí (hysteresis tránh đóng ngắt liên tục)
• pH ngoài 7.5 – 8.5 → Cảnh báo
• Nhiệt độ > 33°C → Cảnh báo + bật sục khí
• DO thấp > N phút → Cảnh báo mức nghiêm trọng

## 1.4 KIẾN TRÚC HỆ THỐNG

────────────────────────────────────────────────────────────────────────────

Wokwi ESP32 / Python Simulator
│ MQTT (publish sensor data)
▼
┌─────────────┐ ┌────────────────────┐ ┌──────────────┐
│ EMQX │────▶│ IoT Agent JSON │────▶│ Orion │ ← MongoDB
│ (MQTT Broker│ │ (MQTT ↔ NGSI-v2) │ │(Context Broker│
└─────────────┘ └────────────────────┘ └──────┬───────┘
▲ │
│ ┌──────────┼──────────┐
│ │ subscription │ subscription
│ ▼ ▼
┌─────┴──────┐ ┌──────────────┐ ┌──────────────┐
│ Thiết bị │◀── command ◀────────│ Node-RED │ │ QuantumLeap │
│ (nhận lệnh)│ (MQTT) │(Rule Engine) │ │ (History) │
└────────────┘ └──────────────┘ └──────┬───────┘
│
▼
┌──────────────┐
│ CrateDB │
│ (Time-series)│
└──────┬───────┘
│
▼
┌──────────────┐
│ Grafana │
│ (Dashboard) │
└──────────────┘

## 1.5 LUỒNG DỮ LIỆU END-TO-END

────────────────────────────────────────────────────────────────────────────
[Sensor] →(MQTT)→ [EMQX] →(MQTT)→ [IoT Agent] →(NGSI-v2)→ [Orion]
│
┌─────────────────────────────────────────────────────┤
│ │
▼ ▼
[QuantumLeap] →(SQL)→ [CrateDB] →(query)→ [Grafana] [Node-RED]
│
(đánh giá rule)
│
┌────────────┴────────────┐
▼ ▼
[Gửi command [Cảnh báo]
qua Orion→IoT Agent
→MQTT→Thiết bị]

# ╔══════════════════════════════════════════════════════════════════════════╗

# ║ PHẦN 2: CẤU HÌNH MÃ NGUỒN & MÔI TRƯỜNG ║

# ╚══════════════════════════════════════════════════════════════════════════╝

## 2.1 CẤU TRÚC THƯ MỤC DỰ ÁN

────────────────────────────────────────────────────────────────────────────
IoT_Nhom5/
├── .env # Biến môi trường (KHÔNG commit)
├── .env.example # Mẫu .env để chia sẻ
├── gitignore # Loại trừ .env khỏi Git
├── duan0.md # Tài liệu: yêu cầu, công cụ, lộ trình
├── duan1.md # Tài liệu: triển khai 1 hay nhiều máy
├── duan2.md # Tài liệu: chi tiết từng bước
│
├── docker/
│ └── docker-compose.yml # Stack 8 services (all-in-one)
│
├── config/
│ └── grafana/
│ └── provisioning/
│ └── datasources/
│ └── cratedb.yml # Auto-provision datasource CrateDB
│
└── source/
├── simulator.py # Giả lập N ao tôm (Python + MQTT)
├── provision.sh # Tạo service group, thiết bị, subscription
└── requirements.txt # paho-mqtt>=1.6

## 2.2 DOCKER SERVICES (8 CONTAINER)

────────────────────────────────────────────────────────────────────────────
┌────┬──────────────┬──────────────────────────────────────┬──────────┬─────────┐
│ # │ Service │ Image │ Cổng │ RAM max │
├────┼──────────────┼──────────────────────────────────────┼──────────┼─────────┤
│ 1 │ emqx │ emqx/emqx:5.8.0 │ 1883 │ 1 GB │
│ │ │ │ 18083 │ │
│ 2 │ mongo-db │ mongo:8.0 │ (intern) │ 1 GB │
│ 3 │ orion │ telefonicaiot/fiware-orion:4.7.0 │ 1026 │ 512 MB │
│ 4 │ iot-agent │ telefonicaiot/iotagent-json:3.13.0 │ 4041 │ 512 MB │
│ 5 │ crate-db │ crate:4.6.7 │ 4200 │ 2 GB │
│ 6 │ quantumleap │ orchestracities/quantumleap:1.0.0 │ 8668 │ 512 MB │
│ 7 │ node-red │ nodered/node-red:4.0.2 │ 1880 │ 512 MB │
│ 8 │ grafana │ grafana/grafana-oss:11.0.0 │ 3000 │ 512 MB │
├────┴──────────────┴──────────────────────────────────────┴──────────┴─────────┤
│ TỔNG RAM ƯỚC TÍNH TỐI ĐA: ~6.5 GB │ YÊU CẦU MÁY: ≥ 8 GB RAM │
└──────────────────────────────────────────────────────────────────────────────┘

## 2.3 BIẾN MÔI TRƯỜNG (.env)

────────────────────────────────────────────────────────────────────────────
┌────────────────────────────┬────────────────────┬──────────────────────────────┐
│ Biến │ Giá trị mặc định │ Mô tả │
├────────────────────────────┼────────────────────┼──────────────────────────────┤
│ EMQX_VERSION │ 5.8.0 │ Phiên bản EMQX │
│ IOTA_VERSION │ 3.13.0 │ Phiên bản IoT Agent JSON │
│ ORION_VERSION │ 4.7.0 │ Phiên bản Orion Context Broker│
│ MONGO_VERSION │ 8.0 │ Phiên bản MongoDB │
│ QL_VERSION │ 1.0.0 │ Phiên bản QuantumLeap │
│ CRATE_VERSION │ 4.6.7 │ Phiên bản CrateDB │
│ GRAFANA_VERSION │ 11.0.0 │ Phiên bản Grafana │
│ NODERED_VERSION │ 4.0.2 │ Phiên bản Node-RED │
│ EMQX_DASHBOARD_PASSWORD │ (bắt buộc đổi) │ Mật khẩu dashboard EMQX │
│ GRAFANA_ADMIN_PASSWORD │ (bắt buộc đổi) │ Mật khẩu admin Grafana │
│ BIND_ADDR │ 127.0.0.1 │ Bind IP cho quản trị │
│ MQTT_BIND_ADDR │ 0.0.0.0 │ Bind IP cho MQTT (mở ra ngoài)│
│ CRATE_HEAP_SIZE │ 1g │ Heap CrateDB │
│ ORION_LOG_LEVEL │ ERROR │ Log level Orion │
│ TZ │ Asia/Ho_Chi_Minh │ Múi giờ │
└────────────────────────────┴────────────────────┴──────────────────────────────┘

## 2.4 MQTT TOPIC & PAYLOAD (QUY ƯỚC IoT Agent JSON)

────────────────────────────────────────────────────────────────────────────
API Key mặc định: shrimpkey

Gửi dữ liệu (thiết bị → platform):
Topic : /{apikey}/{device_id}/attrs
Payload: {"do":5.4, "ph":7.9, "t":29.1, "s":15.2, "a":"OFF"}

Nhận lệnh (platform → thiết bị):
Topic : /{apikey}/{device_id}/cmd
Payload: {"aerator": {"state": "ON"}}

Trả kết quả lệnh (thiết bị → platform):
Topic : /{apikey}/{device_id}/cmdexe
Payload: {"aerator": "ON"}

Ví dụ cho ao 1:
/shrimpkey/pond001/attrs
/shrimpkey/pond001/cmd
/shrimpkey/pond001/cmdexe

## 2.5 NGSI-v2 ENTITY MODEL

────────────────────────────────────────────────────────────────────────────
Entity Name : urn:ngsi-ld:Pond:001 .. urn:ngsi-ld:Pond:N
Entity Type : Pond

┌───────────────────┬──────────┬────────────┬──────────────────────────┐
│ Attribute │ Type │ object_id │ Ý nghĩa │
├───────────────────┼──────────┼────────────┼──────────────────────────┤
│ dissolvedOxygen │ Number │ do │ Oxy hòa tan (mg/L) │
│ pH │ Number │ ph │ Độ pH │
│ temperature │ Number │ t │ Nhiệt độ nước (°C) │
│ salinity │ Number │ s │ Độ mặn (ppt) │
│ aeratorState │ Text │ a │ Trạng thái sục khí │
│ aerator │ command │ - │ Lệnh bật/tắt sục khí │
│ aerator_status │ cmdStatus│ - │ Kết quả thực hiện lệnh │
│ aerator_info │ cmdResult│ - │ Thông tin phản hồi │
└───────────────────┴──────────┴────────────┴──────────────────────────┘

## 2.6 SIMULATOR (source/simulator.py)

────────────────────────────────────────────────────────────────────────────
Ngôn ngữ : Python 3
Thư viện : paho-mqtt >= 1.6
Tính năng :
• Giả lập N ao (mặc định 5), mỗi ao có mức nền khác nhau
• Dữ liệu có chu kỳ ngày/đêm (1 ngày giả lập = 600s mặc định)
• DO cao nhất ~15h (quang hợp), thấp nhất ~3h sáng
• Sự kiện bất thường (anomaly): oxy tụt đột ngột, xác suất có thể cấu hình
• Có thể ép sự kiện anomaly cho ao cụ thể (--anomaly-pond, --anomaly-after)
• Nhận lệnh sục khí (MQTT cmd topic) → thay đổi trạng thái aerator
• Khi bật sục khí: DO hồi dần lên (+1.8 mg/L)
• Tương thích paho-mqtt 1.x và 2.x

Cách chạy:
pip install paho-mqtt
python source/simulator.py --ponds 5 --apikey shrimpkey
python source/simulator.py --anomaly-pond pond003 --anomaly-after 30

## 2.7 PROVISION (source/provision.sh)

────────────────────────────────────────────────────────────────────────────
Ngôn ngữ : Bash
Tính năng :
• Kiểm tra Orion và IoT Agent sẵn sàng (retry 30 lần)
• Tạo Service Group (apikey → entity type Pond)
• Tạo N thiết bị ao (pond001..N) → entity urn:ngsi-ld:Pond:001..N
• Tạo Subscription Orion → QuantumLeap (ghi lịch sử CrateDB)
• Hỗ trợ RESET=1 để xoá và tạo lại
• Idempotent: chạy lại an toàn (bỏ qua nếu đã tồn tại)

Cách chạy (Git Bash / WSL / Linux):
bash source/provision.sh
N_PONDS=10 bash source/provision.sh
RESET=1 bash source/provision.sh

# ╔══════════════════════════════════════════════════════════════════════════╗

# ║ PHẦN 3: TIẾN ĐỘ CÁC TASK (CHECKLIST) ║

# ╚══════════════════════════════════════════════════════════════════════════╝

## 3.1 BẢNG TIẾN ĐỘ TỔNG QUAN

────────────────────────────────────────────────────────────────────────────

Tổng tiến độ ước tính: ████████████░░░░░░░░  ~57-60%

Tuần 1 (Nền tảng)      : ████████████████████  100%
Tuần 2 (Kết nối + Rule): ████████████████████  100%
Tuần 3 (Dashboard + QA): ████████████████░░░░  ~80%
Tuần 4 (Test + Báo cáo): █████░░░░░░░░░░░░░░░  ~25%

## 3.2 CHI TIẾT TỪNG TASK

────────────────────────────────────────────────────────────────────────────

═══════════════════════════════════════════════════════════════════════
GIAI ĐOẠN 1: NỀN TẢNG & HẠ TẦNG
═══════════════════════════════════════════════════════════════════════

[✅] TASK 1.1 — Tài liệu kế hoạch dự án
File : duan0.md, duan1.md, duan2.md
Mô tả : Xác định bài toán, thông số, ngưỡng, kiến trúc,
công cụ, rủi ro, lộ trình 4 tuần, chiến lược
triển khai 1/nhiều máy
Trạng thái: HOÀN THÀNH

[✅] TASK 1.2 — Docker Compose (All-in-one)
File : docker/docker-compose.yml
Mô tả : Stack đầy đủ 8 services với healthcheck, mem_limit,
logging, depends_on, volume persistence
Trạng thái: HOÀN THÀNH

[✅] TASK 1.3 — Cấu hình môi trường (.env)
File : .env, .env.example
Mô tả : Phiên bản image ghim cố định, mật khẩu, bind addr,
log level, tài nguyên. Không hard-code localhost.
Trạng thái: HOÀN THÀNH

[✅] TASK 1.4 — Grafana Datasource Provisioning
File : config/grafana/provisioning/datasources/cratedb.yml
Mô tả : Tự động cấu hình CrateDB làm datasource PostgreSQL
Trạng thái: HOÀN THÀNH

[✅] TASK 1.5 — Gitignore
File : .gitignore
Mô tả : Loại trừ .env khỏi Git
Trạng thái: HOÀN THÀNH (Đã đổi tên thành .gitignore)

═══════════════════════════════════════════════════════════════════════
GIAI ĐOẠN 2: KẾT NỐI THIẾT BỊ & DỮ LIỆU
═══════════════════════════════════════════════════════════════════════

[✅] TASK 2.1 — Python Simulator (giả lập ao tôm)
File : source/simulator.py, source/requirements.txt
Mô tả : Giả lập N ao, chu kỳ ngày/đêm, anomaly, nhận lệnh
sục khí, tương thích paho-mqtt 1.x/2.x
Trạng thái: HOÀN THÀNH

[✅] TASK 2.2 — Provision Script
File : source/provision.sh
Mô tả : Tạo service group, N thiết bị, subscription
Orion→QuantumLeap. Hỗ trợ RESET, idempotent.
Trạng thái: HOÀN THÀNH

[✅] TASK 2.3 — Chạy thử stack & verify end-to-end
File : docker/docker-compose.yml, logs hệ thống
Mô tả : docker compose up → provision → simulator →
kiểm tra entity trong Orion → dữ liệu trong CrateDB
Trạng thái: HOÀN THÀNH (8 containers healthy, CrateDB >20.000 records)

[⬜] TASK 2.4 — Firmware Wokwi (ESP32)
File : (chưa có)
Mô tả : Code Arduino C++/MicroPython cho ESP32 trên Wokwi,
đọc cảm biến (biến trở), gửi MQTT, nhận lệnh relay
Trạng thái: CHƯA THỰC HIỆN
Ưu tiên : 🟡 TRUNG BÌNH

═══════════════════════════════════════════════════════════════════════
GIAI ĐOẠN 3: RULE ENGINE & DASHBOARD
═══════════════════════════════════════════════════════════════════════

[✅] TASK 3.1 — Node-RED Flow (Rule Engine)
File : config/node-red/flows.json
Mô tả : Nhận notification từ Orion webhook (/notify). Rules:
• DO < 4.0 mg/L → Bật sục khí (PATCH command về Orion)
• DO > 6.0 mg/L → Tắt sục khí (hysteresis)
• pH ngoài 7.5 – 8.5 → Cảnh báo chất lượng nước
• Nhiệt độ > 33°C → Cảnh báo + bật sục khí
• DO < 2.5 mg/L → Cảnh báo khẩn cấp
Trạng thái: HOÀN THÀNH (Đã deploy và kiểm thử qua API Node-RED)

  [✅] TASK 3.2 — Grafana Dashboard
       File    : config/grafana/provisioning/dashboards/shrimp_pond_dashboard.json, dashboards.yml
       Mô tả  : Dashboard hiển thị:
                 • Biểu đồ DO, pH, temperature, salinity theo thời gian
                 • Trạng thái sục khí (ON/OFF) mỗi ao
                 • Cảnh báo màu theo ngưỡng (DO, pH, Nhiệt độ)
                 • Tổng hợp trung bình DO theo giờ (hourly aggregation)
                 • Hỗ trợ chọn ao qua dropdown ($pond_id)
                 • Bảng dữ liệu gần nhất của tất cả các ao
       Trạng thái: HOÀN THÀNH (Đã provision & import API thành công tại /d/shrimp-pond-monitor)

[✅] TASK 3.3 — Subscription Orion → Node-RED (notification)
File : source/provision.sh
Mô tả : Tạo subscription để Orion notify Node-RED khi
DO/pH/temp/salinity thay đổi → trigger Rule Engine
Trạng thái: HOÀN THÀNH (Đã tích hợp provision.sh, sub active 200 OK)

═══════════════════════════════════════════════════════════════════════
GIAI ĐOẠN 4: KIỂM THỬ & ĐÁNH GIÁ
═══════════════════════════════════════════════════════════════════════

  [✅] TASK 4.1 — 5 Test Scenario
       File    : source/test_scenarios.py, tests/TEST_REPORT.md
       Mô tả  :
                 Kịch bản 1: Hoạt động bình thường (tất cả thông số trong ngưỡng)
                 Kịch bản 2: DO xuống thấp (< 4 mg/L) → Tự động bật sục khí
                 Kịch bản 3: Tự động bật sục khí → DO hồi phục (> 6 mg/L) → tự tắt
                 Kịch bản 4: Giám sát nhiều ao đồng thời (5 ao độc lập)
                 Kịch bản 5: Xem lại dữ liệu lịch sử trên Grafana / CrateDB aggregation
       Trạng thái: HOÀN THÀNH (Script tự động 100% PASS 5/5 kịch bản)

[⬜] TASK 4.2 — Đo hiệu năng (Throughput / Latency)
File : (chưa có)
Mô tả : Mở rộng 5 → 10 → 50 → 100 ao, đo:
• Message rate (msg/s)
• Latency: thời gian từ publish → entity update Orion
• CPU/RAM: docker stats
• Thời gian query lịch sử khi dữ liệu tăng
Trạng thái: CHƯA THỰC HIỆN
Ưu tiên : 🟡 TRUNG BÌNH

[⬜] TASK 4.3 — Thử nghiệm độ tin cậy
File : (chưa có)
Mô tả : Tắt/bật lại từng service (Orion, IoT Agent, MongoDB),
gửi payload sai kiểu, kiểm tra recovery
Trạng thái: CHƯA THỰC HIỆN
Ưu tiên : 🟢 THẤP

═══════════════════════════════════════════════════════════════════════
GIAI ĐOẠN 5: TRIỂN KHAI NÂNG CAO
═══════════════════════════════════════════════════════════════════════

[⬜] TASK 5.1 — Triển khai nhiều máy
File : (chưa có docker-compose.A/B/C.yml)
Mô tả : Tách stack thành 2-3 máy:
Máy A: Thiết bị + bộ sinh tải
Máy B: EMQX, IoT Agent, Orion, Node-RED
Máy C: QuantumLeap, CrateDB, Grafana
Trạng thái: CHƯA THỰC HIỆN
Ưu tiên : 🟢 THẤP

[⬜] TASK 5.2 — Xác thực MQTT (EMQX username/password)
File : .env (đã comment sẵn MQTT_USER, MQTT_PASSWORD)
Mô tả : Bật xác thực trên EMQX, cấu hình IoT Agent +
simulator sử dụng username/password
Trạng thái: CHƯA THỰC HIỆN
Ưu tiên : 🟢 THẤP

═══════════════════════════════════════════════════════════════════════
GIAI ĐOẠN 6: TÀI LIỆU & BÁO CÁO
═══════════════════════════════════════════════════════════════════════

[⬜] TASK 6.1 — README.md
File : (chưa có)
Mô tả : Hướng dẫn cài đặt, chạy, cấu hình, test.
Dành cho giảng viên và nhóm khác.
Trạng thái: CHƯA THỰC HIỆN
Ưu tiên : 🟡 TRUNG BÌNH

[⬜] TASK 6.2 — Báo cáo (15-25 trang)
File : (chưa có)
Mô tả : Kiến trúc IIAF, FIWARE, data model, PoC, đánh giá,
so sánh, kết luận
Trạng thái: CHƯA THỰC HIỆN
Ưu tiên : 🟡 TRUNG BÌNH

[⬜] TASK 6.3 — Video demo (8-12 phút)
File : (chưa có)
Mô tả : Quay demo luồng end-to-end, 5 kịch bản, dashboard
Trạng thái: CHƯA THỰC HIỆN
Ưu tiên : 🟡 TRUNG BÌNH

[⬜] TASK 6.4 — Slide thuyết trình (10-15 slide)
File : (chưa có)
Mô tả : Tổng quan, kiến trúc, demo, đánh giá, kết luận
Trạng thái: CHƯA THỰC HIỆN
Ưu tiên : 🟡 TRUNG BÌNH

## 3.3 BẢNG TÓM TẮT TRẠNG THÁI

────────────────────────────────────────────────────────────────────────────
┌──────┬──────────────────────────────────────────────┬───────────┬──────────┐
│ Task │ Tên │ Trạng thái│ Ưu tiên │
├──────┼──────────────────────────────────────────────┼───────────┼──────────┤
│ 1.1 │ Tài liệu kế hoạch dự án │ ✅ │ - │
│ 1.2 │ Docker Compose (All-in-one) │ ✅ │ - │
│ 1.3 │ Cấu hình môi trường (.env) │ ✅ │ - │
│ 1.4 │ Grafana Datasource Provisioning │ ✅ │ - │
│ 1.5 │ Gitignore │ ✅ │ - │
│ 2.1 │ Python Simulator │ ✅ │ - │
│ 2.2 │ Provision Script │ ✅ │ - │
│ 2.3 │ Chạy thử stack & verify end-to-end │ ✅ │ - │
│ 2.4 │ Firmware Wokwi (ESP32) │ ⬜ │ 🟡 │
│ 3.1 │ Node-RED Flow (Rule Engine) │ ✅ │ - │
│ 3.2 │ Grafana Dashboard │ ✅ │ - │
│ 3.3 │ Subscription Orion → Node-RED │ ✅ │ - │
│ 4.1 │ 5 Test Scenario │ ✅ │ - │
│ 4.2 │ Đo hiệu năng (Scale test) │ ⬜ │ 🟡 │
│ 4.3 │ Thử nghiệm độ tin cậy │ ⬜ │ 🟢 │
│ 5.1 │ Triển khai nhiều máy │ ⬜ │ 🟢 │
│ 5.2 │ Xác thực MQTT │ ⬜ │ 🟢 │
│ 6.1 │ README.md │ ⬜ │ 🟡 │
│ 6.2 │ Báo cáo (15-25 trang) │ ⬜ │ 🟡 │
│ 6.3 │ Video demo (8-12 phút) │ ⬜ │ 🟡 │
│ 6.4 │ Slide thuyết trình (10-15 slide) │ ⬜ │ 🟡 │
├──────┴──────────────────────────────────────────────┴───────────┴──────────┤
│ TỔNG: 12/21 hoàn thành │ Tiến độ: ~57% │ Toàn bộ ưu tiên cao (🔴) ĐÃ HOÀN THÀNH! │
└───────────────────────────────────────────────────────────────────────────┘

## 3.4 HÀNH ĐỘNG TIẾP THEO (ĐỀ XUẤT THỨ TỰ)

────────────────────────────────────────────────────────────────────────────

BƯỚC 1 (Ngay lập tức):
→ Chạy docker compose up -d (TASK 2.3)
→ Chạy provision.sh
→ Chạy simulator.py
→ Verify: curl Orion /v2/entities, kiểm tra CrateDB có dữ liệu

BƯỚC 2 (Sau khi stack chạy ổn):
→ Tạo Node-RED flow cho rule sục khí (TASK 3.1)
→ Tạo subscription Orion → Node-RED (TASK 3.3)
→ Test: simulator gửi DO < 4 → Node-RED tự bật sục khí

BƯỚC 3 (Dashboard):
→ Tạo Grafana dashboard (TASK 3.2)
→ Panel: DO, pH, temp, salinity time-series
→ Panel: aerator state, alerts
→ Aggregation: trung bình DO theo giờ

BƯỚC 4 (Test & Scale):
→ Thực hiện 5 test scenario (TASK 4.1)
→ Đo hiệu năng 5→10→50→100 ao (TASK 4.2)
→ Screenshot/log kết quả

BƯỚC 5 (Tài liệu):
→ Viết README.md (TASK 6.1)
→ Viết báo cáo (TASK 6.2)
→ Quay video + làm slide (TASK 6.3, 6.4)

BƯỚC 6 (Nâng cao, nếu còn thời gian):
→ Firmware Wokwi ESP32 (TASK 2.4)
→ Triển khai nhiều máy (TASK 5.1)
→ Bật xác thực MQTT (TASK 5.2)

# ╔══════════════════════════════════════════════════════════════════════════╗

# ║ PHẦN 4: CÔNG CỤ SỬ DỤNG ║

# ╚══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────┬─────────────────────────────────────────────────────┐
│ Mục đích │ Công cụ │
├─────────────────────┼─────────────────────────────────────────────────────┤
│ Container hóa │ Docker, Docker Compose │
│ Context Broker │ Orion (NGSI-v2) │
│ Kết nối thiết bị │ IoT Agent for JSON (MQTT) │
│ CSDL cho Orion │ MongoDB │
│ Lịch sử │ QuantumLeap + CrateDB │
│ Broker MQTT │ EMQX │
│ Rule / điều phối │ Node-RED │
│ Dashboard │ Grafana │
│ Giả lập thiết bị │ Python (paho-mqtt), Wokwi (ESP32) │
│ Thử API │ Postman, curl │
│ Đo hiệu năng │ docker stats, Python script │
│ Mô hình dữ liệu │ NGSI-v2 (entity type: Pond) │
│ Quản lý mã nguồn │ Git │
│ Tài liệu │ Markdown │
└─────────────────────┴─────────────────────────────────────────────────────┘

# ╔══════════════════════════════════════════════════════════════════════════╗

# ║ PHẦN 5: GHI CHÚ & RỦI RO ║

# ╚══════════════════════════════════════════════════════════════════════════╝

1. File gitignore nên đổi tên thành .gitignore (có dấu chấm đầu)
2. Wokwi chạy trên cloud → cần broker công khai hoặc tunnel (ngrok/
   Cloudflare Tunnel) để Wokwi kết nối tới EMQX local
3. FIWARE nặng → máy cần ≥ 8 GB RAM, lý tưởng 16 GB
4. Chọn NGSI-v2 (dễ hơn, IoT Agent + QuantumLeap hỗ trợ tốt)
5. Phiên bản image trong .env cần kiểm tra Docker Hub trước khi pull
6. Luôn giữ bản 1 máy làm phương án dự phòng khi demo
7. Cần component từ nhóm khác → chuẩn bị bản tự dựng dự phòng

# ═══════════════════════════════════════════════════════════════════════════

# HẾT FILE MÔ TẢ DỰ ÁN

# Cập nhật lần cuối: 2026-11-02 22:00

# ═══════════════════════════════════════════════════════════════════════════
