from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,csv
p=Path(__file__).parent
im=Image.new('RGB',(1500,1130),'#f3f6f3');d=ImageDraw.Draw(im)
def f(size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
def text(x,y,t,size=24,color='#153d38',bold=False):d.text((x,y),t,font=f(size,bold),fill=color)
def card(x,y,w,h,title,pin):
 d.rounded_rectangle((x,y,x+w,y+h),18,fill='white',outline='#dce6dc',width=2)
 text(x+22,y+16,title,23,bold=True);text(x+w-60,y+20,pin,17,'#71897b')
text(55,35,'UDARAKITA / DASHBOARD BLYNK',36,bold=True)
text(55,90,'Rancangan susunan widget · konfigurasi manual di Blynk.Console',22)
text(55,125,'Ilustrasi, bukan screenshot akun atau data sensor nyata.',19,'#8d6844')
for x,title,pin,color,unit in [(55,'Suhu','V0','#226849','°C'),(525,'Kelembapan','V1','#297ace','%RH'),(995,'Respons Gas','V2','#b58300','ADC')]:
 card(x,180,450,190,title,pin)
 text(x+25,247,'—',55,color,True);text(x+130,280,unit,26,color)
 text(x+25,325,'Label / Gauge',18,'#71897b')
card(55,395,900,350,'Tren respons gas','V2')
for y in [475,535,595,655]:d.line((90,y,920,y),fill='#e7ede7',width=2)
pts=[(90+i*830/120,595-35*math.sin(i*.12)-15*math.cos(i*.23)) for i in range(121)]
d.line(pts,fill='#51865e',width=4)
text(85,700,'Chart single datastream · garis ilustrasi',18,'#71897b')
for y,title,pin,unit in [(395,'Rasio terhadap baseline','V3','× / -1 = belum tersedia'),(515,'Baseline ADC','V7','ADC / -1 = belum diambil'),(635,'Waktu menyala','V8','detik')]:
 card(980,y,465,110,title,pin);text(1000,y+62,unit,19,'#71897b')
card(55,770,1390,105,'Status alat & validitas sensor','V4')
text(80,825,'Label lebar: conditioning / warming / baseline_required / calibrating / normal / elevated / sensor_error',19)
for x,title,pin in [(55,'Conditioning sudah >48 jam','V5'),(765,'Ambil baseline · 60 detik','V6')]:
 card(x,900,680,115,title,pin)
 text(x+25,960,'Button Push / Switch yang di-reset firmware',19,'#71897b')
text(55,1050,'Warna saran: hijau #226849 · biru #297ACE · kuning #B58300',21)
text(55,1088,'Kelompok 7: Zainal Fattah · Naufal Adani · Aisyha N A',20)
im.save(p/'Rancangan_Blynk.png')
rows=[['V0','Suhu','Double',0,50,0,'C'],['V1','Kelembapan','Double',0,100,0,'%RH'],['V2','Respons Gas','Double',0,1023,0,'ADC'],['V3','Rasio Baseline','Double',-1,400,-1,'ratio'],['V4','Status Alat','String','','','Menunggu perangkat',''],['V5','Konfirmasi Conditioning','Integer',0,1,0,'command'],['V6','Ambil Baseline','Integer',0,1,0,'command'],['V7','Baseline ADC','Double',-1,1023,-1,'ADC'],['V8','Waktu Menyala','Integer',0,4294967,0,'seconds']]
with (p.parent/'Datastream_Blynk.csv').open('w',newline='',encoding='utf-8-sig') as out:
 w=csv.writer(out);w.writerow(['Virtual Pin','Name','Type','Min','Max','Default','Unit']);w.writerows(rows)
print('Blynk layout and manual datastream reference CSV created (not a Blynk import file).')
