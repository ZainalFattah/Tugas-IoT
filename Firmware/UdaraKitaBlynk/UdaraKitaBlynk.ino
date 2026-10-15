#include "Config.h" // Blynk macros must be defined before the library header.
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266_SSL.h>
#include <DHT.h>
#include <EEPROM.h>
#include <time.h>
#include "SensorLogic.h"

constexpr uint8_t DHT_PIN = 4, GREEN_PIN = 14, RED_PIN = 12;
constexpr uint32_t CONDITION_MAGIC = 0x4B374331;
DHT dht(DHT_PIN, DHT11);
SensorLogic logic;
float temperature = NAN, humidity = NAN, adc = NAN;
bool conditioned = false, dhtValid = false, mqValid = false, configured = false;
uint32_t bootAt, lastAdc = 0, lastDht = 0, lastReconnect = 0, lastSend = 0;
uint32_t adcSum = 0, adcCount = 0, lastConditionCommand = 0, lastBaselineCommand = 0;
bool conditionCommandSeen = false, baselineCommandSeen = false;
const char* notice = "Konfirmasi conditioning awal >48 jam lewat tombol V5.";

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
uint32_t warmupRemaining() {
  uint32_t elapsed = uint32_t(millis() - bootAt);
  return elapsed >= WARMUP_MS ? 0 : (WARMUP_MS - elapsed + 999) / 1000;
}
void sendStatus() {
  if (!Blynk.connected()) return;
  // V4 is always published, even when invalid numeric readings are withheld.
  String status = String(state()) + " | " + notice;
  status += dhtValid ? " | DHT OK" : " | DHT INVALID";
  status += mqValid ? " | MQ OK" : " | MQ INVALID";
  if (!warmed()) status += " | warmup " + String(warmupRemaining()) + "s";
  if (logic.collecting) {
    uint32_t t = uint32_t(millis()-logic.started);
    status += " | baseline " + String(t>=BASELINE_MS ? 0:(BASELINE_MS-t+999)/1000) + "s";
  }
  Blynk.virtualWrite(V4, status);
}
void sendMeasurements() {
  if (!Blynk.connected()) return;
  if (dhtValid) { Blynk.virtualWrite(V0, temperature); Blynk.virtualWrite(V1, humidity); }
  if (mqValid) Blynk.virtualWrite(V2, adc);
  // -1 is an explicit sentinel for unavailable ratio/baseline, not a reading.
  Blynk.virtualWrite(V3, mqValid && logic.baseline>=3 ? adc/logic.baseline : -1.0f);
  sendStatus();
  Blynk.virtualWrite(V7, logic.baseline>=3 ? logic.baseline : -1.0f);
  Blynk.virtualWrite(V8, uint32_t(millis()-bootAt)/1000);
}
BLYNK_CONNECTED() {
  // Never sync V5/V6: old cloud commands must not confirm conditioning or
  // restart a baseline after reconnect. Controls are momentary PUSH buttons.
  Blynk.virtualWrite(V5, 0); Blynk.virtualWrite(V6, 0);
  // Measurements are sent by the loop, outside this callback.
  lastSend = millis() - BLYNK_SEND_MS;
}
BLYNK_WRITE(V5) {
  if (param.asInt()!=1) return;
  Blynk.virtualWrite(V5, 0);
  uint32_t now=millis();
  if (conditionCommandSeen && uint32_t(now-lastConditionCommand)<2000) return;
  conditionCommandSeen=true;lastConditionCommand=now;
  if (!conditioned) {
    EEPROM.put(0,CONDITION_MAGIC);
    if (!EEPROM.commit()) { notice="Gagal menyimpan konfirmasi conditioning.";sendStatus();return; }
    conditioned=true;
  }
  notice="Conditioning dikonfirmasi pengguna. Tunggu pemanasan dan stabilisasi.";
  sendStatus();
}
BLYNK_WRITE(V6) {
  if (param.asInt()!=1) return;
  Blynk.virtualWrite(V6, 0);
  uint32_t now=millis();
  if (baselineCommandSeen && uint32_t(now-lastBaselineCommand)<2000) return;
  baselineCommandSeen=true;lastBaselineCommand=now;
  if (!conditioned || !warmed() || !sensorsValid() || logic.collecting) {
    notice="Baseline ditolak: cek conditioning, pemanasan, sensor, atau proses aktif.";
  } else {
    logic.startBaseline(now);
    notice="Mengambil baseline 60 detik. Jaga kondisi referensi stabil.";
  }
  sendStatus();
}
void setup() {
  Serial.begin(115200);
  pinMode(GREEN_PIN,OUTPUT);pinMode(RED_PIN,OUTPUT);
  digitalWrite(GREEN_PIN,LOW);digitalWrite(RED_PIN,LOW);
  dht.begin();EEPROM.begin(16);
  uint32_t saved=0;EEPROM.get(0,saved);conditioned=saved==CONDITION_MAGIC;
  bootAt=millis();
  configured=strlen(WIFI_SSID)>0 && strlen(BLYNK_AUTH_TOKEN)>0 &&
    strcmp(BLYNK_TEMPLATE_ID,"TMPL_GANTI_DARI_BLYNK")!=0;
  WiFi.persistent(false);WiFi.mode(WIFI_STA);
  if (configured) {
    WiFi.setAutoReconnect(true);WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
    // Avoid Blynk.begin's blocking Wi-Fi loop; sampling continues offline.
    Blynk.config(BLYNK_AUTH_TOKEN);
    // The SDK's TLS adapter waits for NTP; start it asynchronously and gate
    // connection attempts below so blocked NTP never freezes sensor sampling.
    configTime(0, 0, "pool.ntp.org", "time.nist.gov");
    lastReconnect=millis()-30000UL;
    Serial.println("UdaraKita Blynk: menghubungkan Wi-Fi dan Blynk.Cloud.");
  } else {
    Serial.println("Isi Template ID, Auth Token, dan Wi-Fi pada Config.h lalu upload ulang.");
  }
}
void loop() {
  uint32_t now=millis();
  if (uint32_t(now-lastAdc)>=50) {
    lastAdc=now;adcSum+=analogRead(A0);++adcCount;
    if (adcCount>=20) {
      adc=float(adcSum)/adcCount;adcSum=adcCount=0;
      mqValid=isfinite(adc)&&adc>=3&&adc<1000;
      if (logic.collecting) {
        if (!sensorsValid()) {
          logic.collecting=false;logic.baseline=0;
          notice="Baseline dibatalkan: pembacaan sensor tidak valid.";
        } else {
          logic.sample(adc);
          if (uint32_t(now-logic.started)>=BASELINE_MS) {
            notice=logic.finishBaseline() ? "Baseline tersimpan untuk sesi ini." : "Baseline gagal: respons belum stabil; ulangi.";
          }
        }
      }
    }
  }
  if (uint32_t(now-lastDht)>=2500) {
    lastDht=now;float t=dht.readTemperature(),h=dht.readHumidity();
    dhtValid=isfinite(t)&&isfinite(h)&&t>=0&&t<=50&&h>=0&&h<=100;
    if(dhtValid){temperature=t;humidity=h;}
  }
  logic.update(now,conditioned&&warmed()&&sensorsValid(),adc,ALARM_ON_RATIO,ALARM_OFF_RATIO,ALARM_HOLD_MS);
  bool ready=conditioned&&warmed()&&sensorsValid()&&logic.baseline>=3&&!logic.collecting;
  digitalWrite(GREEN_PIN,ready&&!logic.elevated?HIGH:LOW);
  digitalWrite(RED_PIN,ready&&logic.elevated?HIGH:LOW);
  if (configured && WiFi.status()==WL_CONNECTED) {
    if(!Blynk.connected() && uint32_t(now-lastReconnect)>=30000) {
      lastReconnect=now;
      if(time(nullptr)>=100000) {
        if(Blynk.connect(1000))Serial.println("Blynk connected.");
        else Serial.println("Blynk belum terhubung. Periksa internet, token dan template.");
      } else Serial.println("Menunggu sinkronisasi waktu NTP untuk TLS. Periksa akses internet/NTP.");
    }
    if(Blynk.connected()) {
      Blynk.run();
      // Refresh time: a connection attempt/TLS handshake may take time.
      now=millis();
      if(uint32_t(now-lastSend)>=BLYNK_SEND_MS) {lastSend=now;sendMeasurements();}
    }
  }
  yield();
}
