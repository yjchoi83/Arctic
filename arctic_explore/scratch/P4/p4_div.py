import numpy as np, xarray as xr, glob, os, sys, re, datetime as dt, pandas as pd
sys.path.insert(0,"scratch/P3"); from cells import region_cells, CELL
from pyproj import Transformer
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
CHOKE=["Vilkitsky","Sannikov_DmLaptev","LongStrait","KaraGate","BeringChukchi"]
OSI="+proj=stere +a=6378273 +b=6356889.44891 +lat_0=90 +lat_ts=70 +lon_0=-45"
T=Transformer.from_crs("EPSG:3413",OSI,always_xy=True)
RC=region_cells()
files=sorted(glob.glob("scratch/P4/osisaf/*.nc"))
print("files",len(files),flush=True)
d0=xr.open_dataset(files[0]); xc=d0.xc.values*1000.0; yc=d0.yc.values*1000.0; d0.close()
# map each chokepoint 25km cell -> nearest OSI grid index
CMAP={}
for r in CHOKE:
    for k,(a,b) in enumerate(RC[r]):
        x,y=T.transform(a+CELL/2,b+CELL/2)
        i=int(np.argmin(np.abs(yc-y))); j=int(np.argmin(np.abs(xc-x)))
        CMAP[(r,k)]=(i,j)
print("choke cells",len(CMAP),flush=True)
rows=[]
for f in files:
    m=re.search(r"_(\d{12})-(\d{12})\.nc",os.path.basename(f))
    if not m: continue
    t0=dt.datetime.strptime(m.group(1),"%Y%m%d%H%M"); t1=dt.datetime.strptime(m.group(2),"%Y%m%d%H%M")
    try:
        ds=xr.open_dataset(f)
        dX=ds["dX"].values[0].astype(float); dY=ds["dY"].values[0].astype(float)
        sf=ds["status_flag"].values[0] if "status_flag" in ds else None
        ds.close()
    except Exception: continue
    bad=~np.isfinite(dX)|~np.isfinite(dY)
    if sf is not None: bad|=(sf!=0)&(sf!=30)
    dX=np.where(bad,np.nan,dX); dY=np.where(bad,np.nan,dY)
    dudx=np.full_like(dX,np.nan); dvdy=np.full_like(dY,np.nan)
    dudx[:,1:-1]=(dX[:,2:]-dX[:,:-2])/(2*62.5)
    dvdy[1:-1,:]=(dY[2:,:]-dY[:-2,:])/(2*62.5)
    div=dudx+dvdy
    for (r,k),(i,j) in CMAP.items():
        v=div[i,j]
        if np.isfinite(v):
            rows.append((r,k,t0.date().isoformat(),(t0+(t1-t0)/2).timestamp(),float(v)))
D=pd.DataFrame(rows,columns=["region","cell","date","tmid","div"])
D.to_csv("scratch/P4/divergence.csv",index=False)
print("rows",len(D),"cells with data",D.groupby(['region','cell']).ngroups,flush=True)
print(D.groupby("region").div.describe()[["count","mean","std","min","max"]].round(4).to_string())
