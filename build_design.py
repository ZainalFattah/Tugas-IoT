from pathlib import Path
import math, heapq, random, json, html
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).parent
S=.635
W,H=120,100
parts=[]
def part(ref,value,pads):
    parts.append(dict(ref=ref,value=value,pads=[dict(num=i+1,x=x,y=y,net=n) for i,(x,y,n) in enumerate(pads)]))
part('J1','5V IN',[(10,12,'5V'),(14,12,'GND')])
part('J2','MQ135',[(92,12,'5V'),(96,12,'GND'),(100,12,'MQ_AO')])
part('R1','47k 1%',[(94,30,'MQ_AO'),(82,30,'ADC')])
part('R2','10k 1%',[(82,38,'ADC'),(82,50,'GND')])
part('C1','100nF',[(94,40,'ADC'),(98,40,'GND')])
part('J3','MCU A0/G',[(60,40,'ADC'),(64,40,'GND')])
part('C2','100uF 10V',[(28,16,'5V'),(32,16,'GND')])
part('J4','MCU 3V3/D2/G',[(12,60,'3V3'),(16,60,'DHT'),(20,60,'GND')])
part('J5','DHT11',[(12,84,'3V3'),(16,84,'DHT'),(20,84,'GND')])
part('R3','10k',[(30,64,'3V3'),(30,76,'DHT')])
part('C3','100nF',[(38,82,'3V3'),(42,82,'GND')])
part('J6','MCU D5/D6/G',[(62,62,'D5'),(66,62,'D6'),(70,62,'GND')])
part('R4','1k',[(60,72,'D5'),(60,84,'LED_G')])
part('R5','1k',[(88,72,'D6'),(88,84,'LED_R')])
part('D1','GREEN K/A',[(60,92,'GND'),(64,92,'LED_G')])
part('D2','RED K/A',[(88,92,'GND'),(92,92,'LED_R')])
nets=sorted({p['net'] for c in parts for p in c['pads']})
points={n:[(p['x'],p['y']) for c in parts for p in c['pads'] if p['net']==n] for n in nets}
def near(points,r):
    return {(x+dx,y+dy) for x,y in points for dx in range(-r,r+1) for dy in range(-r,r+1) if dx*dx+dy*dy<=r*r}
padblocks={n:near([p for m in nets if m!=n for p in points[m]],3) for n in nets}
def route(order):
    tracks={}
    for n in order:
        blocked=set(padblocks[n])
        for m,paths in tracks.items(): blocked.update(near([p for path in paths for p in path],2))
        tree={points[n][0]}; paths=[]
        for target in points[n][1:]:
            q=[(0,0,target)]; cost={target:0}; prev={}; end=None
            while q:
                _,g,p=heapq.heappop(q)
                if g!=cost.get(p): continue
                if p in tree: end=p;break
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    v=(p[0]+dx,p[1]+dy)
                    if v in blocked or not(3<=v[0]<=W-3 and 3<=v[1]<=H-3):continue
                    ng=g+1
                    if ng<cost.get(v,1e9):
                        cost[v]=ng;prev[v]=p
                        h=min(abs(v[0]-a)+abs(v[1]-b) for a,b in tree)
                        heapq.heappush(q,(ng+h,ng,v))
            if end is None:return None
            path=[end]
            while path[-1]!=target:path.append(prev[path[-1]])
            paths.append(path);tree.update(path)
        tracks[n]=paths
    return tracks
random.seed(7)
for attempt in range(200):
    order=list(nets);random.shuffle(order)
    tracks=route(order)
    if tracks is not None:break
assert tracks is not None,'Routing failed'
def corners(path):
    return [p for i,p in enumerate(path) if i in (0,len(path)-1) or (p[0]-path[i-1][0],p[1]-path[i-1][1])!=(path[i+1][0]-p[0],path[i+1][1]-p[1])]
segments=[(n,a,b) for n,paths in tracks.items() for path in paths for a,b in zip(corners(path),corners(path)[1:])]
netid={n:i+1 for i,n in enumerate(nets)}
pcb=['(kicad_pcb (version 20221018) (generator pcbnew)','(general (thickness 1.6))','(paper "A4")','(layers (0 "F.Cu" signal) (31 "B.Cu" signal) (36 "B.SilkS" user "b.silkscreen") (37 "F.SilkS" user "f.silkscreen") (38 "B.Mask" user) (39 "F.Mask" user) (44 "Edge.Cuts" user))','(setup (pad_to_mask_clearance 0))','(net 0 "")']
pcb += [f'(net {netid[n]} "{n}")' for n in nets]
for c in parts:
    x,y=c['pads'][0]['x']*S,c['pads'][0]['y']*S
    pcb += [f'(footprint "K7:{c["ref"]}" (layer "F.Cu") (at {x} {y}) (attr through_hole)',f'(fp_text reference "{c["ref"]}" (at 0 -2) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))',f'(fp_text value "{c["value"]}" (at 0 -3.4) (layer "F.Fab") hide (effects (font (size 1 1) (thickness 0.15))))']
    for p in c['pads']:
        pcb.append(f'(pad "{p["num"]}" thru_hole {"rect" if p["num"]==1 else "circle"} (at {p["x"]*S-x:.4f} {p["y"]*S-y:.4f}) (size 1.7 1.7) (drill 0.9) (layers "*.Cu" "*.Mask") (net {netid[p["net"]]} "{p["net"]}"))')
    pcb.append(')')
for n,a,b in segments:pcb.append(f'(segment (start {a[0]*S} {a[1]*S}) (end {b[0]*S} {b[1]*S}) (width 0.5) (layer "B.Cu") (net {netid[n]}))')
for a,b in [((0,0),(W,0)),((W,0),(W,H)),((W,H),(0,H)),((0,H),(0,0))]:pcb.append(f'(gr_line (start {a[0]*S} {a[1]*S}) (end {b[0]*S} {b[1]*S}) (layer "Edge.Cuts") (width 0.05))')
pcb.append('(gr_text "K7 UDARA REV A" (at 38 34) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2))))')
pcb.append(')');(OUT/'Kelompok7_Udara.kicad_pcb').write_text('\n'.join(pcb).replace('(44 "Edge.Cuts" user)', '(44 "Edge.Cuts" user) (49 "F.Fab" user)'))
# Verify connectivity and conservative copper clearance, including square pads.
def dist(p,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1];d=dx*dx+dy*dy
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/d)) if d else 0
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)*S
minclear=100
for n,paths in tracks.items():
    cells={p for path in paths for p in path}; assert all(p in cells for p in points[n])
    visited={next(iter(cells))};todo=list(visited)
    while todo:
        x,y=todo.pop()
        for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if p in cells and p not in visited:visited.add(p);todo.append(p)
    assert cells==visited
for i,(n,a,b) in enumerate(segments):
    for c in parts:
        for p in c['pads']:
            if p['net']!=n:
                clearance=dist((p['x'],p['y']),a,b)-.25-(.85*math.sqrt(2) if p['num']==1 else .85)
                assert clearance>=.25,(n,c['ref'],clearance)
                minclear=min(minclear,clearance)
    for m,c,d in segments[i+1:]:
        if m!=n:
            # Paths live on the grid; crossing orthogonal segments share grid points.
            gap=min(dist(a,c,d),dist(b,c,d),dist(c,a,b),dist(d,a,b))-.5
            assert gap>=.25,(n,m,gap)
            minclear=min(minclear,gap)
report=f'Connected nets: {len(nets)} / {len(nets)}\nTracks: {len(segments)} segments, B.Cu only, 0.50 mm\nMinimum conservative checked clearance: {minclear:.3f} mm\nPads: 1.70 mm, drill 0.90 mm; grid 0.635 mm\nBoard: 76.20 x 63.50 mm\nNo vias. Routing attempt: {attempt+1}\nCustom checks only. KiCad DRC/ERC and physical prototype NOT run.\n'
(OUT/'verification.txt').write_text(report)
(OUT/'netlist.json').write_text(json.dumps(dict(parts=parts,segments=segments,grid_mm=S),indent=2))
# Human-readable vector layout plus a PNG preview, both top/component view.
scale=10; margin=65
im=Image.new('RGB',(int(W*S*scale+2*margin),int(H*S*scale+2*margin+70)), '#f3f6fa');dr=ImageDraw.Draw(im)
fontpath='C:/Windows/Fonts/arial.ttf'
f=ImageFont.truetype(fontpath,14);big=ImageFont.truetype(fontpath,25)
def xy(x,y):return margin+x*S*scale,margin+y*S*scale
dr.rounded_rectangle((margin,margin,*xy(W,H)),radius=12,fill='#123c3c',outline='#0c2525',width=3)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="76.2mm" height="63.5mm" viewBox="0 0 76.2 63.5"><rect width="76.2" height="63.5" fill="#123c3c"/>']
for n,a,b in segments:
    dr.line([xy(*a),xy(*b)],fill='#ea995c',width=5)
    svg.append(f'<path d="M {a[0]*S},{a[1]*S} L {b[0]*S},{b[1]*S}" stroke="#ea995c" stroke-width="0.5"/>')
for c in parts:
    if c['ref'].startswith(('R','C','D')):
        dr.line([xy(c['pads'][0]['x'],c['pads'][0]['y']),xy(c['pads'][1]['x'],c['pads'][1]['y'])],fill='#ddece6',width=2)
    for p in c['pads']:
        x,y=xy(p['x'],p['y']);r=8.5
        fn=dr.rectangle if p['num']==1 else dr.ellipse
        fn((x-r,y-r,x+r,y+r),fill='#ffd87c');dr.ellipse((x-4,y-4,x+4,y+4),fill='#10292c')
        svg.append(f'<circle cx="{p["x"]*S}" cy="{p["y"]*S}" r="0.85" fill="#ffd87c"/><circle cx="{p["x"]*S}" cy="{p["y"]*S}" r="0.45" fill="#10292c"/>')
    p=c['pads'][0];x,y=xy(p['x'],p['y'])
    dr.text((x-8,y-31),c['ref']+' '+c['value'],font=f,fill='white')
    svg.append(f'<text x="{p["x"]*S-1}" y="{p["y"]*S-2}" font-family="sans-serif" font-size="1.2" fill="white">{html.escape(c["ref"]+" "+c["value"])}</text>')
dr.text((margin,15),'KELOMPOK 7 | UDARA',font=big,fill='#173b4b')
dr.text((margin,xy(0,H)[1]+16),'76.2 x 63.5 mm | Tampak atas | Jalur tembaga di bawah',font=f,fill='#173b4b')
dr.text((margin,xy(0,H)[1]+38),'REV A - Periksa di KiCad dan uji prototipe sebelum produksi',font=f,fill='#173b4b')
im.save(OUT/'Preview_PCB.png');svg.append('</svg>');(OUT/'Layout_PCB.svg').write_text('\n'.join(svg))
print(report)
