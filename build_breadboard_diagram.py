"""Build a pictorial, electrically labeled breadboard diagram for UdaraKita."""

from html import escape
from pathlib import Path


OUT = Path(__file__).with_name("Skema_Perakitan_Breadboard.svg")
parts = []

INK = "#173047"
MUTED = "#526779"
RED5 = "#e86b3c"
YELLOW3 = "#d79b1a"
GROUND = "#34495e"
ANALOG = "#7955be"
DATA = "#148f83"
GREEN = "#1da46b"
REDLED = "#d84f63"


def add(s):
    parts.append(s)


def rect(x, y, w, h, fill, stroke="none", radius=0, sw=1):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def line(x1, y1, x2, y2, color=INK, width=4, dash=None):
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{dashed}/>')


def path(d, color=INK, width=4):
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')


def circle(x, y, r, fill, stroke="none", sw=1):
    add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def txt(x, y, value, size=20, color=INK, weight=400, anchor="start"):
    add(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')


def pill(x, y, value, color, width=98):
    rect(x, y - 26, width, 34, "#fff", color, 10, 2)
    txt(x + width / 2, y - 3, value, 18, color, 700, "middle")


def resistor(x1, x2, y, value, label, color):
    rect(x1, y - 17, x2 - x1, 34, "#fff", color, 8, 3)
    txt((x1 + x2) / 2, y + 6, value, 17, INK, 700, "middle")
    txt((x1 + x2) / 2, y - 27, label, 17, MUTED, 700, "middle")


def junction(x, y, color):
    circle(x, y, 7, color, "#fff", 2)


def capacitor(x, top, bottom, color_top, label, polarized=False):
    middle = (top + bottom) / 2
    a, b = middle - 8, middle + 8
    line(x, top, x, a, color_top, 5)
    line(x - 18, a, x + 18, a, INK, 4)
    line(x - 18, b, x + 18, b, INK, 4)
    line(x, b, x, bottom, GROUND, 5)
    if polarized:
        txt(x + 23, a - 2, "+", 18, RED5, 700)
    txt(x + 34, middle + 6, label, 17, INK, 700)


def pin(x, y, label, color, side="right"):
    circle(x, y, 9, "#fff", color, 3)
    if side == "right":
        txt(x - 22, y + 7, label, 18, "#fff", 700, "end")
    else:
        txt(x + 20, y + 7, label, 18, INK, 700)


def led(cx, cy, color, name):
    # Each LED has a visible left anode lead and right cathode lead.
    line(cx - 68, cy, cx - 24, cy, color, 5)
    line(cx + 24, cy, cx + 72, cy, GROUND, 5)
    circle(cx, cy, 24, color, INK, 3)
    line(cx - 9, cy + 9, cx + 7, cy - 9, "#fff", 3)
    circle(cx - 24, cy, 5, "#fff", color, 2)
    circle(cx + 24, cy, 5, "#fff", GROUND, 2)
    txt(cx - 125, cy - 23, "anoda (+)", 17, INK, 700)
    txt(cx + 30, cy - 23, "katoda (−)", 17, INK, 700)
    txt(cx + 125, cy + 36, name, 18, INK, 700)


add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1470" role="img" aria-labelledby="title desc">')
add('<title id="title">Peta kabel breadboard UdaraKita Kelompok 7</title>')
add('<desc id="desc">Diagram perakitan NodeMCU ESP8266, MQ-135, DHT11, dua LED, resistor, dan kapasitor C1 C2 C3. Semua sambungan pin dan kedua kaki LED ditampilkan.</desc>')
rect(0, 0, 2000, 1470, "#f3f7f8")
rect(0, 0, 2000, 12, DATA)
txt(70, 68, "UDARAKITA / PETA KABEL BREADBOARD", 39, INK, 800)
txt(72, 105, "Kelompok 7 · NodeMCU V3 ESP8266 · MQ-135 · DHT11 · dua LED · tanpa PCB", 21, MUTED)
rect(1390, 38, 535, 73, "#e1f6ee", "#a3ddc7", 17, 2)
txt(1420, 68, "Wi-Fi 2,4 GHz → Blynk.Cloud", 23, "#137b5c", 700)
txt(1420, 94, "Gambar jalur listrik; pilih baris lubang yang setara saat merakit.", 16, MUTED)

# NodeMCU card; pin heights line up with the breadboard circuits.
rect(72, 215, 290, 930, "#183d43", "#102d32", 24, 3)
rect(105, 247, 140, 155, "#112d33", "#72968f", 14, 3)
rect(119, 264, 112, 120, "#0d8178", radius=9)
path("M135 295 H212 M145 322 H216 M150 349 H205", "#d7eea2", 7)
txt(217, 431, "NodeMCU V3", 26, "#fff", 800, "middle")
txt(217, 457, "ESP8266 · ESP-12E · CH340", 15, "#d1e8e5", 400, "middle")
rect(168, 1093, 98, 38, "#c0cfd2", radius=7)
txt(217, 1080, "USB data / 5 V", 17, "#d1e8e5", 400, "middle")
for y, name, color in [
    (300, "VU / 5V*", RED5), (355, "GND", GROUND), (405, "3V3", YELLOW3),
    (600, "A0", ANALOG), (820, "D2", DATA),
    (990, "D5", GREEN), (1080, "D6", REDLED),
]:
    pin(350, y, name, color)

# Breadboard body, lightly marked holes, and clearly separated working zones.
rect(437, 215, 1118, 930, "#fff", "#cfdddf", 24, 3)
txt(465, 248, "BREADBOARD", 26, INK, 800)
txt(1520, 247, "lubang/jalur mengikuti sambungan berwarna", 15, MUTED, 400, "end")
for y0, h in [(265, 215), (510, 230), (765, 150), (950, 170)]:
    rect(468, y0, 1054, h, "#f9fbfa", "#dce7e5", 14, 1)
for yy in [520, 550, 580, 610, 640, 670, 700, 730, 780, 810, 840, 870, 900, 970, 1000, 1030, 1060, 1090]:
    for xx in range(500, 1500, 32):
        circle(xx, yy, 2.5, "#dce5e5")

# Power rails and their two-legged bypass capacitors.
txt(490, 282, "1  REL DAYA", 19, MUTED, 700)
line(350, 300, 1600, 300, RED5, 5)
line(350, 355, 1600, 355, GROUND, 5)
line(350, 405, 1470, 405, YELLOW3, 5)
line(550, 460, 1470, 460, GROUND, 5)
path("M350 355 H1490 V460 H1470", GROUND, 5)
line(1490, 460, 550, 460, GROUND, 5)
pill(515, 288, "+5 V", RED5)
pill(515, 343, "GND", GROUND)
pill(515, 393, "+3V3", YELLOW3)
pill(515, 448, "GND", GROUND)
capacitor(925, 300, 355, RED5, "C2 · 100 µF", True)
capacitor(1120, 405, 460, YELLOW3, "C3 · 100 nF")
txt(840, 384, "C2: + ke 5 V, − ke GND", 16, MUTED)
txt(1065, 489, "C3: 3V3 ke GND", 16, MUTED)

# MQ-135 module. Its power and analog pins each have an actual wire.
rect(1600, 235, 325, 435, "#fff", "#d4e2e6", 24, 3)
txt(1630, 272, "MQ-135", 27, INK, 800)
txt(1630, 296, "modul sensor respons gas", 17, MUTED)
rect(1675, 359, 175, 165, "#aebfc2", "#78949a", 20, 4)
circle(1762, 442, 62, "#708c92", "#466772", 4)
circle(1762, 442, 30, "#e6ece9")
txt(1640, 580, "AO analog", 20, ANALOG, 700)
txt(1640, 325, "VCC 5 V", 18, RED5, 700)
txt(1640, 380, "GND", 18, GROUND, 700)
for yy, color in [(300, RED5), (355, GROUND), (600, ANALOG)]:
    circle(1600, yy, 8, "#fff", color, 3)

# Analog divider: AO--47k--ADC--A0; 10k and C1 both go from ADC to GND.
txt(490, 536, "2  JALUR ANALOG MQ-135", 19, MUTED, 700)
line(350, 600, 1100, 600, ANALOG, 5)
resistor(1100, 1200, 600, "47 kΩ", "R1", ANALOG)
line(1200, 600, 1600, 600, ANALOG, 5)
junction(830, 600, ANALOG)
txt(785, 580, "TITIK ADC", 17, ANALOG, 700)
line(830, 600, 830, 635, ANALOG, 5)
rect(810, 635, 40, 56, "#fff", ANALOG, 8, 3)
txt(830, 669, "10k", 15, INK, 700, "middle")
txt(768, 666, "R2 · 1%", 17, MUTED, 700, "end")
line(830, 691, 830, 715, GROUND, 5)
line(930, 600, 930, 645, ANALOG, 5)
line(909, 645, 951, 645, INK, 4)
line(909, 661, 951, 661, INK, 4)
line(930, 661, 930, 715, GROUND, 5)
line(830, 715, 1020, 715, GROUND, 5)
txt(956, 650, "C1 · 100 nF", 17, INK, 700)
pill(1025, 727, "GND", GROUND)
txt(1160, 726, "C1 dan R2: kedua kaki bawah ke GND", 16, MUTED)

# DHT11: a full three-pin sensor plus its optional pull-up.
txt(490, 788, "3  SENSOR SUHU & KELEMBAPAN", 19, MUTED, 700)
line(350, 820, 1600, 820, DATA, 5)
junction(995, 820, DATA)
line(995, 820, 995, 800, DATA, 5)
rect(975, 770, 40, 30, "#fff", DATA, 8, 3)
txt(995, 791, "10k", 15, INK, 700, "middle")
line(995, 770, 995, 764, YELLOW3, 5)
pill(870, 778, "3V3", YELLOW3, 100)
line(970, 765, 995, 765, YELLOW3, 4)
txt(1030, 797, "R3 · hanya jika modul belum punya pull-up", 16, MUTED)
pill(1360, 758, "3V3", YELLOW3)
line(1458, 770, 1600, 770, YELLOW3, 5)
pill(1360, 858, "GND", GROUND)
line(1458, 870, 1600, 870, GROUND, 5)
rect(1600, 730, 325, 210, "#fff", "#d4e2e6", 24, 3)
rect(1740, 764, 105, 132, "#63bed9", "#318da9", 12, 4)
for y in [787, 819, 851]:
    for x in [1760, 1789, 1818]:
        rect(x, y, 16, 16, "#267da0", radius=2)
txt(1630, 767, "DHT11", 26, INK, 800)
txt(1630, 793, "VCC 3V3", 16, YELLOW3, 700)
txt(1630, 843, "DATA", 16, DATA, 700)
txt(1630, 893, "GND", 16, GROUND, 700)
for yy, color in [(770, YELLOW3), (820, DATA), (870, GROUND)]:
    circle(1600, yy, 8, "#fff", color, 3)

# Two independent LED circuits. The dark cathode return is common GND.
txt(490, 976, "4  DUA LED (MASING-MASING 2 KAKI)", 19, MUTED, 700)
line(350, 990, 665, 990, GREEN, 5)
resistor(665, 755, 990, "1 kΩ", "R4", GREEN)
line(755, 990, 1026, 990, GREEN, 5)
led(1050, 990, GREEN, "LED hijau")
line(1122, 990, 1320, 990, GROUND, 5)
line(350, 1080, 665, 1080, REDLED, 5)
resistor(665, 755, 1080, "1 kΩ", "R5", REDLED)
line(755, 1080, 1026, 1080, REDLED, 5)
led(1050, 1080, REDLED, "LED merah")
line(1122, 1080, 1320, 1080, GROUND, 5)
line(1320, 990, 1320, 1080, GROUND, 5)
junction(1320, 990, GROUND)
junction(1320, 1080, GROUND)
line(1320, 1035, 1360, 1035, GROUND, 5)
pill(1360, 1047, "GND", GROUND)

# Practical wiring key and warnings, outside the circuit area.
rect(72, 1173, 1853, 218, "#193e45", radius=22)
txt(104, 1217, "Cara membaca dan merakit", 25, "#fff", 800)
txt(104, 1255, "● Titik bulat = sambungan. Label 5 V / 3V3 / GND yang sama berarti dihubungkan ke rel dengan nama sama.", 19, "#eaf7f3")
txt(104, 1290, "● LED: D5/D6 → resistor 1 kΩ → anoda (kaki panjang); katoda (kaki pendek/sisi datar) → GND.", 19, "#eaf7f3")
txt(104, 1325, "● C1 dan C3 tidak berpolaritas. C2 adalah elko: kaki + ke 5 V, kaki − ke GND. Pin DO MQ-135 tidak dipakai.", 19, "#eaf7f3")
txt(104, 1360, "*Ukur titik ADC sebelum menghubungkannya ke A0: harus di bawah 1 V. Periksa pin VU/5V pada NodeMCU klon Anda.", 18, "#bfdad3")
txt(76, 1432, "Warna: jingga = 5 V · kuning = 3V3 · biru gelap = GND · ungu = analog · toska = DATA DHT11 · hijau/merah = LED", 18, MUTED)
add('</svg>')

OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(OUT)
try:
    import fitz  # Optional PyMuPDF renderer for an easy-to-share PNG copy.
except ImportError:
    pass
else:
    png = OUT.with_suffix(".png")
    document = fitz.open(OUT)
    document[0].get_pixmap(alpha=False).save(png)
    document.close()
    print(png)
