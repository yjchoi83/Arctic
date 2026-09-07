"""ARC-P14 — Figure 7 (was Fig. 6): constellation design curve within matched season windows.
Content unchanged from the P11 version (admissible platform combinations only, from
scratch/P11/ose_region_valid.csv); restyled to 300 dpi, 190 mm, one font family, >= 7 pt.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F, regmap as M

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

V = pd.read_csv("scratch/P11/ose_region_valid.csv")
SEASONS = ["freeze-up", "winter", "melt"]
GROUPS = (("all sixteen regions", V, "0.25", "o"),
          ("chokepoint group", V[V.region.isin(M.CH)], "#b2182b", "s"))

L, R_, TOPM, BOT, GX = 0.075, 0.012, 0.115, 0.290, 0.022
pw = (1 - L - R_ - 2 * GX) / 3
fig = F.figure(F.W2, 2.55)
axs = []
for k, season in enumerate(SEASONS):
    ax = fig.add_axes([L + k * (pw + GX), BOT, pw, 1 - TOPM - BOT])
    for lab, sub, c, m in GROUPS:
        g = sub[sub.season == season].groupby("nsat").H_state3.agg(["mean", "std", "count"])
        sol = g[g.index <= 2]
        ax.errorbar(sol.index, sol["mean"], yerr=sol["std"], color=c, marker=m, lw=1.2,
                    capsize=1.8, ms=3.4, elinewidth=0.7,
                    label=lab if k == 0 else None)
        if 3 in g.index:
            ax.errorbar([3], [g.loc[3, "mean"]], yerr=[g.loc[3, "std"]], color=c, marker=m,
                        ms=5.0, mfc="none", mew=1.0, lw=0, capsize=1.8, elinewidth=0.7)
            ax.plot([2, 3], [g.loc[2, "mean"], g.loc[3, "mean"]], color=c, lw=0.7,
                    ls=(0, (1.3, 1.3)))
    ax.axhline(0.8, color=F.ACCENT, ls=(0, (3.5, 2.0)), lw=0.9, zorder=1)
    ax.set_xticks([1, 2, 3]); ax.set_xlim(0.7, 3.3); ax.set_ylim(0, 1.0)
    ax.set_xlabel("SAR platforms")
    ax.set_title(season, fontsize=8, pad=3)
    ax.grid(axis="y", color="0.90", lw=0.4); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if k == 0:
        ax.set_ylabel("$H_{state}$, $\\geq$ 3 km class")
    else:
        ax.tick_params(labelleft=False)
    axs.append(ax)

axs[0].text(0.74, 0.825, "requirement 0.8", fontsize=7, color=F.ACCENT, va="bottom")
axs[2].annotate("hollow: provisional,\nmelt 2026 only\n(n = 9 regions, two\nof them chokepoints)",
                xy=(3, 0.32), xytext=(1.42, 0.03), fontsize=7, color="0.3",
                ha="left", va="bottom",
                arrowprops=dict(arrowstyle="-", lw=0.5, color="0.55"))
fig.legend(*axs[0].get_legend_handles_labels(), loc="lower center",
           bbox_to_anchor=(0.5, 0.012), ncol=2, fontsize=7, handlelength=1.8,
           columnspacing=2.0, borderpad=0.2)
fig.text(0.004, 0.996,
         "A combination is admitted only when every platform in it acquired in that season; "
         "error bars are the standard deviation across region-year combinations",
         fontsize=7, color="0.35", va="top", ha="left")
F.save(fig, "fig07_design_curve.png", F.W2)
