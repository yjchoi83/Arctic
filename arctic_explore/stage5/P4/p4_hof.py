import numpy as np, pandas as pd, os, sys, datetime as dt
sys.path.insert(0,"scratch/P3"); from cells import region_cells
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
D=pd.read_csv("scratch/P4/divergence.csv")
print("divergence rows",len(D),"regions",D.region.unique().tolist(),flush=True)
# frozen climatology: per (region,cell) 10th percentile over 2016-2025, computed once
clim=D.groupby(["region","cell"]).div.quantile(0.10).rename("p10").reset_index()
nday=D.groupby(["region","cell"]).size().rename("n_days").reset_index()
clim=clim.merge(nday,on=["region","cell"])
clim.to_csv("scratch/P4/climatology.csv",index=False)
D=D.merge(clim,on=["region","cell"])
D["conv"]=D["div"]<D.p10
D["ts"]=pd.to_datetime(D.date)
def seas(m): return "winter" if m<=3 else ("melt" if 6<=m<=9 else ("freeze-up" if m>=10 else "shoulder"))
D["season"]=D.ts.dt.month.map(seas); D["year"]=D.ts.dt.year
# S1 acquisition times per (region,cell)
ACQ={}
RC=region_cells()
for r in D.region.unique():
    for yr in range(2016,2027):
        f=f"scratch/P3/cellacq/{r}_{yr}.npz"
        if not os.path.exists(f): continue
        z=np.load(f,allow_pickle=True)
        ci,t,p,o,c=z["ci"],z["t"],z["p"].astype(str),z["o"].astype(str),z["c"]
        for k in np.unique(ci):
            m=ci==k; tt=t[m]; cc=c[m]; kk=np.char.add(np.char.add(p[m],"_"),o[m])
            order=np.argsort(tt); tt,cc,kk=tt[order],cc[order],kk[order]
            gid=np.zeros(len(tt),np.int64)
            for i in range(1,len(tt)):
                gid[i]=gid[i-1] if (kk[i]==kk[i-1] and tt[i]-tt[i-1]<=15*60*1000) else gid[i-1]+1
            ug=np.unique(gid)
            pt=np.array([tt[gid==g].mean() for g in ug]); pc=np.array([min(1.0,cc[gid==g].sum()) for g in ug])
            sel=pc>=0.5
            if sel.any(): ACQ.setdefault((r,int(k)),[]).extend((pt[sel]/1000.0).tolist())
for k in ACQ: ACQ[k]=np.sort(np.array(ACQ[k]))
print("cells with S1 acq",len(ACQ),flush=True)
def near(r,c,ts,h):
    a=ACQ.get((r,int(c)))
    if a is None or len(a)==0: return False
    i=np.searchsorted(a,ts)
    for j in (i-1,i):
        if 0<=j<len(a) and abs(a[j]-ts)<=h*3600: return True
    return False
C=D[D.conv].copy()
C["obs24"]=[near(r,c,t,24) for r,c,t in zip(C.region,C.cell,C.tmid)]
C["obs12"]=[near(r,c,t,12) for r,c,t in zip(C.region,C.cell,C.tmid)]
C.to_csv("scratch/P4/convergence_days.csv",index=False)
g=C.groupby(["region","season","year"]).agg(n_conv=("conv","size"),hof24=("obs24","mean"),hof12=("obs12","mean")).reset_index()
g.to_csv("scratch/P4/hof.csv",index=False)
print("\nconvergence-day counts by region:"); print(C.groupby("region").size().to_string())
print("\nfreeze-up hazard-observed fraction (n>=10 only):")
q=g[(g.season=="freeze-up")&(g.n_conv>=10)]
print(q.round(3).to_string(index=False) if len(q) else "  none")
print("\nall seasons pooled by region-period:")
C["per"]=np.where(C.year.between(2019,2021),"pre",np.where(C.year.between(2022,2024),"during",
        np.where(C.year>=2025,"post","early")))
print(C.groupby(["region","per"]).agg(n=("conv","size"),hof24=("obs24","mean"),hof12=("obs12","mean")).round(3).to_string())
