# BÁO CÁO DỰ ÁN HỌC PHẦN
# CTH619 – IoT Information Systems
## ĐỀ TÀI: HỆ THỐNG IoT GIÁM SÁT CHẤT LƯỢNG NƯỚC AO NUÔI TÔM VÀ TỰ ĐỘNG ĐIỀU KHIỂN SỤC KHÍ DỰA TRÊN NỀN TẢNG FIWARE VÀ KIẾN TRÚC IIAF 6 TẦNG
**Bậc đào tạo**: Thạc sĩ Kỹ thuật / Công nghệ Thông tin  
**Nhóm thực hiện**: Nhóm 5  
**Năm học**: 2026 - 2027  
**Nền tảng công nghệ chính**: FIWARE Ecosystem (Orion Context Broker, IoT Agent JSON, QuantumLeap), EMQX MQTT Broker, Node-RED, CrateDB, Grafana, ESP32 Wokwi Simulation.

---

# MỤC LỤC BÁO CÁO

- [CHƯƠNG 1: PHÂN TÍCH BÀI TOÁN, YÊU CẦU VÀ CÁC BÊN LIÊN QUAN](#chương-1-phân-tích-bài-toán-yêu-cầu-và-các-bên-liên-quan)
  - [1.1. Bối cảnh và Tính cấp thiết của Đề tài](#11-bối-cảnh-và-tính-cấp-thiết-của-đề-tài)
  - [1.2. Phân tích các Bên liên quan (Stakeholder Analysis)](#12-phân-tích-các-bên-liên-quan-stakeholder-analysis)
  - [1.3. Phạm vi Hệ thống (System Scope)](#13-phạm-vi-hệ-thống-system-scope)
  - [1.4. Yêu cầu Chức năng (Functional Requirements - FR)](#14-yêu-cầu-chức-năng-functional-requirements---fr)
  - [1.5. Yêu cầu Phi Chức năng (Non-Functional Requirements - NFR)](#15-yêu-cầu-phi-chức-năng-non-functional-requirements---nfr)
  - [1.6. Cơ sở Kỹ thuật của các Ngưỡng Giám sát](#16-cơ-sở-kỹ-thuật-của-các-ngưỡng-giám-sát)
- [CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG THEO KHUNG CHUẨN IIAF 6 TẦNG](#chương-2-thiết-kế-kiến-trúc-hệ-thống-theo-khung-chuẩn-iiaf-6-tầng)
  - [2.1. Kiến trúc Tổng thể 6 Tầng IIAF](#21-kiến-trúc-tổng-thể-6-tầng-iiaf)
  - [2.2. Bảng Ánh xạ Toàn diện Kiến trúc IIAF 6 Tầng](#22-bảng-ánh-xạ-toàn-diện-kiến-trúc-iiaf-6-tầng)
  - [2.3. Đánh giá Việc Tích hợp các Thành phần Nghiên cứu](#23-đánh-giá-việc-tích-hợp-các-thành-phần-nghiên-cứu)
- [CHƯƠNG 3: THIẾT BỊ IoT, MÔ PHỎNG WOKWI VÀ THU THẬP DỮ LIỆU](#chương-3-thiết-bị-iot-mô-phỏng-wokwi-và-thu-thập-dữ-liệu)
  - [3.1. Thiết kế Phần cứng Mô phỏng trên Wokwi (ESP32 Model)](#31-thiết-kế-phần-cứng-mô-phỏng-trên-wokwi-esp32-model)
  - [3.2. Cấu trúc Firmware ESP32 và Giao thức Điều khiển](#32-cấu-trúc-firmware-esp32-và-giao-thức-điều-khiển)
  - [3.3. Giải pháp MQTT Bridge Kết nối Wokwi Cloud với Local EMQX](#33-giải-pháp-mqtt-bridge-kết-nối-wokwi-cloud-với-local-emqx)
  - [3.4. Bộ Giả lập Phần mềm Đa Ao (Python Shrimp Simulator)](#34-bộ-giả-lập-phần-mềm-đa-ao-python-shrimp-simulator)
- [CHƯƠNG 4: MÔ HÌNH DỮ LIỆU, GIAO THỨC TRUYỀN THÔNG VÀ NỀN TẢNG FIWARE](#chương-4-mô-hình-dữ-liệu-giao-thức-truyền-thông-và-nền-tảng-fiware)
  - [4.1. Mô hình Thực thể NGSI-v2 (Entity Data Model)](#41-mô-hình-thực-thể-ngsi-v2-entity-data-model)
  - [4.2. Cấu trúc Topic và Định dạng Gói tin MQTT](#42-cấu-trúc-topic-và-định-dạng-gói-tin-mqtt)
  - [4.3. Cấu hình Subscriptions trong Orion Context Broker](#43-cấu-hình-subscriptions-trong-orion-context-broker)
- [CHƯƠNG 5: XỬ LÝ DỮ LIỆU, RULE ENGINE VÀ CHU TRÌNH TỰ ĐỘNG KHÉP KÍN](#chương-5-xử-lý-dữ-liệu-rule-engine-và-chu-trình-tự-động-khép-kín)
  - [5.1. Logic Điều khiển Trễ Hysteresis trên Node-RED](#51-logic-điều-khiển-trễ-hysteresis-trên-node-red)
  - [5.2. Bằng chứng Chu trình Tự động Khép kín (Closed-Loop Proof)](#52-bằng-chứng-chu-trình-tự-động-khép-kín-closed-loop-proof)
  - [5.3. Lưu trữ Chuỗi Thời gian Đơn Nút trên CrateDB và Phép toán Aggregation](#53-lưu-trữ-chuỗi-thời-gian-đơn-nút-trên-cratedb-và-phép-toán-aggregation)
  - [5.4. Thiết kế Dashboard Giám sát Toàn diện trên Grafana](#54-thiết-kế-dashboard-giám-sát-toàn-diện-trên-grafana)
- [CHƯƠNG 6: KIỂM THỬ, ĐÁNH GIÁ HIỆU NĂNG VÀ THỬ NGHIỆM MỞ RỘNG](#chương-6-kiểm-thử-đánh-giá-hiệu-năng-và-thử-nghiệm-mở-rộng)
  - [6.1. Kết quả Thực nghiệm 5 Kịch bản Hoạt động (5 Test Scenarios)](#61-kết-quả-thực-nghiệm-5-kịch-bản-hoạt-động-5-test-scenarios)
  - [6.2. Đánh giá Khả năng Chịu lỗi và Độ Tin cậy (Reliability Test)](#62-đánh-giá-khả-năng-chịu-lỗi-và-độ-tin-cậy-reliability-test)
  - [6.3. Thử nghiệm Chịu tải Tức thời và Đo Hiệu năng Thực tế (Scale Benchmark)](#63-thử-nghiệm-chịu-tải-tức-thời-và-đo-hiệu-năng-thực-tế-scale-benchmark)
  - [6.4. Mức độ Tiêu thụ Tài nguyên Hệ thống (CPU & RAM)](#64-mức-độ-tiêu-thụ-tài-nguyên-hệ-thống-cpu--ram)
- [CHƯƠNG 7: ĐÁNH GIÁ ĐÓNG GÓP, HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN](#chương-7-đánh-giá-đóng-góp-hạn-chế-và-hướng-phát-triển)
  - [7.1. Bảng Phân công Thành viên và Mức độ Đóng góp](#71-bảng-phân-công-thành-viên-và-mức-độ-đóng-góp)
  - [7.2. Bảng Đối chiếu Yêu cầu Đề tài và Minh chứng Thực hiện](#72-bảng-đối-chiếu-yêu-cầu-đề-tài-và-minh-chứng-thực-hiện)
  - [7.3. Hạn chế Hiện tại của Hệ thống](#73-hạn-chế-hiện-tại-của-hệ-thống)
  - [7.4. Hướng Phát triển Tương lai](#74-hướng-phát-triển-tương-lai)
- [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)

---

# CHƯƠNG 1: PHÂN TÍCH BÀI TOÁN, YÊU CẦU VÀ CÁC BÊN LIÊN QUAN

### 1.1. Bối cảnh và Tính cấp thiết của Đề tài
Nuôi tôm thâm canh và siêu thâm canh (đặc biệt là tôm thẻ chân trắng *Litopenaeus vannamei* và tôm sú *Penaeus monodon*) đóng vai trò kinh tế chiến lược trong ngành thủy sản Việt Nam. Tuy nhiên, mô hình nuôi mật độ cao tiềm ẩn rủi ro sinh học cực kỳ lớn do môi trường nước ao nuôi biến động nhanh chóng và phức tạp.

Trong nuôi tôm công nghiệp, **Oxy hòa tan (Dissolved Oxygen - DO)** là thông số sinh tồn quan trọng bậc nhất:
- Nồng độ DO biến động mãnh liệt theo chu kỳ ngày/đêm: Ban ngày, quá trình quang hợp của tảo đẩy DO lên mức cao (thường đạt cực đại vào khoảng 14h - 15h, có thể vượt 8.0 mg/L). Ngược lại, vào ban đêm khi quá trình quang hợp ngừng lại, tảo và các quần xã vi sinh vật chuyển sang hô hấp tiêu thụ oxy kết hợp với quá trình phân hủy bùn bã hữu cơ đáy ao, làm DO tụt dốc liên tục và chạm đáy nguy hiểm vào khoảng **02h00 - 05h00 sáng**.
- Nếu DO giảm xuống dưới **4.0 mg/L**, tôm bắt đầu bị stress, giảm ăn và suy giảm hệ miễn dịch. Khi DO tụt sâu dưới **2.5 mg/L**, tôm bị ngạt, nổi đầu hàng loạt và có thể chết toàn bộ ao chỉ trong vòng **30 đến 45 phút**.
- Bên cạnh DO, các yếu tố môi trường then chốt khác gồm:
  - **Độ pH**: Dải pH thích hợp nằm trong khoảng $7.5 - 8.5$. Biến động pH vượt quá $0.5$ trong một ngày gây sốc thẩm thấu cho tôm.
  - **Nhiệt độ nước ($T$)**: Tối ưu từ $28 - 30^\circ\text{C}$. Nhiệt độ vượt quá $33^\circ\text{C}$ làm giảm độ hòa tan của oxy đồng thời làm gia tăng nhu cầu hô hấp của tôm.
  - **Độ mặn ($S$)**: Dao động tối ưu từ $10 - 25\text{ ppt}$ tùy theo độ tuổi của tôm.

### 1.2. Phân tích các Bên liên quan (Stakeholder Analysis)

| Bên liên quan (Stakeholder) | Vai trò trong hệ thống | Nhu cầu và Kỳ vọng chính |
|---|---|---|
| **Chủ trang trại / Nhà đầu tư** | Quản lý kinh tế và tài sản trang trại | - Bảo vệ tài sản ao nuôi, ngăn ngừa rủi ro tôm chết ngạt.<br>- Tiết kiệm chi phí điện năng tiêu thụ từ dàn quạt nước / sục khí.<br>- Xem báo cáo tổng hợp chi phí và hiệu quả vận hành từ xa. |
| **Kỹ thuật viên / Công nhân ao nuôi** | Trực tiếp chăm sóc và vận hành hàng ngày | - Giảm tải việc đo đạc thủ công vào ban đêm (0h - 4h sáng).<br>- Nhận cảnh báo tức thời khi có thông số vượt ngưỡng an toàn.<br>- Có thể giám sát trạng thái thiết bị và chuyển chế độ điều khiển thủ công khi cần. |
| **Chuyên gia Thủy sản / Kỹ sư nuôi trồng** | Tư vấn kỹ thuật và giám sát môi trường | - Truy xuất chuỗi dữ liệu lịch sử (Time-series) của từng ao để phân tích diễn biến chất lượng nước.<br>- Đánh giá mối tương quan giữa nhiệt độ, DO, pH với chu kỳ lột xác và sức khỏe tôm. |
| **Hội đồng Giảng viên / Đánh giá viên** | Đánh giá học thuật và kỹ thuật đề tài | - Hệ thống phải tuân thủ chuẩn kiến trúc công nghiệp IIAF 6 tầng và nền tảng FIWARE.<br>- Tích hợp thông suốt chuỗi dữ liệu hai chiều (End-to-End closed-loop actuation).<br>- Có mô phỏng phần cứng Wokwi kết nối broker thật, đo đạc hiệu năng mở rộng với số liệu thực chứng minh. |

### 1.3. Phạm vi Hệ thống (System Scope)
- **Trong phạm vi (In-Scope)**:
  - Giám sát đồng thời cụm ao nuôi ($5 - 100$ ao) với 4 thông số: DO, pH, Nhiệt độ, Độ mặn.
  - Mô phỏng thiết bị phần cứng nhúng ESP32 trên nền tảng Wokwi, kết nối hai chiều qua MQTT Broker EMQX với cơ chế MQTT Bridge.
  - Xây dựng bộ giả lập Python Simulator tạo luồng dữ liệu biến thiên theo chu kỳ ngày/đêm và hỗ trợ ép sự kiện bất thường.
  - Chuẩn hóa thực thể ngữ cảnh theo chuẩn FIWARE NGSI-v2 (`urn:ngsi-ld:Pond:XXX`).
  - Xây dựng Rule Engine trên Node-RED tự động kích hoạt máy sục khí theo cơ chế trễ (**Hysteresis Control**).
  - Lưu trữ dữ liệu lịch sử đơn nút trên CrateDB thông qua QuantumLeap và trực quan hóa toàn diện trên Grafana Dashboard.
- **Ngoài phạm vi (Out-of-Scope)**:
  - Triển khai mạch phần cứng vật lý tại ao nuôi ngoài đời thực (sử dụng mô phỏng Wokwi chuẩn công nghiệp).
  - Tự động định lượng thức ăn tự động và xử lý vi sinh bằng hóa chất.

### 1.4. Yêu cầu Chức năng (Functional Requirements - FR)
- **FR1 (Thu thập dữ liệu cảm biến)**: Hệ thống định kỳ ($5\text{ giây/lần}$) thu thập dữ liệu DO, pH, Nhiệt độ, Độ mặn từ thiết bị gửi lên MQTT broker.
- **FR2 (Quản lý trạng thái ngữ cảnh)**: Nền tảng FIWARE Orion cập nhật và quản lý trạng thái thời gian thực của từng ao nuôi dưới dạng NGSI-v2 Entity.
- **FR3 (Tự động ra quyết định & Điều khiển khép kín)**: Khi DO $< 4.0\text{ mg/L}$, hệ thống tự động phát command bật máy sục khí; khi DO hồi phục $> 6.0\text{ mg/L}$, tự động tắt sục khí để tiết kiệm điện.
- **FR4 (Cảnh báo vượt ngưỡng tức thì)**: Phát cảnh báo khi DO $< 2.5\text{ mg/L}$ (nguy cấp), pH nằm ngoài dải $7.5 - 8.5$, hoặc nhiệt độ $> 33.0^\circ\text{C}$.
- **FR5 (Lưu trữ và Truy vấn Lịch sử)**: Đồng bộ tự động toàn bộ dữ liệu đo và trạng thái thiết bị sang CSDL CrateDB; hỗ trợ tính toán tổng hợp theo giờ (Hourly Aggregation).
- **FR6 (Trực quan hóa Dashboard)**: Cung cấp giao diện Web Grafana hiển thị trực quan thông số tức thời, lịch sử bật/tắt sục khí, biểu đồ biến thiên và nhật ký cảnh báo.

### 1.5. Yêu cầu Phi Chức năng (Non-Functional Requirements - NFR)
- **NFR1 (Độ trễ điều khiển vòng lặp - Latency)**: Thời gian từ khi cảm biến gửi bản tin vi phạm ngưỡng đến khi thiết bị nhận được lệnh sục khí $\le 2.0\text{ giây}$.
- **NFR2 (Tính tin cậy & Chống mất gói - Reliability)**: Sử dụng mức dịch vụ MQTT QoS 1 đảm bảo độ tin cậy truyền nhận trong điều kiện mạng hoạt động bình thường.
- **NFR3 (Khả năng mở rộng - Scalability)**: Nền tảng có khả năng chịu tải thông lượng tức thời $\ge 50\text{ msg/s}$ khi có lưu lượng dồn từ nhiều ao nuôi.
- **NFR4 (Khả năng chịu lỗi - Fault Tolerance)**: Các container chạy độc lập; khi một ao gửi bản tin lỗi (Malformed JSON hoặc Type mismatch), hệ thống tự cô lập và không làm gián đoạn các ao khác.
- **NFR5 (Bảo mật & Chuẩn hóa)**: Phân tách không gian tên dịch vụ thông qua FIWARE Service (`shrimp`) và ServicePath (`/`). Trong môi trường PoC thử nghiệm cục bộ, mật khẩu quản trị được thiết lập trên Dashboard EMQX và Grafana; hệ thống sử dụng kết nối nội bộ cổng 1883 không mật khẩu để thuận tiện kiểm thử và phát triển. Trong môi trường sản xuất thực tế, việc triển khai cần kích hoạt xác thực người dùng MQTT và mã hóa TLS/mTLS.

### 1.6. Cơ sở Kỹ thuật của các Ngưỡng Giám sát
Các ngưỡng vận hành trong đề tài được thiết lập dựa trên tài liệu chuyên ngành nuôi trồng thủy sản và khuyến nghị thực tế:
1. **Tiêu chuẩn chất lượng nước**: Tham khảo **Tiêu chuẩn quốc gia TCVN 13656:2023** (*Nước nuôi trồng thủy sản – Yêu cầu chất lượng nước nuôi thâm canh tôm sú và tôm thẻ chân trắng*), trong đó yêu cầu oxy hòa tan tối ưu trong ao nuôi phải duy trì ở mức cao và pH nằm trong dải trung tính kiềm nhẹ.
2. **Ngưỡng điều khiển sục khí (Nhóm đề xuất)**: Dựa trên thực tiễn sản xuất phổ biến trong nuôi thâm canh tôm thẻ chân trắng, nhóm lựa chọn:
   - Ngưỡng kích hoạt sục khí: $\text{DO} < 4.0\text{ mg/L}$ (nhằm ngăn chặn tôm ngạt trước khi oxy tụt xuống dải nguy hiểm $< 2.5\text{ mg/L}$).
   - Ngưỡng ngắt sục khí (Hysteresis): $\text{DO} > 6.0\text{ mg/L}$ (nhằm đảm bảo nước đã đủ oxy dồi dào, đồng thời tạo dải trễ $2.0\text{ mg/L}$ để bảo vệ động cơ relay không bị đóng ngắt liên tục).
3. **Cảnh báo pH và Nhiệt độ**: Dải $\text{pH} = 7.5 - 8.5$ và ngưỡng nhiệt độ $T > 33^\circ\text{C}$ được lựa chọn dựa trên khuyến nghị kỹ thuật của các chuyên gia thủy sản (như giáo trình của GS. Claude E. Boyd - Auburn University), vì vượt qua dải này độc tính của khí độc $\text{NH}_3$ và $\text{H}_2\text{S}$ trong ao nuôi tăng nhanh chóng.

---

# CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG THEO KHUNG CHUẨN IIAF 6 TẦNG

### 2.1. Kiến trúc Tổng thể 6 Tầng IIAF
Theo yêu cầu đề bài, kiến trúc hệ thống được tổ chức thành **6 tầng chức năng** rõ ràng, bảo đảm tính phân tách trách nhiệm (Separation of Concerns) và tích hợp các công nghệ đã nghiên cứu:

```
+-------------------------------------------------------------------------------+
| 6. TẦNG ỨNG DỤNG (Application Tier)                                           |
|    - Grafana Dashboard 11.0 (Trực quan hóa, Giám sát tức thời, Cảnh báo)      |
+-------------------------------------------------------------------------------+
                                    ▲
                                    │ PostgreSQL Protocol (Port 5432)
+-------------------------------------------------------------------------------+
| 5. TẦNG XỬ LÝ & RA QUYẾT ĐỊNH (Processing / Decision Tier)                    |
|    - Node-RED 4.0.2 (Rule Engine: Đánh giá ngưỡng, Logic Hysteresis)          |
+-------------------------------------------------------------------------------+
          ▲                                             │
          │ HTTP POST Notify (1880)                     │ HTTP PATCH Command (1026)
          │                                             ▼
+-------------------------------------------------------------------------------+
| 4. TẦNG DỮ LIỆU & PHÂN TÍCH (Data / Analytics Tier)                           |
|    - QuantumLeap 1.0.0 (Dịch vụ đồng bộ dữ liệu lịch sử từ Orion)             |
|    - CrateDB 4.6.7 (CSDL chuỗi thời gian đơn nút - Single-node Time-series)   |
+-------------------------------------------------------------------------------+
          ▲
          │ HTTP POST Notify (8668)
          │
+-------------------------------------------------------------------------------+
| 3. TẦNG NỀN TẢNG IoT (IoT Platform Tier)                                      |
|    - FIWARE Orion Context Broker 4.7.0 (Quản lý thực thể ngữ cảnh NGSI-v2)    |
|    - FIWARE IoT Agent JSON 3.13.0 (Cầu nối song hướng MQTT <-> NGSI-v2)       |
|    - MongoDB 8.0 (Lưu trữ trạng thái ngữ cảnh hiện hành)                      |
+-------------------------------------------------------------------------------+
          ▲                                             │
          │ MQTT /attrs (Port 1883)                     │ MQTT /cmd & /cmdexe
          ▼                                             ▼
+-------------------------------------------------------------------------------+
| 2. TẦNG TRUYỀN THÔNG (Communication Tier)                                     |
|    - EMQX Broker 5.8.0 (MQTT Broker hiệu năng cao, QoS 1)                     |
|    - MQTT Bridge 2 chiều với Broker công cộng (broker.emqx.io:1883)           |
+-------------------------------------------------------------------------------+
          ▲                                             │
          │ Publish dữ liệu cảm biến                    │ Nhận lệnh sục khí
          ▼                                             ▼
+-------------------------------------------------------------------------------+
| 1. TẦNG THIẾT BỊ (Devices Tier) - 100% WOKWI ESP32 CHO CẢ 5 AO NUÔI           |
|    - 5 Thiết bị ESP32 Wokwi độc lập (pond001 đến pond005)                    |
|    - 4 Cảm biến/thiết bị: DO (GPIO 34), pH (GPIO 35), Độ mặn (GPIO 32), T (GPIO 4)|
|    - 1 Actuator/thiết bị: Relay Module 5V & Đèn LED xanh máy sục khí (GPIO 2)  |
|    - Python Load Simulator: Công cụ phụ trợ phục vụ Scale Test (10 - 100 ao)  |
+-------------------------------------------------------------------------------+
```

### 2.2. Bảng Ánh xạ Toàn diện Kiến trúc IIAF 6 Tầng

| Tầng IIAF | Tên tầng chức năng | Thành phần công nghệ | Vai trò kỹ thuật trong hệ thống | Giao thức & Cổng | Tiêu chuẩn áp dụng |
|:---:|:---|:---|:---|:---:|:---:|
| **Tầng 1** | **Devices (Thiết bị)** | - 5x ESP32 Wokwi Nodes (`pond001` .. `pond005`)<br>- Python Load Generator (phụ trợ đo tải) | Tầng thiết bị chính thức gồm 5 trạm ESP32 Wokwi độc lập đọc 4 loại cảm biến (DO, pH, Temp, Salinity), điều khiển Relay máy sục khí và gửi xác nhận `cmdexe`. Python Simulator đóng vai trò phụ trợ cho kiểm thử tải lớn. | GPIO, ADC, OneWire | Wokwi Hardware Model (5 Nodes) |
| **Tầng 2** | **Communication (Truyền thông)** | - EMQX 5.8.0<br>- MQTT Bridge 2 chiều | Broker trung chuyển bản tin; bắc cầu hai chiều giữa Wokwi Cloud (`broker.emqx.io`) và local stack. | MQTT (Port 1883), HTTP (Port 18083) | OASIS MQTT v3.1.1 (QoS 1) |
| **Tầng 3** | **IoT Platform (Nền tảng IoT)** | - FIWARE Orion 4.7.0<br>- IoT Agent JSON 3.13<br>- MongoDB 8.0 | Bộ giải pháp FIWARE trọn bộ: Quản lý thực thể ngữ cảnh (`Pond`), ánh xạ MQTT sang NGSI-v2 và phân phối thông báo. | HTTP (Port 1026, 4041), TCP (Port 27017) | Đặc tả chuẩn FIWARE NGSI-v2 |
| **Tầng 4** | **Data / Analytics (Dữ liệu & Phân tích)** | - QuantumLeap 1.0.0<br>- CrateDB 4.6.7 (Single-node) | Lưu trữ chuỗi thời gian phân tán; thực thi các phép toán tổng hợp theo giờ (`Hourly Aggregation`). | HTTP (Port 8668, 4200), PostgreSQL (Port 5432) | SQL:1999, Time-series Data Model |
| **Tầng 5** | **Processing / Decision (Xử lý & Ra quyết định)** | - Node-RED 4.0.2 | Rule Engine đánh giá ngưỡng chất lượng nước, thực thi cơ chế trễ Hysteresis, phát lệnh PATCH sục khí. | HTTP (Port 1880) | Event-driven Flow, NGSI-v2 Webhook |
| **Tầng 6** | **Application (Ứng dụng)** | - Grafana 11.0.0 | Bảng điều khiển giám sát trực quan 20 panels, hiển thị giá trị tức thời, đồ thị ngưỡng và nhật ký cảnh báo. | HTTP (Port 3000) | Web Dashboard, PostgreSQL Datasource |

### 2.3. Đánh giá Việc Tích hợp các Thành phần Nghiên cứu
Hệ thống kết hợp thành công các thành phần công nghệ:
1. **Thành phần FIWARE (nhóm nghiên cứu)**: Bộ ba Orion Context Broker, IoT Agent JSON và QuantumLeap, bảo đảm tính mở và chuẩn hóa dữ liệu ngữ cảnh.
2. **Thành phần tích hợp thứ hai (EMQX Broker)**: Đóng vai trò hạt nhân truyền thông với hiệu năng cao và tính năng MQTT Bridge kết nối cloud-to-local.
3. **Thành phần tích hợp thứ ba (Node-RED & CrateDB & Grafana)**: Tạo nên chuỗi xử lý, lưu trữ và biểu diễn dữ liệu công nghiệp hoàn chỉnh.

---

# CHƯƠNG 3: THIẾT BỊ IoT, MÔ PHỎNG WOKWI VÀ THU THẬP DỮ LIỆU

### 3.1. Thiết kế Phần cứng Mô phỏng trên Wokwi (ESP32 Model cho cả 5 Ao Nuôi)
Theo đúng yêu cầu bắt buộc của đề tài về việc sử dụng nền tảng Wokwi với tối thiểu $\ge 5$ thiết bị IoT, mỗi thiết bị có $\ge 2$ loại cảm biến và $\ge 1$ loại cơ cấu chấp hành, nhóm đã xây dựng **5 dự án Wokwi chuyên biệt tương ứng 5 ao nuôi** (`pond001` đến `pond005`), mỗi ao nuôi là một nút phần cứng hoàn chỉnh chạy vi điều khiển **ESP32 DevKit C v4**:
- **Cấu hình 4 loại Cảm biến trên mỗi trạm Wokwi (vượt mức tối thiểu 2 loại)**:
  - `GPIO 34` (ADC1_CH6): Biến trở đo Oxy hòa tan (DO), dải đo $0.0 - 12.0\text{ mg/L}$.
  - `GPIO 35` (ADC1_CH7): Biến trở đo pH, dải đo $6.5 - 9.5$.
  - `GPIO 32` (ADC1_CH4): Biến trở đo Độ mặn, dải đo $5.0 - 35.0\text{ ppt}$.
  - `GPIO 4`: Cảm biến nhiệt độ kỹ thuật số DS18B20 giao tiếp chuẩn OneWire.
  *(Quy hoạch toàn bộ biến trở analog vào khối ADC1 nhằm tránh hoàn toàn hiện tượng xung đột phần cứng với khối truyền thông WiFi/ADC2 của chip ESP32)*.
- **Cơ cấu chấp hành (Actuator) trên mỗi trạm Wokwi (đáp ứng mức tối thiểu 1 loại)**:
  - `GPIO 2`: Nối Module Relay 5V điều khiển động cơ sục khí và Đèn LED màu xanh lục hiển thị trực quan trạng thái đóng/ngắt.
- **Danh mục 5 dự án Wokwi độc lập trong kho mã nguồn**:
  - [wokwi/pond001/](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/wokwi/pond001/): Trạm quan trắc Ao 1 (Thiết bị `pond001`).
  - [wokwi/pond002/](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/wokwi/pond002/): Trạm quan trắc Ao 2 (Thiết bị `pond002`).
  - [wokwi/pond003/](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/wokwi/pond003/): Trạm quan trắc Ao 3 (Thiết bị `pond003`).
  - [wokwi/pond004/](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/wokwi/pond004/): Trạm quan trắc Ao 4 (Thiết bị `pond004`).
  - [wokwi/pond005/](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/wokwi/pond005/): Trạm quan trắc Ao 5 (Thiết bị `pond005`).

### 3.2. Cấu trúc Firmware ESP32 và Giao thức Điều khiển
Firmware viết bằng C/C++ Arduino cho ESP32 ([sketch.ino](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/wokwi/sketch.ino)) bao gồm các khối chức năng chính:
1. Khởi tạo WiFi ảo `Wokwi-GUEST` và kết nối MQTT Broker `broker.emqx.io:1883`.
2. Đăng ký kênh nhận lệnh điều khiển riêng theo từng ao: `iot_nhom5_shrimp_c8d2/{device_id}/cmd`.
3. Định kỳ $5000\text{ ms}$, đọc các kênh ADC và cảm biến DS18B20, đóng gói JSON gửi lên kênh `iot_nhom5_shrimp_c8d2/{device_id}/attrs`:
   ```json
   {"do": 5.40, "ph": 7.82, "t": 28.5, "s": 15.0, "a": "OFF"}
   ```
4. Khi nhận lệnh từ kênh `cmd`:
   ```json
   {"aerator": "ON"}
   ```
   Vi điều khiển xuất mức `HIGH` ra `GPIO 2` làm đóng Relay và sáng đèn LED xanh, đồng thời publish phản hồi xác nhận lên kênh `iot_nhom5_shrimp_c8d2/{device_id}/cmdexe`:
   ```json
   {"aerator": "ON"}
   ```

### 3.3. Giải pháp MQTT Bridge Kết nối Wokwi Cloud với Local EMQX
Do Wokwi chạy trên nền web (Public Cloud Sandbox), các tài khoản miễn phí không thể truy cập trực tiếp vào dải mạng cục bộ (`localhost` hoặc `192.168.x.x`). Nhóm đã áp dụng giải pháp **MQTT Bridge 2 chiều** trực tiếp trên container EMQX local nối với Broker công cộng `broker.emqx.io:1883`:
- Để tránh xung đột dữ liệu với người dùng khác trên Broker công cộng, nhóm sử dụng tiền tố chủ đề độc nhất: **`iot_nhom5_shrimp_c8d2/`**.
- EMQX Container cục bộ tự động bắc cầu 15 bridges hai chiều cho toàn bộ **5 ao nuôi (`pond001` đến `pond005`)**, đáp ứng trọn vẹn yêu cầu tối thiểu $\ge 5$ thiết bị IoT của đề tài:
  - Ingress Attrs (5 bridges): `iot_nhom5_shrimp_c8d2/{pond001..005}/attrs` $\rightarrow$ `/shrimpkey/{pond001..005}/attrs`.
  - Ingress Cmdexe (5 bridges): `iot_nhom5_shrimp_c8d2/{pond001..005}/cmdexe` $\rightarrow$ `/shrimpkey/{pond001..005}/cmdexe`.
  - Egress Cmd (5 bridges): `/shrimpkey/{pond001..005}/cmd` $\rightarrow$ `iot_nhom5_shrimp_c8d2/{pond001..005}/cmd`.
- Toàn bộ 5 thiết bị Wokwi ESP32 đều có thể chạy độc lập hoặc đồng thời qua các tab trình duyệt, gửi dữ liệu 4 cảm biến và nhận lệnh điều khiển Relay. Script [source/test_all_5_wokwi.py](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/source/test_all_5_wokwi.py) đã kiểm chứng tự động toàn bộ 5 thiết bị hoạt động thông suốt 100%.

### 3.4. Công cụ Phụ trợ Đo tải Quy mô lớn (Python Shrimp Simulator)
Trong khi 5 trạm Wokwi ESP32 đóng vai trò là tầng thiết bị IoT chính thức của đề tài, để đáp ứng mục tiêu **khuyến khích thử nghiệm đánh giá khả năng mở rộng (Scale Test từ 10 đến 100 thiết bị)** mà không làm quá tải CPU/RAM trình duyệt của máy trạm cá nhân (vốn không thể duy trì 100 tab Wokwi WebAssembly cùng lúc), nhóm đã phát triển script phụ trợ [simulator.py](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/source/simulator.py):
- Tái hiện quy luật quang hợp ban ngày và hô hấp ban đêm của tảo theo hàm điều hòa:
  $$\text{DO}(t) = \text{DO}_{\text{mean}} + \text{DO}_{\text{amp}} \cdot \sin\left(\frac{2\pi(t - 9)}{24}\right) + \text{Noise}$$
- Khi sục khí được kích hoạt, nồng độ oxy được bù đắp tăng dần $+1.8\text{ mg/L}$.
- Đóng vai trò máy phát tải (Load Generator) sinh dữ liệu nền 24/7 để CrateDB tích lũy hơn 133.000 bản ghi lịch sử phục vụ vẽ biểu đồ và phân tích dữ liệu trên Grafana.
- Hỗ trợ tham số ép sự kiện oxy tụt đột ngột (`--anomaly-pond`, `--anomaly-after`) để kiểm tra phản ứng của hệ thống khi chạy tự động.

---

# CHƯƠNG 4: MÔ HÌNH DỮ LIỆU, GIAO THỨC TRUYỀN THÔNG VÀ NỀN TẢNG FIWARE

### 4.1. Mô hình Thực thể NGSI-v2 (Entity Data Model)
Mô hình thực thể được nhóm thiết kế tham khảo chuẩn FIWARE Smart Data Models trong lĩnh vực nông nghiệp và thủy sản:
- **Entity Type**: `Pond`
- **Entity ID**: `urn:ngsi-ld:Pond:001` .. `urn:ngsi-ld:Pond:005`
- **FIWARE Service**: `shrimp` | **ServicePath**: `/`

| Thuộc tính (Attribute) | Kiểu dữ liệu | Object ID (MQTT) | Ý nghĩa kỹ thuật |
|---|:---:|:---:|---|
| `dissolvedOxygen` | Number | `do` | Nồng độ Oxy hòa tan ($0.0 - 14.0\text{ mg/L}$) |
| `pH` | Number | `ph` | Độ pH của nước ao ($6.5 - 9.5$) |
| `temperature` | Number | `t` | Nhiệt độ nước ao ($15.0 - 40.0^\circ\text{C}$) |
| `salinity` | Number | `s` | Độ mặn ($0.0 - 40.0\text{ ppt}$) |
| `aeratorState` | Text | `a` | Trạng thái máy sục khí (`ON` / `OFF`) |
| `aerator` | command | - | Lệnh bật/tắt sục khí gửi từ Platform xuống thiết bị |
| `aerator_status` | commandStatus | - | Trạng thái thực thi lệnh (`PENDING`, `OK`, `ERROR`) |
| `aerator_info` | commandResult | - | Kết quả phản hồi thực tế từ thiết bị (`ON`, `OFF`) |

### 4.2. Cấu trúc Topic và Định dạng Gói tin MQTT
Quy ước định dạng JSON giữa thiết bị và IoT Agent tuân thủ chuẩn IoTA-JSON:
1. **Dữ liệu quan trắc (Thiết bị $\rightarrow$ IoT Agent)**:
   - Topic: `/shrimpkey/{device_id}/attrs`
   - Payload:
     ```json
     {"do": 5.40, "ph": 7.82, "t": 28.5, "s": 15.0, "a": "OFF"}
     ```
2. **Lệnh điều khiển sục khí (Platform $\rightarrow$ Thiết bị)**:
   - Topic: `/shrimpkey/{device_id}/cmd`
   - Payload:
     ```json
     {"aerator": "ON"}
     ```
3. **Xác nhận thực thi lệnh (Thiết bị $\rightarrow$ Platform)**:
   - Topic: `/shrimpkey/{device_id}/cmdexe`
   - Payload:
     ```json
     {"aerator": "ON"}
     ```

### 4.3. Cấu hình Subscriptions trong Orion Context Broker
Orion sử dụng cơ chế Subscription để tự động chuyển tiếp dữ liệu ngữ cảnh:
1. **Subscription tới QuantumLeap (Đồng bộ Lịch sử)**:
   - Sử dụng **định dạng chuẩn (Normalized format)** theo yêu cầu của QuantumLeap để ánh xạ đầy đủ kiểu dữ liệu thuộc tính vào CrateDB.
   - Trạng thái hoạt động: Đã gửi thành công $> 126.000$ thông báo với mã `HTTP 200`.
2. **Subscription tới Node-RED (Rule Engine)**:
   - Sử dụng **định dạng rút gọn (`attrsFormat: "keyValues"`)** giúp luồng Function node của Node-RED truy xuất trực tiếp các trường `msg.payload.data[i].dissolvedOxygen` mà không cần bóc tách metadata phức tạp.
   - Trạng thái hoạt động: Đã gửi thành công $> 99.000$ thông báo với mã `HTTP 200`.

---

# CHƯƠNG 5: XỬ LÝ DỮ LIỆU, RULE ENGINE VÀ CHU TRÌNH TỰ ĐỘNG KHÉP KÍN

### 5.1. Logic Điều khiển Trễ Hysteresis trên Node-RED
Nhằm chống hiện tượng chập chờn rơ-le (Relay Chattering) khi oxy dao động quanh ngưỡng kích hoạt, hệ thống áp dụng dải trễ (**Hysteresis**):

```
               DO tụt < 4.0 mg/L (Bật sục khí)
  [Máy sục khí OFF] ───────────────────────────▶ [Máy sục khí ON]
          ▲                                             │
          │                                             │
          └─────────────────────────────────────────────┘
               DO hồi phục > 6.0 mg/L (Tắt sục khí)
```

- **Quy tắc 1 (Thiếu oxy)**: Khi $\text{DO} < 4.0\text{ mg/L}$ và sục khí đang `OFF` $\rightarrow$ Gửi lệnh PATCH tới Orion: `aerator: ON`.
- **Quy tắc 2 (Hồi phục & Tiết kiệm điện)**: Khi $\text{DO} > 6.0\text{ mg/L}$ và sục khí đang `ON` $\rightarrow$ Gửi lệnh PATCH tới Orion: `aerator: OFF`.
- **Quy tắc 3 (Báo động nguy cấp)**: Khi $\text{DO} < 2.5\text{ mg/L}$ $\rightarrow$ Phát cảnh báo nguy cấp `CRITICAL` và kích hoạt sục khí khẩn cấp.
- **Quy tắc 4 (Nhiệt độ cao)**: Khi $T > 33.0^\circ\text{C}$ $\rightarrow$ Cảnh báo nhiệt độ cao và kích hoạt sục khí hỗ trợ hòa tan oxy.
- **Quy tắc 5 (Bất thường pH)**: Khi $\text{pH} < 7.5$ hoặc $\text{pH} > 8.5$ $\rightarrow$ Phát cảnh báo kiểm tra môi trường ao nuôi.

### 5.2. Bằng chứng Chu trình Tự động Khép kín (Closed-Loop Proof)
Chu trình khép kín hai chiều được chứng minh qua hai phương thức thực nghiệm:

#### A. Kiểm chứng trên Thiết bị Mô phỏng Phần cứng Wokwi ESP32
Thực thi kiểm chứng qua script [test_wokwi_loop.py](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/source/test_wokwi_loop.py) kết nối trực tiếp với Broker công cộng `broker.emqx.io`:
1. ESP32 Wokwi phát hiện $\text{DO} = 3.1\text{ mg/L} < 4.0\text{ mg/L}$, publish lên `iot_nhom5_shrimp_c8d2/pond001/attrs`.
2. Gói tin được EMQX Bridge chuyển tiếp vào IoT Agent local $\rightarrow$ Orion nhận diện vi phạm $\rightarrow$ Node-RED ra lệnh `aerator: ON`.
3. Lệnh được IoT Agent phát vào local topic `/cmd`, EMQX Bridge chuyển ngược ra `iot_nhom5_shrimp_c8d2/pond001/cmd` trên `broker.emqx.io`.
4. Vi điều khiển ESP32 Wokwi nhận lệnh, kích hoạt `GPIO 2` lên mức cao: **Relay đóng, Đèn LED xanh máy sục khí sáng**.
5. ESP32 gửi gói tin xác nhận `cmdexe: ON` về Broker công cộng $\rightarrow$ Bridge chuyển về Orion cập nhật `aerator_status: OK` và `aeratorState: ON`.
6. Khi nồng độ oxy hồi phục lên $6.4\text{ mg/L} > 6.0\text{ mg/L}$, Node-RED phát lệnh ngắt `aerator: OFF` $\rightarrow$ ESP32 nhận lệnh: **Relay ngắt, Đèn LED tắt** và gửi xác nhận `cmdexe: OFF`.

#### B. Kiểm chứng trên Phần mềm Giả lập Ao nuôi (Software Simulator)
Thực thi kiểm chứng chi tiết từng mốc thời gian qua script [prove_closed_loop.py](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/source/prove_closed_loop.py) trên ao `pond003` ([CLOSED_LOOP_EVIDENCE.md](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/tests/CLOSED_LOOP_EVIDENCE.md)):

| Mốc thời gian | Giai đoạn | Diễn biến thực nghiệm | Trạng thái Orion Entity |
|:---:|:---|:---|:---|
| `23:37:09.954` | **1. Khởi tạo** | Ao `pond003` hoạt động bình thường, DO đầy đủ. | `DO=6.41 mg/L`, `aeratorState=OFF` |
| `23:37:12.955` | **2. Ép sự kiện** | Giả lập sự kiện DO tụt sâu xuống `3.20 mg/L` ($< 4.0$). | `DO=3.20 mg/L`, `aeratorState=OFF` |
| `23:37:12.996` | **3. Ra lệnh** | Node-RED phát hiện vi phạm, gửi lệnh PATCH `aerator: ON`. | `aerator_status=PENDING`, `aerator=ON` |
| `23:37:13.456` | **4. Thực thi** | Simulator nhận lệnh, bật cờ sục khí, gửi `cmdexe: ON`. | `aerator_status=OK`, `aerator_info=ON` |
| `23:37:17.475` | **5. Xác nhận** | Orion cập nhật trạng thái sục khí đang hoạt động. | `DO=3.90 mg/L`, `aeratorState=ON` |
| `23:37:19 - 27` | **6. Hồi phục** | Nồng độ oxy tăng dần: $4.50 \rightarrow 5.20 \rightarrow 5.80 \rightarrow 6.35\text{ mg/L}$. | `DO tăng dần`, `aeratorState=ON` |
| `23:37:27.516` | **7. Tự động ngắt** | Khi $\text{DO} = 6.35 > 6.0$, Node-RED tự động gửi lệnh `aerator: OFF`. | `aerator_status=PENDING`, `aerator=OFF` |
| `23:37:27.978` | **8. Phản hồi** | Simulator ngắt cờ sục khí, gửi `cmdexe: OFF`. | `aerator_status=OK`, `aerator_info=OFF` |
| `23:37:31.999` | **9. Ổn định** | Toàn bộ chu trình hoàn tất an toàn. | `DO=6.10 mg/L`, `aeratorState=OFF` |

### 5.3. Lưu trữ Chuỗi Thời gian Đơn Nút trên CrateDB và Phép toán Aggregation
Dữ liệu lịch sử được QuantumLeap ghi nhận vào bảng `mtshrimp.etpond` trên CrateDB (triển khai dạng đơn nút - Single-node):
- **Cấu trúc bảng**: `entity_id` (Text), `time_index` (Timestamp), `dissolvedoxygen` (Float), `ph` (Float), `temperature` (Float), `salinity` (Float), `aeratorstate` (Text), `aerator_status` (Text), `aerator_info` (Text).
- **Quy mô tích lũy**: Đã tích lũy an toàn **hơn 123.400 bản ghi** trong Docker Volume `crate-data`.
- **Truy vấn tổng hợp theo giờ (Hourly Aggregation)**:
  ```sql
  SELECT date_trunc('hour', time_index) AS "time",
         avg(dissolvedoxygen) AS "DO_TB",
         avg(ph) AS "pH_TB",
         avg(temperature) AS "Temp_TB"
  FROM mtshrimp.etpond
  WHERE entity_id = '$pond_id' AND $__timeFilter(time_index)
  GROUP BY 1 ORDER BY 1 ASC;
  ```
  Thời gian đáp ứng của truy vấn tổng hợp trên CrateDB duy trì ổn định trong khoảng **$12 - 40\text{ ms}$**.

### 5.4. Thiết kế Dashboard Giám sát Toàn diện trên Grafana
Dashboard (UID: `shrimp-pond-monitor`) gồm **20 Panels trực quan**, sử dụng hoàn toàn nhãn tiếng Việt không dấu (ASCII-safe) để tránh lỗi hiển thị ký tự:
1. **Hàng 1 - Trạng thái hệ thống & thiết bị**:
   - Stat: Tổng số bản ghi CrateDB ($> 123.400$).
   - Stat: Số lượng ao đang giám sát ($5\text{ ao}$).
   - Stat: Trạng thái kết nối MQTT Bridge (`ACTIVE` qua `broker.emqx.io`).
   - Stat: Quy định ngưỡng DO an toàn ($\text{DO} < 4.0\text{ mg/L} \rightarrow \text{Bật sục khí}$).
2. **Hàng 2 - Chỉ số tức thời theo ao chọn lọc (`$pond_id`)**:
   - 5 Stat cards cho DO (mg/L), pH, Nhiệt độ ($^\circ\text{C}$), Độ mặn (ppt), Trạng thái sục khí (Đang sục khí xanh / Đang tắt xám).
3. **Hàng 3 - Diễn biến Time-series & Ngưỡng điều khiển**:
   - Biểu đồ DO dạng đường mượt với 3 dải màu ngưỡng trực quan (Đỏ $< 2.5$, Cam $< 4.0$, Xanh $> 6.0$).
   - Biểu đồ bước (Step-after chart) thể hiện lịch sử đóng ngắt máy sục khí ($0$ hoặc $1$).
   - Biểu đồ kết hợp 2 trục tung cho pH (trục trái) và Nhiệt độ (trục phải).
   - Biểu đồ diễn biến Độ mặn theo thời gian.
4. **Hàng 4 - Tổng hợp Thống kê & Nhật ký Cảnh báo**:
   - Biểu đồ cột tổng hợp DO trung bình theo từng giờ (`Hourly Aggregation`).
   - Bảng nhật ký sự kiện cảnh báo vượt ngưỡng (`Alert History`), tự động highlight màu đỏ cho các dòng DO $< 2.5$ và màu cam cho DO $< 4.0$.
   - Bảng đo lường 30 bản ghi gần nhất của tất cả các ao.

---

# CHƯƠNG 6: KIỂM THỬ, ĐÁNH GIÁ HIỆU NĂNG VÀ THỬ NGHIỆM MỞ RỘNG

### 6.1. Kết quả Thực nghiệm 5 Kịch bản Hoạt động (5 Test Scenarios)
Script kiểm thử tự động [test_scenarios.py](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/source/test_scenarios.py) thực thi độc lập và đạt kết quả tuyệt đối **100% PASSED** ([TEST_REPORT.md](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/tests/TEST_REPORT.md)):

| Kịch bản | Tên kịch bản | Hành động thực nghiệm | Kết quả ghi nhận | Đánh giá |
|:---:|:---|:---|:---|:---:|
| **KB 1** | Hoạt động bình thường | Gửi DO=5.5 mg/L, pH=7.8, T=28°C, S=15 ppt, aerator=OFF. | Orion cập nhật đầy đủ, không phát sinh cảnh báo, sục khí duy trì OFF. | **PASSED** |
| **KB 2** | DO xuống thấp ($< 4.0\text{ mg/L}$) | Phát sự kiện DO=3.1 mg/L ($< 4.0$). | Node-RED phát hiện vi phạm, phát lệnh `aerator: ON`, Orion cập nhật `PENDING` $\rightarrow$ `OK`. | **PASSED** |
| **KB 3** | DO hồi phục ($> 6.0\text{ mg/L}$) | Phát sự kiện DO=6.5 mg/L ($> 6.0$). | Node-RED phát hiện hồi phục theo dải trễ Hysteresis, phát lệnh ngắt `aerator: OFF`. | **PASSED** |
| **KB 4** | Giám sát nhiều ao đồng thời | Kiểm tra đồng thời cả 5 ao `urn:ngsi-ld:Pond:001` .. `005`. | Toàn bộ 5 ao cập nhật liên tục song song, không xung đột dữ liệu. | **PASSED** |
| **KB 5** | Dữ liệu lịch sử CrateDB | Kiểm tra CSDL CrateDB và chạy truy vấn Aggregation. | Tích lũy $> 123.400$ bản ghi; truy vấn tính trung bình theo giờ phản hồi nhanh ($18.5\text{ ms}$). | **PASSED** |

### 6.2. Đánh giá Khả năng Chịu lỗi và Độ Tin cậy (Reliability Test)
Script [test_reliability.py](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/source/test_reliability.py) đã kiểm chứng 4 tiêu chí chịu lỗi đạt **4/4 PASS**:
1. **Kháng gói tin hỏng (Malformed JSON)**: Bơm chuỗi ký tự ngẫu nhiên và JSON thiếu ngoặc vào topic `/shrimpkey/pond001/attrs` $\rightarrow$ IoT Agent bắt lỗi an toàn, ghi log cảnh báo và tiếp tục hoạt động mà không bị crash.
2. **Kháng sai lệch kiểu dữ liệu (Type Mismatch)**: Gửi chuỗi `"abc"` vào trường nồng độ oxy `do` $\rightarrow$ Hệ thống từ chối bản tin sai kiểu, giữ nguyên giá trị hợp lệ trước đó.
3. **Cách ly lỗi giữa các ao (Fault Isolation)**: Khi một ao gặp sự cố truyền tin, các ao còn lại vẫn cập nhật dữ liệu bình thường, không bị ảnh hưởng chéo.
4. **Bảo toàn dữ liệu (State Persistence)**: Khi khởi động lại toàn bộ Docker containers (`docker compose restart`), toàn bộ cấu hình, subscriptions và hơn 123.000 bản ghi lịch sử đều được bảo toàn nguyên vẹn nhờ Docker Volumes chuyên dụng.

### 6.3. Thử nghiệm Mở rộng và Đo Hiệu năng Thực tế (Scale Benchmark - Mục 17 Đề tài)
Theo đúng yêu cầu của Mục 17 trong Đề tài về đánh giá khả năng mở rộng (Scale Test từ 5 $\rightarrow$ 10 $\rightarrow$ 50 $\rightarrow$ 100 thiết bị), script [benchmark_scale.py](file:///d:/Hoc_Ths/IoT/IoT_Nhom5/source/benchmark_scale.py) đã thực hiện đo đạc toàn diện **đầy đủ 7 chỉ số mở rộng**:

**Bảng Tổng hợp Hiệu năng Mở rộng Toàn diện (5 $\rightarrow$ 100 Thiết bị)**:

| Quy mô thiết bị | Tổng số gói | Message Rate (Throughput) | Latency E2E TB | Latency p95 | Processing Time (CrateDB Query) | Network Traffic (MQTT Inbound) | Tỷ lệ bản tin nhận |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **5 ao** | 10 | **38.6 msg/s** | **72.3 ms** | 78.0 ms | **18.1 ms** | **0.72 Kbps** (90 B/s) | **10/10 (100%)** |
| **10 ao** | 20 | **73.4 msg/s** | **76.2 ms** | 105.0 ms | **12.1 ms** | **1.44 Kbps** (180 B/s) | **20/20 (100%)** |
| **20 ao** | 40 | **72.0 msg/s** | **170.3 ms** | 220.0 ms | **39.7 ms** | **2.88 Kbps** (360 B/s) | **40/40 (100%)** |
| **50 ao** | 100 | **80.4 msg/s** | **397.9 ms** | 513.7 ms | **12.7 ms** | **7.20 Kbps** (900 B/s) | **100/100 (100%)** |
| **100 ao** | 200 | **96.5 msg/s** | **673.7 ms** | **1,006.7 ms** | **32.0 ms** | **14.40 Kbps** (1.8 KB/s) | **200/200 (100%)** |

**Phân tích Chi tiết 7 Chỉ số Mở rộng (Scalability Metrics)**:
1. **Message Rate**: Tăng từ $38.6\text{ msg/s}$ (5 ao) lên **$96.5\text{ msg/s}$ (100 ao)**, chứng minh nền tảng xử lý đồng thời tốt, không xảy ra nghẽn hàng đợi (Queue Bottleneck).
2. **CPU**: Duy trì trung bình $\approx 2.1\%$ ở mức nền; khi bắn tải 100 ao đồng thời với QoS 1, CPU tăng đỉnh ngắn hạn lên $\approx 90\%$ (chủ yếu tại MongoDB và IoT Agent) trong $1 - 2\text{ giây}$ rồi hạ ngay về bình thường sau khi nạp batch xong.
3. **RAM**: Tiêu thụ ổn định $\approx 2.56\text{ GiB}$ trên toàn bộ stack 8 containers (trong đó CrateDB dùng $1.64\text{ GiB}$ cho Lucene cache và Heap).
4. **Network Traffic (Băng thông mạng)**:
   - Gói tin JSON từ cảm biến: $\approx 60\text{ bytes}$ + Header MQTT $\approx 30\text{ bytes}$ = $\approx 90\text{ bytes/tin}$.
   - Ở quy mô 100 ao (chu kỳ 5s): $100 \times 90 / 5 = 1.8\text{ KB/s}$ (**$14.4\text{ Kbps}$**).
   - Lưu lượng thông báo nội bộ (Orion $\rightarrow$ QuantumLeap/Node-RED): $\approx 10\text{ KB/s}$ ($80\text{ Kbps}$), hoàn toàn nằm trong năng lực mạng viễn thông/4G nông nghiệp.
5. **Storage Growth (Tốc độ tăng trưởng lưu trữ CrateDB)**:
   - Bản ghi `mtshrimp.etpond` (8 trường) chiếm $\approx 200\text{ bytes/dòng}$.
   - Ở quy mô 5 ao: $3.600\text{ dòng/giờ}$ $\rightarrow$ $17.3\text{ MB/ngày}$ ($\approx 0.52\text{ GB/tháng}$).
   - Ở quy mô 100 ao: $72.000\text{ dòng/giờ}$ $\rightarrow$ $345.6\text{ MB/ngày}$ ($\approx 10.37\text{ GB/tháng}$). Ổ cứng tiêu chuẩn $500\text{ GB}$ có thể lưu trữ liên tục $> 3\text{ năm}$.
6. **Latency (Độ trễ End-to-End)**:
   - Trung bình dao động từ $72.3\text{ ms}$ (5 ao) đến $673.7\text{ ms}$ (100 ao), p95 đạt $1.006\text{ ms}$. Đáp ứng xuất sắc yêu cầu giám sát thời gian thực của ao nuôi tôm.
7. **Processing Time (Thời gian xử lý & Truy vấn)**:
   - Orion cập nhật thực thể: $< 5\text{ ms}$.
   - CrateDB thực thi truy vấn tổng hợp theo giờ (`Hourly Aggregation` trên $> 130.000$ dòng): Trung bình $32.0\text{ ms}$ ở mức 100 ao.

### 6.4. Mức độ Tiêu thụ Tài nguyên Hệ thống (CPU & RAM)
Đo đạc trực tiếp qua lệnh `docker stats --no-stream` tại thời điểm hệ thống thực thi đợt thử nghiệm tải 100 luồng:

| Container Service | Vai trò trong Kiến trúc IIAF | Mức chiếm dụng CPU (%) | Bộ nhớ RAM sử dụng / Giới hạn | Tỷ lệ RAM (%) |
|---|---|:---:|:---:|:---:|
| `shrimp-crate` | CSDL CrateDB (Single-node) | 0.21% | 1.646 GiB / 2.0 GiB | 82.32% |
| `shrimp-emqx` | MQTT Broker (EMQX 5.8) | 5.21% | 301.5 MiB / 1.0 GiB | 29.45% |
| `shrimp-grafana` | Monitoring Dashboard | 0.08% | 59.5 MiB / 512 MiB | 11.61% |
| `shrimp-iot-agent` | FIWARE IoT Agent JSON | 1.48% | 104.6 MiB / 512 MiB | 20.43% |
| `shrimp-mongo` | MongoDB (Orion State) | 90.51% (đỉnh tải) | 260.3 MiB / 1.0 GiB | 25.42% |
| `shrimp-node-red` | Rule Engine Automation | 0.01% | 102.8 MiB / 512 MiB | 20.08% |
| `shrimp-orion` | Context Broker (Orion) | 2.93% | 44.1 MiB / 512 MiB | 8.60% |
| `shrimp-quantumleap` | Historical Sync Service | 0.05% | 92.1 MiB / 512 MiB | 17.99% |
| **TỔNG CỘNG** | **Toàn bộ stack 8 containers** | **~2.1% (nền) / ~98% (peak)** | **~2.56 GiB / 6.5 GiB** | **39.38%** |

---

# CHƯƠNG 7: ĐÁNH GIÁ ĐÓNG GÓP, HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN

### 7.1. Bảng Phân công Thành viên và Mức độ Đóng góp

| STT | Thành viên | Nhiệm vụ phân công cụ thể trong dự án | Tỷ lệ đóng góp |
|:---:|---|---|:---:|
| 1 | **Thành viên 1** (Trưởng nhóm) | - Nghiên cứu thiết kế kiến trúc IIAF 6 tầng theo yêu cầu đề bài.<br>- Cấu hình Docker Compose 8 service và mạng nội bộ.<br>- Xây dựng và kiểm chứng cầu nối MQTT Bridge 2 chiều trên EMQX.<br>- Soạn thảo nội dung Chương 1, 2 và chuẩn bị tài liệu thuyết trình. | **25%** |
| 2 | **Thành viên 2** | - Thiết kế sơ đồ phần cứng và viết Firmware ESP32 trên Wokwi.<br>- Xây dựng bộ giả lập Python Simulator đa ao chu kỳ ngày/đêm.<br>- Kiểm chứng luồng đóng ngắt Relay/LED Wokwi qua Broker công cộng.<br>- Soạn thảo nội dung Chương 3 và kịch bản video demo. | **25%** |
| 3 | **Thành viên 3** | - Cấu hình IoT Agent JSON và định nghĩa mô hình thực thể NGSI-v2.<br>- Thiết lập các Subscriptions trong Orion Context Broker.<br>- Lập trình Rule Engine điều khiển trễ Hysteresis trên Node-RED.<br>- Soạn thảo nội dung Chương 4, 5. | **25%** |
| 4 | **Thành viên 4** | - Cấu hình CrateDB đơn nút và QuantumLeap đồng bộ dữ liệu chuỗi thời gian.<br>- Thiết kế Dashboard 20 Panels trên Grafana.<br>- Xây dựng bộ script kiểm thử tự động, đo hiệu năng và thu thập tài nguyên hệ thống.<br>- Soạn thảo nội dung Chương 6, 7. | **25%** |

### 7.2. Bảng Đối chiếu Yêu cầu Đề tài và Minh chứng Thực hiện

| Yêu cầu của Đề tài | Giải pháp kỹ thuật đã triển khai | Vị trí minh chứng kỹ thuật |
|---|---|---|
| **End-to-End Integration** | Tích hợp hoàn chỉnh chuỗi khép kín 2 chiều: Cảm biến $\rightarrow$ EMQX $\rightarrow$ IoT Agent $\rightarrow$ Orion $\rightarrow$ Node-RED $\rightarrow$ Orion $\rightarrow$ IoT Agent $\rightarrow$ Thiết bị đóng Relay $\rightarrow$ QuantumLeap $\rightarrow$ CrateDB $\rightarrow$ Grafana. | - File kiểm chứng: `source/prove_closed_loop.py`<br>- Báo cáo kết quả: `tests/CLOSED_LOOP_EVIDENCE.md`<br>- Mục báo cáo: Mục 5.2 |
| **Kiến trúc IIAF 6 tầng** | Phân bổ chuẩn xác 6 tầng: Devices, Communication, IoT Platform (FIWARE trọn bộ), Data/Analytics (QuantumLeap + CrateDB), Processing/Decision (Node-RED), Application (Grafana). | - Sơ đồ kiến trúc: Chương 2<br>- Bảng ánh xạ: Mục 2.2 |
| **Communication & Broker** | Sử dụng EMQX 5.8 với giao thức MQTT QoS 1; thiết lập MQTT Bridge 2 chiều với Broker công cộng sử dụng tiền tố độc nhất `iot_nhom5_shrimp_c8d2/`. | - Cấu hình: `source/setup_emqx_bridge.py`<br>- Kiểm chứng: `source/verify_bidirectional_bridge.py`<br>- Mục báo cáo: Mục 3.3 |
| **Processing & Rule Engine** | Xây dựng Rule Engine trên Node-RED tự động điều khiển sục khí theo cơ chế trễ Hysteresis (bật khi DO $< 4.0$, tắt khi DO $> 6.0$); thực thi truy vấn tổng hợp theo giờ trên CrateDB. | - Flow Node-RED: `config/node-red/flows.json`<br>- Mục báo cáo: Mục 5.1 & 5.3 |
| **Phân tích Bài toán & Yêu cầu** | Xác định rõ bối cảnh, 4 nhóm stakeholder, phạm vi in/out-scope, 6 yêu cầu chức năng (FR), 5 yêu cầu phi chức năng (NFR) và cơ sở kỹ thuật cho các ngưỡng. | - Mục báo cáo: Chương 1 |
| **IoT Devices & Wokwi** | Sơ đồ phần cứng ESP32 trên Wokwi kết nối Broker công cộng qua Bridge, điều khiển Relay/LED; bộ Simulator Python mô phỏng chu kỳ sinh học ngày/đêm và ép sự kiện. | - Mã nguồn: `wokwi/sketch.ino`, `wokwi/diagram.json`<br>- Bộ giả lập: `source/simulator.py`<br>- Mục báo cáo: Chương 3 |
| **Data Storage & Management** | CrateDB đơn nút lưu trữ an toàn $> 123.400$ bản ghi; cấu trúc bảng thời gian thực `mtshrimp.etpond`; mô tả chính sách lưu trữ (Data Retention). | - CSDL: CrateDB port 4200/5432<br>- Mục báo cáo: Mục 5.3 |
| **Testing & Evaluation** | Kiểm thử tự động 5 kịch bản hoạt động (100% PASS); kiểm tra 4 tiêu chí chịu lỗi (Reliability) đạt 4/4 PASS. | - Kịch bản test: `source/test_scenarios.py`<br>- Báo cáo test: `tests/TEST_REPORT.md`<br>- Mục báo cáo: Mục 6.1 & 6.2 |
| **Đánh giá Khả năng Mở rộng (Mục 17 Đề tài)** | Thử nghiệm scale theo đúng thang bậc $5 \rightarrow 10 \rightarrow 20 \rightarrow 50 \rightarrow 100$ thiết bị. Đánh giá toàn diện đủ 7 tiêu chí: Message rate, CPU, RAM, Network traffic, Storage growth, Latency, Processing time. | - Script benchmark: `source/benchmark_scale.py`<br>- Báo cáo hiệu năng: `tests/BENCHMARK_REPORT.md`<br>- Mục báo cáo: Mục 6.3 & 6.4 |
| **Dashboard & Trực quan hóa** | Grafana Dashboard 20 panels với nhãn tiếng Việt không dấu, theo dõi trạng thái hệ thống, chỉ số tức thời, đồ thị ngưỡng và nhật ký cảnh báo. | - File cấu hình: `config/grafana/.../shrimp_pond_dashboard.json`<br>- Đường dẫn: `/d/shrimp-pond-monitor`<br>- Mục báo cáo: Mục 5.4 |
| **Tích hợp $\ge 2$ thành phần** | Tích hợp thành công nền tảng FIWARE (nhóm nghiên cứu) với EMQX Broker, Node-RED, CrateDB và Grafana. | - Cấu hình stack: `docker/docker-compose.yml`<br>- Mục báo cáo: Mục 2.3 |

### 7.3. Hạn chế Hiện tại của Hệ thống
1. **Triển khai đơn nút (Single-node Deployment)**: Toàn bộ 8 dịch vụ hiện đang được đóng gói trong một máy chủ Docker Compose cục bộ; CrateDB vận hành ở chế độ một nút chưa khai thác tính năng cụm phân tán đa máy (Multi-node Cluster).
2. **Bảo mật kênh truyền**: Môi trường thử nghiệm PoC hiện tại đang mở cổng 1883 không mật khẩu để đơn giản hóa quá trình phát triển và gỡ lỗi gói tin; chưa áp dụng xác thực mTLS trên luồng kết nối Wokwi qua Broker công cộng.
3. **Phụ thuộc kết nối Internet cho Wokwi**: Cơ chế MQTT Bridge bắc cầu thiết bị Wokwi yêu cầu máy chủ phát triển phải có kết nối Internet để liên lạc với `broker.emqx.io`.

### 7.4. Hướng Phát triển Tương lai
1. **Mở rộng cụm phân tán (Distributed Cluster)**: Phân tách hệ thống thành các cụm máy chủ chuyên trách: Edge Gateway thu thập tại trang trại, Context Broker đặt tại trung tâm dữ liệu và cụm CrateDB lưu trữ phân tán có dự phòng dữ liệu.
2. **Kích hoạt toàn diện bảo mật công nghiệp**: Thiết lập danh sách kiểm soát truy cập (ACL) và xác thực người dùng trên EMQX; mã hóa kênh truyền qua giao thức MQTTS (Port 8883) với chứng chỉ số TLS.
3. **Ứng dụng Trí tuệ Nhân tạo (AI/ML Predictive Control)**: Nghiên cứu mô hình học máy chuỗi thời gian (như LSTM) nhằm dự báo xu hướng suy giảm oxy hòa tan trước $2 - 3\text{ giờ}$ dựa trên diễn biến nhiệt độ và ánh sáng, giúp hệ thống chủ động kích hoạt quạt nước trước khi ao rơi vào tình trạng thiếu oxy.
4. **Tích hợp cảnh báo đa kênh**: Mở rộng webhook của Node-RED để gửi thông báo tức thời qua Telegram Bot hoặc tin nhắn SMS khi phát sinh cảnh báo cấp độ `CRITICAL`.

---

# TÀI LIỆU THAM KHẢO

1. **Boyd, C. E. (1998)**. *Water Quality for Pond Aquaculture*. Research and Development Series No. 43, International Center for Aquaculture and Aquatic Environments, Auburn University, Alabama.
2. **Bộ Nông nghiệp và Phát triển Nông thôn (2023)**. *Tiêu chuẩn quốc gia TCVN 13656:2023 - Nước nuôi trồng thủy sản – Yêu cầu chất lượng nước nuôi thâm canh tôm sú và tôm thẻ chân trắng*. Nhà xuất bản Khoa học và Kỹ thuật, Hà Nội.
3. **Bộ Nông nghiệp và Phát triển Nông thôn (2014)**. *Quy chuẩn kỹ thuật quốc gia QCVN 02-19:2014/BNNPTNT về Cơ sở nuôi tôm nước lợ - Điều kiện bảo đảm an toàn thực phẩm, bảo vệ môi trường và thú y*. Hà Nội.
4. **FIWARE Foundation (2023)**. *FIWARE NGSI-v2 API Specifications*. Tài liệu chính thức: `https://fiware-orion.readthedocs.io/en/latest/`.
5. **FIWARE Foundation (2023)**. *FIWARE IoT Agent for JSON Developers Guide*. Tài liệu chính thức: `https://fiware-iotagent-json.readthedocs.io/en/latest/`.
6. **OASIS Open (2014)**. *MQTT Version 3.1.1 OASIS Standard*. OASIS Standard Specification.
7. **EMQ Technologies (2024)**. *EMQX Open Source MQTT Broker Documentation (Version 5.8)*. Tài liệu chính thức: `https://www.emqx.io/docs/en/latest/`.
8. **Wokwi Documentation (2024)**. *ESP32 WiFi Simulation and Network Protocols Guide*. Tài liệu kỹ thuật: `https://docs.wokwi.com/guides/esp32-wifi`.
