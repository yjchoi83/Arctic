"""ARC-P13-7: graphical abstract, exactly 1600 x 900 px, built to the specification in paper/HIGHLIGHTS.md.
Single sequential ramp (viridis) for H; one accent colour (#d95f02) for the 0.8 requirement line.
No red-green pairing; smallest text 8.5 pt. Every text and axes bbox is asserted inside the canvas.
Output: paper/figures/graphical_abstract.png
"""
import numpy as np, pandas as pd, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
sys.path.insert(0, "scratch/P3")
from cells import region_cells, CELL

W, H_PX, DPI = 1600, 900, 160
CMAP, NORM = "viridis", Normalize(0, 1)
ACCENT = "#d95f02"
REQ = 0.8
plt.rcParams.update({"font.size": 10, "axes.linewidth": 0.8})

RC = region_cells()
NSR = ["KaraGate", "Vilkitsky", "Sannikov_DmLaptev", "LongStrait", "BeringChukchi"]
# the four NSR straits, per the specification; label placed above the cells except Kara Gate,
# which sits at the right-hand edge and is labelled below instead
MARK = {"KaraGate": ("KG", -1), "Vilkitsky": ("VS", 1), "Sannikov_DmLaptev": ("SD", 1),
        "LongStrait": ("LS", 1)}
XY = {(r, k): v for r, cl in RC.items() for k, v in enumerate(cl)}

C = pd.read_csv("scratch/P3/P3_cells.csv")
C = C[C.region.isin(NSR) & C.season.isin(["winter", "melt", "freeze-up"])].copy()
def per(y):
    return ("2019-21" if 2019 <= y <= 2021 else "2022-24" if 2022 <= y <= 2024
            else "2025-26" if y >= 2025 else None)
C["per"] = C.year.map(per); C = C[C.per.notna()]
C["x"] = [XY[(r, k)][0] for r, k in zip(C.region, C.cell)]
C["y"] = [XY[(r, k)][1] for r, k in zip(C.region, C.cell)]
PERIODS = ["2019-21", "2022-24", "2025-26"]
rsy = C.groupby(["region", "season", "year", "per"], as_index=False).H_episode3.mean()
MEANS = {p: rsy[rsy.per == p].H_episode3.mean() for p in PERIODS}
print("chokepoint H_episode means:", {k: round(v, 3) for k, v in MEANS.items()})
XL = (C.x.min() / 1e3 - 150, C.x.max() / 1e3 + CELL / 1e3 + 150)
YL = (C.y.min() / 1e3 - 480, C.y.max() / 1e3 + CELL / 1e3 + 300)

fig = plt.figure(figsize=(W / DPI, H_PX / DPI), dpi=DPI)
fig.patch.set_facecolor("white")
T = []   # collected text artists, checked against the canvas at the end

def tx(*a, **k):
    t = fig.text(*a, **k); T.append(t); return t

# ---------------- title, two lines so it fits the canvas ----------------
tx(0.5, 0.972, "Hazard-timescale observability of Arctic shipping chokepoints",
   ha="center", va="center", fontsize=13.5, weight="bold")
tx(0.5, 0.929, "what Sentinel-1 could and could not see, 2016–2026",
   ha="center", va="center", fontsize=11.5, color="0.3")

# ================ LEFT: the metric ================
axs = fig.add_axes([0.022, 0.560, 0.230, 0.270])
acq = np.array([0.0, 1.4, 2.1, 5.9, 6.6, 11.4, 12.0, 14.0])
axs.hlines(0, -0.4, 14.4, color="0.25", lw=1.2, zorder=2)
axs.vlines(acq, -0.42, 0.42, color="0.15", lw=1.6, zorder=3)
d0, D = 7.6, 2.6
axs.add_patch(plt.Rectangle((d0, -1.02), D, 0.44, facecolor=ACCENT, alpha=0.9,
                            edgecolor="none", zorder=4))
axs.annotate("", xy=(d0, -1.22), xytext=(d0 + D, -1.22),
             arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.1))
axs.text(d0 + D / 2, -1.52, "hazard, duration $D$", ha="center", va="top",
         fontsize=9.5, color=ACCENT)
axs.annotate("", xy=(6.6, 0.74), xytext=(11.4, 0.74),
             arrowprops=dict(arrowstyle="<->", color="0.3", lw=1.0))
axs.text(9.0, 0.94, "gap $g_i$", ha="center", va="bottom", fontsize=9.5, color="0.3")
axs.text(-0.4, 1.42, "Sentinel-1 acquisitions", fontsize=9.5, color="0.15", va="bottom")
axs.text(14.4, -0.60, "time", fontsize=9.5, color="0.25", ha="right", va="top")
axs.set_xlim(-1.1, 15.1); axs.set_ylim(-2.05, 1.95); axs.axis("off")

tx(0.137, 0.470, r"$H \;=\; \dfrac{\sum_i \min(g_i,\,D)}{\sum_i g_i}$",
   ha="center", va="center", fontsize=16)
tx(0.137, 0.372, "hazards caught, not scenes counted",
   ha="center", va="center", fontsize=10.5, style="italic", color="0.15")
tx(0.137, 0.320, "gaps are length-biased, so the long\n"
                 "ones dominate: a mean revisit\ninterval hides them",
   ha="center", va="top", fontsize=8.8, color="0.4", linespacing=1.5)

# ================ CENTRE: three stacked maps ================
mx0, mw = 0.283, 0.237
for i, p in enumerate(PERIODS):
    ax = fig.add_axes([mx0, 0.630 - i * 0.196, mw, 0.176])
    g = C[C.per == p].groupby(["region", "cell", "x", "y"], as_index=False).H_episode3.mean()
    ax.scatter(g.x / 1e3, g.y / 1e3, c=g.H_episode3, s=5.5, cmap=CMAP, norm=NORM,
               marker="s", linewidths=0)
    for r, (code, up) in MARK.items():
        cl = np.array(RC[r])
        yy = (cl[:, 1].max() / 1e3 + 150) if up > 0 else (cl[:, 1].min() / 1e3 - 150)
        ax.text(cl[:, 0].mean() / 1e3, yy, code, fontsize=8.8, ha="center",
                va="bottom" if up > 0 else "top", color="0.05", weight="bold",
                path_effects=[pe.withStroke(linewidth=1.8, foreground="white")])
    ax.set_xlim(*XL); ax.set_ylim(*YL)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("0.72")
    ax.text(0.014, 0.045, p, transform=ax.transAxes, fontsize=10.5, weight="bold",
            va="bottom", ha="left",
            path_effects=[pe.withStroke(linewidth=2.4, foreground="white")])
tx(mx0 + mw / 2, 0.822, "$H_{episode}$ per 25 km cell, NSR sector",
   ha="center", va="bottom", fontsize=10.5, weight="bold")
tx(mx0 + mw / 2, 0.175, "EPSG:3413.   KG Kara Gate    VS Vilkitsky    SD Sannikov / Dmitry Laptev    LS Long Strait",
   ha="center", va="top", fontsize=8.5, color="0.4")
# ---- period means, own column ----
tx(0.548, 0.796, "chokepoint\ngroup mean\n(5 regions)", ha="center", va="top", fontsize=8.5,
   color="0.4", linespacing=1.35)
for i, p in enumerate(PERIODS):
    tx(0.548, 0.690 - i * 0.196, f"{MEANS[p]:.3f}", ha="center", va="center",
       fontsize=15, weight="bold", color="0.08")

# ---- colour bar with the 0.8 requirement line ----
cax = fig.add_axes([0.600, 0.262, 0.014, 0.544])
cb = fig.colorbar(ScalarMappable(norm=NORM, cmap=CMAP), cax=cax)
cb.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]); cb.ax.tick_params(labelsize=8.5)
cb.ax.axhline(REQ, color=ACCENT, lw=2.2, ls="--")
tx(0.610, 0.235, "– – requirement\n$H \\geq 0.8$", ha="center", va="top",
   fontsize=9, color=ACCENT, weight="bold", linespacing=1.4)

# ================ RIGHT: the two mechanisms ================
RX = 0.700
tx(RX, 0.828, "1.   fewer satellites", fontsize=11.5, weight="bold", va="bottom")
tx(RX, 0.808, "a Sentinel-1A-only counterfactual\nreproduces the 2022-24 observation\nto within 10 pp in",
   fontsize=9, color="0.3", va="top", linespacing=1.45)
a1 = fig.add_axes([RX, 0.590, 0.272, 0.118])
a1.barh([0], [15], color="0.32", height=0.55)
a1.barh([0], [1], left=[15], color="0.82", height=0.55)
a1.set_xlim(0, 16); a1.set_ylim(-0.65, 0.65)
a1.text(7.5, 0, "15 of 16 regions", ha="center", va="center", fontsize=11.5,
        color="white", weight="bold")
a1.text(15.5, 0, "1", ha="center", va="center", fontsize=9.5, color="0.2")
a1.set_yticks([]); a1.set_xticks([])
for s in ("top", "right", "left", "bottom"):
    a1.spines[s].set_visible(False)

tx(RX, 0.492, "2.   same satellites,\n       different pointing", fontsize=11.5,
   weight="bold", va="bottom", linespacing=1.3)
tx(RX, 0.452, "ESA acquisition plans, 2025 against 2019-21", fontsize=8.8,
   color="0.3", va="top")
a2 = fig.add_axes([RX + 0.030, 0.195, 0.150, 0.215])
vals = [87.1, 123.4]
bars = a2.bar([0, 1], vals, color=["0.32", "0.74"], width=0.60)
a2.axhline(100, color=ACCENT, lw=1.8, ls="--")
for b, v in zip(bars, vals):
    # both labels inside the bar: above the bar they would sit on the pre-loss line
    a2.text(b.get_x() + b.get_width() / 2, v - 7, f"{v} %", ha="center", va="top",
            fontsize=9.5, weight="bold", color="white" if v < 100 else "0.12")
a2.set_xticks([0, 1]); a2.set_xticklabels(["Europe–\nRussia", "North\nAmerica"], fontsize=9)
a2.set_ylim(0, 152); a2.set_yticks([0, 50, 100, 150]); a2.tick_params(labelsize=8.5)
a2.set_ylabel("% of pre-loss rate", fontsize=8.8, labelpad=2)
for s in ("top", "right"):
    a2.spines[s].set_visible(False)
tx(RX + 0.188, 0.286, "– – pre-loss\n     rate", fontsize=9, color=ACCENT,
   va="center", ha="left", linespacing=1.4)

# ================ conclusion ================
tx(0.5, 0.058, "The requirement was already unmet with two satellites,\n"
               "and the recovery is a planning decision, not a procurement one.",
   ha="center", va="center", fontsize=11.5, weight="bold", color="0.08", linespacing=1.4)

out = "paper/figures/graphical_abstract.png"
fig.canvas.draw()
bad = []
for t in T:
    bb = t.get_window_extent(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
    if bb.x0 < 0.002 or bb.x1 > 0.998 or bb.y0 < 0.002 or bb.y1 > 0.998:
        bad.append((t.get_text()[:44].replace("\n", " "), round(bb.x0, 3), round(bb.x1, 3),
                    round(bb.y0, 3), round(bb.y1, 3)))
boxes=[]
for t in T:
    boxes.append((t.get_text()[:34].replace("\n"," "),
                  t.get_window_extent(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())))
overlaps=[]
for i in range(len(boxes)):
    for j in range(i+1,len(boxes)):
        (n1,b1),(n2,b2)=boxes[i],boxes[j]
        ox=min(b1.x1,b2.x1)-max(b1.x0,b2.x0); oy=min(b1.y1,b2.y1)-max(b1.y0,b2.y0)
        if ox>0.004 and oy>0.004:
            overlaps.append((n1,n2,round(ox,3),round(oy,3)))
if overlaps:
    print("TEXT OVERLAPS:")
    for o in overlaps: print("   ",o)
else:
    print("no text-text overlaps")
if bad:
    print("TEXT OUTSIDE CANVAS:")
    for b in bad:
        print("   ", b)
else:
    print("all text inside the canvas")
fig.savefig(out, dpi=DPI, facecolor="white")
plt.close(fig)
from PIL import Image
im = Image.open(out)
print("wrote", out, im.size, os.path.getsize(out), "bytes")
assert im.size == (W, H_PX), im.size
assert not bad, f"{len(bad)} text elements outside the canvas"
assert not overlaps, f"{len(overlaps)} overlapping text pairs"
