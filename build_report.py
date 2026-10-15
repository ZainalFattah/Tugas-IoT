from pathlib import Path
import html,re,zipfile
P=Path(__file__).parent
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="850" viewBox="0 0 1200 850"><rect width="1200" height="850" fill="#f7fafc"/>']
def text(x,y,t,size=17,color='#19394b'):
 s.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">{html.escape(t)}</text>')
def line(*pts):
 s.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#206c81" stroke-width="2.5"/>')
def dot(x,y):s.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#206c81"/>')
def gnd(x,y):
 line((x,y),(x,y+12));line((x-13,y+12),(x+13,y+12));line((x-8,y+18),(x+8,y+18));line((x-3,y+24),(x+3,y+24))
def resistor(x,y,label,vertical=False):
 if vertical:
  line((x,y),(x,y+12));s.append(f'<rect x="{x-7}" y="{y+12}" width="14" height="40" fill="white" stroke="#206c81" stroke-width="2"/>');line((x,y+52),(x,y+65));text(x+14,y+36,label,15)
 else:
  line((x,y),(x+12,y));s.append(f'<rect x="{x+12}" y="{y-7}" width="55" height="14" fill="white" stroke="#206c81" stroke-width="2"/>');line((x+67,y),(x+80,y));text(x+4,y-18,label,15)
def cap(x,y,label):
 line((x,y),(x,y+24));line((x-12,y+24),(x+12,y+24));line((x-12,y+31),(x+12,y+31));line((x,y+31),(x,y+65));text(x+18,y+35,label,15)
text(40,42,'KELOMPOK 7 | SKEMA LISTRIK UDARAKITA',29)
text(40,73,'Rev A · Papan antarmuka NodeMCU ESP8266 · Semua simbol GND terhubung',17)
text(40,120,'1 / MQ-135 dan pembagi analog',22)
text(40,167,'J2.1 = +5 V    J2.2 = GND    J2.3 = AO',16)
line((60,210),(250,210));text(60,199,'AO / J2.3');resistor(250,210,'R1 47k 1%');line((330,210),(630,210));text(515,197,'ADC → J3.1 → A0')
dot(365,210);dot(470,210);resistor(365,210,'R2 10k 1%',True);gnd(365,275);cap(470,210,'C1 100nF');gnd(470,275)
text(40,330,'J3.2 = GND. AO 5 V → ADC sekitar 0,877 V sebelum beban A0.',16)
text(725,120,'2 / Daya',22)
text(725,165,'J1.1 = +5 V teratur',17);line((760,190),(1070,190));text(975,180,'ke J2.1',16);cap(835,190,'C2 100uF');text(816,210,'+',16);gnd(835,255)
text(725,308,'J1.2 = GND. Pad 1 C2 positif.',16)
text(725,335,'Cabang 5 V terpisah ke VIN NodeMCU.',16)
text(40,395,'3 / DHT11 pada 3,3 V',22)
line((65,445),(560,445));text(65,432,'3V3 / J4.1');text(445,432,'J5.1 VCC',16)
resistor(270,445,'R3 10k',True);line((65,525),(560,525));line((270,510),(270,525));dot(270,445);dot(270,525)
text(65,551,'DATA / J4.2 → D2 (GPIO4)',16);text(445,551,'J5.2 DATA',16)
line((560,445),(625,445));cap(625,445,'C3 100nF');gnd(625,510)
text(40,600,'J4.3 = J5.3 = GND. Pilih modul DHT11 yang mendukung 3,3 V.',16)
text(725,395,'4 / Indikator',22)
for y,pin,r,led in [(450,'D5/GPIO14','R4','D1 hijau'),(555,'D6/GPIO12','R5','D2 merah')]:
 text(725,y-22,pin+' / J6.'+('1' if r=='R4' else '2'),16);line((735,y),(840,y));resistor(840,y,r+' 1k');line((920,y),(960,y))
 s.append(f'<polygon points="960,{y-10} 960,{y+10} 980,{y}" fill="none" stroke="#206c81" stroke-width="2"/>');line((980,y-11),(980,y+11));line((980,y),(1050,y));gnd(1050,y)
 line((973,y-17),(985,y-29),(980,y-28));line((980,y-13),(992,y-25),(987,y-24))
 text(945,y+48,led+' : A=2, K=1',15)
text(725,640,'J6.3 = GND. HIGH menyalakan LED.',16)
text(40,697,'KONEKSI MODUL DENGAN KABEL',22)
text(40,730,'NodeMCU dan sensor berada di luar PCB. Urutan pin modul harus mengikuti label modul aktual.',17)
text(40,760,'Jangan hubungkan AO 5 V langsung ke A0. DO MQ-135 tidak dipakai. Suplai DHT tetap 3,3 V.',17)
text(40,805,'Review KiCad dan uji breadboard sebelum fabrikasi. Skema SVG ini bukan berkas ERC KiCad.',16)
s.append('</svg>');(P/'Skema_Rangkaian.svg').write_text('\n'.join(s),encoding='utf-8')
raw=(P/'Rencana_Proyek.md').read_text(encoding='utf-8')
def inline(t):
 t=html.escape(t)
 t=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',t)
 t=re.sub(r'`(.*?)`',r'<code>\1</code>',t)
 t=re.sub(r'(https://[^\s<]+)',r'<a href="\1">sumber ↗</a>',t)
 return t
body=[];table=False
for l in raw.splitlines():
 if l.startswith('|'):
  if not table:body.append('<table>');table=True
  if re.match(r'^\|[\s:|\-]+$',l):continue
  body.append('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in l.strip('|').split('|'))+'</tr>');continue
 if table:body.append('</table>');table=False
 if l.startswith('# '):body.append('<h1>'+inline(l[2:])+'</h1>')
 elif l.startswith('## '):
  if l.startswith('## 4.'):body.append('<img src="Preview_PCB.png" alt="Desain PCB"/>')
  if l.startswith('## 6.'):body.append('<img src="Skema_Rangkaian.svg" alt="Skema rangkaian"/>')
  body.append('<h2>'+inline(l[3:])+'</h2>')
 elif l.strip():body.append('<p>'+inline(l)+'</p>')
page='''<!doctype html><html lang="id"><meta charset="utf-8"><title>Kelompok 7 — UdaraKita</title><style>
body{font:16px/1.65 system-ui,Arial;color:#20394b;max-width:1040px;margin:40px auto;padding:0 28px;background:#f9fbfc}h1{font-size:38px;line-height:1.2;border-top:7px solid #16818d;padding-top:26px}h2{margin-top:42px;color:#106c77}table{border-collapse:collapse;width:100%;font-size:14px;background:white}td{padding:10px;border-bottom:1px solid #dae4e9}tr:first-child{background:#dfeff1;font-weight:bold}img{display:block;width:100%;margin:28px auto}a{color:#087f90}code{background:#edf0f5;padding:2px 5px}@media print{body{margin:0;font-size:11px;background:white}h1{font-size:26px}h2{font-size:18px;break-after:avoid}table{font-size:10px}tr,img{break-inside:avoid}a{color:inherit}img{max-height:750px;object-fit:contain}}
</style><body>'''+''.join(body)+'</body></html>'
(P/'Rencana_Proyek.html').write_text(page,encoding='utf-8')
with zipfile.ZipFile(P/'Kelompok7_Udara_Desain.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in P.iterdir():
  if f.is_file() and f.suffix!='.zip':z.write(f,f.name)
print('Skema, laporan HTML, dan ZIP dibuat.')

