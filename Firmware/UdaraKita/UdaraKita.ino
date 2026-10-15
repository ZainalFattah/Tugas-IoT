#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <EEPROM.h>
#include <DHT.h>
#include <PubSubClient.h>
#include "Config.h"
#include "SensorLogic.h"
#include "Dashboard.h"

constexpr uint8_t DHT_PIN = 4, GREEN_PIN = 14, RED_PIN = 12;
ESP8266WebServer server(80);
WiFiClient transport;
PubSubClient mqtt(transport);
DHT dht(DHT_PIN, DHT11);
SensorLogic logic;
String deviceId, apName, topicData, topicStatus;
bool conditioned = false, dhtValid = false, mqValid = false;
float temperature = NAN, humidity = NAN, adc = 0;
uint32_t bootAt, lastAdc = 0, lastDht = 0, lastMQTTAttempt = 0, lastPublish = 0;
uint32_t lastDhtGood = 0, adcSum = 0, adcCount = 0, sampleSeq = 0;
const char* notice = "Ambil baseline setelah conditioning dan pemanasan.";
const uint32_t CONDITION_MAGIC = 0x4B374331;

bool warmed() { return uint32_t(millis() - bootAt) >= WARMUP_MS; }
bool sensorsValid() { return dhtValid && mqValid; }
const char* state() {
  if (!conditioned) return "conditioning";
  if (!warmed()) return "warming";
  if (!sensorsValid()) return "sensor_error";
  if (logic.collecting) return "calibrating";
  if (logic.baseline < 3) return "baseline_required";
  return logic.elevated ? "elevated" : "normal";
}
String number(float n, bool valid, int decimals = 1) {
  return valid && isfinite(n) ? String(n, decimals) : String("null");
}
String telemetry() {
  const uint32_t now = millis(), elapsed = uint32_t(now - bootAt);
  String j; j.reserve(850);
  j = "{\"device\":\"" + deviceId + "\",\"seq\":" + String(sampleSeq);
  j += ",\"uptime_s\":" + String(elapsed / 1000);
  j += ",\"temperature\":" + number(temperature,dhtValid);
  j += ",\"humidity\":" + number(humidity,dhtValid);
  j += ",\"adc\":" + number(adc,adcCount > 0 || sampleSeq > 0);
  j += ",\"mq_valid\":" + String(mqValid ? "true":"false");
  j += ",\"dht_valid\":" + String(dhtValid ? "true":"false");
  j += ",\"dht_age_s\":" + (lastDhtGood ? String(uint32_t(now-lastDhtGood)/1000) : String("null"));
  j += ",\"baseline\":" + number(logic.baseline,logic.baseline>=3);
  j += ",\"ratio\":" + number(adc / (logic.baseline>=3 ? logic.baseline : 1),mqValid && logic.baseline>=3,3);
  j += ",\"state\":\"" + String(state()) + "\"";
  j += ",\"conditioned\":" + String(conditioned ? "true":"false");
  j += ",\"warmup_remaining_s\":" + String(elapsed>=WARMUP_MS ? 0:(WARMUP_MS-elapsed+999)/1000);
  uint32_t calTime = uint32_t(now-logic.started);
  j += ",\"baseline_remaining_s\":" + String(logic.collecting && calTime<BASELINE_MS ? (BASELINE_MS-calTime+999)/1000:0);
  j += ",\"alarm_on\":" + String(ALARM_ON_RATIO,2) + ",\"alarm_off\":" + String(ALARM_OFF_RATIO,2);
  j += ",\"wifi_connected\":" + String(WiFi.status()==WL_CONNECTED ? "true":"false");
  j += ",\"station_ip\":\"" + WiFi.localIP().toString() + "\"";
  j += ",\"mqtt_enabled\":" + String(MQTT_ENABLED ? "true":"false");
  j += ",\"mqtt_connected\":" + String(mqtt.connected() ? "true":"false");
  j += ",\"notice\":\"" + String(notice) + "\"}";
  return j;
}
void reply(int code, const String& body) {
  server.sendHeader("Cache-Control","no-store");
  server.send(code,"application/json; charset=utf-8",body);
}
bool localRequest() {
  // Custom header prevents ordinary cross-origin forms from changing state.
  if (server.header("X-UdaraKita") != "1") { reply(403,"{\"error\":\"Buka dashboard perangkat untuk tindakan ini.\"}"); return false; }
  return true;
}
void setup() {
  Serial.begin(115200);
  pinMode(GREEN_PIN,OUTPUT); pinMode(RED_PIN,OUTPUT);
  digitalWrite(GREEN_PIN,LOW);digitalWrite(RED_PIN,LOW);
  dht.begin(); EEPROM.begin(16);
  uint32_t saved=0; EEPROM.get(0,saved); conditioned=saved==CONDITION_MAGIC;
  deviceId="k7-"+String(ESP.getChipId(),HEX);
  apName="UdaraKita-7-"+String(ESP.getChipId(),HEX);
  WiFi.persistent(false);
  WiFi.mode(strlen(WIFI_SSID) ? WIFI_AP_STA:WIFI_AP);
  WiFi.softAP(apName.c_str(),AP_PASSWORD);
  if (strlen(WIFI_SSID)) { WiFi.setAutoReconnect(true);WiFi.begin(WIFI_SSID,WIFI_PASSWORD); }
  topicData="udarakita/"+deviceId+"/telemetry";
  topicStatus="udarakita/"+deviceId+"/status";
  if (MQTT_ENABLED) { mqtt.setServer(MQTT_HOST,MQTT_PORT);mqtt.setBufferSize(1536);mqtt.setSocketTimeout(1);transport.setTimeout(1000); }
  server.collectHeaders("X-UdaraKita");
  server.on("/",HTTP_GET,[](){server.sendHeader("Cache-Control","no-cache");server.send_P(200,"text/html; charset=utf-8",DASHBOARD_HTML);});
  server.on("/api/status",HTTP_GET,[](){reply(200,telemetry());});
  server.on("/api/condition",HTTP_POST,[](){
    if (!localRequest()) return;
    if (server.arg("confirm")!="48h") {reply(400,"{\"error\":\"Konfirmasi conditioning lebih dari 48 jam diperlukan.\"}");return;}
    if (!conditioned) {EEPROM.put(0,CONDITION_MAGIC);if(!EEPROM.commit()){reply(500,"{\"error\":\"Gagal menyimpan konfirmasi.\"}");return;}conditioned=true;}
    notice="Conditioning dikonfirmasi pengguna; tunggu pemanasan dan stabilisasi.";
    reply(200,telemetry());
  });
  server.on("/api/baseline",HTTP_POST,[](){
    if (!localRequest()) return;
    if (!conditioned || !warmed() || !sensorsValid() || logic.collecting) {reply(409,"{\"error\":\"Selesaikan conditioning, pemanasan, dan periksa sensor dahulu.\"}");return;}
    logic.startBaseline(millis());notice="Mengambil baseline selama 60 detik; biarkan kondisi referensi stabil.";
    reply(200,telemetry());
  });
  server.onNotFound([](){reply(404,"{\"error\":\"Tidak ditemukan\"}");});
  server.begin();bootAt=millis();
  Serial.println("\nUdaraKita Kelompok 7");Serial.println("SSID: "+apName);
  Serial.println("Dashboard AP: http://192.168.4.1");
}
void loop() {
  server.handleClient();const uint32_t now=millis();
  if (uint32_t(now-lastAdc)>=50) {
    lastAdc=now;adcSum+=analogRead(A0);++adcCount;
    if(adcCount>=20) {
      adc=float(adcSum)/adcCount;adcSum=adcCount=0;++sampleSeq;
      mqValid=isfinite(adc)&&adc>=3&&adc<1000;
      if (logic.collecting) {
        if (!mqValid || !dhtValid) {logic.collecting=false;logic.baseline=0;notice="Baseline dibatalkan: pembacaan sensor tidak valid.";}
        else {logic.sample(adc);if(uint32_t(now-logic.started)>=BASELINE_MS)notice=logic.finishBaseline() ? "Baseline tersimpan untuk sesi ini.":"Baseline gagal: respons belum stabil. Tunggu lalu ulangi.";}
      }
    }
  }
  if(uint32_t(now-lastDht)>=2500) {
    lastDht=now;float h=dht.readHumidity(),t=dht.readTemperature();
    dhtValid=isfinite(h)&&isfinite(t)&&h>=0&&h<=100&&t>=0&&t<=50;
    if(dhtValid){temperature=t;humidity=h;lastDhtGood=now;}
  }
  logic.update(now,conditioned&&warmed()&&sensorsValid(),adc,ALARM_ON_RATIO,ALARM_OFF_RATIO,ALARM_HOLD_MS);
  bool ready=conditioned&&warmed()&&sensorsValid()&&logic.baseline>=3&&!logic.collecting;
  digitalWrite(GREEN_PIN,ready&&!logic.elevated ? HIGH:LOW);
  digitalWrite(RED_PIN,ready&&logic.elevated ? HIGH:LOW);
  if(MQTT_ENABLED && WiFi.status()==WL_CONNECTED) {
    if(!mqtt.connected() && uint32_t(now-lastMQTTAttempt)>=30000) {
      lastMQTTAttempt=now;
      if(mqtt.connect(deviceId.c_str(),strlen(MQTT_USER)?MQTT_USER:nullptr,strlen(MQTT_USER)?MQTT_PASSWORD:nullptr,topicStatus.c_str(),1,true,"offline")) mqtt.publish(topicStatus.c_str(),"online",true);
    }
    mqtt.loop();
    if(mqtt.connected() && uint32_t(now-lastPublish)>=5000) {
      lastPublish=now;String payload=telemetry();mqtt.publish(topicData.c_str(),payload.c_str(),false);
    }
  }
  yield();
}
