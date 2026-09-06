import numpy as np, pandas as pd, os
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
rng=np.random.default_rng(0)
C=pd.read_csv("scratch/P3/P3_cells.csv")
print("cell rows",len(C),flush=True)
agg=[]
for (r,s,y),g in C.groupby(["region","season","year"]):
    d=dict(region=r,season=s,year=y,n_cells=g.cell.nunique(),n_acq_med=float(g.n_acq.median()))
    for col in ("H_episode3","H_episode5","H_state3","H_state5","O24","O12"):
        d[col]=round(float(np.nanmean(g[col])),4)
    v=g["H_state3"].values.astype(float); n=len(v)
    if n>=2:
        idx=rng.integers(0,n,size=(1000,n)); m=np.nanmean(v[idx],axis=1)
        d["H_state3_lo"]=round(float(np.percentile(m,2.5)),4)
        d["H_state3_hi"]=round(float(np.percentile(m,97.5)),4)
    else: d["H_state3_lo"]=d["H_state3_hi"]=np.nan
    agg.append(d)
A=pd.DataFrame(agg); A.to_csv("scratch/P3/P3_region_season_year.csv",index=False)
print(A.groupby("year")[["H_episode3","H_state3","H_state5","O24","O12"]].mean().round(3).to_string())
print("\nchokepoint H_state3 by season/year:")
ch=["Vilkitsky","Sannikov_DmLaptev","LongStrait","KaraGate","BeringChukchi"]
print(A[A.region.isin(ch)].pivot_table(index=["region","season"],columns="year",values="H_state3").round(2).to_string())
