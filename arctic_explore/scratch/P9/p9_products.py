import numpy as np, pandas as pd, os, sys, glob
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import rasterio
from rasterio.transform import from_origin
sys.path.insert(0,"scratch/P3"); sys.path.insert(0,"scratch/P2")
from cells import region_cells, CELL
from regions import regions
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
os.makedirs("data/products",exist_ok=True); os.makedirs("results/P9",exist_ok=True)
C=pd.read_csv("scratch/P3/P3_cells.csv")
def per(y): return "pre2019-21" if 2019<=y<=2021 else ("during2022-24" if 2022<=y<=2024 else ("post2025-26" if y>=2025 else None))
C["per"]=C.year.map(per); C=C[C.per.notna()]
RC=region_cells()
XY={}
for r,cl in RC.items():
    for k,(a,b) in enumerate(cl): XY[(r,k)]=(a,b)
C["x"]=[XY[(r,k)][0] for r,k in zip(C.region,C.cell)]
C["y"]=[XY[(r,k)][1] for r,k in zip(C.region,C.cell)]
xs=np.arange(C.x.min(),C.x.max()+CELL,CELL); ys=np.arange(C.y.min(),C.y.max()+CELL,CELL)
W,H=len(xs),len(ys)
tr=from_origin(xs.min(),ys.max()+CELL,CELL,CELL)
def rasterize(g,col):
    a=np.full((H,W),np.nan,np.float32)
    for x,y,v in zip(g.x,g.y,g[col]):
        j=int(round((x-xs.min())/CELL)); i=int(round((ys.max()-y)/CELL))
        if 0<=i<H and 0<=j<W: a[i,j]=v
    return a
made=[]
for col in ("H_state3","H_episode3"):
    for season in ("freeze-up","winter","melt"):
        fig,axes=plt.subplots(1,3,figsize=(12,4.2))
        for ax,p in zip(axes,["pre2019-21","during2022-24","post2025-26"]):
            g=C[(C.season==season)&(C.per==p)].groupby(["region","cell","x","y"],as_index=False)[col].mean()
            a=rasterize(g,col)
            im=ax.imshow(a,vmin=0,vmax=0.8,cmap="viridis")
            ax.set_title(f"{p}",fontsize=9); ax.set_xticks([]); ax.set_yticks([])
            fn=f"data/products/{col}_{season}_{p}.tif"
            with rasterio.open(fn,"w",driver="GTiff",height=H,width=W,count=1,dtype="float32",
                               crs="EPSG:3413",transform=tr,nodata=np.nan) as d: d.write(a,1)
            made.append(fn)
        cb=fig.colorbar(im,ax=axes,fraction=0.022,pad=0.01); cb.set_label(f"{col} (0.8 = requirement)",fontsize=8)
        fig.suptitle(f"{col} per 25 km cell — {season}",fontsize=10)
        fig.savefig(f"results/P9/{col}_{season}.png",dpi=105,bbox_inches="tight"); plt.close(fig)
print("GeoTIFFs",len(made),"PNGs",len(glob.glob('results/P9/H_*.png')),flush=True)
# planned vs acquired
P=pd.read_csv("scratch/P8/planned_vs.csv",index_col=0)
T=pd.read_csv("scratch/P2/P2_tables.csv"); T=T[T.season!="shoulder"]
acq_pre=T[T.year.between(2019,2021)].groupby("region").n_acq.sum()/3.0
acq_post=T[T.year.between(2025,2026)].groupby("region").n_acq.sum()/1.67
D=pd.DataFrame({"planned_pre":P.planned_pre_per_yr,"planned_post":P.planned_2025,
                "acquired_pre":acq_pre,"acquired_post":acq_post}).dropna()
D=D.sort_values("planned_pre")
fig,ax=plt.subplots(figsize=(9,5)); i=np.arange(len(D)); w=0.2
for k,(c,lab) in enumerate([("planned_pre","planned 2019-21/yr"),("planned_post","planned 2025"),
                            ("acquired_pre","acquired 2019-21/yr"),("acquired_post","acquired 2025-26/yr")]):
    ax.bar(i+(k-1.5)*w,D[c],w,label=lab)
ax.set_xticks(i); ax.set_xticklabels(D.index,rotation=60,ha="right",fontsize=7)
ax.set_yscale("log"); ax.set_ylabel("segments / scenes per year (log)"); ax.legend(fontsize=7)
ax.set_title("ESA planned segments vs acquired scenes, pre vs post",fontsize=10)
fig.savefig("results/P9/planned_vs_acquired.png",dpi=110,bbox_inches="tight"); plt.close(fig)
D.to_csv("scratch/P9/planned_vs_acquired.csv"); print("planned/acquired fig ok",flush=True)
