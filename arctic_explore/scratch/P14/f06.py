"""ARC-P14 item 5 — Figure 6 (was Fig. 5): four strait divergence panels, cropped to the
two-scene overlap, common divergence scale, component outlined, graticule and 50 km scale bar,
before-scene thumbnail. Double column, 190 mm.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F
import straitpanel as SP
import regmap as RM
RNAME = {"Vilkitsky": "Vilkitsky", "Sannikov_DmLaptev": "Sannikov / Dm. Laptev"}
from matplotlib.cm import ScalarMappable

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

E = pd.read_csv("paper/edge_audit.csv").set_index("event")
SEL = [("E002", 1), ("E001", 1), ("E011", 9), ("E010", 9)]
DATA = {p: SP.load(p) for p in {p for _, p in SEL}}
BOX = {p: SP.crop_box(DATA[p]) for p in DATA}
DMEAN = {}
for ev, pi in SEL:
    dd = DATA[pi]
    mm = dd["lab"] == int(ev[1:])
    DMEAN[ev] = float(np.nanmean(dd["div"][mm]))

# one common panel aspect so the four panels are the same size
asp = float(np.mean([(b[3] - b[2]) / (b[1] - b[0]) for b in BOX.values()]))
L, R_, TOPM, CB, GAPX, GAPY = 0.012, 0.012, 0.048, 0.115, 0.010, 0.030
pw = (1 - L - R_ - GAPX) / 2
ph_in = pw * F.W2 * asp
FIG_H = (2 * ph_in) / (1 - TOPM - CB - GAPY)
ph = ph_in / FIG_H

fig = F.figure(F.W2, FIG_H)
for k, (ev, pi) in enumerate(SEL):
    d = DATA[pi]
    i, j = divmod(k, 2)
    ax = fig.add_axes([L + j * (pw + GAPX), 1 - TOPM - (i + 1) * ph - i * GAPY, pw, ph])
    # square-off the box to the common aspect, keeping the overlap centred
    xl, xr, yb, yt = BOX[pi]
    cx, cy = (xl + xr) / 2, (yb + yt) / 2
    hw = max((xr - xl) / 2, (yt - yb) / 2 / asp)
    box = (cx - hw, cx + hw, cy - hw * asp, cy + hw * asp)
    r = E.loc[ev]
    SP.panel(ax, d, ev, box=box, title=None)
    ax.text(0.018, 0.975, f"{ev}   {RNAME[r.region]}   {r.date}",
            transform=ax.transAxes, fontsize=7.5, fontweight="bold", va="top", ha="left",
            color="black",
            bbox=dict(boxstyle="square,pad=0.22", fc="white", ec="none", alpha=0.82))
    ax.text(0.018, 0.905, f"area {r.area_km2:.0f} km$^2$    mean divergence "
                          f"{DMEAN[ev]:+.3f} d$^{{-1}}$",
            transform=ax.transAxes, fontsize=7, va="top", ha="left", color="0.1",
            bbox=dict(boxstyle="square,pad=0.20", fc="white", ec="none", alpha=0.82))

cax = fig.add_axes([0.315, 0.055, 0.37, 0.014])
cb = fig.colorbar(ScalarMappable(norm=SP.DIV_NORM, cmap=F.DIV_CMAP), cax=cax,
                  orientation="horizontal", extend="both")
cb.set_ticks([-0.10, -0.05, 0, 0.05, 0.10]); cb.ax.tick_params(labelsize=7, pad=1.5)
cb.set_label("divergence (d$^{-1}$);  negative = convergence", fontsize=7.5, labelpad=1.5)
fig.text(0.012, 1 - 0.014,
         "Sentinel-1 Extra Wide HH, after-scene, with the retrieved divergence field overlaid; "
         "orange dashes mark the two-scene footprint overlap",
         fontsize=7, color="0.3", va="top", ha="left")
F.save(fig, "fig06_strait_examples.png", F.W2)
