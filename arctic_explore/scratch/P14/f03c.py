"""ARC-P14 item 3 — Figure 3(c): chokepoint strip. The five chokepoint-group regions at large
scale, rows = regions, columns = the three periods, H_episode (>= 3 km) per 25 km cell, with
that region's period mean printed in each panel. Single column, 90 mm.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F, basemap as B, regmap as M
import matplotlib.patheffects as pe
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.cm import ScalarMappable

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

PERIODS = [("pre", "2019–21"), ("during", "2022–24"), ("post", "2025–26")]
ROWNAME = {"KaraGate": "Kara Gate", "Vilkitsky": "Vilkitsky", "Sannikov_DmLaptev": "Sannikov",
           "LongStrait": "Long Strait", "BeringChukchi": "Bering–Chukchi"}
def per(y):
    return ("pre" if 2019 <= y <= 2021 else "during" if 2022 <= y <= 2024
            else "post" if y >= 2025 else None)

C = pd.read_csv("scratch/P3/P3_cells.csv")
C = C[C.region.isin(M.CH) & C.season.isin(["freeze-up", "winter", "melt"])].copy()
C["per"] = C.year.map(per); C = C[C.per.notna()]
XY = {(r, k): v for r, cl in M.RC.items() for k, v in enumerate(cl)}
C["x"] = [XY[(r, k)][0] / 1e3 for r, k in zip(C.region, C.cell)]
C["y"] = [XY[(r, k)][1] / 1e3 for r, k in zip(C.region, C.cell)]

# region means formed exactly as Table 3 forms them: cells -> region-season-year -> period
A = pd.read_csv("scratch/P3/P3_region_season_year.csv")
A = A[A.region.isin(M.CH)].copy(); A["per"] = A.year.map(per); A = A[A.per.notna()]
MEAN = A.groupby(["region", "per"]).H_episode3.mean().to_dict()

SIDE = M.CELL / 1e3
L, RGT, TOPM, CB = 0.150, 0.015, 0.108, 0.105
pw = (1 - L - RGT) / 3
asp = float(np.mean([(d - c) / (b - a) for r in M.CH
                     for (a, b), (c, d) in [M.region_extent(r, 30)]]))
ph_in = pw * F.W1 * asp
FIG_H = ph_in * 5 / (1 - TOPM - CB)
ph = ph_in / FIG_H

fig = F.figure(F.W1, FIG_H)
for i, r in enumerate(M.CH):
    (rx0, rx1), (ry0, ry1) = M.region_extent(r, 30)
    cx, cy = (rx0 + rx1) / 2, (ry0 + ry1) / 2
    hw = max((rx1 - rx0) / 2, (ry1 - ry0) / 2 / asp)
    XL, YL = (cx - hw, cx + hw), (cy - hw * asp, cy + hw * asp)
    for j, (pk, plab) in enumerate(PERIODS):
        ax = fig.add_axes([L + j * pw, 1 - TOPM - (i + 1) * ph, pw, ph])
        ax.set_aspect("equal")
        B.draw(ax, XL, YL, dlon=5, dlat=1, lw_coast=0.3)
        g = C[(C.region == r) & (C.per == pk)].groupby(
            ["cell", "x", "y"], as_index=False).H_episode3.mean()
        pc = PatchCollection([Rectangle((x, y), SIDE, SIDE) for x, y in zip(g.x, g.y)],
                             cmap=F.H_CMAP, norm=F.H_NORM, edgecolor="none", zorder=5)
        pc.set_array(g.H_episode3.values)
        ax.add_collection(pc)
        bx, by = M.box_xy(r)
        ax.plot(bx, by, color="#b2182b", lw=0.5, zorder=6)
        ax.text(0.04, 0.95, f"{MEAN[(r, pk)]:.3f}", transform=ax.transAxes, fontsize=7.5,
                fontweight="bold", va="top", ha="left", color="0.05", zorder=8,
                path_effects=[pe.withStroke(linewidth=1.9, foreground="white")])
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(*XL); ax.set_ylim(*YL)
        for s in ax.spines.values():
            s.set_color("0.6")
        if i == 0:
            ax.set_title(plab, fontsize=7.5, pad=2.5)
        if j == 0:
            ax.set_ylabel(f"{M.SHORT[r]}\n{ROWNAME[r]}", fontsize=7, labelpad=2.5,
                          linespacing=1.3)

cax = fig.add_axes([0.27, 0.058, 0.50, 0.010])
cb = fig.colorbar(ScalarMappable(norm=F.H_NORM, cmap=F.H_CMAP), cax=cax,
                  orientation="horizontal")
cb.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]); cb.ax.tick_params(labelsize=7)
cb.set_label("$H_{episode}$, $\\geq$ 3 km class", fontsize=7.5, labelpad=2)
fig.text(0.008, 0.996,
         "(c)  chokepoint group at large scale. The number in\n"
         "       each panel is that region's mean for the period,\n"
         "       seasons pooled.",
         fontsize=7.5, fontweight="bold", va="top", ha="left", linespacing=1.4)
F.save(fig, "fig03c_chokepoint_strip.png", F.W1)
