import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Rows of Table tab:reply-cycles: (label, dF25, support IoU, weighted Jaccard, free-space recall, sign accuracy)
SEQ = [
    ("1207_acl_jackal2", [
        ("A1", +1.01, 94.45, 92.11, 99.45, 98.46),
        ("B1", -0.58, 98.76, 97.94, 99.92, 99.55),
        ("A2", +0.62, 88.14, 81.38, 98.38, 96.34),
        ("B2", -1.78, 95.65, 92.70, 99.83, 98.53),
        ("A3", -2.63, 79.33, 73.34, 96.55, 86.59)]),
    ("1207_hathor", [
        ("A1", +2.55, 87.80, 83.61, 97.84, 92.74),
        ("B1", +1.58, 88.70, 85.67, 98.18, 93.11),
        ("A2", +1.49, 82.93, 80.75, 96.65, 91.25),
        ("B2", +0.92, 83.14, 80.92, 96.70, 91.31),
        ("A3", +0.37, 81.40, 79.51, 96.07, 90.74),
        ("B3", +0.29, 83.52, 81.83, 96.63, 91.66),
        ("A4", +1.18, 78.19, 77.00, 95.15, 88.59),
        ("B4", +1.43, 78.33, 77.04, 95.22, 88.65),
        ("A5", +1.12, 74.44, 71.84, 94.44, 87.11),
        ("B5", -0.67, 78.62, 76.31, 95.51, 89.18),
        ("A6", -1.48, 71.69, 70.47, 93.61, 84.47)]),
    ("1207_sparkal1", [
        ("A1", +0.06, 88.33, 88.32, 98.92, 95.18),
        ("B1", -0.33, 92.02, 91.02, 99.28, 96.73),
        ("A2", +1.68, 79.62, 71.09, 96.81, 89.19)]),
    ("1208_acl_jackal2", [
        ("A1", -0.07, 88.37, 87.70, 99.33, 96.90),
        ("B1", -0.70, 92.71, 91.57, 99.69, 98.11),
        ("A2", +0.33, 84.90, 78.34, 98.63, 95.44)]),
    ("1208_apis", [
        ("A1", -0.31, 88.98, 87.94, 99.16, 96.20),
        ("B1", -0.30, 91.49, 90.35, 99.35, 97.02),
        ("A2", -0.46, 83.17, 77.91, 98.14, 93.60)]),
]

INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"
METRICS = [  # (name, column index, color, marker) -- validated categorical slots 1-4
    ("Free-space recall", 4, "#2a78d6", "o"),
    ("Sign accuracy", 5, "#eb6834", "s"),
    ("Support IoU", 2, "#1baf7a", "^"),
    ("Weighted Jaccard", 3, "#eda100", "D"),
]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7, "axes.linewidth": 0.6,
    "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2, "ytick.major.size": 2,
    "pdf.fonttype": 42,
})


GAP = 0.45
fig, ax = plt.subplots(figsize=(6.3, 1.85))
axr = ax.twinx()
ax.set_zorder(axr.get_zorder() + 1); ax.patch.set_visible(False)
ax.grid(axis="y", color=GRID, linewidth=0.5)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
for sp in ("top", "left", "bottom"):
    axr.spines[sp].set_visible(False)

xt, xl, pos, centers = [], [], 0.0, []
for name, rows in SEQ:
    x = [pos + i for i in range(len(rows))]
    labels = [r[0] for r in rows]
    isA = [l.startswith("A") for l in labels]
    for xi, a in zip(x, isA):
        if not a:
            axr.axvspan(xi - 0.5, xi + 0.5, color="#f0efec", lw=0, zorder=0)
    for mname, col, color, marker in METRICS:
        y = [rr[col] for rr in rows]
        ax.plot(x, y, color=color, lw=1.0, zorder=2)
        ax.scatter([a for a, k in zip(x, isA) if k], [b for b, k in zip(y, isA) if k], s=9, marker=marker,
                   color=color, lw=0, zorder=3)
        ax.scatter([a for a, k in zip(x, isA) if not k], [b for b, k in zip(y, isA) if not k], s=9,
                   marker=marker, facecolor="white", edgecolor=color, lw=0.7, zorder=3)
    y = [r[1] for r in rows]
    ax.plot(x, [50 + 50 / 6 * v for v in y], color=INK, lw=1.0, zorder=2)
    ax.scatter([a for a, k in zip(x, isA) if k], [50 + 50 / 6 * b for b, k in zip(y, isA) if k], s=9, color=INK, lw=0, zorder=3)
    ax.scatter([a for a, k in zip(x, isA) if not k], [50 + 50 / 6 * b for b, k in zip(y, isA) if not k], s=9,
               facecolor="white", edgecolor=INK, lw=0.7, zorder=3)
    d, r = name.split("_", 1)
    ax.text((x[0] + x[-1]) / 2, 102, f"{r}\n{d}", ha="center", va="bottom", fontsize=6.0, color=INK, linespacing=1.1)
    xt += x; xl += labels
    pos = x[-1] + 1 + GAP

ax.axhline(50, color=INK2, lw=0.6, ls=(0, (3, 2)), zorder=1)
# left axis: volumetric metrics, 0-100 %
ax.set_ylim(0, 100); ax.set_yticks([0, 50, 100])
ax.set_ylabel("Volumetric metrics (%)", color=INK)
# right axis: dF@25, aligned so that 0 pp sits on the 25 % grid line (1 pp = 5 %)
axr.set_ylim(-6, 6)
axr.set_yticks([-6, 0, 6])

axr.set_ylabel(r"$\Delta$F@25 (pp)", color=INK)
axr.yaxis.set_label_coords(1.045, 0.5)
ax.set_xticks(xt); ax.set_xticklabels(xl, fontsize=5.6)
ax.set_xlim(-0.6, xt[-1] + 0.6)

handles = [Line2D([0], [0], color=INK, lw=1.0, marker="o", markersize=3, markeredgewidth=0)]
handles += [Line2D([0], [0], color=c, lw=1.0, marker=m, markersize=3, markeredgewidth=0) for _, _, c, m in METRICS]
names = [r"$\Delta$F@25 (right axis)"] + [m[0] for m in METRICS]
fig.legend(handles, names, loc="lower center", ncol=5, frameon=False, fontsize=5.8,
           bbox_to_anchor=(0.5, 0.0), handlelength=1.3, columnspacing=0.9, handletextpad=0.35)
fig.subplots_adjust(left=0.075, right=0.93, top=0.84, bottom=0.235)
fig.savefig(sys.argv[1])
if len(sys.argv) > 2:
    fig.savefig(sys.argv[2], dpi=300)
