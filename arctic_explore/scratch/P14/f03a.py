"""ARC-P14 item 3 — Figure 3(a): overview map. EPSG:3413, Natural Earth 50m coastline and
light land fill, graticule, all sixteen region boxes drawn and labelled with leader lines,
the five-region chokepoint group highlighted.

Labels sit in the figure margins and are anchored with textcoords="figure fraction" so the
leader lines cross the axes boundary; annotation_clip=False keeps them drawn.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F, basemap as B, regmap as M
from matplotlib.lines import Line2D

F.use()
(x0, x1), (y0, y1) = M.all_extent(110)
XL, YL = (x0, x1), (y0, y1)
AXW = 0.585
axw_in = AXW * F.W2
axh_in = axw_in * (YL[1] - YL[0]) / (XL[1] - XL[0])
BOT, TOP = 0.115, 0.055                      # figure fractions reserved below / above the axes
FIG_H = axh_in / (1.0 - BOT - TOP)
AXL = (1.0 - AXW) / 2.0

# (figure-fraction x, figure-fraction y, horizontal alignment)
LAB = {
    "Sannikov_DmLaptev": (0.985, 0.930, "right"),
    "Vilkitsky":         (0.985, 0.845, "right"),
    "KaraGate":          (0.985, 0.760, "right"),
    "Barents_Svalbard":  (0.985, 0.430, "right"),
    "GreenlandSea_Fram": (0.985, 0.345, "right"),
    "BaffinBay":         (0.985, 0.190, "right"),
    "LongStrait":        (0.015, 0.930, "left"),
    "BeringChukchi":     (0.015, 0.845, "left"),
    "AKcorr_1":          (0.015, 0.752, "left"),
    "AKcorr_2":          (0.015, 0.699, "left"),
    "AKcorr_3":          (0.015, 0.646, "left"),
    "AKcorr_4":          (0.015, 0.593, "left"),
    "AKcorr_5":          (0.015, 0.540, "left"),
    "AKcorr_6":          (0.015, 0.487, "left"),
    "VictoriaStrait":    (0.015, 0.300, "left"),
    "LancasterSound":    (0.015, 0.215, "left"),
}
CH_EDGE = "#b2182b"
AK_EDGE = "#4393c3"
OT_EDGE = "#2166ac"

fig = F.figure(F.W2, FIG_H)
ax = fig.add_axes([AXL, BOT, AXW, 1.0 - BOT - TOP])
ax.set_aspect("equal")
B.draw(ax, XL, YL, dlon=30, dlat=5)

for r in M.ORDER:
    x, y = M.box_xy(r)
    ch = r in M.CHSET
    ec = CH_EDGE if ch else (AK_EDGE if r in M.AK else OT_EDGE)
    if ch:
        ax.fill(x, y, facecolor=CH_EDGE, alpha=0.32, edgecolor="none", zorder=3)
    ax.plot(x, y, color=ec, lw=1.3 if ch else 0.7, zorder=4,
            ls="-" if r not in M.AK else (0, (2.4, 1.3)))

for r, (fx, fy, ha) in LAB.items():
    cx, cy = M.centroid(r)
    ch = r in M.CHSET
    ax.annotate(M.NAME[r] + (f" ({M.SHORT[r]})" if ch else ""),
                xy=(cx, cy), xycoords="data", xytext=(fx, fy), textcoords="figure fraction",
                ha=ha, va="center", fontsize=7.5 if ch else 7,
                fontweight="bold" if ch else "normal",
                color=CH_EDGE if ch else "0.12", zorder=6, annotation_clip=False,
                arrowprops=dict(arrowstyle="-", lw=0.45,
                                color=CH_EDGE if ch else "0.55", shrinkA=0.5, shrinkB=1.5))

# graticule labels: two parallels where they are legible, plus the pole
ax.text(0, 0, "90° N", fontsize=7, color="0.42", ha="center", va="bottom", zorder=5)
for lat in (70, 80):
    px, py = M.FWD.transform(-35.0, lat)
    ax.text(px / 1e3, py / 1e3, f"{lat}° N", fontsize=7, color="0.42", ha="center",
            va="center", zorder=5,
            bbox=dict(boxstyle="square,pad=0.08", fc="white", ec="none", alpha=0.75))
sbx, sby = XL[0] + 170, YL[0] + 150
ax.plot([sbx, sbx + 1000], [sby, sby], color="0.1", lw=1.8, solid_capstyle="butt", zorder=7)
ax.text(sbx + 500, sby + 75, "1000 km", fontsize=7, ha="center", va="bottom", color="0.1", zorder=7)

ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_color("0.55")

fig.legend(handles=[
    Line2D([], [], color=CH_EDGE, lw=1.3,
           label="chokepoint group: 5 regions, the basis of every chokepoint statistic"),
    Line2D([], [], color=AK_EDGE, lw=0.7, ls=(0, (2.4, 1.3)),
           label="Alaskan corridor sectors AK1–AK6, overlapping Bering–Chukchi"),
    Line2D([], [], color=OT_EDGE, lw=0.7, label="contrast regions")],
    loc="lower center", bbox_to_anchor=(0.5, 0.005), ncol=1, fontsize=7,
    handlelength=2.2, labelspacing=0.35, borderpad=0.2)
fig.text(0.015, 1 - TOP + 0.012, "(a)  the sixteen study regions, 1,771 cells of 25 km on EPSG:3413; "
         "graticule 30° meridians, 5° parallels",
         fontsize=8.5, fontweight="bold", va="bottom", ha="left")

F.save(fig, "fig03a_overview.png", F.W2)
