import numpy as np, pandas as pd, os, sys, glob, datetime as dt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.image as mpimg
from matplotlib.colors import Normalize
sys.path.insert(0,"scratch/P3"); sys.path.insert(0,"scratch/P2")
from cells import region_cells, CELL
from regions import regions
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
OUT="paper/figures"; os.makedirs(OUT,exist_ok=True)
plt.rcParams.update({"font.size":8,"axes.titlesize":9,"axes.labelsize":8,
                     "figure.dpi":150,"savefig.dpi":150,"axes.linewidth":0.6})
CMAP="viridis"; NORM=Normalize(0,1.0)
SHORT={"KaraGate":"Kara Gate","Vilkitsky":"Vilkitsky","Sannikov_DmLaptev":"Sannikov","LongStrait":"Long Str.",
 "BeringChukchi":"Bering-Chukchi","Barents_Svalbard":"Barents/Svalbard","GreenlandSea_Fram":"Fram",
 "BaffinBay":"Baffin","LancasterSound":"Lancaster","VictoriaStrait":"Victoria Str.",
 **{f"AKcorr_{i}":f"AK{i}" for i in range(1,7)}}
CH={"Vilkitsky","Sannikov_DmLaptev","LongStrait","KaraGate","BeringChukchi"}
RC=region_cells(); R=regions()

# ---- Fig 1: schematic of H ----
fig,ax=plt.subplots(1,2,figsize=(7.2,2.6))
g=np.array([6,9,40,12,70,8,30]); t=np.concatenate([[0],np.cumsum(g)])
ax[0].vlines(t,0,1,color="k",lw=1.2)
for i in range(len(g)):
    ax[0].annotate("",xy=(t[i+1],0.5),xytext=(t[i],0.5),arrowprops=dict(arrowstyle="<->",lw=0.7,color="0.4"))
    ax[0].text((t[i]+t[i+1])/2,0.58,f"$g_{{{i+1}}}$",ha="center",fontsize=7)
ax[0].add_patch(plt.Rectangle((52,0.12),12,0.18,color="crimson",alpha=0.75))
ax[0].text(58,0.05,"hazard, duration $D$",ha="center",color="crimson",fontsize=7)
ax[0].set_xlim(-4,180); ax[0].set_ylim(0,1); ax[0].set_yticks([]); ax[0].set_xlabel("time (h)")
ax[0].set_title("(a) acquisitions, gaps $g_i$, and a hazard")
D=np.linspace(0,60,300)
for gg,c in ((12,"0.2"),(24,"0.45"),(48,"0.7")):
    ax[1].plot(D,np.minimum(1,D/gg),color=c,lw=1.3,label=f"single gap {gg} h")
ax[1].plot(D,[np.minimum(g,d).sum()/g.sum() for d in D],color="crimson",lw=1.8,label="length-biased mix (a)")
ax[1].set_xlabel("hazard duration $D$ (h)"); ax[1].set_ylabel("$H$"); ax[1].set_ylim(0,1.02)
ax[1].legend(fontsize=6.5,frameon=False); ax[1].set_title("(b) $H=E_D[\\sum_i \\min(g_i,D)]/\\sum_i g_i$")
fig.tight_layout(); fig.savefig(f"{OUT}/fig01_H_schematic.png",bbox_inches="tight"); plt.close(fig)

# ---- Fig 2: hazard duration / persistence by class ----
z=np.load("scratch/P3/step2t_native1h.npz"); ed,em=z["dur"].astype(float),z["mag"].astype(float)
P=pd.read_csv("scratch/P1b/events_persist.csv"); P=P[P.season!="shoulder"].copy()
P["relmag"]=P.magnitude_km/P.sep_start_km; Pr=P[P.relmag>=0.10]
fig,ax=plt.subplots(1,2,figsize=(7.2,2.8))
for lo,hi,lab in ((1,3,"1-3 km"),(3,5,"3-5 km"),(5,np.inf,">=5 km")):
    v=ed[(em>=lo)&(em<hi)]
    if len(v)>20:
        x=np.sort(v); ax[0].plot(x,np.arange(1,len(x)+1)/len(x),lw=1.3,label=f"{lab} (n={len(v)})")
ax[0].set_xscale("log"); ax[0].set_xlabel("episode duration (h, 1-h sampling)"); ax[0].set_ylabel("cumulative fraction")
ax[0].axvline(12,color="crimson",ls="--",lw=0.9); ax[0].text(12.5,0.06,"12 h",color="crimson",fontsize=7)
ax[0].legend(fontsize=6.5,frameon=False); ax[0].set_title("(a) episode duration by magnitude class")
for lo,hi,lab in ((1,3,"1-3 km"),(3,5,"3-5 km"),(5,np.inf,">=5 km")):
    v=Pr[(Pr.magnitude_km>=lo)&(Pr.magnitude_km<hi)].persist_h.values
    if len(v)>20:
        x=np.sort(v); ax[1].plot(x,np.arange(1,len(x)+1)/len(x),lw=1.3,label=f"{lab} (n={len(v)})")
ax[1].set_xscale("log"); ax[1].set_xlabel("state persistence (h, 3-h sampling)")
ax[1].axvline(24,color="crimson",ls="--",lw=0.9); ax[1].text(25,0.06,"24 h",color="crimson",fontsize=7)
ax[1].legend(fontsize=6.5,frameon=False); ax[1].set_title("(b) persistence, relative magnitude >= 10 %")
fig.tight_layout(); fig.savefig(f"{OUT}/fig02_hazard_timescales.png",bbox_inches="tight"); plt.close(fig)
print("fig1,2 ok",flush=True)

# ---- Fig 3: H maps per 25 km cell, EPSG:3413, with region labels ----
C=pd.read_csv("scratch/P3/P3_cells.csv")
def per(y): return "pre 2019-21" if 2019<=y<=2021 else ("during 2022-24" if 2022<=y<=2024 else ("post 2025-26" if y>=2025 else None))
C["per"]=C.year.map(per); C=C[C.per.notna()]
XY={(r,k):v for r,cl in RC.items() for k,v in enumerate(cl)}
C["x"]=[XY[(r,k)][0] for r,k in zip(C.region,C.cell)]; C["y"]=[XY[(r,k)][1] for r,k in zip(C.region,C.cell)]
CENT={r:(np.mean([a for a,b in cl])+CELL/2,np.mean([b for a,b in cl])+CELL/2) for r,cl in RC.items()}
for col,lab in (("H_state3","$H_{state}$ (>=3 km)"),("H_episode3","$H_{episode}$ (>=3 km)")):
    fig,axes=plt.subplots(3,3,figsize=(8.4,8.0))
    for i,season in enumerate(("freeze-up","winter","melt")):
        for j,p in enumerate(("pre 2019-21","during 2022-24","post 2025-26")):
            ax=axes[i,j]
            g=C[(C.season==season)&(C.per==p)].groupby(["region","cell","x","y"],as_index=False)[col].mean()
            sc=ax.scatter(g.x/1e3,g.y/1e3,c=g[col],s=2.2,cmap=CMAP,norm=NORM,marker="s",linewidths=0)
            for r,(cx,cy) in CENT.items():
                if r in CH: ax.text(cx/1e3,cy/1e3,SHORT[r],fontsize=4.6,ha="center",va="center",
                                    color="w",weight="bold",zorder=5)
            ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
            if i==0: ax.set_title(p,fontsize=8)
            if j==0: ax.set_ylabel(season,fontsize=8)
    cb=fig.colorbar(sc,ax=axes,fraction=0.020,pad=0.01); cb.set_label(lab+"   (1.0 = every hazard caught)",fontsize=7.5)
    fig.suptitle(f"{lab} per 25 km cell, EPSG:3413 (chokepoints labelled)",fontsize=10)
    fig.savefig(f"{OUT}/fig03_{col}_maps.png",bbox_inches="tight"); plt.close(fig)
print("fig3 ok",flush=True)

# ---- Fig 4: design curve ----
O=pd.read_csv("scratch/P6/ose_region.csv")
O["per"]=np.where(O.year.between(2019,2021),"pre 2019-21","post 2025-26")
fig,ax=plt.subplots(figsize=(4.2,3.0))
for lab,sub,c,m in (("all regions",O,"0.35","o"),("NSR chokepoints",O[O.region.isin(CH)],"crimson","s")):
    g=sub.groupby("nsat").H_state3.agg(["mean","std"])
    ax.errorbar(g.index,g["mean"],yerr=g["std"],color=c,marker=m,lw=1.4,capsize=2,label=lab,ms=4)
ax.axhline(0.8,color="k",ls="--",lw=0.9); ax.text(1.05,0.82,"requirement 0.8",fontsize=7)
ax.set_xticks([1,2,3]); ax.set_xlabel("number of SAR platforms"); ax.set_ylabel("$H_{state}$ (>=3 km)")
ax.set_ylim(0,1.0); ax.legend(fontsize=7,frameon=False); ax.set_title("Constellation design curve")
fig.tight_layout(); fig.savefig(f"{OUT}/fig06_design_curve.png",bbox_inches="tight"); plt.close(fig)

# ---- Fig 5: planned vs acquired ----
D=pd.read_csv("scratch/P9/planned_vs_acquired.csv",index_col=0)
EUR=["Barents_Svalbard","GreenlandSea_Fram","KaraGate","Vilkitsky","Sannikov_DmLaptev","LongStrait"]
D["sector"]=np.where(D.index.isin(EUR),"European-Russian","North American-Bering")
D=D.sort_values(["sector","planned_pre"])
fig,ax=plt.subplots(figsize=(7.6,3.4)); i=np.arange(len(D)); w=0.2
for k,(c,l,col) in enumerate([("planned_pre","planned 2019-21 /yr","#4c72b0"),("planned_post","planned 2025","#a0c4e8"),
                              ("acquired_pre","acquired 2019-21 /yr","#c44e52"),("acquired_post","acquired 2025-26 /yr","#f2a6a3")]):
    ax.bar(i+(k-1.5)*w,D[c],w,label=l,color=col)
ax.set_xticks(i); ax.set_xticklabels([SHORT[x] for x in D.index],rotation=55,ha="right",fontsize=6.5)
ax.set_yscale("log"); ax.set_ylabel("segments or scenes per year (log)")
nE=(D.sector=="European-Russian").sum(); ax.axvline(nE-0.5,color="k",lw=0.8)
ax.text(nE/2-0.5,ax.get_ylim()[1]*0.6,"European-Russian",ha="center",fontsize=7)
ax.text(nE+(len(D)-nE)/2-0.5,ax.get_ylim()[1]*0.6,"North American-Bering",ha="center",fontsize=7)
ax.legend(fontsize=6.5,frameon=False,ncol=2); ax.set_title("ESA planned acquisition segments vs acquired scenes")
fig.tight_layout(); fig.savefig(f"{OUT}/fig07_planned_vs_acquired.png",bbox_inches="tight"); plt.close(fig)
print("fig4,5 ok",flush=True)

# ---- Fig 6: DTU availability heatmap ----
Dv=pd.read_csv("scratch/P8/dtu_availability.csv")
g=Dv.groupby(["region","year"]).availability.mean().unstack()
g=g.reindex([r for r in RC if r in g.index])
fig,ax=plt.subplots(figsize=(5.4,4.2))
im=ax.imshow(g.values,aspect="auto",cmap="magma",vmin=0,vmax=float(np.nanmax(g.values)))
ax.set_yticks(range(len(g.index))); ax.set_yticklabels([SHORT[r] for r in g.index],fontsize=6.5)
ax.set_xticks(range(len(g.columns))); ax.set_xticklabels(g.columns,fontsize=7)
for j,y in enumerate(g.columns):
    if y in (2022,2025): ax.axvline(j-0.5,color="cyan",lw=1.1)
cb=fig.colorbar(im,ax=ax,fraction=0.035); cb.set_label("DTU S1-drift availability (valid pixels >= 5 %)",fontsize=7)
ax.set_title("DTU Sentinel-1 drift availability per region-year\ncyan: S1B loss (2022), S1C routine (2025)",fontsize=8.5)
fig.tight_layout(); fig.savefig(f"{OUT}/fig08_dtu_availability.png",bbox_inches="tight"); plt.close(fig)

# ---- Fig 7: virtual-pair closure distribution (main-text reconciliation) ----
V=pd.read_csv("scratch/P9/virtual_pairs_all.csv.gz")
fig,ax=plt.subplots(figsize=(4.6,3.0))
x=np.sort(-V.ds.values); ax.plot(x,1-np.arange(1,len(x)+1)/len(x),color="0.3",lw=1.4,label="all virtual pairs")
sel=-V[V.rate<=-2.954].ds.values
xs=np.sort(sel); ax.plot(xs,(1-np.arange(1,len(xs)+1)/len(xs))*len(xs)/len(x),color="crimson",lw=1.6,
        label="pairs passing the buoy rate threshold")
ax.set_xscale("symlog",linthresh=0.1); ax.set_yscale("log")
ax.axvline(3,color="k",ls="--",lw=0.8); ax.axvline(5,color="k",ls=":",lw=0.8)
ax.text(3.1,3e-4,"3 km",fontsize=6.5); ax.text(5.2,3e-4,"5 km",fontsize=6.5)
ax.set_xlabel("closure over the window (km), 20-100 km baseline"); ax.set_ylabel("fraction exceeding")
ax.legend(fontsize=6.5,frameon=False); ax.set_title("Strait fields expressed in the buoy-pair metric")
fig.tight_layout(); fig.savefig(f"{OUT}/fig04_virtual_pairs.png",bbox_inches="tight"); plt.close(fig)

# ---- Fig 8 (Appendix A): contact sheet ----
files=sorted(glob.glob("results/P8/quicklooks/E*.png")); Q=pd.read_csv("results/P9/qc_table_p9.csv")
n=len(files); ncol=3; nrow=int(np.ceil(n/ncol))
fig,axes=plt.subplots(nrow,ncol,figsize=(13,2.9*nrow))
for ax,f in zip(axes.ravel(),files):
    ax.imshow(mpimg.imread(f)); ax.set_xticks([]); ax.set_yticks([])
    ev=os.path.basename(f).split("_")[0]; r=Q[Q.event==ev]
    ax.set_title(f"{ev} {SHORT.get(r.region.iloc[0],r.region.iloc[0])} {r.date.iloc[0]}  "
                 f"{r.area_km2.iloc[0]:.0f} km$^2$  rescaled {r.mag_buoy_baseline_km.iloc[0]:.2f} km",fontsize=5.6)
for ax in axes.ravel()[n:]: ax.axis("off")
fig.suptitle("Appendix A: 19 candidate strait convergence events, unvalidated (decision column blank)",fontsize=10)
fig.savefig(f"{OUT}/figA1_contact_sheet.png",bbox_inches="tight"); plt.close(fig)

# ---- Fig 9: strait examples (2 Vilkitsky, 2 Sannikov) ----
sel=["E002","E001","E011","E010"]
fig,axes=plt.subplots(2,2,figsize=(11,6.4))
for ax,ev in zip(axes.ravel(),sel):
    f=glob.glob(f"results/P8/quicklooks/{ev}_*.png")
    if not f: continue
    ax.imshow(mpimg.imread(f[0])); ax.set_xticks([]); ax.set_yticks([])
    r=Q[Q.event==ev]
    ax.set_title(f"{ev}  {SHORT.get(r.region.iloc[0],'')}  {r.date.iloc[0]}  "
                 f"area {r.area_km2.iloc[0]:.0f} km$^2$",fontsize=7)
fig.suptitle("Strait divergence examples: before / after HH with divergence overlay",fontsize=10)
fig.savefig(f"{OUT}/fig05_strait_examples.png",bbox_inches="tight"); plt.close(fig)
print("fig6,7,8,A1 ok",flush=True)
