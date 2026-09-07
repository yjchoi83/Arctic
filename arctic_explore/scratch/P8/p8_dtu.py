import copernicusmarine as cm, numpy as np, pandas as pd, sys, os
sys.path.insert(0,"scratch/P2"); from regions import regions
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
ds=cm.open_dataset(dataset_id="cmems_obs-si_glo_phy-drift-north_my_l4_P1D-m")
V="dX_mean"
R=regions(); rows=[]
def seas(m): return "winter" if m<=3 else ("melt" if 6<=m<=9 else ("freeze-up" if m>=10 else "shoulder"))
for name,(w,e,s,n) in R.items():
    if w<=e: sub=ds[V].sel(latitude=slice(s,n),longitude=slice(w,e))
    else:    sub=ds[V].sel(latitude=slice(s,n))
    if sub.sizes.get("latitude",0)==0 or sub.sizes.get("longitude",0)==0:
        print(name,"empty box"); continue
    frac=(np.isfinite(sub)).mean(dim=["latitude","longitude"]).compute()
    t=pd.to_datetime(frac.time.values)
    d=pd.DataFrame({"date":t,"frac":frac.values})
    d["year"]=d.date.dt.year; d["season"]=d.date.dt.month.map(seas)
    d=d[(d.season!="shoulder")&(d.year.between(2019,2025))]
    g=d.groupby(["year","season"]).agg(days_avail=("frac",lambda x:(x>=0.05).sum()),
                                       days_total=("frac","size"),mean_frac=("frac","mean")).reset_index()
    g["region"]=name; g["availability"]=g.days_avail/g.days_total
    rows.append(g)
    print(name,"ok  mean availability %.3f"%g.availability.mean(),flush=True)
A=pd.concat(rows,ignore_index=True)
A.to_csv("scratch/P8/dtu_availability.csv",index=False)
print("rows",len(A))
