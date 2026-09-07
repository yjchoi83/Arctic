"""ARC-P14 item 7 — Figure 9 (was Fig. 8): DTU Sentinel-1 drift product availability per
region-year. The final column is labelled 2025 (partial): the record ends 1 November 2025,
so that year is not a full annual sample.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F, regmap as M
SHORT = dict(M.NAME)
SHORT.update({"Sannikov_DmLaptev": "Sannikov", "GreenlandSea_Fram": "Greenland / Fram",
              "Barents_Svalbard": "Barents", "LancasterSound": "Lancaster",
              "VictoriaStrait": "Victoria", "BeringChukchi": "Bering–Chukchi"})

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

D = pd.read_csv("scratch/P8/dtu_availability.csv")
G = D.groupby(["region", "year"]).availability.mean().unstack()
ROWS = [r for r in M.ORDER if r in G.index]
G = G.reindex(ROWS)
years = list(G.columns)
lab = [str(y) if y != max(years) else f"{y} (partial)" for y in years]

fig = F.figure(F.W1, 3.15)
ax = fig.add_axes([0.255, 0.230, 0.560, 0.680])
vmax = float(np.nanmax(G.values))
im = ax.imshow(G.values, aspect="auto", cmap="magma", vmin=0, vmax=vmax,
               interpolation="nearest", extent=[0, len(years), len(ROWS), 0])
ax.set_yticks(np.arange(len(ROWS)) + 0.5)
ax.set_yticklabels([SHORT[r] for r in ROWS], fontsize=7)
for t, r in zip(ax.get_yticklabels(), ROWS):
    if r in M.CHSET:
        t.set_fontweight("bold"); t.set_color("#b2182b")
ax.set_xticks(np.arange(len(years)) + 0.5)
ax.set_xticklabels(lab, fontsize=7, rotation=90)
ax.tick_params(length=0, pad=1.5)
for s in ax.spines.values():
    s.set_visible(False)
for k, y in enumerate(years):
    if y in (2022, 2025):
        ax.axvline(k, color="#00d5ff", lw=1.3)
        ax.annotate("S1B lost" if y == 2022 else "S1C routine",
                    xy=(k, -0.15), xytext=(k, -1.15), fontsize=7, color="0.15",
                    ha="center", va="bottom", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", lw=0.5, color="0.4"))
cax = fig.add_axes([0.832, 0.230, 0.026, 0.680])
cb = fig.colorbar(im, cax=cax)
cb.ax.tick_params(labelsize=7, pad=1.5)
cb.set_label("fraction of days with $\\geq$ 5 % valid pixels", fontsize=7.5, labelpad=2)
fig.text(0.004, 0.010, "chokepoint-group regions in bold red", fontsize=7, color="0.35",
         va="bottom", ha="left")
F.save(fig, "fig09_dtu_availability.png", F.W1)
