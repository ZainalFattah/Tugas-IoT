#pragma once
// Langsung upload: kosongkan Wi-Fi untuk memakai hotspot NodeMCU.
// HP -> UdaraKita-7-xxxxxx -> http://192.168.4.1
constexpr char AP_PASSWORD[] = "udaraK7demo"; // minimal 8 karakter; ganti jika perlu
constexpr char WIFI_SSID[] = "";
constexpr char WIFI_PASSWORD[] = "";

// MQTT opsional: pakai broker lokal, misalnya Eclipse Mosquitto.
// Mode TCP ini untuk LAN tepercaya; jangan buka port broker ke internet.
constexpr bool MQTT_ENABLED = false;
constexpr char MQTT_HOST[] = "192.168.1.10";
constexpr unsigned short MQTT_PORT = 1883;
constexpr char MQTT_USER[] = "";
constexpr char MQTT_PASSWORD[] = "";

constexpr unsigned long WARMUP_MS = 10UL * 60UL * 1000UL;
constexpr unsigned long BASELINE_MS = 60UL * 1000UL;
constexpr unsigned long ALARM_HOLD_MS = 10UL * 1000UL;
constexpr float ALARM_ON_RATIO = 1.30f;
constexpr float ALARM_OFF_RATIO = 1.15f;
// Pemanasan 10 menit hanya minimum per boot, bukan pengganti conditioning >48 jam.
// Tunggu sampai respons stabil sebelum ambil baseline.

