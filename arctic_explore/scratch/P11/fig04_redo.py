import pandas as pd, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, os
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
plt.rcParams.update({"font.size":8,"axes.titlesize":9,"axes.labelsize":8,"figure.dpi":150,"savefig.dpi":150})
V=pd.read_csv("scratch/P11/ose_region_valid.csv")
CH=["Vilkitsky","Sannikov_DmLaptev","LongStrait","KaraGate","BeringChukchi"]
fig,axes=plt.subplots(1,3,figsize=(8.6,3.0),sharey=True)
for ax,season in zip(axes,["freeze-up","winter","melt"]):
    for lab,sub,c,m in (("all regions",V,"0.35","o"),("NSR chokepoints",V[V.region.isin(CH)],"crimson","s")):
        s=sub[sub.season==season]
        g=s.groupby("nsat").H_state3.agg(["mean","std","count"])
        solid=g[g.index<=2]
        ax.errorbar(solid.index,solid["mean"],yerr=solid["std"],color=c,marker=m,lw=1.4,capsize=2,ms=4,label=lab)
        if 3 in g.index:
            ax.errorbar([3],[g.loc[3,"mean"]],yerr=[g.loc[3,"std"]],color=c,marker=m,ms=6,
                        mfc="none",mew=1.3,lw=0,capsize=2)
            ax.plot([2,3],[g.loc[2,"mean"],g.loc[3,"mean"]],color=c,lw=0.9,ls=":")
    ax.axhline(0.8,color="k",ls="--",lw=0.9)
    ax.set_xticks([1,2,3]); ax.set_xlabel("number of SAR platforms"); ax.set_title(season)
    ax.set_ylim(0,1.0)
axes[0].set_ylabel("$H_{state}$ (>=3 km)")
axes[0].text(1.02,0.83,"requirement 0.8",fontsize=6.5)
axes[2].text(2.15,0.10,"hollow: provisional,\nmelt 2026 only (n=9)",fontsize=6,color="0.25")
axes[0].legend(fontsize=6.5,frameon=False,loc="lower right")
fig.suptitle("Constellation design curve, matched season windows (valid platform combinations only)",fontsize=9.5)
fig.tight_layout(); fig.savefig("paper/figures/fig04_design_curve.png",bbox_inches="tight"); plt.close(fig)
print("fig4 redone")
