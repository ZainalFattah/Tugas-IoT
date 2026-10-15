# Rencana Proyek IoT — Kelompok 7 Udara

> **Revisi 15 Oktober 2026:** implementasi akhir memakai **Blynk** dan dirakit **tanpa PCB**. Seluruh komponen dipasang pada breadboard menggunakan kabel jumper sehingga rangkaian mudah diperiksa, diperbaiki, dan dipresentasikan.

**Judul:** UdaraKita — Pemantauan Respons Gas, Suhu, dan Kelembapan Berbasis Blynk

**Anggota:** Zainal Fattah, Naufal Adani, Aisyha N A.

**Batas anggaran:** Rp150.000.

## 1. Tujuan dan cara kerja

NodeMCU ESP8266 membaca MQ-135 dan DHT11, mengendalikan LED hijau/merah, lalu mengirim data melalui Wi-Fi 2,4 GHz ke dashboard Blynk. Dashboard menampilkan suhu, kelembapan, respons gas, status alat, grafik, serta tombol conditioning dan pengambilan baseline.

MQ-135 pada proyek ini digunakan untuk melihat **perubahan respons gas relatif terhadap baseline**. Alat ini bukan pengukur AQI/ISPU, PM2.5, CO2 ppm, atau alarm keselamatan yang tervalidasi.

## 2. Rencana belanja tanpa PCB

Harga merupakan alokasi agar total tetap di bawah Rp150.000. Periksa kembali harga toko dan ongkir sebelum membeli.

| Komponen | Jumlah | Anggaran | Keterangan |
|---|---:|---:|---|
| NodeMCU V3 ESP8266 ESP-12E, CH340, flash 4 MB | 1 | Rp35.000 | Board utama dan Wi-Fi |
| Modul MQ-135 dengan pin AO | 1 | Rp20.000 | Sensor respons gas |
| Modul DHT11 3 pin yang mendukung 3,3 V | 1 | Rp18.000 | Suhu dan kelembapan |
| Breadboard MB-102 830 titik | 1 | Rp15.000 | Perakitan tanpa solder/PCB |
| Kabel jumper male–male | 1 set | Rp8.000 | Jalur di breadboard |
| Kabel jumper male–female | 1 set | Rp8.000 | Menghubungkan modul sensor |
| LED hijau dan merah 3/5 mm | 2 | Rp2.000 | Indikator kondisi |
| R 47 kΩ 1%, R 10 kΩ 1% ×2, R 1 kΩ ×2 | 5 | Rp3.000 | Pembagi A0, pull-up, LED |
| Kapasitor 100 nF ×2 dan elko 100 µF ≥10 V | 3 | Rp4.000 | Filter dan stabilisasi |
| Kabel USB data sesuai NodeMCU | 1 | Rp8.000 | Upload dan pengujian |
| Adaptor USB 5 V 1–2 A | 1 | Rp15.000 | Catu saat demonstrasi |
| Alas sederhana dan cable tie | 1 set | Rp5.000 | Merapikan prototipe |
| Cadangan harga/ongkir | — | Rp9.000 | Cadangan |
| **Total maksimum** | | **Rp150.000** | |

Jika adaptor dan kabel USB sudah tersedia, sisa anggaran dapat dipakai untuk breadboard yang lebih baik atau jumper cadangan. Solder dan PCB tidak diperlukan.

## 3. Sambungan breadboard

Gunakan rel merah untuk 5 V, rel biru untuk GND, dan buat jalur 3,3 V terpisah. Semua GND harus tersambung menjadi satu.

| Dari | Melalui | Ke |
|---|---|---|
| NodeMCU VIN/VU* | — | rel 5 V dan VCC MQ-135 |
| NodeMCU GND | — | rel GND dan GND semua modul |
| MQ-135 AO | resistor 47 kΩ | titik ADC |
| titik ADC | resistor 10 kΩ | GND |
| titik ADC | C1 kapasitor 100 nF | GND |
| titik ADC | — | A0 NodeMCU |
| NodeMCU 3V3 | — | VCC DHT11 |
| DHT11 DATA | — | D2 / GPIO4 |
| DHT11 DATA | resistor 10 kΩ | 3V3, bila modul belum memiliki pull-up |
| NodeMCU D5 / GPIO14 | resistor 1 kΩ | anoda LED hijau |
| NodeMCU D6 / GPIO12 | resistor 1 kΩ | anoda LED merah |
| Katoda kedua LED | — | GND |
| rel 5 V | C2 elko 100 µF (+ ke 5 V, − ke GND) | rel GND |
| rel 3V3 | C3 kapasitor 100 nF | rel GND |

\*Saat memakai USB, gunakan pin 5 V yang memang berlabel **VIN/VU/5V** pada board aktual. Klon NodeMCU berbeda-beda; cek tulisan silkscreen. Jangan memasukkan 5 V ke pin 3V3.

Pin DO MQ-135 tidak digunakan. Pembagi 47 kΩ/10 kΩ wajib dipasang agar tegangan AO tidak langsung masuk ke A0. Hasil ideal saat AO 5 V adalah sekitar 0,88 V.

## 4. Tata letak yang disarankan

- Letakkan NodeMCU melintang di celah tengah breadboard. Jika board V3 terlalu lebar, pasang NodeMCU di samping breadboard dan hubungkan memakai jumper male–female.
- Tempatkan pembagi tegangan 47 kΩ/10 kΩ dekat pin A0.
- Letakkan DHT11 minimal sekitar 10 cm dari MQ-135 karena pemanas MQ-135 dapat memengaruhi suhu.
- MQ-135 harus terbuka dan berventilasi; jangan ditutup casing rapat.
- Pakai warna kabel konsisten: merah 5 V, oranye 3,3 V, hitam GND, kuning sinyal, hijau LED.

Panduan langkah demi langkah terdapat di `PANDUAN_PERAKITAN_BREADBOARD.md`.
Skema kabel berwarna terdapat di `Skema_Perakitan_Breadboard.svg`.

## 5. Perangkat lunak dan Blynk

Firmware utama berada di `Firmware/UdaraKitaBlynk/UdaraKitaBlynk.ino`. Datastream yang digunakan adalah V0–V8. Cara mengisi Auth Token, Wi-Fi, dan meng-upload program dijelaskan di `CARA_RUN_BLYNK.md`.

## 6. Pembagian kerja

| Anggota | Tanggung jawab | Hasil |
|---|---|---|
| Zainal Fattah | NodeMCU, firmware, dan Blynk | Perangkat online dan data tampil |
| Naufal Adani | Belanja, breadboard, kabel, dan pengujian daya | Rangkaian rapi dan tabel sambungan |
| Aisyha N A | Pengujian sensor, laporan, dan presentasi | Catatan hasil dan dokumentasi |

## 7. Jadwal ringkas

1. Hari 1: beli komponen, cek board dan kabel USB, mulai conditioning MQ-135.
2. Hari 2–3: lanjutkan conditioning MQ-135 lebih dari 48 jam dan susun rangkaian breadboard.
3. Hari 4: upload firmware, hubungkan Blynk, dan cek semua datastream.
4. Hari 5: ambil baseline, uji perubahan data, rapikan kabel, dan catat hasil.
5. Hari 6–7: dokumentasi, perbaikan, dan latihan demonstrasi.

## 8. Pemeriksaan sebelum dinyalakan

1. Pastikan tidak ada hubungan langsung antara 5 V dan GND.
2. Pastikan DHT11 menerima 3,3 V dan MQ-135 menerima 5 V.
3. Pastikan AO MQ-135 melewati pembagi 47 kΩ/10 kΩ sebelum A0.
4. Pastikan polaritas LED dan elko benar.
5. Upload program dengan sumber eksternal dilepas; selama pengujian awal cukup gunakan USB.
6. Setelah alat menyala, lihat status pada Serial Monitor dan Blynk sebelum menilai angka sensor.

## 9. Batasan

Rangkaian dan firmware belum diuji pada perangkat fisik karena komponen belum dibeli. Nilai sensor akan berbeda antarmodul, sehingga baseline harus diambil pada perangkat yang sudah dirakit. File PCB lama tetap disimpan sebagai arsip desain dan bukan bagian dari implementasi akhir.
