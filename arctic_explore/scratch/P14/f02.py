"""ARC-P14 item 2 — Figure 2: hazard timescales from buoy pairs. Design kept; restyled to
300 dpi, 190 mm, single font family, all text >= 7 pt. The 2 h left-censoring floor of the
one-hourly sampling is drawn explicitly.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

z = np.load("scratch/P3/step2t_native1h.npz")
ed, em = z["dur"].astype(float), z["mag"].astype(float)
P = pd.read_csv("scratch/P1b/events_persist.csv")
P = P[P.season != "shoulder"].copy()
P["relmag"] = P.magnitude_km / P.sep_start_km
Pr = P[P.relmag >= 0.10]

CLASSES = ((1, 3, "1–3 km"), (3, 5, "3–5 km"), (5, np.inf, "$\\geq$ 5 km"))
COL = ("0.62", "0.38", "0.10")

fig = F.figure(F.W2, 2.75)
axa = fig.add_axes([0.070, 0.215, 0.395, 0.635])
axb = fig.add_axes([0.585, 0.215, 0.395, 0.635])

for (lo, hi, lab), c in zip(CLASSES, COL):
    v = ed[(em >= lo) & (em < hi)]
    if len(v) > 20:
        x = np.sort(v)
        axa.step(x, np.arange(1, len(x) + 1) / len(x), where="post", color=c, lw=1.1,
                 label=f"{lab}  (n = {len(v):,})")
axa.axvline(2, color="0.15", ls=(0, (1.2, 1.2)), lw=0.8, zorder=1)
axa.text(2.12, 0.985, "2 h censoring floor", fontsize=7, color="0.15", va="top", rotation=90)
axa.axvline(12, color=F.ACCENT, ls=(0, (3.5, 2.0)), lw=0.9)
axa.text(12.6, 0.06, "12 h episode\nrequirement", fontsize=7, color=F.ACCENT, va="bottom")
axa.set_xscale("log")
axa.set_xlabel("convergence episode duration (h), one-hourly sampling")
axa.set_ylabel("cumulative fraction")
axa.set_ylim(0, 1.02); axa.set_xlim(1.6, 400)
axa.legend(fontsize=7, loc="lower right", handlelength=1.7, borderpad=0.2, labelspacing=0.32)
axa.set_title("(a)  episode duration by magnitude class", loc="left", fontsize=8)

for (lo, hi, lab), c in zip(CLASSES, COL):
    v = Pr[(Pr.magnitude_km >= lo) & (Pr.magnitude_km < hi)].persist_h.values
    if len(v) > 20:
        x = np.sort(v)
        axb.step(x, np.arange(1, len(x) + 1) / len(x), where="post", color=c, lw=1.1,
                 label=f"{lab}  (n = {len(v):,})")
axb.axvline(24, color=F.ACCENT, ls=(0, (3.5, 2.0)), lw=0.9)
axb.text(25, 0.06, "24 h state\nrequirement", fontsize=7, color=F.ACCENT, va="bottom")
axb.set_xscale("log")
axb.set_xlabel("hazard-state persistence (h), three-hourly sampling")
axb.set_ylabel("cumulative fraction")
axb.set_ylim(0, 1.02)
axb.legend(fontsize=7, loc="lower right", handlelength=1.7, borderpad=0.2, labelspacing=0.32)
axb.set_title("(b)  persistence, relative magnitude $\\geq$ 10 %", loc="left", fontsize=8)

for ax in (axa, axb):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

F.save(fig, "fig02_hazard_timescales.png", F.W2)
