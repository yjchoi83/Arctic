"""ARC-P14 item 4 — Figure 5 (was Fig. 4): strait drift fields in the buoy-pair metric.
Main panel: positive closures on log-log. Inset (upper right): the negative side, opening.
3 km and 5 km boundaries labelled separately; median closure of the threshold-passing pairs
(5.88 km) and their share of all pairs (0.50 %) annotated.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

V = pd.read_csv("scratch/P9/virtual_pairs_all.csv.gz")
clo = -V.ds.values
THR = -2.954
sel = clo[V.rate.values <= THR]
N = len(clo)
med, frac = float(np.median(sel)), len(sel) / N
print(f"n={N}  passing={len(sel)} ({100*frac:.2f} %)  median {med:.3f} km")


def exceed(v, denom):
    x = np.sort(v[v > 0])
    return x, (len(x) - np.arange(len(x))) / denom


fig = F.figure(F.W1, 3.25)
ax = fig.add_axes([0.170, 0.245, 0.810, 0.640])

x, y = exceed(clo, N)
ax.plot(x, y, color="0.30", lw=1.1, label=f"all virtual pairs  (n = {N:,})")
xs, ys = exceed(sel, N)
ax.plot(xs, ys, color=F.ACCENT, lw=1.4,
        label=f"passing the buoy rate threshold  (n = {len(sel):,})")

for xv, lab, ls in ((3.0, "3 km", (0, (4, 1.6))), (5.0, "5 km", (0, (1.3, 1.3)))):
    ax.axvline(xv, color="0.15", ls=ls, lw=0.7, zorder=1)
    ax.text(xv * 1.04, 2.2e-5, lab, fontsize=7, color="0.15", ha="left", va="center")

ax.axhline(frac, color=F.ACCENT, ls=(0, (2.5, 1.8)), lw=0.7, zorder=1)
ax.text(0.94, frac * 0.62, f"{100*frac:.2f} % of all pairs pass", fontsize=7,
        color=F.ACCENT, ha="left", va="top")
ax.plot([med], [frac / 2], marker="o", ms=3.4, color=F.ACCENT, zorder=6)
ax.annotate(f"median closure of\npassing pairs, {med:.2f} km",
            xy=(med, frac / 2), xytext=(0.94, 6.0e-4), fontsize=7, color=F.ACCENT,
            ha="left", va="top",
            arrowprops=dict(arrowstyle="-", lw=0.5, color=F.ACCENT, shrinkB=2))

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(0.9, 13.0); ax.set_ylim(8e-6, 1.05)
ax.set_xticks([1, 2, 3, 5, 10]); ax.set_xticklabels(["1", "2", "3", "5", "10"])
ax.set_xlabel("closure over the acquisition window (km)")
ax.set_ylabel("fraction of all virtual pairs exceeding")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

fig.legend(fontsize=7, loc="lower left", bbox_to_anchor=(0.055, 0.008), handlelength=1.8,
           labelspacing=0.30, borderpad=0.2)

ins = fig.add_axes([0.680, 0.630, 0.285, 0.230])
xo, yo = exceed(-clo, N)
ins.plot(xo, yo, color="0.30", lw=0.9)
so = -clo[V.rate.values <= THR]
if (so > 0).sum() > 5:
    x2, y2 = exceed(so, N)
    ins.plot(x2, y2, color=F.ACCENT, lw=1.0)
ins.set_xscale("log"); ins.set_yscale("log")
ins.set_xlim(0.9, 15.0); ins.set_ylim(8e-6, 1.05)
ins.set_xticks([1, 10]); ins.set_xticklabels(["1", "10"])
ins.set_yticks([1e-4, 1e-2, 1e0])
ins.tick_params(labelsize=7, pad=1.2)
ins.set_title("opening", fontsize=7.5, pad=1.5)
ins.set_xlabel("km", fontsize=7, labelpad=0.5)
for s in ("top", "right"):
    ins.spines[s].set_visible(False)

F.save(fig, "fig05_virtual_pairs.png", F.W1)
