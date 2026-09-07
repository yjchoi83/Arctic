"""ARC-P14 item 6 — Figure 8 (was Fig. 7): ESA planned acquisition segments against acquired
scenes, by region. Two panels titled by sector, planned 2022-24 bars added from Table 5,
logarithmic axis kept, legend below the axes.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F, regmap as M

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

# planned counts: the Table 5 source, which includes the gap years
P = pd.read_csv("scratch/P11/planned_with_gap.csv").set_index("region")
Aq = pd.read_csv("scratch/P9/planned_vs_acquired.csv").set_index("region")
EUR = [r for r in M.ORDER if P.loc[r, "sector"] == "EUR"]
NAM = [r for r in M.ORDER if P.loc[r, "sector"] == "NAM"]
EUR = sorted(EUR, key=lambda r: -P.loc[r, "pre"])
NAM = sorted(NAM, key=lambda r: -P.loc[r, "pre"])

SERIES = [
    ("planned 2019–21 / yr", lambda r: P.loc[r, "pre"], "#08519c"),
    ("planned 2022–24 / yr", lambda r: P.loc[r, "gap"], "#6baed6"),
    ("planned 2025",         lambda r: P.loc[r, "p25"], "#c6dbef"),
    ("acquired 2019–21 / yr", lambda r: Aq.loc[r, "acquired_pre"], "#7f2704"),
    ("acquired 2025–26 / yr", lambda r: Aq.loc[r, "acquired_post"], "#fdae6b"),
]

SHORT = dict(M.NAME)
SHORT.update({"Sannikov_DmLaptev": "Sannikov", "GreenlandSea_Fram": "Fram",
              "Barents_Svalbard": "Barents", "LancasterSound": "Lancaster",
              "VictoriaStrait": "Victoria", "BeringChukchi": "Bering–Ch."})
L, R_, TOPM, BOT, GAPX = 0.062, 0.012, 0.088, 0.335, 0.055
FIG_H = 3.55
fig = F.figure(F.W2, FIG_H)
tot = len(EUR) + len(NAM)
wtot = 1 - L - R_ - GAPX
axs = []
x0 = L
for regs, title in ((EUR, "European–Russian sector"), (NAM, "North American–Bering sector")):
    w = wtot * len(regs) / tot
    ax = fig.add_axes([x0, BOT, w, 1 - TOPM - BOT])
    x0 += w + GAPX
    i = np.arange(len(regs)); bw = 0.165
    for k, (lab, fn, c) in enumerate(SERIES):
        ax.bar(i + (k - 2) * bw, [fn(r) for r in regs], bw, color=c,
               label=lab if not axs else None, linewidth=0)
    ax.set_yscale("log")
    ax.set_ylim(20, 4e4)
    ax.set_xticks(i)
    ax.set_xticklabels([SHORT[r] for r in regs], rotation=90, ha="center", fontsize=7)
    for t, r in zip(ax.get_xticklabels(), regs):
        if r in M.CHSET:
            t.set_fontweight("bold"); t.set_color("#b2182b")
    ax.set_title(title, fontsize=8, pad=3)
    ax.tick_params(axis="x", length=0, pad=1.5)
    ax.grid(axis="y", color="0.88", lw=0.4, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if not axs:
        ax.set_ylabel("segments or scenes per year")
    else:
        ax.tick_params(labelleft=False)
    axs.append(ax)

fig.legend(*axs[0].get_legend_handles_labels(), loc="lower center",
           bbox_to_anchor=(0.5, 0.006), ncol=3, fontsize=7, handlelength=1.5,
           columnspacing=1.4, handletextpad=0.5, borderpad=0.2)
fig.text(0.004, 0.997, "chokepoint-group regions in bold red;  logarithmic axis",
         fontsize=7, color="0.35", va="top", ha="left")
F.save(fig, "fig08_planned_vs_acquired.png", F.W2)
