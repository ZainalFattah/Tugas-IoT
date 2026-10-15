from pathlib import Path
import hashlib,json,shutil,zipfile,subprocess

p=Path(__file__).parent
binary=p/'.pio/build/nodemcuv2/firmware.bin'
assert binary.is_file(), 'Build firmware first.'
shutil.copyfile(binary,p/'Release/UdaraKita-NodeMCU-4MB.bin')
firmware=p/'Release/UdaraKita-NodeMCU-4MB.bin'
sources=list((p/'Firmware/UdaraKita').glob('*'))+[p/'Dashboard/index.html',p/'platformio.ini']
manifest={str(f.relative_to(p)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in [firmware,*sources]}
(p/'Release/SHA256.json').write_text(json.dumps(manifest,indent=2))
report='''UdaraKita software verification — 12 October 2026

BUILD PASS: PlatformIO espressif8266 4.2.1, Arduino Core 3.1.2.
Target: nodemcuv2 / ESP8266 ESP-12E / 4 MB flash / 80 MHz.
RAM static: 30,104 / 81,920 bytes (36.7%).
Program flash: 330,523 / 1,044,464 bytes (31.6%).
Source and binary SHA256: Release/SHA256.json.

PASS native C++ SensorLogic tests:
- stable baseline accepted;
- unstable, too-short, zero, and saturated baseline rejected;
- 10-second alarm onset/recovery and hysteresis;
- interrupted excursion resets timer;
- invalid sensor clears indicator state;
- unsigned millis rollover.

PASS JavaScript syntax check (node --check).
PASS browser simulation: normal/elevated/sensor-error display,
baseline collection state and disabled action, CSV download.
CSV inspected: mode SIMULASI and measurement/status columns present.
PASS live mode without API: disconnected banner, empty data, baseline disabled.
PASS responsive check: viewport 390 px, document width 375 px, no overflow.
Browser console: no errors in simulation during inspection.

NOT TESTED: flashing board, physical sensor readings, power integrity,
real ESP8266 web-server operation, or connection to a live MQTT broker.
MQTT compile-time option defaults OFF. Demo data are not real readings.
PCB remains Rev A; no KiCad DRC/ERC or physical validation added by this build.
'''
(p/'HASIL_PENGUJIAN.txt').write_text(report,encoding='utf-8')
with zipfile.ZipFile(p/'Kelompok7_Udara_Siap_Upload.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in p.rglob('*'):
  if not f.is_file() or any(x in {'.pio','__pycache__','.git'} for x in f.relative_to(p).parts):continue
  if f.suffix in {'.zip','.exe','.pyc'}:continue
  z.write(f,f.relative_to(p))
with zipfile.ZipFile(p/'Kelompok7_Udara_Siap_Upload.zip') as z:
 assert z.testzip() is None
 print('Release ZIP verified:',len(z.namelist()),'files')
print('Firmware:',firmware.stat().st_size,'bytes')
print('SHA256:',manifest['Release/UdaraKita-NodeMCU-4MB.bin'])
