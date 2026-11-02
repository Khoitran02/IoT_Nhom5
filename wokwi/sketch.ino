/*
 * ============================================================================
 *  FIRMWARE ESP32 WOKWI - HE THONG GIAM SAT VA DIEU KHIEN AO NUOI TOM (NHOM 5)
 * ============================================================================
 *  Mo hinh ket noi:
 *    - Cam bien DO (Bien tro): Chan GPIO 34 (ADC1)
 *    - Cam bien pH (Bien tro): Chan GPIO 35 (ADC1)
 *    - Cam bien Do man (Bien tro): Chan GPIO 32 (ADC1)
 *    - Cam bien Nhiet do nuoc: DS18B20 tren chan GPIO 4 (OneWire)
 *    - Actuator May suc khi: Relay + LED tren chan GPIO 2
 *
 *  Giao thuc: MQTT (IoTA-JSON cho FIWARE)
 *    - Publish attrs : /{apikey}/{device_id}/attrs
 *    - Subscribe cmd : /{apikey}/{device_id}/cmd
 *    - Publish cmdexe: /{apikey}/{device_id}/cmdexe
 * ============================================================================
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>

// --- CAU HINH WI-FI & MQTT ---
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";

// Thay doi thanh IP may chay EMQX Broker hoac public broker
// Khi test Wokwi voi local broker, co the dung Wokwi IoT Gateway (localhost:1883) hoac Cloudflare tunnel
const char* MQTT_SERVER = "broker.emqx.io"; // Hoac IP may tinh cua ban
const int   MQTT_PORT   = 1883;
const char* APIKEY      = "shrimpkey";
const char* DEVICE_ID   = "pond001";

// --- DINH NGHIA CHAN PHAN CUNG ---
#define PIN_DO        34
#define PIN_PH        35
#define PIN_SAL       32
#define PIN_TEMP      4
#define PIN_RELAY     2

// --- KHOI TAO DOI TUONG ---
WiFiClient espClient;
PubSubClient mqttClient(espClient);
OneWire oneWire(PIN_TEMP);
DallasTemperature tempSensor(&oneWire);

// --- BIEN TRANG THAI ---
bool aeratorState = false;
unsigned long lastPublishTime = 0;
const unsigned long PUBLISH_INTERVAL = 5000; // 5 giay gui 1 lan

// Topic MQTT
String topicAttrs  = String("/") + APIKEY + "/" + DEVICE_ID + "/attrs";
String topicCmd    = String("/") + APIKEY + "/" + DEVICE_ID + "/cmd";
String topicCmdexe = String("/") + APIKEY + "/" + DEVICE_ID + "/cmdexe";

void setupWifi() {
  Serial.print("Dang ket noi WiFi: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi da ket noi!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.println("\n-------------------------------------------");
  Serial.print("[MQTT] Nhan lenh tu topic: ");
  Serial.println(topic);
  Serial.print("[MQTT] Payload: ");
  Serial.println(message);

  // Parse JSON command
  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, message);
  if (error) {
    Serial.print("Loi parse JSON: ");
    Serial.println(error.c_str());
    return;
  }

  if (doc.containsKey("aerator")) {
    String cmdVal = "";
    if (doc["aerator"].is<JsonObject>()) {
      cmdVal = doc["aerator"]["state"].as<String>();
    } else {
      cmdVal = doc["aerator"].as<String>();
    }
    cmdVal.toUpperCase();

    if (cmdVal == "ON" || cmdVal == "1" || cmdVal == "TRUE") {
      aeratorState = true;
      digitalWrite(PIN_RELAY, HIGH);
      Serial.println("[ACTUATOR] >>> BAT MAY SUC KHI (AERATOR = ON) <<<");
    } else if (cmdVal == "OFF" || cmdVal == "0" || cmdVal == "FALSE") {
      aeratorState = false;
      digitalWrite(PIN_RELAY, LOW);
      Serial.println("[ACTUATOR] >>> TAT MAY SUC KHI (AERATOR = OFF) <<<");
    }

    // Tra loi phan hoi ket qua len cmdexe (quy uoc IoT Agent)
    StaticJsonDocument<128> respDoc;
    respDoc["aerator"] = aeratorState ? "ON" : "OFF";
    char respBuffer[128];
    serializeJson(respDoc, respBuffer);

    mqttClient.publish(topicCmdexe.c_str(), respBuffer);
    Serial.print("[MQTT] Gui ket qua thuc thi len: ");
    Serial.print(topicCmdexe);
    Serial.print(" -> ");
    Serial.println(respBuffer);
  }
  Serial.println("-------------------------------------------\n");
}

void reconnectMqtt() {
  while (!mqttClient.connected()) {
    Serial.print("Dang ket noi MQTT Broker: ");
    Serial.print(MQTT_SERVER);
    Serial.print("...");

    String clientId = "ESP32-Shrimp-" + String(DEVICE_ID) + "-" + String(random(0xffff), HEX);
    if (mqttClient.connect(clientId.c_str())) {
      Serial.println(" DA KET NOI!");
      // Dang ky lang nghe topic nhan lenh dieu khien
      mqttClient.subscribe(topicCmd.c_str(), 1);
      Serial.print("Da subscribe topic nhan lenh: ");
      Serial.println(topicCmd);
    } else {
      Serial.print(" That bai, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" Thu lai sau 3s...");
      delay(3000);
    }
  }
}

float readDO() {
  int raw = analogRead(PIN_DO);
  // Bien tro 0 - 4095 map sang 0.0 - 12.0 mg/L
  return (float)raw * 12.0 / 4095.0;
}

float readPH() {
  int raw = analogRead(PIN_PH);
  // Bien tro 0 - 4095 map sang 6.5 - 9.5
  return 6.5 + ((float)raw * (9.5 - 6.5) / 4095.0);
}

float readSalinity() {
  int raw = analogRead(PIN_SAL);
  // Bien tro 0 - 4095 map sang 5.0 - 35.0 ppt
  return 5.0 + ((float)raw * (35.0 - 5.0) / 4095.0);
}

float readTemperature() {
  tempSensor.requestTemperatures();
  float tempC = tempSensor.getTempCByIndex(0);
  if (tempC == DEVICE_DISCONNECTED_C) {
    return 28.0; // Gia tri du phong neu chua cam bien
  }
  return tempC;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_RELAY, OUTPUT);
  digitalWrite(PIN_RELAY, LOW);

  analogReadResolution(12); // ADC 12-bit
  tempSensor.begin();

  setupWifi();
  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);

  Serial.println("\n=== HE THONG ESP32 WOKWI KHOI DONG THANH CONG ===");
}

void loop() {
  if (!mqttClient.connected()) {
    reconnectMqtt();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublishTime >= PUBLISH_INTERVAL) {
    lastPublishTime = now;

    float doVal   = readDO();
    float phVal   = readPH();
    float salVal  = readSalinity();
    float tempVal = readTemperature();

    // Dong goi du lieu theo quy uoc IoT Agent JSON
    StaticJsonDocument<256> doc;
    doc["do"] = round(doVal * 100.0) / 100.0;
    doc["ph"] = round(phVal * 100.0) / 100.0;
    doc["t"]  = round(tempVal * 100.0) / 100.0;
    doc["s"]  = round(salVal * 100.0) / 100.0;
    doc["a"]  = aeratorState ? "ON" : "OFF";

    char payload[256];
    serializeJson(doc, payload);

    mqttClient.publish(topicAttrs.c_str(), payload, true);

    Serial.print("[POND SENSORS] ");
    Serial.println(payload);
  }
}

