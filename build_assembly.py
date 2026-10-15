from pathlib import Path
import json,zipfile,csv,html
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

P=Path(__file__).parent
data=json.loads((P/'netlist.json').read_text()); parts=data['parts']; S=data['grid_mm']
INK='#19394b';TEAL='#087d88'; BG='#f3f7fb'
def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),n)
def start(title,subtitle,h=1150):
 im=Image.new('RGB',(1600,h),BG);d=ImageDraw.Draw(im)
 d.text((65,35),title,font=font(38,True),fill=INK);d.text((65,92),subtitle,font=font(21),fill=INK)
 return im,d
def box(d,rect,title,color='#ffffff'):
 d.rounded_rectangle(rect,18,fill=color,outline='#bbced8',width=2)
 d.text((rect[0]+20,rect[1]+15),title,font=font(25,True),fill=INK)
def save(im,name):im.save(P/name)

# Actual coordinate-based component assembly view; no traces obscure the bodies.
im,d=start('01 / Pemasangan komponen PCB','Tampak atas / sisi komponen. Pad persegi = nomor 1. Gambar diperbesar, bukan skala cetak 1:1.')
ox,oy,sc=95,180,11
def xy(p):return ox+p['x']*S*sc,oy+p['y']*S*sc
d.rounded_rectangle((ox,oy,ox+76.2*sc,oy+63.5*sc),14,fill='#176259',outline='#073a39',width=4)
for c in parts:
 ps=c['pads'];a,b=xy(ps[0]),xy(ps[-1]);ref=c['ref']
 if ref.startswith('R'):
  d.line([a,b],fill='#dddddd',width=5)
  mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
  if a[0]==b[0]:r=(mx-10,my-24,mx+10,my+24)
  else:r=(mx-24,my-10,mx+24,my+10)
  d.rounded_rectangle(r,4,fill='#e9cc9c',outline='#a97e43',width=2)
 elif ref=='C2':
  mx,my=(a[0]+b[0])/2,a[1]
  d.ellipse((mx-32,my-32,mx+32,my+32),fill='#25414f',outline='#e0e4e5',width=3)
  d.text((mx+12,my-18),'-',font=font(20,True),fill='white')
 elif ref.startswith('C'):
  d.line([a,b],fill='#dddddd',width=4);mx,my=(a[0]+b[0])/2,a[1]
  d.ellipse((mx-14,my-18,mx+14,my+18),fill='#ebad50',outline='#6f451b',width=2)
 elif ref.startswith('D'):
  mx,my=(a[0]+b[0])/2,a[1]
  d.ellipse((mx-17,my-17,mx+17,my+17),fill='#66f6a0' if ref=='D1' else '#ff6876',outline='white',width=2)
 else:d.rectangle((a[0]-12,a[1]-12,b[0]+12,b[1]+12),fill='#202c37')
 for p in ps:
  x,y=xy(p);r=5
  (d.rectangle if p['num']==1 else d.ellipse)((x-r,y-r,x+r,y+r),fill='#ffe498')
  if ref.startswith('J'):d.text((x-5,y+17),str(p['num']),font=font(14),fill='white')
 d.text((a[0]-12,min(a[1],b[1])-47),ref,font=font(21,True),fill='white')
 if ref.startswith('D'):d.text((a[0]-4,a[1]+24),'K    A',font=font(15),fill='white')
box(d,(1000,180,1535,920),'Nilai & arah pemasangan')
items=['R1  47 kΩ 1%','R2  10 kΩ 1%','R3  10 kΩ (pull-up DHT)','R4, R5  1 kΩ','C1, C3  100 nF (104)','C2  100 µF / ≥10 V','C2: pad 1 (+), pad 2 (-)','D1: LED hijau 3 mm','D2: LED merah 3 mm','LED: pad 1 K, pad 2 A','J1–J6: header 2,54 mm','Resistor & C1/C3: bebas arah']
for i,t in enumerate(items):d.text((1020,245+i*49),t,font=font(23),fill=INK)
d.text((95,957),'Urutan solder: resistor → kapasitor kecil → LED → header → elko C2.',font=font(25,True),fill=INK)
d.text((95,1002),'Kaki masuk dari atas; solder dari sisi bawah. Ukuran PCB: 76,20 × 63,50 mm.',font=font(24),fill=INK)
d.text((95,1045),'D2 pada PCB = LED merah. D2 pada NodeMCU = GPIO4 untuk sensor DHT11.',font=font(23),fill='#a04430')
save(im,'01_Pemasangan_Komponen.png')

# Exact connection schedule, represented as colored parallel lanes.
connections=[
('J2.1','MQ-135 VCC / 5V','Merah','#d63f4c'),('J2.2','MQ-135 GND','Hitam','#344354'),('J2.3','MQ-135 AO','Kuning','#b58300'),
('J3.1','NodeMCU A0','Kuning','#b58300'),('J3.2','NodeMCU GND','Hitam','#344354'),
('J4.1','NodeMCU 3V3','Oranye','#de7b22'),('J4.2','NodeMCU D2 / GPIO4','Biru','#297ace'),('J4.3','NodeMCU GND','Hitam','#344354'),
('J5.1','DHT11 VCC / 3V3','Oranye','#de7b22'),('J5.2','DHT11 DATA / S','Biru','#297ace'),('J5.3','DHT11 GND / -','Hitam','#344354'),
('J6.1','NodeMCU D5 / GPIO14','Hijau','#269667'),('J6.2','NodeMCU D6 / GPIO12','Ungu','#9c55b7'),('J6.3','NodeMCU GND','Hitam','#344354')]
im,d=start('02 / Diagram kabel pin ke pin','Posisi baris adalah diagram logis, bukan urutan pin fisik modul. Ikuti label pada modul yang dibeli.',1300)
box(d,(65,155,500,1120),'HEADER PCB');box(d,(1060,155,1535,1120),'LABEL MODUL')
for i,(src,dst,color,col) in enumerate(connections):
 y=225+i*62
 d.text((100,y-14),src,font=font(25,True),fill=INK);d.text((1085,y-14),dst,font=font(23),fill=INK)
 d.line((475,y,1080,y),fill=col,width=5);d.ellipse((466,y-7,480,y+7),fill=col)
 d.text((720,y-27),color,font=font(17),fill=col)
d.text((65,1160),'J1 adalah input daya: lihat diagram daya pada panduan. DO MQ-135 tidak dihubungkan.',font=font(24),fill=INK)
d.text((65,1205),'Jangan menyamakan urutan VCC / GND / AO di gambar dengan posisi fisik pin sensor.',font=font(24,True),fill='#a04430')
save(im,'02_Diagram_Kabel.png')
with (P/'Daftar_Kabel.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['Dari PCB','Ke label modul','Warna saran']);w.writerows([r[:3] for r in connections])

im,d=start('03 / Dudukan dan posisi perangkat','Desain mekanik usulan: alas 200 × 150 mm. Ukur modul aktual sebelum membuat dudukan.',1200)
bx,by,k=120,195,5.4
def rectmm(x,y,w,h):return (bx+x*k,by+y*k,bx+(x+w)*k,by+(y+h)*k)
d.rounded_rectangle(rectmm(0,0,200,150),20,fill='#e5d8b9',outline='#9b8b67',width=3)
for x,y in [(5,5),(195,5),(5,145),(195,145)]:
 px,py=bx+x*k,by+y*k;d.ellipse((px-6,py-6,px+6,py+6),fill=BG,outline='#8e805f',width=2)
# Locations allow >=100 mm separation between complete sensor envelopes.
box(d,rectmm(10,12,25,30),'DHT11','#b4e4f7')
box(d,rectmm(163,12,27,32),'MQ-135','#ccdde9')
cx,cy=bx+176*k,by+26*k;d.ellipse((cx-37,cy-37,cx+37,cy+37),fill='#bdc5ce',outline='#788592',width=3)
for off in [-20,-10,0,10,20]:d.line((cx-25,cy+off,cx+25,cy+off),fill='#788592',width=2)
box(d,rectmm(10,77,32,58),'NodeMCU','#dde6ec')
d.rectangle(rectmm(12,120,12,12),fill='#b1b9c1');d.text((bx+12*k,by+138*k),'USB',font=font(21),fill=INK)
pcb=Image.open(P/'01_Pemasangan_Komponen.png').crop((95,180,int(95+76.2*11),int(180+63.5*11))).resize((int(76.2*k),int(63.5*k)))
im.paste(pcb,(int(bx+65*k),int(by+72*k)))
box(d,rectmm(65,12,63,22),'Distribusi daya','#fff7dc')
for pts in [[(35,34),(53,34),(53,119),(65,119)],[(163,35),(150,35),(150,78),(137,78)],[(42,101),(54,101),(54,108),(65,108)]]:
 d.line([(bx+x*k,by+y*k) for x,y in pts],fill='#588994',width=5)
d.text((bx+62*k,by+140*k),'PCB 76,2 × 63,5 mm',font=font(23,True),fill=INK)
d.line((bx+35*k,by+52*k,bx+163*k,by+52*k),fill=INK,width=2)
d.text((bx+52*k,by+55*k),'Jarak sensor >100 mm',font=font(23),fill=INK)
for i,t in enumerate(['Alas 200 × 150 mm','Bahan bekas nonkonduktif','PCB ditahan klip tepi','Celah bawah 8–10 mm','Jangan bor jalur PCB','MQ terbuka & berventilasi','DHT jauh dari panas','Lubang alas Ø3 mm','Koordinat: (5,5), (195,5),','(5,145), (195,145) mm']):d.text((1235,210+i*63),t,font=font(21),fill=INK)
d.text((120,1043),'Area modul bersifat nominal. Antena NodeMCU jangan tertutup logam atau kabel.',font=font(24),fill=INK)
d.text((120,1085),'Konsep ini memakai alas terbuka agar tetap hemat; bukan casing kedap atau untuk luar ruangan.',font=font(23),fill=INK)
save(im,'03_Desain_Dudukan.png')

im,d=start('04 / Distribusi daya 5 V','Satu sumber 5 V teratur, minimal 1 A. Semua ground terhubung. Jangan gabungkan dua sumber daya.',900)
box(d,(65,180,525,685),'SATU ADAPTOR 5 V / 1 A')
box(d,(1110,180,1535,380),'PCB / J1');box(d,(1110,470,1535,685),'NODEMCU')
for y,label,col in [(275,'+5 V: cabang PCB','#d63f4c'),(340,'GND: cabang PCB','#344354'),(560,'+5 V: cabang MCU','#d63f4c'),(625,'GND: cabang MCU','#344354')]:
 d.text((90,y-18),label,font=font(25),fill=col)
 d.line([(515,y),(1110,y)],fill=col,width=6)
d.text((95,419),'Dua cabang dari +5 V yang sama.',font=font(20),fill=INK)
d.text((95,453),'Dua cabang dari GND yang sama.',font=font(20),fill=INK)
d.text((1130,257),'J1.1 → +5 V',font=font(26),fill=INK);d.text((1130,321),'J1.2 → GND',font=font(26),fill=INK)
d.text((1130,542),'VIN / input 5 V*',font=font(26),fill=INK);d.text((1130,607),'GND',font=font(26),fill=INK)
d.text((65,735),'*Pastikan VIN board yang dibeli memang menerima 5 V. Jangan masukkan 5 V ke pin 3V3.',font=font(24),fill=INK)
d.text((65,778),'Saat upload: lepas adaptor eksternal. Gunakan USB laptop; lepas USB sebelum menyalakan adaptor.',font=font(23),fill=INK)
d.text((65,823),'Percabangan berada di luar PCB. Isolasi sambungan; identifikasi polaritas dengan multimeter.',font=font(23),fill=INK)
save(im,'04_Distribusi_Daya.png')

# Printable assembly booklet, with controlled page layout.
pdf=canvas.Canvas(str(P/'Panduan_Desain_dan_Perakitan.pdf'),pagesize=(595.28,841.89))
style=ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=15,textColor=HexColor(INK))
page=0;y=0
def new(title,sub=''):
 global page,y
 if page:pdf.showPage()
 page+=1;pdf.setFillColor(HexColor(TEAL));pdf.rect(0,821,596,21,fill=1,stroke=0)
 pdf.setFillColor(HexColor(INK));pdf.setFont('Helvetica-Bold',19);pdf.drawString(38,786,title)
 pdf.setFont('Helvetica',9);pdf.drawString(38,764,sub)
 pdf.setFont('Helvetica',9);pdf.drawString(38,24,'Kelompok 7 Udara | Rev A | 12 Oktober 2026');pdf.drawRightString(557,24,str(page));y=735
def para(t):
 global y
 p=Paragraph(t,style);_,h=p.wrap(519,700)
 assert y-h>44,('Page overflow',page,t)
 p.drawOn(pdf,38,y-h);y-=h+12
def pic(name,height):
 global y
 img=Image.open(P/name);w,h=img.size;ww=min(519,height*w/h);hh=ww*h/w
 pdf.drawImage(ImageReader(img),38+(519-ww)/2,y-hh,width=ww,height=hh);y-=hh+14
new('UdaraKita: desain & perakitan','Zainal Fattah / Naufal Adani / Aisyha N A')
para('<b>Yang dirakit:</b> alat demonstrasi pemantau respons gas MQ-135, suhu dan kelembapan DHT11, dengan NodeMCU ESP8266. Sensor dan NodeMCU berada di luar PCB, terhubung melalui kabel. Dua LED dipasang pada PCB.')
pic('03_Desain_Dudukan.png',420)
para('<b>Paket:</b> PCB KiCad, skema SVG, empat gambar pemasangan, daftar kabel CSV, dan panduan ini. Anggaran tetap Rp150.000 dengan adaptor dan alat dipinjam. Alas memakai bahan bekas dalam alokasi dudukan Rp8.000; bukan casing pabrik atau cetak 3D.')
para('<b>Status:</b> rancangan prototipe Rev A. Koneksi dan clearance telah diperiksa dengan skrip; belum dibuka di KiCad atau diuji fisik. Firmware belum disertakan. Nilai MQ-135 bukan AQI, PM2.5, atau CO2 ppm yang tervalidasi.')
new('1. Persiapan dan daftar komponen')
for t in [
'<b>Elektronik:</b> NodeMCU ESP8266 V3 CH340 x1; modul MQ-135 dengan AO x1; modul DHT11 kompatibel 3,3 V x1; LED hijau dan merah 3 mm masing-masing x1.',
'<b>Komponen PCB:</b> R1 47 kohm 1%; R2 10 kohm 1%; R3 10 kohm; R4 dan R5 1 kohm. Gunakan resistor 1/4 W. C1 dan C3 100 nF keramik, kode 104. C2 100 uF minimal 10 V, diameter maksimal 6,3 mm, pitch kaki 2,54 mm.',
'<b>Konektor:</b> header male pitch 2,54 mm: J1 2 pin, J2 3 pin, J3 2 pin, J4 3 pin, J5 3 pin, J6 3 pin. Total 16 posisi. Sediakan 14 kabel female-female untuk sensor/MCU, serta sambungan catu dua cabang. GND dapat memakai satu percabangan ke ground MCU bila pin GND fisik terbatas; semua GND harus tetap tersambung.',
'<b>Mekanik:</b> alas nonkonduktif 200 x 150 mm; klip tepi PCB atau penyangga isolasi 8-10 mm; pengikat kabel. Gunakan bahan bekas untuk menjaga anggaran. PCB Rev A tidak mempunyai lubang baut, jadi jangan mengebor papan sembarangan.',
'<b>Alat dipinjam:</b> solder, timah, flux, tang potong, multimeter, penggaris, laptop, HP, adaptor 5 V minimal 1 A. Fabrikasi PCB dilakukan dengan fasilitas/jasa lokal setelah review KiCad.',
'<b>Periksa sebelum membeli:</b> suplai DHT11 harus mendukung 3,3 V; NodeMCU harus memiliki input 5 V/VIN yang sesuai; jangan membeli ESP-01 sebagai pengganti. Ukuran dan urutan pin modul belum dipastikan karena foto/tipe barang aktual belum diberikan.',
'<b>Budget:</b> NodeMCU 35rb + MQ135 20rb + DHT11 18rb + pasif/LED 8rb + konektor/kabel jumper 13rb + PCB 20rb + USB/dudukan 16rb + cadangan 20rb = 150rb. Ini alokasi, bukan harga checkout. Rincian sumber tersedia di Rencana_Proyek.html.'
]:para(t)
new('2. Pasang komponen di PCB','Orientasi sama dengan file PCB: J1 di kiri atas, J2 di kanan atas.')
pic('01_Pemasangan_Komponen.png',410)
for t in ['<b>1.</b> Cek pola PCB, putus jalur dan jembatan timah. Resistor dipasang terlebih dahulu; tekuk kaki dengan jarak 7,62 mm lalu solder dari bawah.',
'<b>2.</b> Pasang C1 dan C3 (tanpa polaritas), lalu LED D1/D2. Katoda LED adalah sisi pipih/kaki pendek dan masuk pad 1; anoda masuk pad 2. Gunakan mode diode multimeter bila kaki sudah dipotong.',
'<b>3.</b> Pasang header J1-J6 tegak lurus, kemudian C2. Garis minus pada badan C2 menuju pad 2; kaki positif menuju pad 1. Potong sisa kaki setelah solder dingin.',
'<b>4.</b> Bersihkan residu sesuai jenis flux. Jangan memasang NodeMCU atau sensor sebelum pemeriksaan listrik pada halaman 6.'] :para(t)
new('3. Kabel sensor dan NodeMCU','Warna memudahkan pemasangan; label pin tetap menjadi acuan utama.')
pic('02_Diagram_Kabel.png',555)
para('Jangan mengikuti urutan fisik pin pada ilustrasi: diagram ini sengaja memakai label fungsi karena modul klon berbeda. DO MQ-135 tidak dipakai. J2 menuju sensor MQ-135; J3, J4, J6 menuju NodeMCU; J5 menuju DHT11.')
para('<b>Penting:</b> jangan menukar D2 NodeMCU (DATA DHT11) dengan komponen D2 PCB (LED merah). Pin 3V3 NodeMCU memberi daya pada J4.1 dan sensor DHT11; jangan hubungkan ke 5 V.')
new('4. Daya dan pemasangan pada alas')
pic('04_Distribusi_Daya.png',310)
for t in ['<b>1.</b> Adaptor 5 V memiliki dua cabang: ke J1.1/J1.2 PCB dan ke input VIN/GND NodeMCU yang sudah diverifikasi. Gunakan sambungan yang kuat dan berisolasi. Jangan mengandalkan VIN sebagai keluaran 5 V dari USB.',
'<b>2.</b> Untuk upload melalui USB laptop, lepaskan kedua cabang suplai adaptor. MQ-135 tidak harus menyala saat upload. Lepaskan USB laptop sebelum kembali memberi daya adaptor.',
'<b>3.</b> Buat alas 200 x 150 mm. Posisi usulan: DHT11 x10 y12; MQ-135 x163 y12; NodeMCU x10 y77; PCB x65 y72 mm. Koordinat dari pojok kiri atas alas. Area/ukuran modul pada gambar bersifat nominal; ukur barang aktual.',
'<b>4.</b> Jepit PCB dengan klip tepi isolasi, beri ruang 8-10 mm di bawah solder. Pasang modul dengan lubang bawaannya jika tersedia atau klip yang tidak menyentuh kaki. Jangan menutup sensor MQ dengan lem atau busa.',
'<b>5.</b> Letakkan sensor pada sisi berlawanan agar jarak >100 mm. MQ-135 menghasilkan panas. DHT11 harus mendapat aliran udara bebas. Arahkan antena NodeMCU menjauhi logam; beri akses USB dan beri penahan tarikan kabel.'
]:para(t)
new('5. Pemeriksaan sebelum menyalakan')
for t in [
'<b>A. Tanpa daya, sensor dan MCU dilepas.</b> Periksa konektivitas: J1.1-J2.1; J1.2 ke semua GND; J4.1-J5.1; J4.2-J5.2; J3.1 ke titik temu R1/R2/C1. Gunakan tabel pin dan netlist. Jangan menganggap bunyi continuity harus muncul melintasi resistor 47 kohm.',
'<b>B. Pastikan tidak ada hubung singkat.</b> Periksa 5 V-GND dan 3V3-GND. Elko dapat membuat pembacaan resistansi berubah sesaat; tahan probe sampai stabil. Hentikan jika ada resistansi mendekati nol yang menetap.',
'<b>C. Catu PCB saja.</b> Beri 5 V teratur ke J1. Dengan probe hitam di J1.2, ukur J2.1 sekitar 5 V. C2 tidak boleh terbalik. Matikan daya sebelum mengubah kabel.',
'<b>D. Uji pembagi analog.</b> Lepas MQ-135 dan NodeMCU. Hubungkan sumber uji 5 V teratur ke J2.3, GND sumber ke J1.2. Ukur J3.1 sekitar 0,88 V terhadap GND dan pastikan <1 V. Setelah selesai, matikan dan lepas sumber/jumper uji. Jangan membiarkan jumper AO-ke-5V terpasang saat memasang MQ.',
'<b>E. Pasang NodeMCU dan sensor.</b> Setelah rangkaian lolos, pasang kabel sesuai diagram dalam keadaan mati. Hidupkan; ukur pin 3V3 NodeMCU dan J5.1 sekitar 3,3 V. Periksa polaritas dan suplai lebih dulu jika ada komponen selain pemanas MQ yang cepat panas.',
'<b>F. Uji fungsi sesudah firmware tersedia.</b> Uji LED hijau di GPIO14 dan merah di GPIO12, DHT di GPIO4, serta ADC A0. Pembacaan LED tidak otomatis bekerja hanya karena kabel dipasang: program harus diunggah.',
'<b>G. Conditioning sensor.</b> MQ-135 memerlukan conditioning awal lebih dari 48 jam menurut Winsen. Tempatkan aman dan berventilasi. Setelah setiap penyalaan, tunggu respons stabil sebelum mengambil baseline. Jangan menyatakan udara aman hanya karena LED hijau.'
]:para(t)
new('6. Urutan demonstrasi dan pemecahan masalah')
for t in ['<b>Demonstrasi:</b> tunjukkan komponen, jalur sensor ke PCB lalu NodeMCU, koneksi Wi-Fi ke HP, dan pembacaan yang berubah. Jelaskan bahwa sistem menggunakan baseline relatif, bukan standar pengukuran AQI. Uji logika alarm memakai nilai simulasi tanpa membuat asap atau melepas gas.',
'<b>NodeMCU mati/restart:</b> periksa 5 V pada input board, kualitas adaptor, kontinuitas ground, dan sambungan kabel. Jangan mengganti input 5 V ke pin 3V3.',
'<b>DHT gagal terbaca:</b> periksa label DATA dan VCC; pastikan modul cocok pada 3,3 V, kabel pendek, dan pustaka memakai DHT11/ GPIO4. Jangan menaikkan catu modul ke 5 V pada desain ini.',
'<b>ADC selalu nol/maksimum:</b> cek AO, jangan DO; ukur pembagi R1/R2; periksa solder; cek ground bersama. Nilai maksimum yang terpakai bisa jauh di bawah 1023 karena pembagi internal NodeMCU, sehingga ambang harus berdasarkan baseline aktual.',
'<b>LED tidak menyala:</b> periksa K/A, nilai 1 kohm, nomor GPIO dan program. LED merah punya reference D2 pada PCB; itu bukan instruksi untuk menghubungkannya ke D2 NodeMCU.',
'<b>HP belum menampilkan data:</b> firmware dan konfigurasi Wi-Fi diperlukan. Paket ini melengkapi desain hardware/perakitan; belum termasuk firmware. Rencana software ada di Rencana_Proyek.html.',
'<b>Catatan hasil:</b> simpan foto rakitan, pengukuran 5 V/3,3 V/ADC uji, hasil continuity, waktu conditioning, data sensor, dan masalah yang ditemukan. Semua ukuran modul harus dicocokkan dengan barang aktual.',
'<b>Referensi teknis:</b> Winsen MQ-135: https://www.winsen-sensor.com/manual/mq135.html<br/>Espressif ESP8266EX: https://documentation.espressif.com/0a-esp8266ex_datasheet_en.html<br/>Adafruit DHT: https://learn.adafruit.com/dht?view=all',
'<b>Belum diverifikasi:</b> KiCad DRC/ERC, ukuran modul aktual, fabrikasi, pengujian listrik fisik, dan firmware. PDF dan gambar adalah petunjuk perakitan Rev A, bukan bukti bahwa perangkat sudah dibuat atau diuji.'
]:para(t)
pdf.save()
cards=''.join(f'<section><h2>{html.escape(t)}</h2><img src="{f}"></section>' for t,f in [('Pemasangan komponen','01_Pemasangan_Komponen.png'),('Kabel pin ke pin','02_Diagram_Kabel.png'),('Dudukan perangkat','03_Desain_Dudukan.png'),('Distribusi daya','04_Distribusi_Daya.png')])
(P/'Panduan_Perakitan.html').write_text('<!doctype html><html lang="id"><meta charset="utf-8"><title>Perakitan UdaraKita</title><style>body{font:17px/1.6 system-ui;max-width:1150px;margin:45px auto;padding:20px;color:#19394b;background:#f3f7fb}img{width:100%}a{color:#087d88}h1{font-size:38px}section{margin:40px 0}</style><h1>UdaraKita / Kelompok 7</h1><p>Panduan pemasangan hardware Rev A. PCB satu sisi, NodeMCU dan sensor menggunakan kabel.</p><p><a href="Panduan_Desain_dan_Perakitan.pdf">Buka panduan PDF 7 halaman</a> · <a href="Rencana_Proyek.html">Rencana dan anggaran</a> · <a href="Kelompok7_Udara.kicad_pcb">File PCB KiCad</a> · <a href="Skema_Rangkaian.svg">Skema listrik</a></p><p>Ikuti label pin barang aktual. Belum diverifikasi di KiCad atau diuji fisik. Firmware belum termasuk.</p>'+cards,encoding='utf-8')
with zipfile.ZipFile(P/'Kelompok7_Udara_Lengkap.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in P.iterdir():
  if f.is_file() and f.suffix!='.zip':z.write(f,f.name)
print('Created assembly PDF:',page,'pages; 4 diagrams, CSV, HTML, complete ZIP.')
