"""ARC-P14 item 3 — Figure 3(b): H_episode (>= 3 km) per 25 km cell, season x period small
multiples, on the same coastline and graticule as panel (a).
Also builds Supplementary Figure S1, the same grid for H_state, when run with --state.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F, basemap as B, regmap as M
from matplotlib.cm import ScalarMappable

STATE = "--state" in sys.argv
COL = "H_state3" if STATE else "H_episode3"
LETTER = "S1" if STATE else "(b)"
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

C = pd.read_csv("scratch/P3/P3_cells.csv")
C = C[C.season.isin(["freeze-up", "winter", "melt"])].copy()
def per(y):
    return ("pre 2019–21" if 2019 <= y <= 2021 else "during 2022–24" if 2022 <= y <= 2024
            else "post 2025–26" if y >= 2025 else None)
C["per"] = C.year.map(per); C = C[C.per.notna()]
XY = {(r, k): v for r, cl in M.RC.items() for k, v in enumerate(cl)}
C["x"] = [XY[(r, k)][0] / 1e3 for r, k in zip(C.region, C.cell)]
C["y"] = [XY[(r, k)][1] / 1e3 for r, k in zip(C.region, C.cell)]

SEASONS = ["freeze-up", "winter", "melt"]
PERIODS = ["pre 2019–21", "during 2022–24", "post 2025–26"]
(x0, x1), (y0, y1) = M.all_extent(110)
XL, YL = (x0, x1), (y0, y1)

L, R_, TOPM, CB = 0.055, 0.012, 0.075, 0.095   # figure fractions
pw = (1 - L - R_) / 3
ph_in = pw * F.W2 * (YL[1] - YL[0]) / (XL[1] - XL[0])
FIG_H = ph_in * 3 / (1 - TOPM - CB)
ph = ph_in / FIG_H

fig = F.figure(F.W2, FIG_H)
sc = None
for i, season in enumerate(SEASONS):
    for j, p in enumerate(PERIODS):
        ax = fig.add_axes([L + j * pw, 1 - TOPM - (i + 1) * ph, pw, ph])
        ax.set_aspect("equal")
        B.draw(ax, XL, YL, dlon=30, dlat=10, lw_coast=0.22)
        g = C[(C.season == season) & (C.per == p)].groupby(
            ["region", "cell", "x", "y"], as_index=False)[COL].mean()
        sc = ax.scatter(g.x, g.y, c=g[COL], s=1.5, cmap=F.H_CMAP, norm=F.H_NORM,
                        marker="s", linewidths=0, zorder=5)
        for r in M.CH:
            bx, by = M.box_xy(r)
            ax.plot(bx, by, color="#b2182b", lw=0.55, zorder=6)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("0.6")
        if i == 0:
            ax.set_title(p, fontsize=8, pad=3)
        if j == 0:
            ax.set_ylabel(season, fontsize=8, labelpad=3)

cax = fig.add_axes([0.30, 0.052, 0.42, 0.010])
cb = fig.colorbar(ScalarMappable(norm=F.H_NORM, cmap=F.H_CMAP), cax=cax, orientation="horizontal")
cb.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
cb.ax.tick_params(labelsize=7)
lab = "$H_{state}$" if STATE else "$H_{episode}$"
cb.set_label(f"{lab}, $\\geq$ 3 km class   (0 = no hazard caught, 1 = every hazard caught)",
             fontsize=7.5, labelpad=2)
cb.ax.plot([0.8, 0.8], [0, 1], color=F.ACCENT, lw=1.4, transform=cb.ax.transAxes, clip_on=False)
fig.text(0.726, 0.052, "  requirement 0.8", fontsize=7, color=F.ACCENT, va="bottom", ha="left")
head = (f"{LETTER}  {lab} per 25 km cell; chokepoint group outlined in red"
        if STATE else f"{LETTER}  $H_{{episode}}$ per 25 km cell; chokepoint group outlined in red")
fig.text(0.008, 1 - 0.028, head, fontsize=8.5, fontweight="bold", va="bottom", ha="left")

F.save(fig, ("figS1_H_state_maps.png" if STATE else "fig03b_H_episode_maps.png"), F.W2)
