"""ARC-P13-2: merge fig03_H_state3_maps.png and fig03_H_episode3_maps.png into one Figure 3
with panel groups (a) H_state and (b) H_episode. Same data, style and colour scale as P10."""
import numpy as np, pandas as pd, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import Normalize
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
sys.path.insert(0, "scratch/P3"); sys.path.insert(0, "scratch/P2")
from cells import region_cells, CELL

OUT = "paper/figures"
plt.rcParams.update({"font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8,
                     "figure.dpi": 150, "savefig.dpi": 150, "axes.linewidth": 0.6})
CMAP = "viridis"; NORM = Normalize(0, 1.0)
# two-letter codes: the merged panels are too small for full names, which clipped at the axes edge
SHORT = {"KaraGate": "KG", "Vilkitsky": "VS", "Sannikov_DmLaptev": "SD",
         "LongStrait": "LS", "BeringChukchi": "BC"}
CODEKEY = "chokepoints: KG Kara Gate, VS Vilkitsky, SD Sannikov/Dmitry Laptev, LS Long Strait, BC Bering-Chukchi"
CH = set(SHORT)
RC = region_cells()

C = pd.read_csv("scratch/P3/P3_cells.csv")
def per(y):
    return ("pre 2019-21" if 2019 <= y <= 2021 else
            "during 2022-24" if 2022 <= y <= 2024 else
            "post 2025-26" if y >= 2025 else None)
C["per"] = C.year.map(per); C = C[C.per.notna()]
XY = {(r, k): v for r, cl in RC.items() for k, v in enumerate(cl)}
C["x"] = [XY[(r, k)][0] for r, k in zip(C.region, C.cell)]
C["y"] = [XY[(r, k)][1] for r, k in zip(C.region, C.cell)]
CENT = {r: (np.mean([a for a, b in cl]) + CELL / 2, np.mean([b for a, b in cl]) + CELL / 2)
        for r, cl in RC.items()}

SEASONS = ("freeze-up", "winter", "melt")
PERIODS = ("pre 2019-21", "during 2022-24", "post 2025-26")
GROUPS = (("a", "H_state3", r"(a)  $H_{\rm state}$"), ("b", "H_episode3", r"(b)  $H_{\rm episode}$"))

fig = plt.figure(figsize=(13.4, 7.4))
# two 3x3 blocks side by side, with a gap between them for the panel-group labels
gs = fig.add_gridspec(3, 7, width_ratios=[1, 1, 1, 0.18, 1, 1, 1],
                      wspace=0.06, hspace=0.06, left=0.045, right=0.90, top=0.845, bottom=0.03)
sc = None
for gi, (letter, col, glab) in enumerate(GROUPS):
    c0 = 0 if gi == 0 else 4
    for i, season in enumerate(SEASONS):
        for j, p in enumerate(PERIODS):
            ax = fig.add_subplot(gs[i, c0 + j])
            g = (C[(C.season == season) & (C.per == p)]
                 .groupby(["region", "cell", "x", "y"], as_index=False)[col].mean())
            sc = ax.scatter(g.x / 1e3, g.y / 1e3, c=g[col], s=2.2, cmap=CMAP, norm=NORM,
                            marker="s", linewidths=0)
            for r, (cx, cy) in CENT.items():
                if r in CH:
                    ax.text(cx / 1e3, cy / 1e3, SHORT[r], fontsize=6.0, ha="center", va="center",
                            color="w", weight="bold", zorder=5,
                            path_effects=[pe.withStroke(linewidth=1.1, foreground="0.15")])
            ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
            if i == 0: ax.set_title(p, fontsize=8)
            if j == 0 and gi == 0: ax.set_ylabel(season, fontsize=8)
    # panel-group label centred over the block
    x0 = gs[0, c0].get_position(fig).x0; x1 = gs[0, c0 + 2].get_position(fig).x1
    fig.text((x0 + x1) / 2, 0.888, glab + r"  ($\geq$ 3 km class)", ha="center", va="bottom",
             fontsize=11, weight="bold")

cax = fig.add_axes([0.915, 0.10, 0.013, 0.70])
cb = fig.colorbar(sc, cax=cax); cb.set_label("H   (1.0 = every hazard caught)", fontsize=8)
fig.suptitle("H per 25 km cell, EPSG:3413; rows are seasons, columns are periods",
             fontsize=10, y=0.985)
fig.text(0.5, 0.955, CODEKEY, ha="center", va="top", fontsize=7.5, color="0.25")
path = f"{OUT}/fig03_H_maps.png"
fig.savefig(path, bbox_inches="tight"); plt.close(fig)
print("wrote", path, os.path.getsize(path), "bytes")
