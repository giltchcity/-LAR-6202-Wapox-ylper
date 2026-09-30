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
W, H = 16.0, 10.2
fig = plt.figure(figsize=(W / 2.54, H / 2.54), dpi=300)
ax = fig.add_axes([0, 0, 1, 1], xlim=(0, W), ylim=(0, H), aspect="equal")
ax.axis("off")
C = {
    "ink": "#233440", "muted": "#657580", "grid": "#DCE2E6",
    "blue": "#376D98", "bluefill": "#A8C5DA", "pale": "#E8F0F6",
    "teal": "#37857A", "tealfill": "#C3DDD3",
    "orange": "#B76535", "orangefill": "#F2CEAF",
    "white": "#FFFFFF", "gate": "#F2F5F7", "source": "#D4DDE4",
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

def panel(x, y, width, letter, title):
    text(x,y,letter,9,"left",bold=True)
    text(x+.50,y,title,8.6,"left",bold=True)
    line([(x,y-.31),(x+width,y-.31)],"grid",.6)

def bezier_arrow(p0,p1,p2,p3,color="blue",width=.7):
    points=[]
    for i in range(65):
        t=i/64
        points.append(tuple((1-t)**3*p0[k]+3*(1-t)**2*t*p1[k]
                            +3*(1-t)*t*t*p2[k]+t**3*p3[k] for k in (0,1)))
    arrow(points,color,width,True)

panel(.10,9.82,7.65,"(a)","Observation association")
panel(8.10,9.82,7.80,"(b)","Component-aware clustering")
panel(.10,5.88,15.80,"(c)","Source-supported TSDF reconstruction")

# (a) The range samples are displayed after applying their old keyframe poses.
v=(4.05,7.77)
cams=[(.45,8.94),(.45,7.78),(.45,6.57)]
fractions=[.925,.92,.47]
samples=[tuple(k[j]+f*(v[j]-k[j]) for j in (0,1))
         for k,f in zip(cams,fractions)]
surface=[(4.17,6.52),(3.98,7.10),v,(4.22,8.45),(4.13,9.10)]
line(surface,"ink",1.15)
for i,(k,m) in enumerate(zip(cams,samples)):
    color="blue" if i<2 else "orange"
    line([k,v],"muted",.5,True)
    line([k,m],color,.85)
    camera(*k,v)
    text(k[0]+.01,k[1]+.28,f"$K_{i+1}$",8.3)
    if i<2:
        circle(*m,.055,"blue","blue",.3)
    else:
        cross(*m)
circle(*v,.045,"ink","ink",.4)
text(v[0]+.24,v[1]-.13,r"$v_j^-$",8.7,"left")
text(4.11,9.28,r"$\mathcal{M}^-$",9)
text(samples[0][0]-.05,samples[0][1]+.28,r"$m_1$",8,color="blue")
text(samples[1][0]-.10,samples[1][1]-.28,r"$m_2$",8,color="blue")
text(samples[2][0]+.03,samples[2][1]-.29,r"$m_3$",8,color="orange")
circle(5.17,8.83,.05,"blue","blue",.4)
text(5.37,8.83,"Retained observation",7.5,"left")
cross(5.17,8.33,.05)
text(5.37,8.33,"Rejected observation",7.5,"left")
text(6.40,7.59,r"$\delta_{rj}\leq g_0+g_1z_{rj}^-$",8)
text(6.38,7.01,"Multiple keyframes,",7.7)
text(6.38,6.66,"one surface vertex.",7.7)
text(3.96,6.30,"Old poses establish observation support",7.5,color="muted")

# (b) A spatial cell may contain different connected components.
x0=8.43
cx,cy,cw,ch=9.72,6.63,2.02,2.19
line([(cx,cy),(cx+cw,cy),(cx+cw,cy+ch),(cx,cy+ch),(cx,cy)],
     "muted",.65,True)
text(cx+cw/2,9.13,"One spatial cell",7.4)
xs=[.15,.79,1.42,2.00,2.61,3.22,3.92,4.65]
for mid,color,phase in [(8.23,"blue",0),(7.12,"teal",1.4)]:
    upper=[(x0+x,mid+.18+.08*math.sin(1.6*x+phase)) for x in xs]
    lower=[(x0+x,mid-.18+.08*math.sin(1.6*x+phase)) for x in xs]
    polygon(upper+lower[::-1],"white",color,.55)
    for i in range(len(xs)):
        line([upper[i],lower[i]],color,.4)
        if i+1<len(xs):
            line([lower[i],upper[i+1]],color,.4)
        for p in (upper[i],lower[i]):
            circle(*p,.024,color,color,.2)
    xp=cx+cw/2
    yp=mid+.08*math.sin(1.6*(xp-x0)+phase)
    circle(xp,yp,.105,"white",color,1.2)
    text(xp+.27,yp+.32,r"$p_A^-$" if color=="blue" else r"$p_B^-$",
         8.5,"left",color)
line([(13.73,8.23),(13.99,8.23)],"blue",1.0)
text(14.11,8.23,"Component A",7.4,"left")
line([(13.73,7.74),(13.99,7.74)],"teal",1.0)
text(14.11,7.74,"Component B",7.4,"left")
circle(13.87,7.13,.083,"white","ink",1)
text(14.11,7.13,"Proxy vertex",7.4,"left")
text(12.04,6.30,"One proxy vertex per (cell, component) pair",7.5,color="muted")

# (c) An explicit planar local example. All positions use one paired frame map.
# The 2-D weight field represents a slice constant in its third coordinate.
# This is a geometric schematic, not an experimental reconstruction.
s=.32
rho,tau=1.5*s,4*s
sgx,tgx,gy=.35,5.52,2.25
snx,tnx,ny=10,14,9
qm=(1.55,3.80)
qp=(7.28,3.69)
angle=math.radians(25)
nm=(math.cos(angle),-math.sin(angle))
tm=(math.sin(angle),math.cos(angle))

def source_uv(p):
    d=(p[0]-qm[0],p[1]-qm[1])
    return sum(d[i]*nm[i] for i in (0,1)),sum(d[i]*tm[i] for i in (0,1))

def pullback(p):
    u,v=p[0]-qp[0],p[1]-qp[1]
    return tuple(qm[i]+u*nm[i]+v*tm[i] for i in (0,1))

def forward(p):
    u,v=source_uv(p)
    return qp[0]+u,qp[1]+v

def source_center(ix,iy):
    return sgx+(ix+.5)*s,gy+(iy+.5)*s

def source_weight(ix,iy):
    u,v=source_uv(source_center(ix,iy))
    observed=(-tau<=u<=tau+3*s) and not (u>.34 and v<-.60)
    return 8.0 if observed else 0.0

def source_sample(p):
    # Valid interpolation is attempted first; otherwise use the containing voxel.
    zx,zy=(p[0]-sgx)/s-.5,(p[1]-gy)/s-.5
    ix,iy=math.floor(zx),math.floor(zy)
    fx,fy=zx-ix,zy-iy
    taps=[(ix+a,iy+b,((fx if a else 1-fx)*(fy if b else 1-fy)))
          for a in (0,1) for b in (0,1)]
    taps=[t for t in taps if t[2]>1e-10]
    valid=all(source_weight(a,b)>0 for a,b,c in taps)
    if valid:
        return True,sum(c*source_weight(a,b) for a,b,c in taps)
    return False,source_weight(math.floor((p[0]-sgx)/s),
                               math.floor((p[1]-gy)/s))

classes={}
for iy in range(ny):
    for ix in range(tnx):
        p=(tgx+(ix+.5)*s,gy+(iy+.5)*s)
        r=abs(p[0]-qp[0])
        cls="unknown"
        if r<=tau+1e-9:
            old=pullback(p)
            valid,w=source_sample(old)
            old_q=pullback((qp[0],p[1]))
            probes=[tuple(old_q[k]+direction*s*nm[k] for k in (0,1))
                    for direction in (-1,1)]
            orientation=all(source_sample(probe)[0] for probe in probes)
            if w>0 and (not valid or orientation or r<=rho):
                cls="narrow" if r<=rho else "extended"
            elif w<=0 and r<rho:
                cls="fallback"
        classes[ix,iy]=cls

# Keep extended samples connected to near-surface support.
seen={p for p,c in classes.items() if c in ("narrow","fallback")}
queue=list(seen)
while queue:
    ix,iy=queue.pop()
    for p in ((ix-1,iy),(ix+1,iy),(ix,iy-1),(ix,iy+1)):
        if p not in seen and classes.get(p)=="extended":
            seen.add(p)
            queue.append(p)
for p,c in list(classes.items()):
    if c=="extended" and p not in seen:
        classes[p]="unknown"

# Observed free space is transported forward, writing into unsupported voxels.
for sy in range(-8,20):
    for sx in range(-8,24):
        old=source_center(sx,sy)
        u,v=source_uv(old)
        if source_weight(sx,sy)<=0 or u<rho:
            continue
        dest=forward(old)
        ix,iy=math.floor((dest[0]-tgx)/s),math.floor((dest[1]-gy)/s)
        if classes.get((ix,iy))!="unknown":
            continue
        has_negative=any(classes.get((ix+dx,iy+dy),"unknown")!="unknown"
                         and tgx+(ix+dx+.5)*s<qp[0]
                         for dx in (-1,0,1) for dy in (-1,0,1))
        if not has_negative:
            classes[ix,iy]="free"

# Source volume: shaded voxels have positive source weight.
for iy in range(ny):
    for ix in range(snx):
        old=source_center(ix,iy)
        u,_=source_uv(old)
        fill="white"
        if source_weight(ix,iy)>0:
            fill="tealfill" if u>tau else "source"
        rect(sgx+ix*s,gy+iy*s,s,s,fill,"grid",.30)

# Corrected volume: weight provenance is color, distance is a boundary.
fills={"unknown":"white","narrow":"bluefill","extended":"bluefill",
       "fallback":"orangefill","free":"tealfill"}
for iy in range(ny):
    for ix in range(tnx):
        rect(tgx+ix*s,gy+iy*s,s,s,fills[classes[ix,iy]],"grid",.30)

old_line=[]
for y in (gy-.04,gy+ny*s+.04):
    v=(y-qm[1])/tm[1]
    old_line.append((qm[0]+v*tm[0],y))
line(old_line,"ink",1.2)
line([(qp[0],gy-.04),(qp[0],gy+ny*s+.04)],"ink",1.2)
for bound,color in ((rho,"blue"),(tau,"muted")):
    for direction in (-1,1):
        xx=qp[0]+direction*bound
        line([(xx,gy),(xx,gy+ny*s)],color,.45,True)

text(1.96,5.36,r"Source TSDF $(\Phi^-,w^-)$",8)
text(7.76,5.36,"Corrected TSDF",8)
text(1.82,4.94,r"$\bar{\mathcal{M}}^-$",8.8)
text(6.99,4.95,r"$\mathcal{M}^+$",8.8)
text(.63,4.91,"$-$",8.5,color="muted")
text(3.27,4.91,"$+$",8.5,color="muted")
text(5.79,4.91,"$-$",8.5,color="muted")
text(9.77,4.91,"$+$",8.5,color="muted")

# Explicit paired positions: x is an output voxel centre; x^- is its query.
x=(tgx+7.5*s,gy+4.5*s)
xm=pullback(x)
assert math.dist(x,qp)>rho and source_sample(xm)[1]>0
assert abs(math.dist(x,qp)-math.dist(xm,qm))<1e-12
assert math.dist(forward(xm),x)<1e-12
assert classes[6,1]=="fallback"
bezier_arrow(x,(6.25,4.97),(4.45,4.97),xm,"blue",.75)
text(4.47,4.94,r"$x^-=\Psi_f(x)$",8.2)
for q,p in ((qm,xm),(qp,x)):
    arrow([q,p],"ink",.95)
    circle(*q,.041,"ink","ink",.4)
    circle(*p,.052,"blue","blue",.4)
text(qm[0]-.24,qm[1]+.10,r"$q^-$",8.7)
text(xm[0]+.26,xm[1]-.10,r"$x^-$",8.7)
text(1.90,3.90,r"$r$",8.7)
text(qp[0]-.26,qp[1]-.25,r"$q^+$",8.7)
text(x[0]+.18,x[1]-.16,r"$x$",8.7)
text((qp[0]+x[0])/2,qp[1]+.25,r"$r$",8.7)
text(4.48,3.25,"Paired surface",7.4)
text(4.48,2.94,"frames",7.4)

# A secondary query grounds the fallback patch in the same source geometry.
fb=(tgx+6.5*s,gy+1.5*s)
fbm=pullback(fb)
assert source_sample(fbm)[1]==0 and abs(fb[0]-qp[0])<rho
bezier_arrow(fb,(6.0,2.35),(3.4,2.35),fbm,"orange",.65)
circle(*fbm,.045,"white","orange",.8)
circle(*fb,.043,"orange","orange",.4)
text(4.48,2.13,r"$w_{\rm src}^{+}=0$",7.8,color="orange")

text(1.95,1.99,r"Shaded source voxels: $w^->0$",7.4)
text(2.26,1.56,"Offset length preserved",7.4)
text(2.26,1.12,r"$\|x^- - q^-\|=\|x-q^+\|$",8.5)
dimension(qp[0],qp[0]+rho,2.01,r"$\rho$",1.85)
dimension(qp[0],qp[0]+tau,1.59,r"$\tau$",1.43)
text(7.72,1.02,r"$|\Phi^+(x)|=\min(\tau,r)$",8.5)

# The purpose of reconstruction: carry a distance--weight state into fusion.
arrow([(10.18,4.36),(11.52,4.36)],"ink",.85)
text(13.42,4.38,r"$(\Phi^+,w^+)$",12)
text(13.42,3.89,"Corrected native TSDF",8.3)
arrow([(13.42,3.58),(13.42,3.21)],"ink",.75)
text(13.42,2.83,r"$\Phi_{\rm next}=\operatorname{clip}_{\tau}\!\left(\frac{w^+\Phi^+ + \omega d}{w^+ + \omega}\right)$",9)
text(13.42,2.14,"Continue weighted fusion",8.2)
text(13.42,1.72,r"Next measurement: $(d,\omega)$",7.3,color="muted")

# Three supported output classes; narrow / extended subdivide transferred support.
swatch(.36,.50,"bluefill","Transferred support",7.5)
swatch(4.55,.50,"orangefill","Geometric fallback",7.5)
swatch(8.88,.50,"tealfill","Transported free space",7.5)
swatch(13.66,.50,"white","Unobserved",7.5)

tex.append(r"\end{tikzpicture}")
(OUT/"mechanisms.tikz").write_text("\n".join(tex)+"\n",encoding="utf-8")
fig.savefig(OUT/"mechanisms.svg",metadata={"Date":None})
svg=(OUT/"mechanisms.svg").read_text(encoding="utf-8")
(OUT/"mechanisms.svg").write_text("\n".join(t.rstrip() for t in svg.splitlines())+"\n",
                                encoding="utf-8")
fig.savefig(OUT/"mechanisms.png",dpi=320)
plt.close(fig)
print("Wrote mechanisms.tikz, mechanisms.svg, mechanisms.png")
print("Verified paired offsets, inverse mapping, and illustrated fallback condition.")
