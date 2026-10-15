# Panduan Perakitan UdaraKita Tanpa PCB

Panduan ini dipakai untuk implementasi akhir Kelompok 7. Rangkaian dapat dibongkar-pasang dan tidak memerlukan solder.

Lihat [skema perakitan berwarna](Skema_Perakitan_Breadboard.svg) atau [versi PNG](Skema_Perakitan_Breadboard.png) untuk mengikuti jalur pin, daya, resistor, dan sensor. Gambar menunjukkan hubungan listrik; posisi lubang breadboard dapat disesuaikan dengan ukuran board yang dibeli. Label `3V3` dan `GND` yang berulang pada bagian sensor/LED berarti hubungkan titik tersebut ke rel dengan nama yang sama pada breadboard. Titik bulat pada jalur menandakan sambungan listrik.

## Komponen inti

- NodeMCU V3 ESP8266 ESP-12E dengan CH340, flash 4 MB.
- MQ-135 modul 4 pin yang memiliki AO.
- DHT11 modul 3 pin yang mendukung 3,3 V.
- Breadboard MB-102 830 titik.
- Jumper male–male dan male–female.
- Resistor 47 kΩ, 10 kΩ ×2, dan 1 kΩ ×2.
- LED hijau dan merah.
- Kapasitor 100 nF ×2 dan elko 100 µF minimal 10 V.

## Urutan pemasangan

1. Jangan sambungkan USB atau adaptor terlebih dahulu.
2. Hubungkan GND NodeMCU ke rel biru breadboard.
3. Hubungkan pin 3V3 ke satu baris khusus 3,3 V. Jangan gabungkan dengan rel 5 V.
4. Hubungkan MQ-135: VCC ke 5 V dari pin VU/5V yang sudah diverifikasi dengan multimeter saat USB menyala, GND ke rel GND, dan biarkan DO kosong. Pada klon yang tidak menyediakan keluaran 5 V dari USB, gunakan sumber 5 V terpisah dengan GND bersama; jangan menebak fungsi pin VIN.
5. Buat pembagi analog: AO MQ-135 → 47 kΩ → titik ADC; titik ADC → 10 kΩ → GND; titik ADC → A0. Pasang **C1 100 nF** dari titik ADC ke GND untuk meredam gangguan bacaan.
6. Hubungkan DHT11: VCC ke 3V3, GND ke GND, DATA ke D2. Bila modul tidak memiliki resistor pull-up, pasang 10 kΩ antara DATA dan 3V3.
7. Pasang LED hijau: D5 → 1 kΩ → **anoda (+, kaki panjang)** LED; **katoda (−, kaki pendek/sisi datar)** → GND.
8. Pasang LED merah: D6 → 1 kΩ → **anoda (+, kaki panjang)** LED; **katoda (−, kaki pendek/sisi datar)** → GND.
9. Pasang **C2 elko 100 µF** antara 5 V dan GND dekat MQ-135: kaki positif ke 5 V dan kaki negatif ke GND. Pasang **C3 100 nF** antara rel 3V3 dan GND. C1 dan C3 tidak memiliki polaritas.
10. Periksa ulang semua sambungan dengan tabel di bawah sebelum memberi daya.

Pada breadboard, tempatkan **dua kaki setiap LED pada baris yang tidak saling terhubung**. Pastikan resistor 1 kΩ berada seri di sisi anoda, bukan dipasang sejajar dengan LED. Beberapa breadboard memiliki rel daya yang terputus di tengah; cek kontinuitas rel 5 V, 3V3, dan GND, lalu beri jumper penghubung jika perlu.

## Tabel kabel cepat

| Pin perangkat | Tujuan |
|---|---|
| NodeMCU D2 | DATA DHT11 |
| NodeMCU D5 | resistor 1 kΩ → LED hijau |
| NodeMCU D6 | resistor 1 kΩ → LED merah |
| NodeMCU A0 | titik tengah pembagi 47 kΩ/10 kΩ |
| NodeMCU 3V3 | VCC DHT11 |
| NodeMCU VIN/VU/5V | VCC MQ-135 |
| NodeMCU GND | semua GND |
| C1 100 nF | titik ADC ↔ GND |
| C2 100 µF | kaki + ke 5 V, kaki − ke GND |
| C3 100 nF | 3V3 ↔ GND |

## Bentuk pembagi A0

```text
AO MQ-135 ----[ 47 kΩ ]----+---- A0 NodeMCU
                            |
                         [ 10 kΩ ]
                            |
GND ------------------------+---- GND NodeMCU

Kapasitor 100 nF dipasang dari titik A0 ke GND.
```

## Pengujian aman

1. Saat upload firmware, lepaskan adaptor 5 V eksternal dan gunakan USB data.
2. Sebelum memasang kabel A0 ke NodeMCU, ukur titik ADC terhadap GND. Dengan AO maksimum 5 V, titik ADC seharusnya sekitar 0,88 V dan harus tetap di bawah 1 V.
3. Nyalakan dahulu tanpa mengandalkan angka kualitas udara. Pastikan NodeMCU online di Blynk, DHT11 terbaca, dan kedua LED dapat berubah sesuai status.
4. MQ-135 baru memerlukan conditioning lebih dari 48 jam. Sesudah itu tunggu pemanasan setiap kali alat dinyalakan, lalu tekan tombol baseline selama 60 detik.

## Penataan untuk presentasi

Tempel breadboard pada alas karton tebal, akrilik, atau papan plastik. Letakkan MQ-135 di sisi terbuka dan DHT11 sejauh mungkin dari panas MQ-135. Ikat kabel per kelompok dan beri label kecil `5V`, `3V3`, `GND`, `D2`, `D5`, `D6`, dan `A0`.
