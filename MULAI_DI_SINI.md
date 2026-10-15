# UdaraKita — dashboard dan firmware Kelompok 7

> **Pembaruan 14 Oktober 2026:** tugas wajib memakai Blynk. Mulai dari [CARA_RUN_BLYNK.md](CARA_RUN_BLYNK.md) dan upload `Firmware/UdaraKitaBlynk/UdaraKitaBlynk.ino`. Bagian di bawah adalah panduan versi dashboard lokal sebelumnya.

Paket software melengkapi desain hardware sebelumnya. Firmware dan dashboard sekarang sudah tersedia; keterangan “firmware belum termasuk” pada dokumen perakitan lama sudah digantikan oleh panduan ini.

## Pilihan sistem

Dashboard HTML/CSS/JavaScript disimpan langsung dalam flash ESP8266. HP meminta data JSON melalui HTTP setiap 2 detik. Tidak perlu instal aplikasi, server, internet, akun, atau langganan. Semua aset tersedia lokal tanpa CDN. Kode buatan proyek tersedia dengan lisensi MIT; pustaka pihak ketiga mengikuti lisensinya masing-masing.

MQTT tersedia sebagai **keluaran opsional** ke broker LAN seperti Eclipse Mosquitto. MQTT tidak diperlukan untuk membuka dashboard. Cocok jika dosen meminta integrasi broker, pencatatan terpusat, atau beberapa perangkat; menjalankan broker memerlukan laptop/Raspberry Pi tambahan yang sudah tersedia.

## Cara paling mudah: Arduino IDE

1. Ekstrak ZIP ke folder biasa. Pasang Arduino IDE dari https://www.arduino.cc/en/software . Internet hanya diperlukan untuk menyiapkan IDE, board, dan pustaka.
2. Buka Preferences → Additional Boards Manager URLs, tambahkan `https://arduino.esp8266.com/stable/package_esp8266com_index.json`.
3. Di Boards Manager, pasang **esp8266 by ESP8266 Community 3.1.2**. Pilih **NodeMCU 1.0 (ESP-12E Module)**, CPU 80 MHz, flash 4 MB, upload speed 115200. Board V3 CH340 tetap memakai pilihan NodeMCU ini. Pastikan modul memang ESP8266 4 MB, bukan ESP32/ESP-01.
4. Pasang melalui Library Manager: **DHT sensor library by Adafruit 1.4.6**, **Adafruit Unified Sensor 1.1.15**, dan **PubSubClient by Nick O'Leary 2.8**. Pustaka MQTT tetap diperlukan saat compile walaupun fitur MQTT dimatikan.
5. Buka `Firmware/UdaraKita/UdaraKita.ino`. Biarkan `Config.h`, `Dashboard.h`, dan `SensorLogic.h` di folder yang sama. Tidak perlu mengisi SSID/password rumah untuk mode awal.
6. Lepaskan adaptor 5 V eksternal, sambungkan NodeMCU ke laptop memakai kabel USB **data**, pilih port COM board, lalu klik **Upload**. MQ-135 tidak perlu menyala saat upload. Jika port tidak muncul, periksa kabel data dan driver CH340 sesuai perangkat/vendor board.
7. Setelah upload, untuk operasi rangkaian lengkap lepas USB laptop lalu gunakan adaptor eksternal sesuai diagram perakitan. Jangan memasok USB laptop dan VIN eksternal bersamaan.
8. Sambungkan HP ke hotspot **UdaraKita-7-xxxxxx**, password **`udaraK7demo`**. Enam digit akhir nama mengikuti chip perangkat dan bisa lebih pendek. Pilih tetap terhubung bila HP mengatakan “tidak ada internet”.
9. Ketik **`http://192.168.4.1`** di browser (HTTP, bukan HTTPS). Dashboard asli membaca sensor secara langsung. Tidak perlu upload filesystem/LittleFS terpisah.

Serial Monitor 115200 menampilkan nama hotspot. Jika dashboard tidak terbuka, matikan sementara perpindahan otomatis HP ke data seluler dan pastikan HP terhubung ke hotspot alat.

## Pilihan alternatif: langsung flash file .bin

`Release/UdaraKita-NodeMCU-4MB.bin` adalah firmware dashboard lokal lama. Untuk tugas akhir gunakan firmware Blynk dan pin breadboard yang sama seperti tabel berikut.

Pasang sekali: `python -m pip install esptool==4.8.1`.

Di terminal folder paket, jalankan (ganti COM3 dengan port board yang benar):

```text
python -m esptool --chip esp8266 --port COM3 --baud 115200 write_flash --flash_mode dio --flash_freq 40m --flash_size 4MB 0x0 Release/UdaraKita-NodeMCU-4MB.bin
```

Flash menggantikan program lama pada board. Tidak ada port yang dipilih atau perangkat yang di-flash otomatis oleh paket ini. Bila ingin mengubah Wi-Fi/MQTT, edit Config.h dan upload dari source, bukan memakai binary default.

## Pin untuk breadboard

| Fungsi | GPIO/label NodeMCU | Koneksi breadboard |
|---|---|---|
| MQ-135 analog | A0 | Sesudah pembagi 47 kΩ + 10 kΩ |
| DHT11 DATA | GPIO4 / D2 | DATA DHT11 |
| LED hijau | GPIO14 / D5 | Resistor 1 kΩ → anoda LED hijau |
| LED merah | GPIO12 / D6 | Resistor 1 kΩ → anoda LED merah |
| Daya DHT | 3V3 | VCC DHT11 |
| Ground | GND | Rel GND breadboard bersama |

MQ-135 tetap diberi 5 V. DHT11 harus mendukung 3,3 V. Jangan hubungkan AO 5 V langsung ke A0. Lihat `PANDUAN_PERAKITAN_BREADBOARD.md` sebelum menyalakan rangkaian.

## Saat pertama kali menjalankan

1. Sensor MQ-135 baru memerlukan conditioning awal **lebih dari 48 jam** sesuai manual Winsen. Checklist dashboard adalah pengakuan pengguna, **bukan penghitung waktu conditioning**. Jangan centang sebelum dilakukan. Konfirmasi disimpan pada EEPROM emulasi flash.
2. Setiap boot tetap memerlukan pemanasan minimum 10 menit. Nilai mentah tetap terlihat, tetapi kedua LED mati dan alarm belum dinilai. Waktu ini bukan jaminan stabil; tunggu sampai tren sensor stabil.
3. Buka “Persiapan sensor”, simpan konfirmasi conditioning, lalu klik **Ambil baseline · 60 dtk** setelah pemanasan dan kedua sensor valid. Pengambilan membutuhkan minimal 20 sampel; baseline ditolak jika simpangan baku relatif >10%, nilainya di luar batas, atau sensor gagal dibaca.
4. Baseline hanya disimpan di RAM untuk sesi tersebut. Restart memerlukan baseline baru; pengambilan ulang menghapus referensi lama sampai pengambilan baru berhasil.
5. LED hijau menyala saat data valid dan respons dekat baseline. LED merah menyala jika ADC/baseline >1,30 selama 10 detik; kembali hijau jika <1,15 selama 10 detik. Ambang ini untuk demonstrasi, bukan ambang kesehatan. Selama pemanasan, baseline belum ada, pengambilan baseline, atau error sensor, kedua LED mati.

Jika mengganti MQ-135 dengan sensor baru, conditioning harus dilakukan lagi. Konfirmasi lama dapat dihapus dengan opsi **Erase Flash: All Flash Contents** saat upload ulang; ini menghapus semua data flash perangkat, jadi lakukan hanya pada board proyek yang memang ingin direset.

## Fitur dashboard

- Suhu °C, kelembapan %RH, ADC mentah, rasio terhadap baseline.
- Grafik 120 sampel terakhir; maksimum 900 sampel disimpan di RAM tab browser (sekitar 30 menit ketika polling berjalan normal).
- Ekspor CSV termasuk waktu ISO dari HP/laptop, status validitas, baseline, dan rasio. Waktu bukan berasal dari RTC board.
- Tombol conditioning dan pengambilan baseline. Sensor error tampil “—”, bukan angka nol yang dianggap valid.
- Jika koneksi gagal, data lama diredupkan dan diberi keterangan tidak diperbarui. Setelah koneksi pulih polling berlanjut. Saat board restart, riwayat sesi dibersihkan.
- Tampilan responsif untuk HP/laptop. Data hilang jika tab dimuat ulang; ekspor CSV sebelum menutup tab.
- Mode simulasi untuk pratinjau: buka `Dashboard/index.html` di komputer atau gunakan `?demo=1`. Mode ini jelas berlabel **SIMULASI**. Jangan memakai mode simulasi untuk laporan pembacaan alat.

Tombol simulasi mengubah tampilan langsung; mode ini tidak menyimulasikan rangkaian fisik atau jeda histeresis firmware. Untuk data asli gunakan alamat perangkat tanpa `?demo=1`.

## Wi-Fi router dan MQTT opsional

Edit `Firmware/UdaraKita/Config.h`:

```cpp
constexpr char WIFI_SSID[] = "NAMA_WIFI_2_4_GHZ";
constexpr char WIFI_PASSWORD[] = "PASSWORD_WIFI";
constexpr bool MQTT_ENABLED = true;
constexpr char MQTT_HOST[] = "192.168.1.10"; // IP laptop broker
constexpr unsigned short MQTT_PORT = 1883;
constexpr char MQTT_USER[] = "k7";
constexpr char MQTT_PASSWORD[] = "PASSWORD_BROKER_ANDA";
```

Upload ulang. ESP8266 perlu Wi-Fi 2,4 GHz. Hotspot perangkat tetap tersedia walaupun router atau broker mati. Ketika router terhubung, dashboard menampilkan IP station; HP pada LAN yang sama juga bisa membuka IP itu. Broker harus dapat dijangkau dari Wi-Fi tersebut; client isolation/hotspot tertentu dapat menghalangi koneksi antarperangkat.

Gunakan broker **Eclipse Mosquitto** dari https://mosquitto.org/download/ . Contoh konfigurasi untuk Mosquitto 2.x pada laptop LAN (sesuaikan alamat/path):

```text
listener 1883 192.168.1.10
allow_anonymous false
password_file C:/mqtt/passwords
```

Buat folder `C:/mqtt` sendiri, lalu jalankan `mosquitto_passwd -c C:/mqtt/passwords k7` sekali untuk membuat pengguna. Opsi `-c` menimpa file yang ada; gunakan hanya saat membuat file baru. Simpan konfigurasi sebagai `C:/mqtt/mosquitto-k7.conf`, lalu jalankan `mosquitto -c C:/mqtt/mosquitto-k7.conf -v`. Jika sudah ada service broker, gunakan konfigurasi service itu atau hentikan instance proyek yang lama agar port tidak bentrok. Izin firewall, jika diperlukan, cukup pada jaringan privat yang digunakan.

Firmware mengirim JSON tiap 5 detik ke `udarakita/k7-<chipid>/telemetry`, QoS 0, tidak retained. Status online/offline di `udarakita/k7-<chipid>/status` memakai retained dan Last Will. Status offline setelah putus mendadak mengikuti timeout MQTT; tidak selalu instan. Subscribe `udarakita/+/telemetry` memakai MQTT client lokal untuk melihat data. Broker tidak menyimpan histori otomatis.

Firmware tidak menerima perintah MQTT. Pengambilan baseline tetap melalui dashboard. Koneksi broker memakai TCP tanpa TLS khusus LAN tepercaya; jangan gunakan password penting lain atau membuka broker ke internet. Reconnect dicoba tiap 30 detik dan dapat menunda loop sebentar saat broker tidak tersedia. Versi broker lain mungkin memiliki konfigurasi autentikasi berbeda: ikuti dokumentasi versi yang dipasang.

Contoh payload ringkas (contoh ilustratif):

```json
{"device":"k7-ab12cd","temperature":28.5,"humidity":64.0,"adc":120,"baseline":118,"ratio":1.017,"state":"normal","mq_valid":true,"dht_valid":true}
```

## Build ulang / pengembangan

Untuk mengedit tampilan, ubah `Dashboard/index.html`, jalankan `python Dashboard/embed_dashboard.py`, lalu compile/upload. File Dashboard.h sudah tersedia untuk penggunaan langsung. Dashboard berada di PROGMEM agar tidak menghabiskan RAM.

Dengan PlatformIO: buka folder yang berisi `platformio.ini`; jalankan `pio run`, lalu `pio run -t upload --upload-port COM3`. Dependensi dipatok versi. Lisensi dan sumber pustaka dicatat di THIRD_PARTY.md.

## Batas verifikasi

Firmware telah berhasil dibangun untuk NodeMCU 1.0 / ESP8266 core 3.1.2, flash 4 MB. Logika baseline, histeresis, hold time, invalidasi sensor dan rollover millis diuji di komputer. Tampilan, tombol simulasi, tampilan error, ukuran layar HP, dan ekspor CSV diperiksa di browser.

Belum diuji: upload ke board fisik, ketepatan sensor, daya nyata, HTTP dari ESP8266 nyata, serta koneksi broker MQTT nyata. File .bin siap untuk dicoba pada board yang sesuai, bukan jaminan semua varian modul langsung cocok. Lihat HASIL_PENGUJIAN.txt untuk angka build.

Referensi: https://arduino-esp8266.readthedocs.io/en/latest/installing.html ; https://pubsubclient.knolleary.net/api ; https://github.com/adafruit/DHT-sensor-library ; https://mosquitto.org/documentation/ ; https://www.winsen-sensor.com/manual/mq135.html .
