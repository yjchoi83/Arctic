import copernicusmarine as cm, numpy as np, pandas as pd, sys, os
sys.path.insert(0,"scratch/P2"); from regions import regions
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
ds=cm.open_dataset(dataset_id="cmems_obs-si_glo_phy-drift-north_my_l4_P1D-m")
R=regions(); out=[]
for name,(w,e,s,n) in R.items():
    sub=ds["dX_mean"].sel(latitude=slice(s,n),longitude=slice(w,e))
    if sub.sizes.get("latitude",0)==0 or sub.sizes.get("longitude",0)==0: continue
    frac=(np.isfinite(sub)).mean(dim=["latitude","longitude"]).compute()
    out.append(pd.DataFrame({"region":name,"date":pd.to_datetime(frac.time.values),"frac":frac.values}))
    print(name,"ok",flush=True)
D=pd.concat(out,ignore_index=True); D.to_csv("scratch/P9/dtu_daily_frac.csv",index=False)
print("rows",len(D))
