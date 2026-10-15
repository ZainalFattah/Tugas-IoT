# Kelompok 7 — UdaraKita

Proyek IoT untuk memantau kondisi udara menggunakan NodeMCU ESP8266, sensor DHT11, dan sensor gas MQ-135. Data dikirim ke Blynk melalui Wi-Fi.

## Anggota

- Zainal Fattah
- Naufal Adani
- Aisyha N A

## Versi perakitan

Versi final menggunakan **breadboard dan kabel jumper**, tanpa PCB khusus. Panduan kabel dan gambar rangkaian tersedia di:

- [Panduan perakitan breadboard](PANDUAN_PERAKITAN_BREADBOARD.md)
- [Skema perakitan berwarna](Skema_Perakitan_Breadboard.svg)
- [Daftar komponen dan rencana proyek](Rencana_Proyek.md)

## Menjalankan proyek

1. Buka [CARA_RUN_BLYNK.md](CARA_RUN_BLYNK.md) untuk menyiapkan template, datastream, dan dashboard Blynk.
2. Buka `Firmware/UdaraKitaBlynk/Config.h` di komputer sendiri.
3. Isi Wi-Fi dan Auth Token Blynk secara lokal, lalu upload firmware ke NodeMCU.
4. Jangan commit Auth Token atau kata sandi Wi-Fi ke repositori.

Firmware Blynk menggunakan pin berikut: DHT11 pada D2/GPIO4, LED hijau pada D5/GPIO14, LED merah pada D6/GPIO12, dan MQ-135 pada A0.

## Lisensi

Lihat [LICENSE](LICENSE) dan [THIRD_PARTY.md](THIRD_PARTY.md).
