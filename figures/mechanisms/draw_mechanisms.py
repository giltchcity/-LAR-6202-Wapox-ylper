"""Draw the same vector schematic as TikZ, SVG, and a PNG preview."""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon

OUT = Path(__file__).resolve().parent
plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix',
                     'svg.fonttype': 'none', 'savefig.facecolor': 'white'})
W, H = 16.0, 5.5
fig = plt.figure(figsize=(W / 2.54, H / 2.54), dpi=240)
ax = fig.add_axes([0, 0, 1, 1], xlim=(0, W), ylim=(0, H), aspect='equal')
ax.axis('off')
C = {'ink': '#26343F', 'gray': '#7C8791', 'grid': '#CDD3D8',
     'blue': '#326FA1', 'teal': '#398878', 'orange': '#C67936',
     'pale': '#DCE8F1', 'narrow': '#89B1CF', 'free': '#B7D4C7',
     'fallback': '#EBC497', 'white': '#FFFFFF', 'gate': '#F1F5F8'}
tex = [r'\begin{tikzpicture}[x=1cm,y=1cm,line cap=round,line join=round]',
       rf'\path[use as bounding box] (0,0) rectangle ({W},{H});']
for name, value in C.items():
    tex.append(rf'\definecolor{{wv{name}}}{{HTML}}{{{value[1:]}}}')

def pt(p):
    return f'({p[0]:.4f},{p[1]:.4f})'

def line(points, color='ink', width=.7, dashed=False):
    ax.plot(*zip(*points), color=C[color], lw=width,
            ls=(0, (3, 2.5)) if dashed else '-', solid_capstyle='round')
    opt = f'draw=wv{color},line width={width}pt' + (',dashed' if dashed else '')
    tex.append('\\draw[' + opt + '] ' + ' -- '.join(map(pt, points)) + ';')

def rect(x, y, w, h, fill='white', edge='grid', width=.35, dashed=False):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=C[fill], edgecolor=C[edge],
                          lw=width, linestyle='--' if dashed else '-'))
    opt = f'fill=wv{fill},draw=wv{edge},line width={width}pt'
    if dashed:
        opt += ',dashed'
    tex.append(rf'\draw[{opt}] {pt((x,y))} rectangle {pt((x+w,y+h))};')

def circle(x, y, r, fill='white', edge='ink', width=.7, dashed=False):
    ax.add_patch(Circle((x, y), r, facecolor=C[fill], edgecolor=C[edge],
                        lw=width, linestyle='--' if dashed else '-'))
    opt = f'fill=wv{fill},draw=wv{edge},line width={width}pt'
    if dashed:
        opt += ',dashed'
    tex.append(rf'\draw[{opt}] {pt((x,y))} circle ({r:.4f});')

def polygon(points, fill='white', edge='ink', width=.7):
    ax.add_patch(Polygon(points, facecolor=C[fill], edgecolor=C[edge], lw=width))
    tex.append(f'\\draw[fill=wv{fill},draw=wv{edge},line width={width}pt] '
               + ' -- '.join(map(pt, points)) + ' -- cycle;')

def text(x, y, value, size=8, align='center', color='ink', bold=False):
    ax.text(x, y, value, fontsize=size, ha=align, va='center', color=C[color],
            weight='bold' if bold else 'normal')
    anchor = {'left': 'west', 'right': 'east', 'center': 'center'}[align]
    font = rf'\fontsize{{{size}}}{{{size+1}}}\selectfont' + (r'\bfseries' if bold else '')
    tex.append(rf'\node[anchor={anchor},inner sep=0pt,text=wv{color},font={{{font}}}]'
               rf' at {pt((x,y))} {{{value}}};')

def cross(x, y, r=.09, color='orange'):
    line([(x-r, y-r), (x+r, y+r)], color, 1.3)
    line([(x-r, y+r), (x+r, y-r)], color, 1.3)

def camera(x, y, target):
    angle = math.atan2(target[1]-y, target[0]-x)
    c, s = math.cos(angle), math.sin(angle)
    points = [(x+c*u-s*v, y+s*u+c*v) for u,v in [(-.18,-.15),(.18,0),(-.18,.15)]]
    polygon(points)

# (a) Two rays interrogate the same source vertex. One sample passes the gate.
text(.15, 5.12, '(a) Observation association', 9, 'left', bold=True)
v = (3.60, 2.88)
k1, k2 = (.55, 4.02), (.55, 1.60)
m1 = tuple(k1[i] + .905*(v[i]-k1[i]) for i in range(2))
m2 = tuple(k2[i] + .49*(v[i]-k2[i]) for i in range(2))
circle(*v, .43, 'gate', 'gray', .6, True)
surface = [(3.70,1.62), (3.53,2.12), v, (3.74,3.57), (3.66,4.23)]
line(surface, width=1.1)
for k in [k1, k2]:
    line([k, v], 'gray', .65, True)
line([k1, m1], 'blue', 1.0)
line([k2, m2], 'orange', 1.0)
camera(*k1, v)
camera(*k2, v)
circle(*m1, .075, 'blue', 'blue')
cross(*m2)
circle(*v, .055, 'ink', 'ink')
text(.52, 4.46, '$K_1$', 9)
text(.52, 1.22, '$K_2$', 9)
text(m1[0]-.18, m1[1]+.37, '$m_1$', 9, color='blue')
text(m2[0]+.06, m2[1]-.32, '$m_2$', 9, color='orange')
text(v[0]+.31, v[1]-.25, '$v_j^-$', 9, 'left')
text(3.66, 4.49, 'Source surface', 7.5)
circle(.65, .85, .065, 'blue', 'blue')
text(.84, .85, 'Retained', 7.5, 'left')
cross(2.55, .85, .065)
text(2.75, .85, 'Rejected', 7.5, 'left')
text(2.50, .35, r'Gate: $\|m-\hat v^-\|\leq g_0+g_1z^-$', 8)

# (b) Grid cells group by component as well as position.
o = 5.50
text(o+.05, 5.12, '(b) Component-aware clustering', 9, 'left', bold=True)
rect(o+1.05, 1.57, 2.28, 2.45, 'white', 'gray', .65, True)
text(o+2.19, 4.35, 'One grid cell', 7.5)
xs = [.25,1.05,1.82,2.62,3.4,4.35]
for mid, color, phase in [(3.35,'blue',0),(2.20,'teal',1.5)]:
    upper = [(o+x,mid+.19+.07*math.sin(2*x+phase)) for x in xs]
    lower = [(o+x,mid-.19+.07*math.sin(2*x+phase)) for x in xs]
    polygon(upper+lower[::-1], 'white', color, .6)
    for i in range(len(xs)):
        line([upper[i],lower[i]], color, .45)
        if i+1 < len(xs):
            line([lower[i],upper[i+1]], color, .45)
        for p in [upper[i],lower[i]]:
            circle(*p,.027,color,color,.25)
    y = mid+.07*math.sin(2*2.18+phase)
    circle(o+2.18,y,.105,'white',color,1.15)
    text(o+2.49,y+.39,'$p_A^-$' if color=='blue' else '$p_B^-$',9,'left',color)
line([(o+.34,.85),(o+.62,.85)],'blue',1.2)
text(o+.76,.85,'Component A',7.2,'left')
line([(o+2.57,.85),(o+2.85,.85)],'teal',1.2)
text(o+2.99,.85,'Component B',7.2,'left')
text(o+2.40,.35,'One cell, two proxy vertices.',8)

# (c) A schematic signed-distance slice. Color encodes support, not magnitude.
o = 11.05
text(o+.02,5.12,'(c) TSDF support',9,'left',bold=True)
cell, gx, gy = .4, o+.10, 1.58
for iy in range(7):
    surf_col = 5.5+.6*math.sin(iy/2)
    for ix in range(11):
        d = ix+.5-surf_col
        fill = 'white'
        if abs(d)<=2.05:
            fill='narrow' if abs(d)<=1.05 else 'pale'
        if iy in (2,3) and abs(d)<.85:
            fill='fallback'
        if ix>=8 and iy<=5:
            fill='free'
        rect(gx+ix*cell,gy+iy*cell,cell,cell,fill)
curve=[]
for i in range(57):
    y=i*7/56
    curve.append((gx+cell*(5.5+.6*math.sin((y-.5)/2)),gy+cell*y))
line(curve,'ink',1.1)
text(o+2.45,4.64,r'$\mathcal{M}^+$',9)
text(o+.88,4.64,'$-$',10)
text(o+3.82,4.64,'$+$',10)
def swatch(x,y,fill,label):
    rect(x,y-.075,.15,.15,fill,'gray',.35)
    text(x+.23,y,label,7.1,'left')
swatch(o+.12,1.07,'narrow','Narrow')
swatch(o+1.63,1.07,'pale','Extended')
swatch(o+3.29,1.07,'fallback','Fallback')
swatch(o+.12,.60,'free','Free space')
swatch(o+2.36,.60,'white','Unobserved')

tex.append(r'\end{tikzpicture}')
(OUT/'mechanisms.tikz').write_text('\n'.join(tex)+'\n', encoding='utf-8')
fig.savefig(OUT/'mechanisms.svg')
fig.savefig(OUT/'mechanisms.png', dpi=260)
plt.close(fig)
print('Wrote mechanisms.tikz, mechanisms.svg, mechanisms.png')
