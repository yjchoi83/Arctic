import copernicusmarine as cm, xarray as xr, numpy as np, pandas as pd, os, sys, glob
sys.path.insert(0,"scratch/P2"); from regions import regions
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
os.makedirs("scratch/P8/asip",exist_ok=True)
PLAN=[("my",2019,["1105","1115","1125","0215"]),("my",2021,["1105","1115","1125","0215"]),
      ("my",2023,["1105","1115","1125","0215"]),("nrt",2025,["1105","1115","1125","0215"])]
for kind,yr,dds in PLAN:
    did=f"cmems_obs-si_arc_phy_{kind}_l3_P1D"
    for dd in dds:
        m,d=dd[:2],dd[2:]
        fn=f"dmi_asip_seaice_mosaic_arc_l3_{yr}{m}{d}.nc"
        if os.path.exists(f"scratch/P8/asip/{fn}"): continue
        try:
            cm.get(dataset_id=did,filter=f"*{yr}/{m}/{fn}",no_directories=True,
                   output_directory="scratch/P8/asip",overwrite=False)
        except Exception as e: print("miss",fn,str(e)[:60],flush=True)
fs=sorted(glob.glob("scratch/P8/asip/*.nc")); print("files",len(fs),flush=True)
R=regions()
from pyproj import Transformer
rows=[]
for f in fs:
    ds=xr.open_dataset(f)
    sic=ds["sic"]; crs=ds["crs"].attrs
    proj=crs.get("proj4_string") or crs.get("proj4")
    T=Transformer.from_crs("EPSG:4326",proj,always_xy=True) if proj else None
    xc=ds.xc.values; yc=ds.yc.values
    date=os.path.basename(f).split("_")[-1][:8]
    a=sic.values[0] if sic.ndim==3 else sic.values
    for name,(w,e,s,n) in R.items():
        if T is None: continue
        lo=np.linspace(w,e,25); la=np.linspace(s,n,25)
        X,Y=T.transform(np.repeat(lo,25),np.tile(la,25))
        i0,i1=np.searchsorted(yc[::-1] if yc[0]>yc[-1] else yc,[min(Y),max(Y)])
        j0,j1=np.searchsorted(xc,[min(X),max(X)])
        if yc[0]>yc[-1]:
            i0,i1=len(yc)-i1,len(yc)-i0
        sub=a[max(i0,0):i1,max(j0,0):j1]
        if sub.size==0: rows.append((date,name,np.nan,0)); continue
        rows.append((date,name,float(np.isfinite(sub).mean()),int(sub.size)))
    ds.close(); print("done",date,flush=True)
D=pd.DataFrame(rows,columns=["date","region","valid_frac","npix"])
D.to_csv("scratch/P8/asip_valid.csv",index=False)
D["year"]=D.date.str[:4].astype(int)
print(D.groupby("year").valid_frac.mean().round(3).to_string())
