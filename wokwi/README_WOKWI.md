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

### 3. KET NOI WOKWI VOI EMQX BROKER LOCAL

Wokwi chạy trên cloud browser, để kết nối với EMQX Broker đang chạy trên máy tính (`localhost:1883`), bạn có 3 lựa chọn:
1. **Dùng Public Broker test**: Đặt `MQTT_SERVER = "broker.emqx.io"` trong code.
2. **Dùng Cloudflare Tunnel / Ngrok**: Mở tunnel từ cổng 1883 của máy bạn ra Internet và nhập domain tunnel vào `MQTT_SERVER`.
3. **Dùng Wokwi IoT Gateway** (Dành cho tài khoản Wokwi Club / Private Gateway): trỏ thẳng về `10.0.2.2`.

