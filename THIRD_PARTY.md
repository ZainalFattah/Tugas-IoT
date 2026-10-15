# Pustaka dan toolchain

Lisensi MIT proyek tidak menggantikan lisensi dependensi.

- Blynk library 1.3.2 (firmware Blynk): https://github.com/blynkkk/blynk-library/tree/v1.3.2 — MIT. Blynk.Cloud memiliki ketentuan layanan/paket terpisah.

- ESP8266 Arduino Core 3.1.2: https://github.com/esp8266/Arduino/tree/3.1.2 — lisensi core LGPL-2.1 dan berbagai lisensi komponen; SDK Espressif mengikuti ketentuannya sendiri. Lisensi: https://github.com/esp8266/Arduino/blob/3.1.2/LICENSE .
- DHT sensor library 1.4.6: https://github.com/adafruit/DHT-sensor-library/tree/1.4.6 — MIT.
- Adafruit Unified Sensor 1.1.15: https://github.com/adafruit/Adafruit_Sensor/tree/1.1.15 — Apache-2.0.
- PubSubClient 2.8: https://github.com/knolleary/pubsubclient/tree/v2.8 — MIT.
- PlatformIO espressif8266 4.2.1: https://github.com/platformio/platform-espressif8266/tree/v4.2.1 — Apache-2.0.

Source aplikasi dan konfigurasi build disertakan. Dependensi diunduh oleh Arduino/PlatformIO dari sumber di atas. Salinan berkas lisensi dependensi utama ada di folder Licenses. Jika mendistribusikan ulang binary kepada publik, penuhi persyaratan source/relinking serta pemberitahuan lisensi masing-masing dependensi; lisensi MIT aplikasi tidak mencakup seluruh binary firmware.
