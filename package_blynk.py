from pathlib import Path
import hashlib,json,zipfile

p=Path(__file__).parent
required=[
 p/'Firmware/UdaraKitaBlynk/UdaraKitaBlynk.ino',
 p/'Firmware/UdaraKitaBlynk/Config.h',
 p/'Firmware/UdaraKitaBlynk/SensorLogic.h',
 p/'platformio_blynk.ini',p/'CARA_RUN_BLYNK.md',p/'PANDUAN_PERAKITAN_BREADBOARD.md',p/'Skema_Perakitan_Breadboard.svg',
 p/'Dashboard/Rancangan_Blynk.png',p/'Datastream_Blynk.csv',
 p/'HASIL_PENGUJIAN_BLYNK.txt'
]
assert all(f.is_file() for f in required)
config=(p/'Firmware/UdaraKitaBlynk/Config.h').read_text(encoding='utf-8')
assert '#define BLYNK_AUTH_TOKEN ""' in config
assert 'TMPL6WAqmMi4A' in config
manifest={str(f.relative_to(p)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in required}
(p/'BLYNK_SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
include=[
 'Firmware/UdaraKitaBlynk','CARA_RUN_BLYNK.md','PANDUAN_PERAKITAN_BREADBOARD.md','Skema_Perakitan_Breadboard.svg','platformio_blynk.ini',
 'Dashboard/Rancangan_Blynk.png','Dashboard/build_blynk_layout.py',
 'Datastream_Blynk.csv','HASIL_PENGUJIAN_BLYNK.txt','BLYNK_SHA256.json',
 'Rencana_Proyek.md','LICENSE','THIRD_PARTY.md',
 'Licenses/Blynk.txt','Licenses/DHT.txt','Licenses/Adafruit_Unified_Sensor.txt',
 'Licenses/ESP8266_Core.txt'
]
target=p/'Kelompok7_Udara_Blynk.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for item in include:
  src=p/item
  if src.is_dir():
   for f in src.rglob('*'):
    if f.is_file():z.write(f,f.relative_to(p))
  elif src.is_file():z.write(src,src.relative_to(p))
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None
 print('Blynk ZIP verified:',len(z.namelist()),'files')
print('Package:',target)
