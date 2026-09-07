import numpy as np, xarray as xr, glob, os, sys, re, datetime as dt, pandas as pd, collections
sys.path.insert(0,"scratch/P3"); from cells import region_cells, CELL
from pyproj import Transformer
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
CH=["Vilkitsky","Sannikov_DmLaptev","LongStrait","KaraGate","BeringChukchi"]
OSI="+proj=stere +a=6378273 +b=6356889.44891 +lat_0=90 +lat_ts=70 +lon_0=-45"
T=Transformer.from_crs("EPSG:3413",OSI,always_xy=True)
RC=region_cells()
fs=sorted(glob.glob("scratch/P4/osisaf/*.nc"))
d0=xr.open_dataset(fs[0]); xc=d0.xc.values*1000.; yc=d0.yc.values*1000.; d0.close()
CMAP={}
for r in CH:
    for k,(a,b) in enumerate(RC[r]):
        x,y=T.transform(a+CELL/2,b+CELL/2)
        CMAP[(r,k)]=(int(np.argmin(np.abs(yc-y))),int(np.argmin(np.abs(xc-x))))
VALID={20,21,22,30}
rows=[]; flagcnt=collections.Counter(); nb_fail=collections.Counter(); interp=collections.Counter()
for f in fs:
    m=re.search(r"_(\d{12})-(\d{12})\.nc",os.path.basename(f))
    if not m: continue
    t0=dt.datetime.strptime(m.group(1),"%Y%m%d%H%M"); t1=dt.datetime.strptime(m.group(2),"%Y%m%d%H%M")
    try:
        ds=xr.open_dataset(f); dX=ds["dX"].values[0].astype(float); dY=ds["dY"].values[0].astype(float)
        sf=ds["status_flag"].values[0]; ds.close()
    except Exception: continue
    ok=np.isin(sf,list(VALID))&np.isfinite(dX)&np.isfinite(dY)
    X=np.where(ok,dX,np.nan); Y=np.where(ok,dY,np.nan)
    dudx=np.full_like(X,np.nan); dvdy=np.full_like(Y,np.nan)
    dudx[:,1:-1]=(X[:,2:]-X[:,:-2])/(2*62.5)
    dvdy[1:-1,:]=(Y[2:,:]-Y[:-2,:])/(2*62.5)
    div=dudx+dvdy
    tm=(t0+(t1-t0)/2)
    for (r,k),(i,j) in CMAP.items():
        flagcnt[(r,int(sf[i,j]))]+=1
        if not ok[i,j]: continue
        interp[(r,"interp" if sf[i,j]==22 else "measured")]+=1
        v=div[i,j]
        if not np.isfinite(v): nb_fail[r]+=1; continue
        rows.append((r,k,t0.date().isoformat(),tm.timestamp(),float(v),int(sf[i,j])))
D=pd.DataFrame(rows,columns=["region","cell","date","tmid","div","flag"])
D.to_csv("scratch/P4/divergence.csv",index=False)
print("rows",len(D),flush=True)
tot=collections.Counter()
for (r,fl),c in flagcnt.items(): tot[r]+=c
for r in CH:
    v=sum(c for (rr,fl),c in flagcnt.items() if rr==r and fl in VALID)
    n=len(D[D.region==r])
    print(f"{r:20s} point-days {tot[r]:7d} valid {v:6d} ({100*v/max(tot[r],1):4.1f}%) "
          f"| divergence computable {n:6d} ({100*n/max(tot[r],1):4.1f}%) | neighbour-fail {nb_fail[r]:6d} "
          f"| of valid: interpolated {interp[(r,'interp')]} measured {interp[(r,'measured')]}",flush=True)
