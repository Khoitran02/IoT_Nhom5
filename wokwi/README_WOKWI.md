# HUONG DAN CHAY MO PHONG ESP32 TREN WOKWI (TASK 2.4)
## HE THONG GIAM SAT VA DIEU KHIEN SUC KHI AO TOM (IOT NHOM 5)

Thư mục này chứa toàn bộ mã nguồn Firmware và sơ đồ mạch phần cứng để chạy mô phỏng thiết bị ao nuôi tôm bằng ESP32 trên nền tảng **Wokwi** (trực tiếp trên trình duyệt web hoặc VS Code Wokwi extension).

---

### 1. CAC LINH KIEN MO PHONG (PARTS)

1. **Board điều khiển**: ESP32 DevKit C v4.
2. **Cảm biến Oxy hòa tan (DO)**: Biến trở nối chân `GPIO 34` (ADC1), dải đo 0.0 - 12.0 mg/L.
3. **Cảm biến pH**: Biến trở nối chân `GPIO 35` (ADC1), dải đo 6.5 - 9.5 pH.
4. **Cảm biến Độ mặn**: Biến trở nối chân `GPIO 32` (ADC1), dải đo 5.0 - 35.0 ppt.
5. **Cảm biến Nhiệt độ nước**: Cảm biến kỹ thuật số DS18B20 nối chân `GPIO 4` (OneWire).
6. **Cơ cấu chấp hành (Actuator)**: Relay Module + Đèn LED xanh (May suc khi) nối chân `GPIO 2`.

---

### 2. CACH CHAY TREN WOKWI WEB (wokwi.com)

1. Mở trình duyệt truy cập: [https://wokwi.com/projects/new/esp32](https://wokwi.com/projects/new/esp32)
2. Copy toàn bộ nội dung file [`sketch.ino`](sketch.ino) dán vào tab **`sketch.ino`**.
3. Copy toàn bộ nội dung file [`diagram.json`](diagram.json) dán vào tab **`diagram.json`**.
4. Vào tab **`libraries.txt`**, thêm 4 thư viện:
   ```text
   PubSubClient
   OneWire
   DallasTemperature
   ArduinoJson
   ```
5. Bấm nút **Play (Run Simulation)** để bắt đầu chạy.
   - Xoay biến trở DO, pH, Độ mặn hoặc bấm vào DS18B20 để thay đổi nhiệt độ.
   - Nhìn Serial Monitor để thấy ESP32 đóng gói JSON và publish lên MQTT.
   - Khi hệ thống FIWARE / Node-RED phát lệnh sục khí, Relay đóng, đèn LED sáng lên và ESP32 gửi phản hồi xác nhận `cmdexe`.

---

### 3. KET NOI WOKWI VOI EMQX LOCAL QUA MQTT BRIDGE (HO TRO CA 5 AO WOKWI)

Hệ thống đã cấu hình sẵn **15 MQTT Bridge 2 chiều** trực tiếp trên container EMQX local nối với public broker `broker.emqx.io` cho toàn bộ **5 ao nuôi (`pond001` đến `pond005`)**:
- **Ingress (Sensor Data)**: Wokwi publish lên `iot_nhom5_shrimp_c8d2/{device_id}/attrs` trên `broker.emqx.io` -> EMQX Bridge tự động bắc cầu vào `/shrimpkey/{device_id}/attrs` local -> IoT Agent JSON -> Orion Context Broker -> CrateDB & Grafana.
- **Egress (Control Command)**: Node-RED gửi lệnh sục khí vào Orion -> IoT Agent bắn vào `/shrimpkey/{device_id}/cmd` -> EMQX Bridge tự động bắc cầu ra `iot_nhom5_shrimp_c8d2/{device_id}/cmd` trên `broker.emqx.io` -> Wokwi ESP32 nhận lệnh, bật Relay/LED sáng.
- **Ingress (Command Execution Result)**: Wokwi publish kết quả lên `iot_nhom5_shrimp_c8d2/{device_id}/cmdexe` -> EMQX Bridge chuyển về `/shrimpkey/{device_id}/cmdexe` -> IoT Agent xác nhận trạng thái lệnh `OK`.

---

### 4. CAU TRUC 5 THIET BI WOKWI CHUYEN BIET CHO 5 AO (DAP UNG >= 5 THIET BI BAT BUOC)

Mỗi ao nuôi được trang bị 1 thư mục dự án Wokwi độc lập, đã cấu hình sẵn đúng `DEVICE_ID` và sơ đồ mạch riêng:
- [`wokwi/pond001/`](pond001/): Thiết bị trạm Ao 1 (`pond001`) - ESP32 + 4 cảm biến + Relay sục khí
- [`wokwi/pond002/`](pond002/): Thiết bị trạm Ao 2 (`pond002`) - ESP32 + 4 cảm biến + Relay sục khí
- [`wokwi/pond003/`](pond003/): Thiết bị trạm Ao 3 (`pond003`) - ESP32 + 4 cảm biến + Relay sục khí
- [`wokwi/pond004/`](pond004/): Thiết bị trạm Ao 4 (`pond004`) - ESP32 + 4 cảm biến + Relay sục khí
- [`wokwi/pond005/`](pond005/): Thiết bị trạm Ao 5 (`pond005`) - ESP32 + 4 cảm biến + Relay sục khí

**Cách khởi chạy đồng thời 5 ao trên Wokwi:**
1. Mở 5 tab trình duyệt tại [https://wokwi.com/projects/new/esp32](https://wokwi.com/projects/new/esp32).
2. Tương ứng mỗi tab, nạp mã nguồn từ thư mục `wokwi/pond001` đến `wokwi/pond005`.
3. Bấm **Play (Run)** trên cả 5 tab: Cả 5 trạm ESP32 Wokwi sẽ đồng thời phát dữ liệu cảm biến và sẵn sàng nhận lệnh điều khiển rơ-le độc lập.
4. Kiểm chứng tự động toàn bộ 5 thiết bị Wokwi bằng lệnh: `python source/test_all_5_wokwi.py`.

