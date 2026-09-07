"""ARC-P14 item 3 — Figure 4 (new): H by region and season-period, values printed in cells.
Rows are the sixteen regions grouped by sector, columns are season x period.
(a) H_state, (b) H_episode, both >= 3 km class. Double column, 190 mm.
Layout is specified in inches and converted, so nothing collides.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F, regmap as M
from matplotlib.cm import ScalarMappable
import matplotlib.cm as cm

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
F.use()

ROWNAME = dict(M.NAME); ROWNAME["Sannikov_DmLaptev"] = "Sannikov"
EUR = ["KaraGate", "Vilkitsky", "Sannikov_DmLaptev", "LongStrait",
       "Barents_Svalbard", "GreenlandSea_Fram"]
NAM = ["BeringChukchi"] + [f"AKcorr_{i}" for i in range(1, 7)] + \
      ["BaffinBay", "LancasterSound", "VictoriaStrait"]
ROWS = EUR + NAM
SEASONS = ["freeze-up", "winter", "melt"]
PERIODS = [("pre", "2019–21"), ("during", "2022–24"), ("post", "2025–26")]
COLS = [(s, p) for s in SEASONS for p, _ in PERIODS]
NC, NR, NEUR = len(COLS), len(ROWS), len(EUR)

def per(y):
    return ("pre" if 2019 <= y <= 2021 else "during" if 2022 <= y <= 2024
            else "post" if y >= 2025 else None)
A = pd.read_csv("scratch/P3/P3_region_season_year.csv")
A["per"] = A.year.map(per); A = A[A.per.notna()]
G = A.groupby(["region", "season", "per"])[["H_state3", "H_episode3"]].mean()

# ---- layout in inches ----
ROW_IN, NOTE_IN, LAB_IN, HDR_IN, XT_IN, CB_IN, GAP_IN = 0.132, 0.17, 0.20, 0.19, 0.46, 0.52, 0.10
PANEL_IN = ROW_IN * NR
FIG_H = NOTE_IN + 2 * (LAB_IN + HDR_IN + PANEL_IN) + XT_IN + CB_IN + GAP_IN
LEFT, RIGHT = 0.148, 0.020
pw = 1 - LEFT - RIGHT
def fr(v):
    return v / FIG_H

fig = F.figure(F.W2, FIG_H)
fig.text(0.004, 1 - fr(0.035),
         "Rows: European–Russian sector above the rule, North American–Bering below. "
         "Chokepoint-group regions in bold red. Leading zeros dropped.",
         fontsize=7, color="0.30", va="top", ha="left")

def panel(top_in, col, letter, label, xticks):
    y0 = 1 - fr(top_in + PANEL_IN)
    ax = fig.add_axes([LEFT, y0, pw, fr(PANEL_IN)])
    Z = np.full((NR, NC), np.nan)
    for i, r in enumerate(ROWS):
        for j, (s, p) in enumerate(COLS):
            try:
                Z[i, j] = G.loc[(r, s, p), col]
            except KeyError:
                pass
    ax.imshow(Z, aspect="auto", cmap=F.H_CMAP, norm=F.H_NORM,
              extent=[0, NC, NR, 0], interpolation="nearest")
    for i in range(NR):
        for j in range(NC):
            v = Z[i, j]
            if not np.isfinite(v):
                continue
            rgb = cm.viridis(F.H_NORM(v))[:3]
            fc = "white" if (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) < 0.55 else "0.05"
            ax.text(j + 0.5, i + 0.56, f"{v:.2f}".lstrip("0"), ha="center", va="center",
                    fontsize=7, color=fc)
    for j in range(3, NC, 3):
        ax.axvline(j, color="white", lw=1.5)
    ax.axhline(NEUR, color="white", lw=1.5)
    ax.set_yticks(np.arange(NR) + 0.5)
    ax.set_yticklabels([ROWNAME[r] for r in ROWS], fontsize=7)
    for i, r in enumerate(ROWS):
        if r in M.CHSET:
            ax.get_yticklabels()[i].set_fontweight("bold")
            ax.get_yticklabels()[i].set_color("#b2182b")
    if xticks:
        ax.set_xticks(np.arange(NC) + 0.5)
        ax.set_xticklabels([lab for _ in SEASONS for _, lab in PERIODS], fontsize=7, rotation=90)
    else:
        ax.set_xticks([])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.text(0.004, 1 - fr(top_in - HDR_IN - 0.02), f"{letter}  {label}",
             fontsize=8.5, fontweight="bold", va="top", ha="left")
    for k, s in enumerate(SEASONS):
        fig.text(LEFT + pw * (3 * k + 1.5) / NC, 1 - fr(top_in - 0.025), s,
                 fontsize=7.5, fontweight="bold", ha="center", va="bottom")
    return ax

t1 = NOTE_IN + LAB_IN + HDR_IN
panel(t1, "H_state3", "(a)", "$H_{state}$, $\\geq$ 3 km class", False)
t2 = t1 + PANEL_IN + LAB_IN + HDR_IN
panel(t2, "H_episode3", "(b)", "$H_{episode}$, $\\geq$ 3 km class", True)

cy = fr(0.285)
cax = fig.add_axes([0.40, cy, 0.30, fr(0.045)])
cb = fig.colorbar(ScalarMappable(norm=F.H_NORM, cmap=F.H_CMAP), cax=cax, orientation="horizontal")
cb.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]); cb.ax.tick_params(labelsize=7, pad=1.5)
cb.set_label("$H$   (1 = every hazard caught)", fontsize=7.5, labelpad=1)
cb.ax.plot([0.8, 0.8], [0, 1], color=F.ACCENT, lw=1.5, transform=cb.ax.transAxes, clip_on=False)
fig.text(0.715, cy, "  requirement 0.8", fontsize=7, color=F.ACCENT, va="bottom", ha="left")

F.save(fig, "fig04_H_heatmap.png", F.W2)
