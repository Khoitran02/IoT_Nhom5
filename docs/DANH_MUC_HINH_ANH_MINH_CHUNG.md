# DANH MỤC VÀ HƯỚNG DẪN CHỤP HÌNH ẢNH MINH CHỨNG
## DỰ ÁN HỆ THỐNG IoT GIÁM SÁT CHẤT LƯỢNG NƯỚC AO NUÔI TÔM (NHÓM 5)
**Học phần**: CTH619 – IoT Information Systems  

Tài liệu này dùng cho các thành viên trong nhóm mở hệ thống đang chạy cục bộ để chụp ảnh màn hình chèn vào Báo cáo Word chính thức.

---

### 1. Nhóm ảnh Khởi chạy & Kiến trúc Hạ tầng (Chương 2 & Chương 4)
* [ ] **Hình 1.1 — Sơ đồ kiến trúc 6 tầng IIAF kết hợp nền tảng FIWARE**
  * *Nguồn*: Sao chép sơ đồ trong Chương 2 của Báo cáo hoặc vẽ lại bằng Draw.io / PowerPoint.
* [ ] **Hình 1.2 — Trạng thái 8 Docker Containers đang chạy (`docker compose ps`)**
  * *Thao tác*: Mở PowerShell gõ `docker compose ps` để thấy 8 container đều xanh: `shrimp-emqx`, `shrimp-mongo`, `shrimp-orion`, `shrimp-iot-agent`, `shrimp-crate`, `shrimp-quantumleap`, `shrimp-node-red`, `shrimp-grafana`.
* [ ] **Hình 1.3 — Giao diện quản trị EMQX Dashboard & Cấu hình MQTT Bridge 2 chiều**
  * *Đường dẫn*: [http://localhost:18083](http://localhost:18083) (Tài khoản: `admin`, mật khẩu trong `.env`).
  * *Nội dung*:
    - Màn hình *Overview* hiển thị lưu lượng Message In/Out.
    - Màn hình *Data Integration / Bridges* hiển thị 6 Bridge kết nối tới `broker.emqx.io:1883` với trạng thái `Connected`.

### 2. Nhóm ảnh Mô phỏng & Thiết bị Wokwi (Chương 3 - Đáp ứng bắt buộc Wokwi >= 5 thiết bị)
* [ ] **Hình 2.1 — Sơ đồ mạch mô phỏng ESP32 trên Wokwi Web**
  * *Đường dẫn*: Mở trình duyệt truy cập Wokwi với file [`wokwi/pond001/diagram.json`](../wokwi/pond001/diagram.json).
  * *Nội dung*: Bo mạch ESP32 kết nối với 3 biến trở ADC1 (DO, pH, Salinity), cảm biến DS18B20 OneWire và module Relay + Đèn LED xanh báo sục khí (tổng cộng 4 cảm biến và 1 actuator).
* [ ] **Hình 2.2 — Cửa sổ Serial Monitor Wokwi ESP32 nhận lệnh và điều khiển LED/Relay**
  * *Thao tác*: Mở tab Wokwi Ao 1 (`wokwi/pond001`), vặn biến trở DO xuống dưới 4.0 mg/L:
    - Serial Monitor hiển thị: Đóng gói JSON gửi lên `iot_nhom5_shrimp_c8d2/pond001/attrs`.
    - Nhận lệnh `{"aerator":"ON"}` từ topic `.../cmd` $\rightarrow$ Relay đóng, đèn LED xanh trên mạch Wokwi sáng lên.
    - Serial Monitor xác nhận gửi `cmdexe: ON` về hệ thống.
* [ ] **Hình 2.3 — Minh chứng cả 5 thiết bị Wokwi hoạt động độc lập qua MQTT Bridge**
  * *Thao tác*: Chạy `python source/test_all_5_wokwi.py` trên PowerShell và chụp màn hình console:
    - Cả 5 thiết bị Wokwi (`pond001` .. `pond005`) publish dữ liệu lên `broker.emqx.io`.
    - EMQX Bridge chuyển tiếp vào Orion Context Broker và cả 5 ao đều cập nhật thông số.
    - Nhận lệnh điều khiển sục khí hai chiều qua Bridge thành công 100%.

### 3. Nhóm ảnh Context Broker & IoT Agent (Chương 4)
* [ ] **Hình 3.1 — Kết quả truy vấn Orion Context Broker API**
  * *Thao tác*: Gọi `GET http://localhost:1026/v2/entities?type=Pond&options=keyValues` (với header `fiware-service: shrimp`).
  * *Nội dung*: JSON trả về danh sách 5 ao với các thuộc tính `dissolvedOxygen`, `pH`, `temperature`, `salinity`, `aeratorState`.
* [ ] **Hình 3.2 — Trạng thái Subscriptions của Orion**
  * *Thao tác*: Gọi API `GET http://localhost:1026/v2/subscriptions` (header `fiware-service: shrimp`).
  * *Nội dung*: Thấy 2 subscription `active` (1 tới QuantumLeap định dạng normalized và 1 tới Node-RED định dạng keyValues) với `lastSuccessCode: 200` và `timesSent` lớn.

### 4. Nhóm ảnh Rule Engine Node-RED (Chương 5)
* [ ] **Hình 4.1 — Giao diện Flow Rule Engine trên Node-RED**
  * *Đường dẫn*: [http://localhost:1880](http://localhost:1880).
  * *Nội dung*: Màn hình Flow tab **Shrimp Pond Rule Engine** gồm: node Webhook `POST /notify`, node Function `Rule Engine (DO, pH, Temp)`, node HTTP Request `Gui Command toi Orion`.
* [ ] **Hình 4.2 — Khung Debug log của Node-RED khi tự động ra quyết định**
  * *Nội dung*: Cột bên phải (Debug window) chụp các thông báo:
    - `[urn:ngsi-ld:Pond:00X] DO thap (< 4.0 mg/L). Bat suc khi.`
    - `[urn:ngsi-ld:Pond:00X] DO doi dao (> 6.0 mg/L). Tat suc khi.`

### 5. Nhóm ảnh Dashboard Grafana (Chương 5)
* [ ] **Hình 5.1 — Toàn cảnh Dashboard Grafana 20 Panels**
  * *Đường dẫn*: [http://localhost:3000/d/shrimp-pond-monitor](http://localhost:3000/d/shrimp-pond-monitor).
  * *Nội dung*: Màn hình tổng quan gồm: Hàng System Health, Hàng chỉ số tức thời 5 thuộc tính, Hàng Time-series & Ngưỡng điều khiển, Hàng Thống kê & Cảnh báo.
* [ ] **Hình 5.2 — Biểu đồ Oxy hòa tan (DO) kèm các đường ngưỡng cảnh báo**
  * *Nội dung*: Phóng to Panel biểu đồ DO thấy đường dao động và 3 đường ngưỡng màu Đỏ (2.5 mg/L), Cam (4.0 mg/L) và Xanh (6.0 mg/L).
* [ ] **Hình 5.3 — Biểu đồ Lịch sử đóng ngắt sục khí (Step timeline) & Bảng nhật ký cảnh báo**
  * *Nội dung*: Biểu đồ sục khí chuyển đổi bậc thang giữa mức 0 (TẮT) và 1 (BẬT); Bảng Alert History với các dòng vượt ngưỡng.

### 6. Nhóm ảnh CrateDB & Bằng chứng kiểm thử (Chương 6)
* [ ] **Hình 6.1 — Giao diện quản trị CrateDB Admin UI**
  * *Đường dẫn*: [http://localhost:4200](http://localhost:4200) (Tab Tables).
  * *Nội dung*: Bảng `mtshrimp.etpond` hiển thị số lượng bản ghi đã tích lũy (> 123.000 bản ghi).
* [ ] **Hình 6.2 — Kết quả chạy Script kiểm thử 5 Kịch bản (`test_scenarios.py`)**
  * *Thao tác*: Chạy `python source/test_scenarios.py` và chụp màn hình kết quả in ra: **100% PASS cả 5/5 kịch bản**.
* [ ] **Hình 6.3 — Kết quả chạy Script kiểm thử mở rộng Scale Benchmark (`benchmark_scale.py`)**
  * *Thao tác*: Chạy `python source/benchmark_scale.py` và chụp bảng số liệu benchmark 5 ➔ 100 ao nuôi.
* [ ] **Hình 6.4 — Kết quả chạy kiểm tra toàn diện hệ thống (`health_check.py`)**
  * *Thao tác*: Chạy `python source/health_check.py` và chụp màn hình xanh 8/8 service và các luồng đều `HOAT DONG [OK]`.

