#include <WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>

/*
 * ==============================================================================
 * DU AN IoT NHOM 5 - HE THONG GIAM SAT VA DIEU KHIEN SUC KHI AO NUOI TOM
 * BOARD: ESP32 DevKit C v4
 * THIET BI: AO NUOI 003 (POND003)
 *
 * PHAN CUNG KET NOI:
 *   - GPIO 34 (ADC1): Cam bien Oxy hoa tan (DO) qua bien tro (0.0 - 12.0 mg/L)
 *   - GPIO 35 (ADC1): Cam bien pH qua bien tro (6.5 - 9.5 pH)
 *   - GPIO 32 (ADC1): Cam bien Do man qua bien tro (5.0 - 35.0 ppt)
 *   - GPIO 4        : Cam bien Nhiet do DS18B20 (OneWire)
 *   - GPIO 2        : Relay Module 5V & Den LED bao trang thai May suc khi (Aerator)
 *
 * GIAO THUC TRUYEN THONG:
 *   - MQTT QoS 1 qua EMQX Public Broker (broker.emqx.io:1883)
 *   - Bridge 2 chieu ve EMQX Container cuc bo (iot_nhom5_shrimp_c8d2/pond001/...)
 * ==============================================================================
 */

// --- CAU HINH WI-FI & MQTT ---
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";

const char* MQTT_SERVER  = "broker.emqx.io";
const int   MQTT_PORT    = 1883;
const char* TOPIC_PREFIX = "iot_nhom5_shrimp_c8d2";
const char* DEVICE_ID    = "pond003";

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
unsigned long lastMqttReconnectAttempt = 0;
int mqttFailCount = 0;

// Topic MQTT bac cau qua EMQX Bridge
String topicAttrs  = String(TOPIC_PREFIX) + "/" + DEVICE_ID + "/attrs";
String topicCmd    = String(TOPIC_PREFIX) + "/" + DEVICE_ID + "/cmd";
String topicCmdexe = String(TOPIC_PREFIX) + "/" + DEVICE_ID + "/cmdexe";

void setupWifi() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFi.disconnect(true);
    delay(100);
  }

  Serial.print("Dang ket noi WiFi: ");
  Serial.println(WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 25) {
    delay(400);
    Serial.print(".");
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi da ket noi thanh cong!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[CANH BAO] Dang cho ket noi Gateway, se tu dong thu lai...");
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  char message[256];
  if (length >= sizeof(message)) length = sizeof(message) - 1;
  memcpy(message, payload, length);
  message[length] = '\0';

  Serial.println("\n----------------------------------------");
  Serial.print("[MQTT NHAN LENH] Topic: ");
  Serial.println(topic);
  Serial.print("[MQTT PAYLOAD]   : ");
  Serial.println(message);

  StaticJsonDocument<256> doc;
  DeserializationError err = deserializeJson(doc, message);

  if (err) {
    Serial.print("[JSON ERROR] Parse that bai: ");
    Serial.println(err.c_str());
    return;
  }

  if (doc.containsKey("aerator")) {
    const char* cmd = doc["aerator"];
    if (strcmp(cmd, "ON") == 0) {
      aeratorState = true;
      digitalWrite(PIN_RELAY, HIGH);
      Serial.println("[ACTUATOR] RELAY DONG - MAY SUC KHI: [BAT - ON]");
    } else if (strcmp(cmd, "OFF") == 0) {
      aeratorState = false;
      digitalWrite(PIN_RELAY, LOW);
      Serial.println("[ACTUATOR] RELAY NGAT - MAY SUC KHI: [TAT - OFF]");
    }

    StaticJsonDocument<128> respDoc;
    respDoc["aerator"] = aeratorState ? "ON" : "OFF";
    char respBuffer[128];
    serializeJson(respDoc, respBuffer);

    mqttClient.publish(topicCmdexe.c_str(), respBuffer);
    Serial.print("[MQTT PHAN HOI] Gui cmdexe: ");
    Serial.println(respBuffer);
  }
  Serial.println("----------------------------------------\n");
}

void reconnectMqtt() {
  if (WiFi.status() != WL_CONNECTED || mqttFailCount >= 3) {
    mqttFailCount = 0;
    setupWifi();
    return;
  }

  unsigned long now = millis();
  if (now - lastMqttReconnectAttempt < 3000) {
    return; // Khong block vi dieu khien, 3 giay thu lai 1 lan
  }
  lastMqttReconnectAttempt = now;

  Serial.print("Dang ket noi MQTT Broker (");
  Serial.print(MQTT_SERVER);
  Serial.print(")... ");

  String clientId = "Wokwi-ESP32-" + String(DEVICE_ID) + "-" + String(random(0xffff), HEX);
  if (mqttClient.connect(clientId.c_str())) {
    mqttFailCount = 0;
    Serial.println("DA KET NOI THANH CONG!");
    mqttClient.subscribe(topicCmd.c_str(), 1);
    Serial.print("Da dang ky (Subscribe) topic lenh: ");
    Serial.println(topicCmd);
  } else {
    mqttFailCount++;
    Serial.print("That bai, ma loi rc=");
    Serial.print(mqttClient.state());
    Serial.println(" - Se thu lai sau 3s");
  }
}

float readDO() {
  int raw = analogRead(PIN_DO);
  return (float)raw * 12.0 / 4095.0;
}

float readPH() {
  int raw = analogRead(PIN_PH);
  return 6.5 + ((float)raw * 3.0 / 4095.0);
}

float readSalinity() {
  int raw = analogRead(PIN_SAL);
  return 5.0 + ((float)raw * 30.0 / 4095.0);
}

float readTemperature() {
  tempSensor.requestTemperatures();
  float t = tempSensor.getTempCByIndex(0);
  if (t == DEVICE_DISCONNECTED_C) return 28.0;
  return t;
}

void publishSensorData() {
  float valDO   = readDO();
  float valPH   = readPH();
  float valSal  = readSalinity();
  float valTemp = readTemperature();

  StaticJsonDocument<256> doc;
  doc["do"]  = round(valDO * 100.0) / 100.0;
  doc["ph"]  = round(valPH * 100.0) / 100.0;
  doc["t"]   = round(valTemp * 10.0) / 10.0;
  doc["s"]   = round(valSal * 10.0) / 10.0;
  doc["a"]   = aeratorState ? "ON" : "OFF";

  char jsonBuffer[256];
  serializeJson(doc, jsonBuffer);

  bool success = mqttClient.publish(topicAttrs.c_str(), jsonBuffer);

  Serial.println("========================================");
  Serial.print("[THIET BI WOKWI] ");
  Serial.println(DEVICE_ID);
  Serial.print("[MQTT PUBLISH] Topic: ");
  Serial.println(topicAttrs);
  Serial.print("[DU LIEU JSON] : ");
  Serial.println(jsonBuffer);
  Serial.print("[TRANG THAI]   : ");
  Serial.println(success ? "THANH CONG (OK)" : "THAT BAI (FAIL)");
  Serial.println("========================================");
}

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.println("\n\n================================================");
  Serial.println("  KHOI TAO THIET BI WOKWI ESP32 AO NUOI TOM     ");
  Serial.print  ("  MA THIET BI (DEVICE ID): "); Serial.println(DEVICE_ID);
  Serial.println("================================================");

  pinMode(PIN_RELAY, OUTPUT);
  digitalWrite(PIN_RELAY, LOW);

  analogReadResolution(12);
  tempSensor.begin();

  setupWifi();

  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  mqttClient.setBufferSize(512);   // Tang bo dem tranh tran goi tin MQTT
  mqttClient.setKeepAlive(30);     // Duy tri nhip tim heartbeat voi broker

  randomSeed(micros());
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    setupWifi();
  } else if (!mqttClient.connected()) {
    reconnectMqtt();
  } else {
    mqttClient.loop();
  }

  unsigned long currentMillis = millis();
  if (currentMillis - lastPublishTime >= PUBLISH_INTERVAL) {
    lastPublishTime = currentMillis;
    if (mqttClient.connected()) {
      publishSensorData();
    }
  }
}
