"""ARC-P14 item 1 — Figure 1: construction of H.
Keeps the P10 design. Panel (a) gains a second hazard lying entirely inside g5, drawn as an
open rectangle labelled "missed", beside the filled caught hazard. Panel (b) gains the dashed
H = 0.8 requirement line.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as F
import matplotlib.pyplot as plt

F.use()
G = np.array([6, 9, 40, 12, 70, 8, 30], float)     # gaps, hours
T = np.concatenate([[0], np.cumsum(G)])            # acquisition times

fig = F.figure(F.W2, 2.55)
axa = fig.add_axes([0.052, 0.235, 0.545, 0.60])
axb = fig.add_axes([0.705, 0.235, 0.268, 0.60])

# ---------------- (a) acquisitions, gaps, one caught and one missed hazard ----------------
axa.vlines(T, 0.42, 1.0, color="0.15", lw=1.0, zorder=3)
axa.hlines(0.42, T[0], T[-1], color="0.55", lw=0.6, zorder=2)
for i in range(len(G)):
    axa.annotate("", xy=(T[i], 1.12), xytext=(T[i + 1], 1.12),
                 arrowprops=dict(arrowstyle="<->", lw=0.5, color=F.GREY,
                                 shrinkA=0, shrinkB=0))
    axa.text((T[i] + T[i + 1]) / 2, 1.20, f"$g_{{{i+1}}}$", ha="center", va="bottom",
             fontsize=7, color=F.GREY)

# caught: straddles the acquisition at t = 55 h
c0, cD = 45.0, 20.0
axa.add_patch(plt.Rectangle((c0, 0.08), cD, 0.24, facecolor=F.ACCENT, edgecolor=F.ACCENT,
                            lw=0.6, zorder=4))
axa.annotate("caught", xy=(c0 + cD / 2, 0.06), xytext=(c0 + cD / 2, -0.20),
             ha="center", va="top", fontsize=7, color=F.ACCENT, fontweight="bold",
             arrowprops=dict(arrowstyle="-", lw=0.5, color=F.ACCENT))
# missed: begins and ends inside g5 (67 h to 137 h)
m0, mD = 86.0, 20.0   # identical duration, but inside g5
axa.add_patch(plt.Rectangle((m0, 0.08), mD, 0.24, facecolor="none", edgecolor=F.ACCENT,
                            lw=0.8, ls=(0, (2.2, 1.4)), zorder=4))
axa.annotate("missed", xy=(m0 + mD / 2, 0.06), xytext=(m0 + mD / 2, -0.20),
             ha="center", va="top", fontsize=7, color=F.ACCENT,
             arrowprops=dict(arrowstyle="-", lw=0.5, color=F.ACCENT))
axa.annotate("acquisitions", xy=(T[0], 0.70), xytext=(-4, 0.70), ha="right", va="center",
             fontsize=7, color="0.15")
axa.set_xlim(-42, T[-1] + 4)
axa.set_ylim(-0.42, 1.42)
axa.set_yticks([])
axa.set_xlabel("time (h)")
axa.set_xticks([0, 50, 100, 150])
for s in ("top", "right", "left"):
    axa.spines[s].set_visible(False)
axa.set_title("(a)  acquisitions, gaps $g_i$, and two hazards of the same duration", loc="left",
              fontsize=8)

# ---------------- (b) H against hazard duration ----------------
D = np.linspace(0, 60, 600)
for gg, c, ls in ((12, "0.15", "-"), (24, "0.45", (0, (4, 1.5))), (48, "0.68", (0, (1.4, 1.2)))):
    axb.plot(D, np.minimum(1, D / gg), color=c, lw=0.9, ls=ls, label=f"single gap, {gg} h")
axb.plot(D, [np.minimum(G, d).sum() / G.sum() for d in D], color=F.ACCENT, lw=1.6,
         label="length-biased mixture of (a)")
axb.axhline(0.8, color="0.15", ls=(0, (3.5, 2.0)), lw=0.8, zorder=1)
axb.text(0.8, 0.815, "requirement $H = 0.8$", ha="left", va="bottom", fontsize=7, color="0.15")
axb.set_xlabel("hazard duration $D$ (h)")
axb.set_ylabel("$H$")
axb.set_xlim(0, 60); axb.set_ylim(0, 1.04)
axb.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
axb.legend(fontsize=7, loc="lower right", handlelength=1.9, borderpad=0.2,
           labelspacing=0.32, handletextpad=0.5)
for s in ("top", "right"):
    axb.spines[s].set_visible(False)
axb.set_title("(b)  $H(D)$", loc="left", fontsize=8)

F.save(fig, "fig01_H_schematic.png", F.W2)
