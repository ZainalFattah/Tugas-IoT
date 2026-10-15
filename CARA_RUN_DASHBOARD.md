# Cara Menjalankan Web Dashboard UdaraKita

> **Tugas wajib memakai Blynk:** ikuti [CARA_RUN_BLYNK.md](CARA_RUN_BLYNK.md). Panduan di bawah menjelaskan dashboard lokal/pratinjau versi sebelumnya.

Panduan untuk **Kelompok 7 Udara**: Zainal Fattah, Naufal Adani, dan Aisyha N A.

Ada dua cara menjalankan dashboard:

| Tujuan | Cara | Sumber data |
|---|---|---|
| Melihat tampilan sebelum alat dirakit | Buka dashboard di laptop | Simulasi |
| Memantau sensor pada alat | Buka dashboard yang disediakan NodeMCU | Sensor MQ-135 dan DHT11 |

## 1. Pratinjau paling mudah di laptop

Cara ini bisa dijalankan tanpa NodeMCU, Python, atau koneksi internet.

1. Ekstrak paket ZIP jika belum diekstrak.
2. Buka folder `D:\IoT\Kelompok7_Udara\Dashboard` melalui File Explorer.
3. Klik kanan `index.html` → **Open with** → pilih browser, misalnya Chrome atau Edge.
4. Dashboard akan terbuka dengan label **SIMULASI · bukan data sensor**.

Jika folder proyek disimpan di lokasi lain, buka folder `Dashboard` pada lokasi tersebut.

Tombol **Dekat baseline**, **Respons meningkat**, **Pemanasan**, dan **Sensor terlepas** dapat dipakai untuk mencoba tampilan. Tombol **CSV** mengunduh riwayat simulasi. Angka pada mode ini dibuat oleh program untuk pratinjau.

## 2. Menjalankan dengan server lokal

Gunakan cara ini jika ingin membuka dashboard melalui alamat `localhost` saat mengembangkan tampilan.

### Langkah A — Periksa Python

Buka PowerShell atau terminal VS Code, lalu jalankan:

```powershell
python --version
```

Jika perintah `python` tidak ditemukan tetapi Python Launcher tersedia, gunakan:

```powershell
py --version
```

Jika keduanya tidak tersedia, pasang Python atau gunakan cara membuka `index.html` langsung pada bagian 1.

### Langkah B — Jalankan server

Di PowerShell:

```powershell
Set-Location 'D:\IoT\Kelompok7_Udara\Dashboard'
python -m http.server 8080 --bind 127.0.0.1
```

Jika memakai Python Launcher, ganti baris kedua dengan:

```powershell
py -m http.server 8080 --bind 127.0.0.1
```

Biarkan terminal terbuka selama dashboard digunakan. Server ini hanya dapat diakses dari laptop yang menjalankannya.

### Langkah C — Buka browser

Buka **[http://127.0.0.1:8080/?demo=1](http://127.0.0.1:8080/?demo=1)**.

Bagian **`?demo=1` wajib disertakan untuk pratinjau melalui server lokal**. Server Python hanya menyajikan file HTML; server tersebut tidak menyediakan API sensor. Jika parameter ini dihilangkan, dashboard akan mencoba membaca `/api/status` dan menampilkan status koneksi terputus.

Untuk menghentikan server, tekan **Ctrl+C** pada terminal.

## 3. Menjalankan dashboard dengan sensor asli

Pada cara ini, NodeMCU menjadi server web. Dashboard sudah tertanam dalam firmware; server Python tidak diperlukan.

### Langkah A — Upload program ke NodeMCU

Jika firmware sudah di-upload, langsung lanjut ke langkah B.

1. Siapkan Arduino IDE. Pada **Preferences → Additional Boards Manager URLs**, tambahkan:

   ```text
   https://arduino.esp8266.com/stable/package_esp8266com_index.json
   ```

2. Pada **Boards Manager**, pasang **esp8266 by ESP8266 Community**, versi **3.1.2** yang digunakan pada build proyek.
3. Pilih board **NodeMCU 1.0 (ESP-12E Module)**, flash **4 MB**, dan upload speed **115200**.
4. Pada **Library Manager**, pasang:
   - **DHT sensor library** oleh Adafruit, versi **1.4.6**.
   - **Adafruit Unified Sensor**, versi **1.1.15**.
   - **PubSubClient** oleh Nick O'Leary, versi **2.8**.
5. Buka `D:\IoT\Kelompok7_Udara\Firmware\UdaraKita\UdaraKita.ino`. File `Config.h`, `Dashboard.h`, dan `SensorLogic.h` harus tetap berada dalam folder yang sama.
6. Lepaskan adaptor eksternal, sambungkan NodeMCU ke laptop dengan kabel USB data, pilih port COM perangkat, lalu klik **Upload**.
7. Setelah upload selesai, lepaskan USB laptop lalu nyalakan rangkaian lengkap dengan adaptor sesuai diagram perakitan. Jangan memasok USB laptop dan VIN eksternal bersamaan.

Pengaturan bawaan sudah memakai hotspot NodeMCU. Tidak perlu mengisi Wi-Fi rumah atau mengaktifkan MQTT. Tidak ada upload filesystem terpisah.

### Langkah B — Sambungkan HP atau laptop

1. Cari Wi-Fi bernama **`UdaraKita-7-xxxxxx`**. Akhiran mengikuti identitas chip perangkat dan panjangnya dapat berbeda.
2. Sambungkan dengan password **`udaraK7demo`**.
3. Jika muncul pesan **tidak ada internet**, pilih tetap terhubung.
4. Buka **[http://192.168.4.1](http://192.168.4.1)** pada browser. Gunakan **HTTP**.

Untuk pembacaan sensor asli, buka alamat tersebut **tanpa `?demo=1`**. Membuka file HTML di laptop tetap menghasilkan simulasi, meskipun NodeMCU sudah menyala.

### Langkah C — Siapkan pembacaan sensor

1. Untuk MQ-135 baru, lakukan conditioning awal **lebih dari 48 jam** sesuai petunjuk sensor.
2. Setelah proses itu selesai, buka **Persiapan sensor & cara membaca data**, centang konfirmasi conditioning, lalu klik **Simpan konfirmasi**. Checklist ini adalah konfirmasi pengguna, bukan timer conditioning otomatis.
3. Setiap NodeMCU dinyalakan, tunggu pemanasan minimum **10 menit**, lalu pastikan pembacaan stabil.
4. Ketika kedua sensor valid, klik **Ambil baseline · 60 dtk**. Biarkan kondisi referensi stabil selama proses berlangsung.
5. Pantau nilai, grafik, dan status. Klik **CSV** untuk menyimpan riwayat sebelum memuat ulang atau menutup halaman.

Baseline perlu diambil ulang setelah restart. Riwayat berada pada tab browser: grafik menampilkan 120 sampel terakhir, sedangkan ekspor mencakup maksimum 900 sampel yang tersimpan pada tab tersebut.

MQ-135 pada proyek ini menampilkan respons gas relatif terhadap baseline; pembacaannya belum dikonversi menjadi AQI, PM2.5, atau CO₂ ppm yang tervalidasi.

## 4. Setelah mengedit tampilan dashboard

Untuk pratinjau di laptop, edit `Dashboard/index.html`, simpan, lalu muat ulang browser.

Untuk menerapkan perubahan pada NodeMCU, jalankan:

```powershell
Set-Location 'D:\IoT\Kelompok7_Udara'
python Dashboard\embed_dashboard.py
```

Kemudian upload ulang `Firmware\UdaraKita\UdaraKita.ino` melalui Arduino IDE. Script tersebut memperbarui `Dashboard.h` yang dimasukkan ke firmware.

## 5. Jika dashboard belum berjalan

| Masalah | Langkah pemeriksaan |
|---|---|
| Server lokal menunjukkan koneksi terputus | Pastikan alamat berakhiran `?demo=1`. |
| Port 8080 sudah digunakan | Jalankan server pada port 8081, lalu buka `http://127.0.0.1:8081/?demo=1`. |
| Dashboard tidak bisa dibuka setelah terminal ditutup | Jalankan kembali server lokal dan biarkan terminal terbuka. |
| `192.168.4.1` tidak terbuka | Pastikan HP/laptop terhubung ke hotspot NodeMCU; pilih tetap terhubung meskipun tanpa internet. Periksa apakah HP berpindah otomatis ke data seluler. |
| Wi-Fi NodeMCU tidak muncul | Periksa daya board dan buka Serial Monitor pada 115200 untuk melihat nama hotspot. |
| Tombol baseline belum aktif | Selesaikan konfirmasi conditioning, pemanasan, dan periksa validitas kedua sensor. |
| Suhu/kelembapan atau ADC tampil `—` | Periksa kabel, label pin, suplai sensor, dan ground bersama sesuai panduan perakitan. |
| Tampilan alat tidak berubah setelah HTML diedit | Jalankan `embed_dashboard.py`, upload ulang firmware, lalu muat ulang halaman. |

**MQTT tidak perlu diaktifkan untuk menjalankan dashboard ini.** Pengaturan MQTT opsional tersedia dalam `MULAI_DI_SINI.md` bila diperlukan untuk tugas.
