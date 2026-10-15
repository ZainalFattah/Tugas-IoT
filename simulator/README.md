# Simulator web UdaraKita

Simulator ini dibuat khusus untuk rangkaian akhir Kelompok 7: NodeMCU V3 ESP8266, MQ-135, DHT11, dua LED, pembagi 47 kΩ/10 kΩ, dan C1–C3. Semua komponen ditampilkan dengan sambungan yang dapat disorot. Ini **simulasi perilaku di browser**, bukan emulasi rangkaian analog, firmware ESP8266, atau koneksi Blynk.Cloud. Data pada pratinjau V0–V8 bersifat lokal dan tidak dikirim ke akun Blynk.

## Menjalankan

Cara tercepat: buka [`index.html`](index.html) di browser. Situs ini tidak membutuhkan instalasi, server, atau koneksi internet untuk fungsi inti. Font akan memakai pengganti lokal jika offline.

Jika ingin menjalankan dari server lokal (misalnya supaya tautan ke panduan utama tetap tersedia), dari folder akar repositori jalankan:

```powershell
python -m http.server 8766
```

Lalu buka `http://127.0.0.1:8766/simulator/`.

## Cara mencoba

1. Klik komponen pada rangkaian untuk melihat fungsi dan jalurnya.
2. Klik **Konfirmasi demo**. Pada perangkat nyata, sensor MQ-135 baru perlu conditioning lebih dari 48 jam.
3. Tunggu pemanasan (60 detik di demo mewakili 10 menit pada firmware), atau klik **Percepat demo**.
4. Biarkan slider MQ-135 stabil lalu klik **Mulai kalibrasi**. Proses memerlukan 6 detik demo, setara 60 detik pada firmware.
5. Geser nilai MQ-135 melewati 1,30× baseline. Setelah kira-kira 1 detik demo (10 detik waktu firmware), LED merah menyala. Turunkan ke bawah 1,15× baseline untuk kembali ke LED hijau.

Suhu, kelembapan, dan respons MQ-135 dapat diubah dengan slider. Nilai MQ-135 adalah bacaan ADC relatif, bukan ppm atau AQI. Waktu dan pembacaan dapat sedikit berbeda dari perangkat nyata; pemodelan elektronik sensor, catu daya, dan Wi-Fi tidak dilakukan.

Untuk perakitan asli, gunakan [panduan breadboard](../PANDUAN_PERAKITAN_BREADBOARD.md), [skema berwarna](../Skema_Perakitan_Breadboard.svg), dan [firmware ESP8266](../Firmware/UdaraKitaBlynk/). Sebelum menyambungkan A0, ukur titik tengah pembagi dengan multimeter dan pastikan di bawah 1 V.
