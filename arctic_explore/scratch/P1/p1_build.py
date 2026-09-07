import pandas as pd, numpy as np, os
from pyproj import Transformer
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
OUT="scratch/P1"
tr=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
frames=[]
for y in range(2016,2026):
    f=f"{OUT}/LEVEL1_{y}.csv"
    hdr=open(f).readline().strip().split(",")
    mn="Min" if "Min" in hdr else "Minute"
    d=pd.read_csv(f,usecols=["BuoyID","Year","Month","Day","Hour",mn,"Lat","Lon"],
                  dtype={"BuoyID":str},low_memory=False).rename(columns={mn:"Min"})
    d=d[(d.Lat>=70)&(d.Lat<=90)&(d.Lon>=-180)&(d.Lon<=180)]
    d=d.dropna()
    frames.append(d); print(y,len(d),flush=True)
D=pd.concat(frames,ignore_index=True); del frames
D["t"]=pd.to_datetime(dict(year=D.Year.astype(int),month=D.Month.astype(int),day=D.Day.astype(int),
                           hour=D.Hour.astype(int),minute=D.Min.astype(int)),errors="coerce")
D=D.dropna(subset=["t"]).sort_values(["BuoyID","t"])
D=D.drop_duplicates(subset=["BuoyID","t"],keep="first").reset_index(drop=True)
x,y=tr.transform(D.Lon.values,D.Lat.values); D["x"]=x; D["y"]=y
bid=D.BuoyID.values; tt=D.t.values.astype("datetime64[s]").astype(np.int64)
xx=D.x.values; yy=D.y.values
same=np.zeros(len(D),bool); same[1:]=bid[1:]==bid[:-1]
dtm=np.zeros(len(D)); dtm[1:]=(tt[1:]-tt[:-1])/86400.0
dist=np.zeros(len(D)); dist[1:]=np.hypot(xx[1:]-xx[:-1],yy[1:]-yy[:-1])/1e3
with np.errstate(divide="ignore",invalid="ignore"):
    v=np.where(same&(dtm>0),dist/dtm,0.0)
drop=same&((dtm<=0)|(v>120))
print("speed-QC dropped",int(drop.sum()),flush=True)
D=D[~drop]
print("fixes after QC",len(D),"buoys",D.BuoyID.nunique(),flush=True)
T0=np.datetime64("2016-01-01T00:00:00").astype("datetime64[s]").astype(np.int64)
T1=np.datetime64("2026-01-01T00:00:00").astype("datetime64[s]").astype(np.int64)
grid=np.arange(T0,T1,3*3600)
buoys=sorted(D.BuoyID.unique()); bidx={b:i for i,b in enumerate(buoys)}
re_,rb,rx,ry=[],[],[],[]
for b,g in D.groupby("BuoyID",sort=False):
    ts=g.t.values.astype("datetime64[s]").astype(np.int64)
    if len(ts)<2: continue
    gx=g.x.values; gy=g.y.values
    lo=np.searchsorted(grid,ts[0]); hi=np.searchsorted(grid,ts[-1],side="right")
    if hi<=lo: continue
    gt=grid[lo:hi]
    j=np.clip(np.searchsorted(ts,gt),1,len(ts)-1)
    ok=((gt-ts[j-1])<=3*3600)&((ts[j]-gt)<=3*3600)
    if not ok.any(): continue
    den=np.maximum(ts[j]-ts[j-1],1)
    w=(gt-ts[j-1])/den
    px=gx[j-1]+w*(gx[j]-gx[j-1]); py=gy[j-1]+w*(gy[j]-gy[j-1])
    re_.append(np.arange(lo,hi,dtype=np.int32)[ok]); rb.append(np.full(int(ok.sum()),bidx[b],np.int32))
    rx.append(px[ok].astype(np.float32)); ry.append(py[ok].astype(np.float32))
E=np.concatenate(re_); B=np.concatenate(rb); X=np.concatenate(rx); Y=np.concatenate(ry)
o=np.argsort(E,kind="stable"); E,B,X,Y=E[o],B[o],X[o],Y[o]
print("gridded samples",len(E),"epochs used",len(np.unique(E)),flush=True)
np.savez_compressed(f"{OUT}/grid.npz",E=E,B=B,X=X,Y=Y,buoys=np.array(buoys),grid=grid)
print("BUILD DONE",flush=True)
