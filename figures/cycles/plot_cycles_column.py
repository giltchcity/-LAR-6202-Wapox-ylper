# Single-column version of plot_cycles.py for the paper (Figure R1 stays wide in the reply).
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

FUSION_S = {  # duration of each continued-fusion interval (s), in order of the B checkpoints
    "1207_acl_jackal2": [290.62, 599.03],
    "1207_hathor": [154.25, 8.96, 177.31, 1.44, 182.89],
    "1207_sparkal1": [238.77],
    "1208_acl_jackal2": [289.05],
    "1208_apis": [206.08],
}
DF_10_50 = {  # (dF@10, dF@50) per checkpoint, from the former Table tab:reply-cycles
    "1207_acl_jackal2": [(-0.20, 0.90), (-0.71, -0.32), (0.40, 1.72), (-0.90, -0.62), (-0.12, 0.05)],
    "1207_hathor": [(1.54, 2.34), (0.79, 0.50), (1.23, 1.17), (0.83, 1.14), (0.24, 0.57), (0.29, 0.65),
                    (0.73, 0.77), (0.82, 0.66), (0.25, 1.48), (-0.58, -0.11), (0.00, -1.28)],
    "1207_sparkal1": [(0.10, -0.12), (-0.26, -0.37), (0.78, 0.82)],
    "1208_acl_jackal2": [(0.29, -1.77), (-0.43, -1.67), (0.47, -0.80)],
    "1208_apis": [(0.29, -1.38), (0.19, -0.88), (0.03, -1.04)],
}
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
    "font.family": "DejaVu Sans", "font.size": 5.6, "axes.linewidth": 0.6,
    "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2, "ytick.major.size": 2,
    "pdf.fonttype": 42,
})


GAP = 0.4
fig, ax = plt.subplots(figsize=(3.40, 1.55))  # one paper column
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
    durs = iter(FUSION_S[name])
    for xi, a in zip(x, isA):
        if not a:
            axr.axvspan(xi - 0.5, xi + 0.5, color="#f0efec", lw=0, zorder=0)
            ax.text(xi, 3, (lambda d: f"{d:.0f} s" if d >= 10 else f"{d:.1f} s")(next(durs)), rotation=90, ha="center", va="bottom",
                    fontsize=4.2, color=INK2, zorder=1)
    for mname, col, color, marker in METRICS:
        y = [rr[col] for rr in rows]
        ax.plot(x, y, color=color, lw=0.8, zorder=2)
        ax.scatter([a for a, k in zip(x, isA) if k], [b for b, k in zip(y, isA) if k], s=5, marker=marker,
                   color=color, lw=0, zorder=3)
        ax.scatter([a for a, k in zip(x, isA) if not k], [b for b, k in zip(y, isA) if not k], s=5,
                   marker=marker, facecolor="white", edgecolor=color, lw=0.5, zorder=3)
    d10 = [v[0] for v in DF_10_50[name]]; d50 = [v[1] for v in DF_10_50[name]]
    ax.plot(x, [50 + 50 / 6 * v for v in d10], color="#4a3aa7", lw=0.8, alpha=0.5, zorder=2)
    ax.plot(x, [50 + 50 / 6 * v for v in d50], color="#d55181", lw=0.8, alpha=0.5, ls=(0, (4, 1.5)), zorder=2)
    y = [r[1] for r in rows]
    ax.plot(x, [50 + 50 / 6 * v for v in y], color=INK, lw=0.8, zorder=2)
    ax.scatter([a for a, k in zip(x, isA) if k], [50 + 50 / 6 * b for b, k in zip(y, isA) if k], s=5, color=INK, lw=0, zorder=3)
    ax.scatter([a for a, k in zip(x, isA) if not k], [50 + 50 / 6 * b for b, k in zip(y, isA) if not k], s=5,
               facecolor="white", edgecolor=INK, lw=0.5, zorder=3)
    date, robot = name.split("_", 1)
    # one horizontal line per sequence; the two names around the short middle group move outward
    align = {"1207_sparkal1": ("right", x[-1]), "1208_apis": ("left", x[0])}.get(
        name, ("center", (x[0] + x[-1]) / 2))
    ax.text(align[1], 101.5, f"{robot} {date}", ha=align[0], va="bottom", fontsize=4.0, color=INK)
    xt += x; xl += labels
    pos = x[-1] + 1 + GAP

ax.axhline(50, color=INK2, lw=0.6, ls=(0, (3, 2)), zorder=1)
# left axis: volumetric metrics, 0-100 %
ax.set_ylim(0, 100); ax.set_yticks([0, 50, 100])
ax.set_ylabel("Volumetric metrics (%)", color=INK, labelpad=0.5)
ax.tick_params(axis="y", labelrotation=90, pad=1)
for t in ax.get_yticklabels(): t.set_va("center")
# right axis: dF@25, aligned so that 0 pp sits on the 25 % grid line (1 pp = 5 %)
axr.set_ylim(-6, 6)
axr.set_yticks([-6, 0, 6])

axr.set_ylabel(r"$\Delta$F (pp)", color=INK, labelpad=0.5)
axr.tick_params(axis="y", labelrotation=90, pad=1)
for t in axr.get_yticklabels(): t.set_va("center")
ax.set_xticks(xt); ax.set_xticklabels(xl, fontsize=4.2)
ax.tick_params(axis="x", pad=1)
ax.set_xlim(-0.25, xt[-1] + 0.25)

handles = [Line2D([0], [0], color="#4a3aa7", lw=0.8, alpha=0.5),
           Line2D([0], [0], color=INK, lw=1.0, marker="o", markersize=3, markeredgewidth=0),
           Line2D([0], [0], color="#d55181", lw=0.8, alpha=0.5, ls=(0, (4, 1.5)))]
handles += [Line2D([0], [0], color=c, lw=1.0, marker=m, markersize=3, markeredgewidth=0) for _, _, c, m in METRICS]
names = [r"$\Delta$F@10", r"$\Delta$F@25", r"$\Delta$F@50"] + [m[0] for m in METRICS]
ax.legend(handles, names, loc="upper center", ncol=7, frameon=False, fontsize=4.4,
           bbox_to_anchor=(0.5, -0.15), bbox_transform=ax.transAxes, handlelength=1.0, columnspacing=0.55,
           handletextpad=0.25, borderaxespad=0.0, borderpad=0.0)
fig.subplots_adjust(left=0.075, right=0.93, top=0.84, bottom=0.235)
fig.savefig(sys.argv[1], bbox_inches="tight", pad_inches=0.01)
if len(sys.argv) > 2:
    fig.savefig(sys.argv[2], dpi=300, bbox_inches="tight", pad_inches=0.01)
