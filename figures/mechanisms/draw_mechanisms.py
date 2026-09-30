"""Publication vector schematic: one scene generates TikZ, SVG, and PNG."""
from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon

OUT = Path(__file__).resolve().parent
plt.rcParams.update({
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "svg.fonttype": "none", "svg.hashsalt": "warpvox-mechanisms",
    "savefig.facecolor": "white",
})
W, H = 16.0, 6.9
fig = plt.figure(figsize=(W / 2.54, H / 2.54), dpi=300)
ax = fig.add_axes([0, 0, 1, 1], xlim=(0, W), ylim=(0, H), aspect="equal")
ax.axis("off")
C = {
    "ink": "#233440", "muted": "#657580", "grid": "#DCE2E6",
    "blue": "#376D98", "bluefill": "#A8C5DA", "pale": "#E8F0F6",
    "teal": "#37857A", "tealfill": "#C3DDD3",
    "orange": "#B76535", "orangefill": "#F2CEAF",
    "white": "#FFFFFF", "gate": "#F2F5F7",
}
tex = [r"\begin{tikzpicture}[x=1cm,y=1cm,line cap=round,line join=round]",
       rf"\path[use as bounding box] (0,0) rectangle ({W},{H});"]
for name, value in C.items():
    tex.append(rf"\definecolor{{wv{name}}}{{HTML}}{{{value[1:]}}}")

def pt(p):
    return f"({p[0]:.4f},{p[1]:.4f})"

def line(points, color="ink", width=.65, dashed=False):
    ax.plot(*zip(*points), color=C[color], lw=width,
            ls=(0, (3, 2.5)) if dashed else "-", solid_capstyle="round")
    opt = f"draw=wv{color},line width={width}pt" + (",dashed" if dashed else "")
    tex.append("\\draw[" + opt + "] " + " -- ".join(map(pt, points)) + ";")

def rect(x, y, w, h, fill="white", edge="grid", width=.35):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=C[fill], edgecolor=C[edge], lw=width))
    tex.append(rf"\draw[fill=wv{fill},draw=wv{edge},line width={width}pt] "
               rf"{pt((x,y))} rectangle {pt((x+w,y+h))};")

def circle(x, y, r, fill="white", edge="ink", width=.7, dashed=False):
    ax.add_patch(Circle((x, y), r, facecolor=C[fill], edgecolor=C[edge], lw=width,
                        linestyle=(0, (3, 2.5)) if dashed else "-"))
    opt = f"fill=wv{fill},draw=wv{edge},line width={width}pt"
    if dashed:
        opt += ",dashed"
    tex.append(rf"\draw[{opt}] {pt((x,y))} circle ({r:.4f});")

def polygon(points, fill="white", edge="ink", width=.7):
    ax.add_patch(Polygon(points, facecolor=C[fill], edgecolor=C[edge], lw=width))
    tex.append(f"\\draw[fill=wv{fill},draw=wv{edge},line width={width}pt] "
               + " -- ".join(map(pt, points)) + " -- cycle;")

def text(x, y, value, size=8, align="center", color="ink", bold=False):
    ax.text(x, y, value, fontsize=size, ha=align, va="center", color=C[color],
            weight="bold" if bold else "normal")
    anchor = {"left": "west", "right": "east", "center": "center"}[align]
    font = rf"\fontsize{{{size}}}{{{size+1}}}\selectfont" + (r"\bfseries" if bold else "")
    tex.append(rf"\node[anchor={anchor},inner sep=0pt,text=wv{color},font={{{font}}}]"
               rf" at {pt((x,y))} {{{value}}};")

def arrow(points, color="ink", width=.7, dashed=False):
    line(points, color, width, dashed)
    p, q = points[-2:]
    angle = math.atan2(q[1]-p[1], q[0]-p[0])
    length, half = .11, .045
    c, s = math.cos(angle), math.sin(angle)
    polygon([q, (q[0]-length*c+half*s, q[1]-length*s-half*c),
             (q[0]-length*c-half*s, q[1]-length*s+half*c)], color, color, .2)

def cross(x, y, r=.065, color="orange"):
    line([(x-r,y-r),(x+r,y+r)],color,1.2)
    line([(x-r,y+r),(x+r,y-r)],color,1.2)

def camera(x, y, target):
    angle = math.atan2(target[1]-y,target[0]-x)
    c,s = math.cos(angle),math.sin(angle)
    polygon([(x+c*u-s*v,y+s*u+c*v)
             for u,v in [(-.15,-.115),(.16,0),(-.15,.115)]])

def swatch(x, y, fill, label, size=7.3):
    rect(x,y-.07,.14,.14,fill,"muted",.3)
    text(x+.22,y,label,size,"left")

def dimension(x1, x2, y, label, label_y):
    line([(x1,y),(x2,y)],"muted",.55)
    for x in (x1,x2):
        line([(x,y-.055),(x,y+.055)],"muted",.55)
    text((x1+x2)/2,label_y,label,8)

def panel(x, width, letter, title):
    text(x,6.53,letter,9,"left",bold=True)
    text(x+.49,6.53,title,8.6,"left",bold=True)
    line([(x,6.22),(x+width,6.22)],"grid",.6)

panel(.10,4.15,"(a)","Observation association")
panel(4.55,4.10,"(b)","Proxy clustering")
panel(8.95,6.94,"(c)","TSDF support")

# (a) Two accepted observations and one rejected return for a source vertex.
v = (3.35,3.85)
cams = [(.40,5.40),(.40,3.78),(.40,2.08)]
fractions = [.93,.91,.46]
samples = [tuple(k[i]+f*(v[i]-k[i]) for i in range(2))
           for k,f in zip(cams,fractions)]
circle(*v,.40,"gate","muted",.55,True)
surface = [(3.54,2.05),(3.46,2.45),(3.28,3.10),v,(3.51,4.62),(3.42,5.70)]
line(surface,"ink",1.15)
for i,(k,m) in enumerate(zip(cams,samples)):
    color = "blue" if i<2 else "orange"
    line([k,v],"muted",.5,True)
    line([k,m],color,.85)
    camera(*k,v)
    text(k[0],k[1]+.30,f"$K_{i+1}$",8.3)
    if i<2:
        circle(*m,.055,"blue","blue",.3)
    else:
        cross(*m)
text(samples[0][0]-.06,samples[0][1]+.32,"$m_1$",8.1,color="blue")
text(samples[1][0]-.25,samples[1][1]-.30,"$m_2$",8.1,color="blue")
text(samples[2][0]+.07,samples[2][1]-.32,"$m_3$",8.1,color="orange")
circle(*v,.042,"ink","ink",.4)
text(v[0]+.24,v[1]-.18,"$v_j^-$",8.7,"left")
text(3.40,5.96,r"$\mathcal{M}^-$",9)
circle(.48,1.47,.05,"blue","blue",.4)
text(.65,1.47,"Retained",7.4,"left")
cross(2.26,1.47,.05)
text(2.43,1.47,"Rejected",7.4,"left")
text(2.14,.92,r"$\|m-\hat v^-\|\leq g_0+g_1z^-$",8)
text(2.14,.39,"Verified surface-to-keyframe links",7.5,color="muted")

# (b) Spatial clustering is separated by connected component.
x0 = 4.60
cell_x,cell_y,cell_w,cell_h = 5.66,2.80,2.00,2.57
line([(cell_x,cell_y),(cell_x+cell_w,cell_y),
      (cell_x+cell_w,cell_y+cell_h),(cell_x,cell_y+cell_h),
      (cell_x,cell_y)],"muted",.65,True)
text(cell_x+cell_w/2,5.72,"One spatial cell",7.4)
xs=[.18,.70,1.24,1.81,2.39,2.95,3.68]
for mid,color,phase in [(4.67,"blue",0),(3.46,"teal",1.4)]:
    upper=[(x0+x,mid+.20+.09*math.sin(1.6*x+phase)) for x in xs]
    lower=[(x0+x,mid-.20+.09*math.sin(1.6*x+phase)) for x in xs]
    polygon(upper+lower[::-1],"white",color,.55)
    for i in range(len(xs)):
        line([upper[i],lower[i]],color,.4)
        if i+1<len(xs):
            line([lower[i],upper[i+1]],color,.4)
        for p in (upper[i],lower[i]):
            circle(*p,.024,color,color,.2)
    xp=cell_x+cell_w/2
    yp=mid+.09*math.sin(1.6*(xp-x0)+phase)
    circle(xp,yp,.105,"white",color,1.2)
    text(xp+.25,yp+.37,"$p_A^-$" if color=="blue" else "$p_B^-$",
         8.6,"left",color)
line([(4.92,1.47),(5.18,1.47)],"blue",1.0)
text(5.30,1.47,"Component A",7.1,"left")
line([(6.95,1.47),(7.21,1.47)],"teal",1.0)
text(7.33,1.47,"Component B",7.1,"left")
text(6.62,.92,"One cell, two proxy vertices",7.8)
text(6.62,.39,"Disconnected surfaces stay separate",7.5,color="muted")

# (c) A and B are equally far from the corrected surface.
# Their paired source queries determine inherited vs geometric support.
s,gx,gy=.30,9.08,2.90
nx,ny=14,9
surface_x=gx+6.5*s
rho,tau=1.5*s,4*s
for iy in range(ny):
    for ix in range(nx):
        r=abs(gx+(ix+.5)*s-surface_x)
        fill="white"
        if r<=tau+1e-8:
            fill="bluefill" if r<=rho+1e-8 else "pale"
        # A local source-support gap on the positive side, inside rho.
        if ix==7 and iy in (3,4):
            fill="orangefill"
        # Transported free space, explicitly distinct from unknown.
        if ix>=11 and iy<=6:
            fill="tealfill"
        rect(gx+ix*s,gy+iy*s,s,s,fill,"grid",.3)
line([(surface_x,gy-.02),(surface_x,gy+ny*s+.03)],"ink",1.2)
text(surface_x,5.88,r"$\mathcal{M}^+$",9)
text(gx+.56,5.87,"$-$",9,color="muted")
text(gx+3.45,5.87,"$+$",9,color="muted")

# Distance boundaries are subordinate to the zero set.
for x in (surface_x-rho,surface_x+rho):
    line([(x,gy),(x,gy+ny*s)],"blue",.5,True)
for x in (surface_x-tau,surface_x+tau):
    line([(x,gy),(x,gy+ny*s)],"muted",.45,True)
dimension(surface_x,surface_x+rho,2.64,r"$\rho$",2.46)
dimension(surface_x,surface_x+tau,2.19,r"$\tau$",2.02)

# Compact query inset: arrows trace Psi, not deformation displacements.
query_x=14.97
text(query_x,5.91,"Source query",7.5)
text(query_x,5.59,r"$x^-=\Psi(x)$",8)
for iy,letter,color,fill in [(7,"A","blue","bluefill"),
                             (4,"B","orange","orangefill")]:
    xx,yy=gx+7*s,gy+iy*s
    rect(xx,yy,s,s,fill,color,1.0)
    text(xx+s/2,yy+s/2,letter,6.5,bold=True)
    y=yy+s/2
    arrow([(xx+s+.025,y),(query_x-.38,y)],color,.75)
    # A supported patch versus an unsupported patch at the source query.
    qfill="bluefill" if letter=="A" else "white"
    for a in range(2):
        for b in range(2):
            rect(query_x-.27+a*.27,y-.27+b*.27,.27,.27,qfill,"grid",.4)
    circle(query_x-.05,y+.04,.031,color,color,.25)
    text(query_x,y-.43,
         r"$w_{\rm src}^{+}>0$" if letter=="A" else r"$w_{\rm src}^{+}=0$",
         7.9,color=color)

# Legends separate distance-defined subclasses from weight sources.
swatch(9.13,1.47,"bluefill",r"Narrow ($r\leq\rho$)",7.1)
swatch(12.10,1.47,"pale",r"Extended ($\rho<r\leq\tau$)",7.1)
swatch(9.13,.92,"orangefill","Fallback",7.2)
swatch(11.25,.92,"tealfill","Free space",7.2)
swatch(13.70,.92,"white","Unknown",7.2)
text(12.43,.39,"Same distance; different source support",7.5,color="muted")

tex.append(r"\end{tikzpicture}")
(OUT/"mechanisms.tikz").write_text("\n".join(tex)+"\n",encoding="utf-8")
fig.savefig(OUT/"mechanisms.svg",metadata={"Date":None})
# Keep generated vector source stable and whitespace-clean.
svg=(OUT/"mechanisms.svg").read_text(encoding="utf-8")
(OUT/"mechanisms.svg").write_text("\n".join(t.rstrip() for t in svg.splitlines())+"\n",
                                encoding="utf-8")
fig.savefig(OUT/"mechanisms.png",dpi=320)
plt.close(fig)
print("Wrote mechanisms.tikz, mechanisms.svg, mechanisms.png")
