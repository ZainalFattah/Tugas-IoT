# Cara Menjalankan UdaraKita dengan Blynk

**Kelompok 7 Udara:** Zainal Fattah, Naufal Adani, Aisyha N A.

Panduan ini adalah jalur utama untuk tugas yang **wajib memakai Blynk**. Gunakan sketch `Firmware/UdaraKitaBlynk/UdaraKitaBlynk.ino`. Dashboard utama dibuat pada akun Blynk; halaman HTML lokal sebelumnya adalah versi pratinjau terpisah.

## 1. Cara kerja

MQ-135 dan DHT11 → NodeMCU ESP8266 → Wi-Fi 2,4 GHz dengan internet → Blynk.Cloud → Blynk.Console di browser atau Blynk.App di HP.

Rangkaian akhir dirakit tanpa PCB menggunakan breadboard MB-102 dan kabel jumper. Ikuti `PANDUAN_PERAKITAN_BREADBOARD.md` dan `Skema_Perakitan_Breadboard.svg`; file PCB lama hanya arsip desain. NodeMCU memakai Wi-Fi router/hotspot yang menyediakan internet. Untuk demonstrasi dengan hotspot HP, gunakan perangkat lain sebagai penampil dashboard jika diperlukan.

Kode aplikasi tersedia dengan lisensi MIT. Pustaka Blynk juga menggunakan MIT; Blynk.Cloud adalah layanan vendor dengan batas akun/paket. Akun Free dapat digunakan untuk mulai mencoba, tetapi jumlah widget dan kuota pesan mengikuti paket akun. [Batas platform Blynk](https://docs.blynk.io/en/blynk.console/limits).

## 2. Buat template dan perangkat

1. Buka [Blynk.Console](https://blynk.cloud) dan masuk dengan akun kamu.
2. Aktifkan **Developer Mode** pada profil jika menu template/editor belum tersedia.
3. Buka **Templates / Developer Zone → New Template**. Nama menu dapat berbeda menurut tampilan akun.
4. Isi nama **UdaraKita Kelompok 7**, hardware **ESP8266**, connection type **WiFi**. Simpan.
5. Catat **Template ID** dan **Template Name** pada template.
6. Buat Datastreams pada bagian berikut, lalu simpan template.
7. Pada **Devices → New Device → From Template**, pilih template tersebut dan buat perangkat bernama **UdaraKita-07**.
8. Pada **Device Info / Developer Tools**, salin **Auth Token** perangkat untuk diisi di komputer sendiri. Token perangkat berbeda dari Template ID. Jangan menaruh token di screenshot laporan atau repo publik.

## 3. Buat sembilan Virtual Pin

Pada template → **Datastreams → New Datastream → Virtual Pin**, buat sesuai tabel. Jangan memilih Digital Pin atau Analog Pin untuk tabel ini. Virtual Pin adalah kanal Blynk, bukan pin fisik board.

| Pin | Nama | Tipe | Min | Max | Default | Unit/keterangan |
|---|---|---|---:|---:|---|---|
| V0 | Suhu | Double | 0 | 50 | 0 | °C, 1 desimal |
| V1 | Kelembapan | Double | 0 | 100 | 0 | %RH, 1 desimal |
| V2 | Respons Gas | Double | 0 | 1023 | 0 | ADC, 0–1 desimal |
| V3 | Rasio Baseline | Double | -1 | 400 | -1 | Rasio, 2 desimal; -1 = belum tersedia |
| V4 | Status Alat | String | — | — | Menunggu perangkat | Status dan pesan persiapan/error |
| V5 | Konfirmasi Conditioning | Integer | 0 | 1 | 0 | Perintah pengguna; tombol sesaat |
| V6 | Ambil Baseline | Integer | 0 | 1 | 0 | Perintah pengguna; tombol sesaat |
| V7 | Baseline ADC | Double | -1 | 1023 | -1 | -1 = belum diambil |
| V8 | Waktu Menyala | Integer | 0 | 4294967 | 0 | Detik sejak boot |

Untuk V5 dan V6, **matikan “Sync with latest server value every time device connects”** bila tersedia. Program juga tidak memakai `syncVirtual`/`syncAll` pada tombol tersebut supaya perintah lama tidak dijalankan lagi setelah reconnect. Pilih **Push / Momentary** pada widget; bila widget web yang tersedia berupa Switch, firmware akan mengembalikannya ke OFF setelah menerima perintah.

V0/V1/V2 hanya dikirim jika pembacaan valid. Jika sensor gagal, angka terakhir pada widget Blynk mungkin tetap terlihat: **lihat V4 dan indikator Online/Offline sebelum menafsirkan angka**. Default nol juga belum berarti sudah ada pembacaan. Untuk rasio dan baseline, nilai -1 secara eksplisit menandakan belum tersedia.

## 4. Susunan Web Dashboard

Buka **Template → Web Dashboard → Edit**. Tambahkan widget dan pilih Datastream sesuai tabel. Tata letaknya:

```text
UDARAKITA / KELOMPOK 7                       Device Online/Offline

[Suhu · V0]       [Kelembapan · V1]       [Respons Gas · V2]

[Chart respons gas · V2            ]     [Rasio · V3]
[                                 ]     [Baseline ADC · V7]
[                                 ]     [Waktu menyala · V8]

[Status alat · V4 — lebar penuh                           ]

[Conditioning sudah >48 jam · V5]   [Ambil baseline 60 dtk · V6]
```

- V0/V1: **Gauge** atau **Label**. Warna saran hijau `#226849` dan biru `#297ACE`.
- V2: **Label** angka ADC; tambahkan **Chart single datastream** memakai V2 untuk tren. Warna saran kuning `#B58300`.
- V3/V7/V8: **Label**. Judul dan unit dibuat jelas agar rasio tidak dianggap ppm.
- V4: **Label** teks berukuran lebar, warna netral. Pastikan pesan panjang tidak terpotong; perbesar widget.
- V5/V6: **Button Push** bila tersedia; jika web hanya menyediakan **Switch**, gunakan switch dengan fungsi reset oleh firmware. Jangan memilih button yang membuka URL.

Gunakan widget yang tersedia di paket akun. Jika jumlah widget terbatas, prioritaskan V0, V1, V2, V4, V5, dan V6; chart serta label tambahan bisa ditambahkan setelahnya. **Save / Apply** perubahan. Untuk melihat data nyata, buka **Devices → UdaraKita-07 → Dashboard**, bukan hanya editor template.

Ilustrasi `Dashboard/Rancangan_Blynk.png` adalah rancangan susunan widget; bukan screenshot dashboard yang sudah terpasang di akun.

## 5. Dashboard HP

Pasang Blynk.App dan masuk dengan akun yang sama. Pada Developer Mode, pilih template lalu susun widget dengan Virtual Pin yang sama. Setelah selesai, buka perangkat **UdaraKita-07** untuk melihat data.

**Web Dashboard dan Mobile Dashboard dibuat masing-masing**, walaupun Datastreams dipakai bersama. [Panduan resmi Web Dashboard](https://docs.blynk.io/en/blynk.console/templates/dashboard).

## 6. Isi konfigurasi program

Buka `Firmware/UdaraKitaBlynk/Config.h` dan isi:

```cpp
#define BLYNK_TEMPLATE_ID "TMPL6WAqmMi4A"
#define BLYNK_TEMPLATE_NAME "UdaraKita Kelompok 7"
#define BLYNK_AUTH_TOKEN "AUTH_TOKEN_PERANGKAT_KAMU"

constexpr char WIFI_SSID[] = "NAMA_WIFI_2_4_GHZ";
constexpr char WIFI_PASSWORD[] = "PASSWORD_WIFI";
```

Template ID dan nama template sudah diisi berdasarkan template **UdaraKita Kelompok 7**. Auth Token dan Wi-Fi masih kosong: **harus diisi sebelum alat dapat online di Blynk**. Tidak perlu mengirim token ke chat. Program memberi pesan konfigurasi pada Serial Monitor jika data wajib belum diisi.

## 7. Upload dengan Arduino IDE

1. Pada Preferences → Additional Boards Manager URLs, masukkan `https://arduino.esp8266.com/stable/package_esp8266com_index.json`.
2. Pasang **esp8266 by ESP8266 Community 3.1.2** melalui Boards Manager.
3. Library Manager: pasang **Blynk 1.3.2**, **DHT sensor library by Adafruit 1.4.6**, dan **Adafruit Unified Sensor 1.1.15**.
4. Pilih **NodeMCU 1.0 (ESP-12E Module)**, flash **4 MB**, CPU **80 MHz**, upload speed **115200**.
5. Buka **`Firmware/UdaraKitaBlynk/UdaraKitaBlynk.ino`**. `Config.h` dan `SensorLogic.h` tetap di folder yang sama.
6. Lepaskan suplai VIN eksternal, sambungkan USB data ke laptop, pilih port COM, dan klik **Upload**.
7. Buka Serial Monitor **115200**. Pesan **Blynk connected.** berarti koneksi cloud berhasil.
8. Untuk menyalakan rangkaian lengkap, lepaskan USB laptop lalu gunakan adaptor eksternal sesuai panduan perakitan.
9. Buka perangkat di Blynk.Console/Blynk.App. Nilai dikirim setiap **10 detik** pada pengaturan demonstrasi.

Jangan memakai binary lama `UdaraKita-NodeMCU-4MB.bin` untuk tugas Blynk: binary itu menjalankan versi dashboard lokal. Versi Blynk perlu di-compile setelah konfigurasi milik akun kamu diisi.

Alternatif PlatformIO dari folder proyek:

```powershell
pio run -c platformio_blynk.ini
pio run -c platformio_blynk.ini -t upload --upload-port COM3
```

Ganti COM3 sesuai board. Jangan memakai `platformio.ini` lama untuk build Blynk.

## 8. Persiapan sensor dan tombol dashboard

1. Lakukan conditioning MQ-135 baru **lebih dari 48 jam** sesuai manual sensor.
2. Setelah benar-benar dilakukan, tekan **Conditioning sudah >48 jam** pada V5. Konfirmasi disimpan di EEPROM. Tombol ini mengakui proses yang dilakukan pengguna, bukan timer conditioning.
3. Setiap boot, tunggu pemanasan minimal **10 menit**, kemudian tunggu pembacaan stabil. Informasi sisa pemanasan tampil di V4.
4. Tekan **Ambil baseline 60 dtk** pada V6. Perintah ditolak jika belum siap; lihat pesan V4.
5. Baseline yang berhasil terlihat di V7. Baseline disimpan untuk sesi berjalan; setelah restart, ambil baseline lagi.

Ambang demonstrasi: LED merah jika ADC/baseline >1,30 selama 10 detik, kembali hijau jika <1,15 selama 10 detik. Kedua LED mati selama belum siap atau sensor error. Pemantauan lokal tetap beroperasi setelah koneksi internet terputus, tetapi dashboard cloud dan tombol jarak jauh memerlukan koneksi.

Pin hardware: DHT DATA = D2/GPIO4; LED hijau = D5/GPIO14; LED merah = D6/GPIO12; ADC = A0 lewat pembagi R1/R2. MQ-135 mendapat 5 V dan DHT11 yang kompatibel mendapat 3,3 V.

## 9. Kuota dan koneksi

Pengaturan 10 detik dibuat untuk sesi tugas/demonstrasi, **bukan operasi 24 jam sebulan** pada paket gratis. Satu siklus mengirim sampai 7 pembaruan Datastream. Untuk penggunaan terus-menerus, ubah `BLYNK_SEND_MS` menjadi `300000UL` (5 menit), pantau kuota akun, dan sesuaikan dengan kebutuhan. Firmware tidak mengirim angka pada setiap putaran loop dan tidak mengirim notifikasi otomatis yang berulang.

TLS memakai pustaka resmi `BlynkSimpleEsp8266_SSL.h`. Percobaan reconnect tiap 30 detik; handshake jaringan dapat menunda pembacaan sebentar. Jika internet mati, LED masih memakai keputusan sensor lokal dan riwayat cloud akan memiliki jeda.

| Masalah | Periksa |
|---|---|
| Pesan “Isi Template ID…” | Isi `Config.h`, kemudian upload ulang. |
| Device Offline | SSID/password, internet, Auth Token perangkat, Template ID, Wi-Fi 2,4 GHz. |
| Serial menunggu NTP | Jaringan harus dapat melakukan sinkronisasi waktu untuk verifikasi TLS; periksa akses internet/NTP atau coba jaringan lain. |
| Online tetapi widget kosong | Virtual Pin dan tipe Datastream harus sesuai tabel; widget harus diarahkan ke Datastream yang benar. |
| Editor template terlihat kosong | Buka dashboard perangkat nyata melalui menu Devices setelah Save/Apply. |
| V3 atau V7 bernilai -1 | Rasio/baseline belum tersedia; tunggu pemanasan lalu ambil baseline. |
| Angka berhenti saat sensor error | Firmware menahan angka invalid; lihat status V4 sebelum memakai angka lama. |
| V6 ditolak | Periksa conditioning, pemanasan, sensor valid, dan apakah pengambilan baseline sedang aktif. |
| Tombol terasa tidak merespons | Lepaskan lalu tekan lagi; status V4 menjelaskan hasil. Tombol diberi debounce 2 detik. |
| Cloud jarang memperbarui data | Periksa `BLYNK_SEND_MS`, koneksi internet, kuota, dan interval tampilan widget. |

Rancangan memakai sensor MQ-135 sebagai indikator perubahan gas; tidak menghasilkan AQI/ISPU, PM2.5, atau CO₂ ppm yang tervalidasi. Label “dekat baseline” bukan jaminan udara aman.

## 10. Status penyerahan

Dashboard cloud **belum dibuat di akun pengguna**, dan kredensial perangkat belum diisi. Paket berisi firmware, pemetaan Virtual Pin, rancangan widget, dan panduan setup. Pengujian build dicatat pada `HASIL_PENGUJIAN_BLYNK.txt`; koneksi dengan token akun serta board fisik belum diuji.

Referensi: [Datastreams](https://docs.blynk.io/en/getting-started/template-quick-setup/set-up-datastreams), [Virtual Pins](https://docs.blynk.io/en/blynk-library-firmware-api/virtual-pins), [Koneksi Blynk](https://docs.blynk.io/en/blynk-library-firmware-api/connection-management), [Widget web](https://docs.blynk.io/en/blynk.console/widgets-console).
