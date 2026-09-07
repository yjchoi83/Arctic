"""ARC-P14 item 8 — Figure A1: contact sheet of the nineteen candidate events, in the same
style as Figure 6 — cropped to the two-scene overlap, common divergence scale, component
outlined, graticule, scale bar, before-scene thumbnail. Stays in Appendix A.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F
import straitpanel as SP
from matplotlib.cm import ScalarMappable

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

RNAME = {"Vilkitsky": "VS", "Sannikov_DmLaptev": "SD"}
E = pd.read_csv("paper/edge_audit.csv")
Q = pd.read_csv("results/P9/qc_table_p9.csv").set_index("event")
PAIRS = sorted(E.pair.unique())
DATA = {int(p): SP.load(int(p)) for p in PAIRS}
BOX = {p: SP.crop_box(DATA[p]) for p in DATA}
asp = float(np.mean([(b[3] - b[2]) / (b[1] - b[0]) for b in BOX.values()]))

NCOL = 4
NROW = int(np.ceil(len(E) / NCOL))
L, R_, TOPM, CB, GX, GY = 0.010, 0.010, 0.052, 0.070, 0.008, 0.020
pw = (1 - L - R_ - (NCOL - 1) * GX) / NCOL
ph_in = pw * F.W2 * asp
FIG_H = (NROW * ph_in) / (1 - TOPM - CB - (NROW - 1) * GY)
ph = ph_in / FIG_H

fig = F.figure(F.W2, FIG_H)
for k, r in E.reset_index(drop=True).iterrows():
    i, j = divmod(k, NCOL)
    ax = fig.add_axes([L + j * (pw + GX),
                       1 - TOPM - (i + 1) * ph - i * GY, pw, ph])
    d = DATA[int(r.pair)]
    xl, xr, yb, yt = BOX[int(r.pair)]
    cx, cy = (xl + xr) / 2, (yb + yt) / 2
    hw = max((xr - xl) / 2, (yt - yb) / 2 / asp)
    box = (cx - hw, cx + hw, cy - hw * asp, cy + hw * asp)
    SP.panel(ax, d, r.event, box=box, grat_lon=4, grat_lat=1, label_fs=7,
             thumb_rect=(0.700, 0.700, 0.285, 0.285))
    mg = Q.loc[r.event, "mag_buoy_baseline_km"] if r.event in Q.index else np.nan
    ax.text(0.025, 0.972, f"{r.event}  {RNAME[r.region]}  {r.date}",
            transform=ax.transAxes, fontsize=7, fontweight="bold", va="top", ha="left",
            bbox=dict(boxstyle="square,pad=0.18", fc="white", ec="none", alpha=0.85))
    ax.text(0.025, 0.882,
            f"{r.area_km2:.0f} km$^2$ · {r.centroid_dist_km:.0f} km",
            transform=ax.transAxes, fontsize=7, va="top", ha="left", color="0.1",
            bbox=dict(boxstyle="square,pad=0.16", fc="white", ec="none", alpha=0.85))
    ax.text(0.975, 0.028, "decision:", transform=ax.transAxes, fontsize=7, va="bottom",
            ha="right", color="0.1",
            bbox=dict(boxstyle="square,pad=0.22", fc="white", ec="0.4", lw=0.4))

for k in range(len(E), NROW * NCOL):
    i, j = divmod(k, NCOL)
    ax = fig.add_axes([L + j * (pw + GX), 1 - TOPM - (i + 1) * ph - i * GY, pw, ph])
    ax.axis("off")

cax = fig.add_axes([0.335, 0.030, 0.33, 0.010])
cb = fig.colorbar(ScalarMappable(norm=SP.DIV_NORM, cmap=F.DIV_CMAP), cax=cax,
                  orientation="horizontal", extend="both")
cb.set_ticks([-0.10, -0.05, 0, 0.05, 0.10]); cb.ax.tick_params(labelsize=7, pad=1.5)
cb.set_label("divergence (d$^{-1}$);  negative = convergence", fontsize=7.5, labelpad=1.5)
fig.text(0.010, 1 - 0.008,
         "Per panel, top line: event, strait (VS Vilkitsky, SD Sannikov / Dm. Laptev), date.  "
         "Second line: component area · centroid distance to the two-scene overlap\nboundary.  "
         "Magnitudes on the buoy baseline are in the Appendix A table.  Decision boxes are deliberately blank.",
         fontsize=7, color="0.3", va="top", ha="left", linespacing=1.4)
F.save(fig, "figA1_contact_sheet.png", F.W2)
