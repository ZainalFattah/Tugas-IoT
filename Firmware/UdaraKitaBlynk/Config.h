#pragma once
// Isi hanya di komputer sendiri. Jangan unggah Auth Token ke repo publik.
#define BLYNK_TEMPLATE_ID "TMPL6WAqmMi4A"
#define BLYNK_TEMPLATE_NAME "UdaraKita Kelompok 7"
#define BLYNK_AUTH_TOKEN ""

constexpr char WIFI_SSID[] = "";       // Wi-Fi 2,4 GHz dengan internet
constexpr char WIFI_PASSWORD[] = "";

// Untuk demonstrasi: 10 detik. Untuk operasi terus-menerus, naikkan menjadi
// 300000UL (5 menit) dan periksa kuota pesan di akun Blynk.
constexpr unsigned long BLYNK_SEND_MS = 10000UL;
constexpr unsigned long WARMUP_MS = 10UL * 60UL * 1000UL;
constexpr unsigned long BASELINE_MS = 60UL * 1000UL;
constexpr unsigned long ALARM_HOLD_MS = 10000UL;
constexpr float ALARM_ON_RATIO = 1.30f;
constexpr float ALARM_OFF_RATIO = 1.15f;
