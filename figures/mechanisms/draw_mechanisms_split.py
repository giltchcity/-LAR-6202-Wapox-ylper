"""Three single-column mechanism figures (association, clustering, reconstruction).

Same scenes as draw_mechanisms.py, laid out for one column of the paper
(ieeeconf \\columnwidth = 245.7 pt = 8.64 cm) and included at that width, so font
sizes below are the printed sizes. The reconstruction figure keeps only the two
grids: no equations and no continued-fusion inset. Writes PDF (paper) and PNG
(preview).
"""
from pathlib import Path
import math
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
plt.rcParams.update({
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "savefig.facecolor": "white", "pdf.fonttype": 42,
})
C = {
    "ink": "#233440", "muted": "#657580", "grid": "#DCE2E6",
    "blue": "#376D98", "bluefill": "#A8C5DA", "pale": "#E8F0F6",
    "teal": "#37857A", "tealfill": "#C3DDD3",
    "orange": "#B76535", "orangefill": "#F2CEAF",
    "white": "#FFFFFF", "gate": "#F2F5F7", "source": "#D4DDE4",
}
ax = None
FS = 1.0  # font scale of the current figure
WIDTH_CM = 8.64  # \\columnwidth of ieeeconf
RECON_CM = 6.6   # Fig. 5 width, 0.764\\columnwidth
TXT, NOTE, MATH = 7.5, 7.0, 8.2  # printed font sizes (pt)


def new_figure(x0, x1, y0, y1, width_cm=WIDTH_CM, font_scale=1.0):
    """Figure whose data window [x0,x1]x[y0,y1] (cm) is drawn at width_cm."""
    global ax, FS
    FS = font_scale
    k = width_cm / (x1 - x0)
    fig = plt.figure(figsize=(width_cm / 2.54, (y1 - y0) * k / 2.54))
    ax = fig.add_axes([0, 0, 1, 1], xlim=(x0, x1), ylim=(y0, y1), aspect="equal")
    ax.axis("off")
    return fig


def line(points, color="ink", width=.65, dashed=False):
    ax.plot(*zip(*points), color=C[color], lw=width,
            ls=(0, (3, 2.5)) if dashed else "-", solid_capstyle="round")


def rect(x, y, w, h, fill="white", edge="grid", width=.35):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=C[fill], edgecolor=C[edge], lw=width))


def circle(x, y, r, fill="white", edge="ink", width=.7):
    ax.add_patch(Circle((x, y), r, facecolor=C[fill], edgecolor=C[edge], lw=width))


def polygon(points, fill="white", edge="ink", width=.7):
    ax.add_patch(Polygon(points, facecolor=C[fill], edgecolor=C[edge], lw=width))


def text(x, y, value, size=8, align="center", color="ink", bold=False):
    return ax.text(x, y, value, fontsize=size * FS, ha=align, va="center",
                   color=C[color], weight="bold" if bold else "normal")


def text_width(value, size):
    """Width of a text label in data units of the current axes."""
    fig = ax.figure
    t = ax.text(0, 0, value, fontsize=size * FS)
    box = t.get_window_extent(renderer=fig.canvas.get_renderer())
    t.remove()
    inv = ax.transData.inverted()
    return inv.transform((box.x1, 0))[0] - inv.transform((box.x0, 0))[0]


def text_box(value, size):
    """(width, height) of a text label in data units of the current axes."""
    fig = ax.figure
    t = ax.text(0, 0, value, fontsize=size * FS)
    box = t.get_window_extent(renderer=fig.canvas.get_renderer())
    t.remove()
    inv = ax.transData.inverted()
    (a, b), (c, d) = inv.transform((box.x0, box.y0)), inv.transform((box.x1, box.y1))
    return c - a, d - b


def swatch_legend(rows, y_top, x_left, x_right, row_gap, size=NOTE, box=.15, pad=.2, gap=.42):
    """Column-aligned swatch legend centred between x_left and x_right."""
    ncol = max(len(r) for r in rows)
    widths = [max(box + pad + text_width(r[c][1], size) for r in rows if c < len(r))
              for c in range(ncol)]
    total = sum(widths) + gap * (ncol - 1)
    x = x_left + (x_right - x_left - total) / 2
    starts = []
    for w in widths:
        starts.append(x)
        x += w + gap
    for i, r in enumerate(rows):
        for c, (fill, label) in enumerate(r):
            yy = y_top - i * row_gap
            rect(starts[c], yy - box / 2, box, box, fill, "muted", .3)
            text(starts[c] + box + pad, yy, label, size, "left")


def arrow(points, color="ink", width=.7, dashed=False):
    line(points, color, width, dashed)
    p, q = points[-2:]
    angle = math.atan2(q[1] - p[1], q[0] - p[0])
    length, half = .11, .045
    c, s = math.cos(angle), math.sin(angle)
    polygon([q, (q[0] - length * c + half * s, q[1] - length * s - half * c),
             (q[0] - length * c - half * s, q[1] - length * s + half * c)], color, color, .2)


def cross(x, y, r=.065, color="orange"):
    line([(x - r, y - r), (x + r, y + r)], color, 1.2)
    line([(x - r, y + r), (x + r, y - r)], color, 1.2)


def camera(x, y, target):
    angle = math.atan2(target[1] - y, target[0] - x)
    c, s = math.cos(angle), math.sin(angle)
    polygon([(x + c * u - s * v, y + s * u + c * v)
             for u, v in [(-.15, -.115), (.16, 0), (-.15, .115)]])


def swatch(x, y, fill, label, size=7.3):
    rect(x, y - .07, .14, .14, fill, "muted", .3)
    text(x + .22, y, label, size, "left")


def dimension(x1, x2, y, label, label_y):
    line([(x1, y), (x2, y)], "muted", .55)
    for x in (x1, x2):
        line([(x, y - .055), (x, y + .055)], "muted", .55)
    text((x1 + x2) / 2, label_y, label, 8)


def bezier_arrow(p0, p1, p2, p3, color="blue", width=.7):
    points = []
    for i in range(65):
        t = i / 64
        points.append(tuple((1 - t) ** 3 * p0[k] + 3 * (1 - t) ** 2 * t * p1[k]
                            + 3 * (1 - t) * t * t * p2[k] + t ** 3 * p3[k] for k in (0, 1)))
    arrow(points, color, width, True)


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", pad_inches=0.0, metadata={"CreationDate": None})
    fig.savefig(OUT / f"{name}.png", dpi=400, pad_inches=0.0)
    plt.close(fig)


# ---------------------------------------------------------------- (a) association
# Half-column panel (Figs. 3 and 4 share one row of a column); legend under the rays.
HALF_CM = 4.2
fig = new_figure(0.15, 4.85, 6.30, 8.98, HALF_CM)
v = (4.05, 7.77)
cams = [(.45, 8.52), (.45, 7.78), (.45, 7.03)]
fractions = [.925, .92, .47]
samples = [tuple(k[j] + f * (v[j] - k[j]) for j in (0, 1)) for k, f in zip(cams, fractions)]
surface = [(4.14, 6.88), (3.97, 7.34), v, (4.19, 8.26), (4.11, 8.86)]
line(surface, "ink", 1.15)
for i, (k, m) in enumerate(zip(cams, samples)):
    color = "blue" if i < 2 else "orange"
    line([k, v], "muted", .5, True)
    line([k, m], color, .85)
    camera(*k, v)
    text(k[0] + .01, k[1] + .25, f"$K_{i+1}$", MATH)
    if i < 2:
        circle(*m, .055, "blue", "blue", .3)
    else:
        cross(*m)
circle(*v, .045, "ink", "ink", .4)
text(v[0] + .22, v[1] - .12, r"$v_j^-$", MATH, "left")
text(4.36, 8.78, r"$\mathcal{M}^-$", MATH, "left")
text(samples[0][0] - .10, samples[0][1] + .22, r"$m_1$", MATH, color="blue")
text(samples[1][0] - .12, samples[1][1] - .24, r"$m_2$", MATH, color="blue")
text(samples[2][0] + .03, samples[2][1] - .25, r"$m_3$", MATH, color="orange")
circle(.55, 6.50, .05, "blue", "blue", .4)
text(.72, 6.50, "Retained", NOTE, "left")
cross(2.05, 6.50, .05)
text(2.22, 6.50, "Rejected", NOTE, "left")
save(fig, "mech_assoc")

# ---------------------------------------------------------------- (b) clustering
# The "(cell, component)" rule moves to the caption; labels sit outside the bands.
fig = new_figure(8.25, 13.25, 6.00, 8.86, HALF_CM)
x0 = 8.43
cx, cy, cw, ch = 9.72, 6.72, 2.02, 2.02
line([(cx, cy), (cx + cw, cy), (cx + cw, cy + ch), (cx, cy + ch), (cx, cy)], "muted", .65, True)
xs = [.15, .79, 1.42, 2.00, 2.61, 3.22, 3.92, 4.65]
for mid, color, phase, side in [(8.06, "blue", 0, 1), (7.48, "teal", 1.4, -1)]:
    upper = [(x0 + x, mid + .18 + .08 * math.sin(1.6 * x + phase)) for x in xs]
    lower = [(x0 + x, mid - .18 + .08 * math.sin(1.6 * x + phase)) for x in xs]
    polygon(upper + lower[::-1], "white", color, .55)
    for i in range(len(xs)):
        line([upper[i], lower[i]], color, .4)
        if i + 1 < len(xs):
            line([lower[i], upper[i + 1]], color, .4)
        for p in (upper[i], lower[i]):
            circle(*p, .024, color, color, .2)
    xp = cx + cw / 2
    yp = mid + .08 * math.sin(1.6 * (xp - x0) + phase)
    circle(xp, yp, .105, "white", color, 1.2)
    text(xp, yp + side * (.43 if side > 0 else .38), r"$p_A^-$" if color == "blue" else r"$p_B^-$", MATH, color=color)
for (lx, ly), kind, label in [((8.55, 6.50), "blue", "Component A"),
                              ((10.85, 6.50), "teal", "Component B"),
                              ((8.55, 6.17), "proxy", "Proxy vertex"),
                              ((10.85, 6.17), "cell", "Spatial cell")]:
    if kind == "proxy":
        circle(lx, ly, .083, "white", "ink", 1)
    elif kind == "cell":
        line([(lx - .12, ly - .12), (lx + .12, ly - .12), (lx + .12, ly + .12),
              (lx - .12, ly + .12), (lx - .12, ly - .12)], "muted", .6, True)
    else:
        line([(lx - .13, ly), (lx + .13, ly)], kind, 1.0)
    text(lx + .25, ly, label, NOTE, "left")
save(fig, "mech_cluster")

# ---------------------------------------------------------------- (c) reconstruction
# Same planar local example; the equations and the continued-fusion inset are omitted.
s = .32
rho, tau = 1.5 * s, 4 * s
sgx, tgx, gy = .35, 5.52, 2.25
snx, tnx, ny = 10, 14, 9
qm = (1.55, 3.80)
qp = (7.28, 3.69)
angle = math.radians(25)
nm = (math.cos(angle), -math.sin(angle))
tm = (math.sin(angle), math.cos(angle))


def source_uv(p):
    d = (p[0] - qm[0], p[1] - qm[1])
    return sum(d[i] * nm[i] for i in (0, 1)), sum(d[i] * tm[i] for i in (0, 1))


def pullback(p):
    u, v = p[0] - qp[0], p[1] - qp[1]
    return tuple(qm[i] + u * nm[i] + v * tm[i] for i in (0, 1))


def forward(p):
    u, v = source_uv(p)
    return qp[0] + u, qp[1] + v


def source_center(ix, iy):
    return sgx + (ix + .5) * s, gy + (iy + .5) * s


def source_weight(ix, iy):
    u, v = source_uv(source_center(ix, iy))
    observed = (-tau <= u <= tau + 3 * s) and not (u > .34 and v < -.60)
    return 8.0 if observed else 0.0


def source_sample(p):
    zx, zy = (p[0] - sgx) / s - .5, (p[1] - gy) / s - .5
    ix, iy = math.floor(zx), math.floor(zy)
    fx, fy = zx - ix, zy - iy
    taps = [(ix + a, iy + b, ((fx if a else 1 - fx) * (fy if b else 1 - fy)))
            for a in (0, 1) for b in (0, 1)]
    taps = [t for t in taps if t[2] > 1e-10]
    valid = all(source_weight(a, b) > 0 for a, b, c in taps)
    if valid:
        return True, sum(c * source_weight(a, b) for a, b, c in taps)
    return False, source_weight(math.floor((p[0] - sgx) / s), math.floor((p[1] - gy) / s))


classes = {}
for iy in range(ny):
    for ix in range(tnx):
        p = (tgx + (ix + .5) * s, gy + (iy + .5) * s)
        r = abs(p[0] - qp[0])
        cls = "unknown"
        if r <= tau + 1e-9:
            old = pullback(p)
            valid, w = source_sample(old)
            old_q = pullback((qp[0], p[1]))
            probes = [tuple(old_q[k] + direction * s * nm[k] for k in (0, 1)) for direction in (-1, 1)]
            orientation = all(source_sample(probe)[0] for probe in probes)
            if w > 0 and (not valid or orientation or r <= rho):
                cls = "narrow" if r <= rho else "extended"
            elif w <= 0 and r < rho:
                cls = "fallback"
        classes[ix, iy] = cls
seen = {p for p, c in classes.items() if c in ("narrow", "fallback")}
queue = list(seen)
while queue:
    ix, iy = queue.pop()
    for p in ((ix - 1, iy), (ix + 1, iy), (ix, iy - 1), (ix, iy + 1)):
        if p not in seen and classes.get(p) == "extended":
            seen.add(p)
            queue.append(p)
for p, c in list(classes.items()):
    if c == "extended" and p not in seen:
        classes[p] = "unknown"
for sy in range(-8, 20):
    for sx in range(-8, 24):
        old = source_center(sx, sy)
        u, v = source_uv(old)
        if source_weight(sx, sy) <= 0 or u < rho:
            continue
        dest = forward(old)
        ix, iy = math.floor((dest[0] - tgx) / s), math.floor((dest[1] - gy) / s)
        if classes.get((ix, iy)) != "unknown":
            continue
        has_negative = any(classes.get((ix + dx, iy + dy), "unknown") != "unknown"
                           and tgx + (ix + dx + .5) * s < qp[0]
                           for dx in (-1, 0, 1) for dy in (-1, 0, 1))
        if not has_negative:
            classes[ix, iy] = "free"

fig = new_figure(0.22, 10.12, 0.93, 5.62, RECON_CM, RECON_CM / WIDTH_CM * 1.08)
for iy in range(ny):
    for ix in range(snx):
        old = source_center(ix, iy)
        u, _ = source_uv(old)
        fill = "white"
        if source_weight(ix, iy) > 0:
            fill = "tealfill" if u > tau else "source"
        rect(sgx + ix * s, gy + iy * s, s, s, fill, "grid", .30)
fills = {"unknown": "white", "narrow": "bluefill", "extended": "bluefill",
         "fallback": "orangefill", "free": "tealfill"}
for iy in range(ny):
    for ix in range(tnx):
        rect(tgx + ix * s, gy + iy * s, s, s, fills[classes[ix, iy]], "grid", .30)
old_line = []
for y in (gy - .04, gy + ny * s + .04):
    vv = (y - qm[1]) / tm[1]
    old_line.append((qm[0] + vv * tm[0], y))
line(old_line, "ink", 1.2)
line([(qp[0], gy - .04), (qp[0], gy + ny * s + .04)], "ink", 1.2)
for bound, color in ((rho, "blue"), (tau, "muted")):
    for direction in (-1, 1):
        xx = qp[0] + direction * bound
        line([(xx, gy), (xx, gy + ny * s)], color, .45, True)
top = gy + ny * s
text(sgx + snx * s / 2, top + .30, "Source TSDF", TXT)
text(tgx + tnx * s / 2, top + .30, "Corrected TSDF", TXT)
# \bar{\mathcal{M}}^- with a hand-placed bar (mathtext sets \bar off-centre on \mathcal)
lab = text(1.36, 4.88, r"$\mathcal{M}^{-}$", MATH, "left")
bb = text_box(r"$\mathcal{M}$", MATH)
line([(1.36 + .22 * bb[0], 4.88 + .62 * bb[1]), (1.36 + .92 * bb[0], 4.88 + .62 * bb[1])], "ink", .55)
text(7.02, 4.88, r"$\mathcal{M}^{+}$", MATH)
for gx, n in ((sgx, snx), (tgx, tnx)):
    text(gx + .26, 4.92, "$-$", MATH, color="muted")
    text(gx + n * s - .26, 4.92, "$+$", MATH, color="muted")
x = (tgx + 7.5 * s, gy + 4.5 * s)
xm = pullback(x)
assert math.dist(x, qp) > rho and source_sample(xm)[1] > 0
assert abs(math.dist(x, qp) - math.dist(xm, qm)) < 1e-12
assert classes[6, 1] == "fallback"
bezier_arrow(x, (6.25, 4.97), (4.45, 4.97), xm, "blue", .75)
for q, p in ((qm, xm), (qp, x)):
    arrow([q, p], "ink", .95)
    circle(*q, .041, "ink", "ink", .4)
    circle(*p, .052, "blue", "blue", .4)
text(qm[0] - .24, qm[1] + .10, r"$q^-$", MATH)
text(xm[0] + .24, xm[1] - .12, r"$x^-$", MATH)
text(1.90, 3.90, r"$r$", MATH)
text(qp[0] - .24, qp[1] - .24, r"$q^+$", MATH)
text(x[0] + .17, x[1] - .15, r"$x$", MATH)
text((qp[0] + x[0]) / 2, qp[1] + .24, r"$r$", MATH)
mid_gap = (sgx + snx * s + tgx) / 2
text(mid_gap, 3.52, "Paired surface", TXT)
text(mid_gap, 3.22, "frames", TXT)
fb = (tgx + 6.5 * s, gy + 1.5 * s)
fbm = pullback(fb)
assert source_sample(fbm)[1] == 0 and abs(fb[0] - qp[0]) < rho
bezier_arrow(fb, (6.0, 2.35), (3.4, 2.35), fbm, "orange", .65)
circle(*fbm, .045, "white", "orange", .8)
circle(*fb, .043, "orange", "orange", .4)
text(mid_gap, 2.88, "No source", NOTE, color="orange")
text(mid_gap, 2.62, "weight", NOTE, color="orange")
# band half-widths on one level: tau to the left of the surface, rho to the right
ybar = 2.04
for x1, x2, label in ((qp[0] - tau, qp[0], r"$\tau$"), (qp[0], qp[0] + rho, r"$\rho$")):
    line([(x1, ybar), (x2, ybar)], "muted", .55)
    for xx in (x1, x2):
        line([(xx, ybar - .055), (xx, ybar + .055)], "muted", .55)
    text((x1 + x2) / 2, ybar - .20, label, MATH)
swatch_legend([[("source", "Observed in source"), ("bluefill", "Transferred support"),
                ("orangefill", "Geometric fallback")],
               [("tealfill", "Transported free space"), ("white", "Unobserved")]],
              1.53, .22, 10.12, .36)
save(fig, "mech_recon")
print("Wrote mech_assoc, mech_cluster, mech_recon (.pdf, .png)")
