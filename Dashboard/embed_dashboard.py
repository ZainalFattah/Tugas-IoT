from pathlib import Path
p=Path(__file__).resolve().parent
html=(p/'index.html').read_text(encoding='utf-8')
assert ')UDARAKITA"' not in html
(p.parent/'Firmware/UdaraKita/Dashboard.h').write_text('#pragma once\n#include <pgmspace.h>\nconst char DASHBOARD_HTML[] PROGMEM = R"UDARAKITA('+html+')UDARAKITA";\n',encoding='utf-8')
print('Dashboard embedded:',len(html.encode()),'bytes')
