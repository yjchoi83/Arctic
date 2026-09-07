import pandas as pd, numpy as np, os
from pyproj import Transformer
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
tr=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
fr=[]
for y in range(2016,2026):
    f=f"scratch/P1/LEVEL1_{y}.csv"; hdr=open(f).readline().strip().split(",")
    mn="Min" if "Min" in hdr else "Minute"
    d=pd.read_csv(f,usecols=["BuoyID","Year","Month","Day","Hour",mn,"Lat","Lon"],
                  dtype={"BuoyID":str},low_memory=False).rename(columns={mn:"Min"})
    d=d[(d.Lat>=70)&(d.Lat<=90)&(d.Lon>=-180)&(d.Lon<=180)].dropna(); fr.append(d)
D=pd.concat(fr,ignore_index=True); del fr
D["t"]=pd.to_datetime(dict(year=D.Year.astype(int),month=D.Month.astype(int),day=D.Day.astype(int),
                           hour=D.Hour.astype(int),minute=D.Min.astype(int)),errors="coerce")
D=D.dropna(subset=["t"]).sort_values(["BuoyID","t"]).drop_duplicates(["BuoyID","t"]).reset_index(drop=True)
x,y=tr.transform(D.Lon.values,D.Lat.values); D["x"]=x; D["y"]=y
bid=D.BuoyID.values; tt=D.t.values.astype("datetime64[s]").astype(np.int64)
same=np.zeros(len(D),bool); same[1:]=bid[1:]==bid[:-1]
dts=np.zeros(len(D)); dts[1:]=(tt[1:]-tt[:-1])
dist=np.zeros(len(D)); dist[1:]=np.hypot(D.x.values[1:]-D.x.values[:-1],D.y.values[1:]-D.y.values[:-1])/1e3
with np.errstate(divide="ignore",invalid="ignore"):
    v=np.where(same&(dts>0),dist/(dts/86400.0),0.0)
D=D[~(same&((dts<=0)|(v>120)))].reset_index(drop=True)
gap=D.assign(dt=D.groupby("BuoyID").t.diff().dt.total_seconds()).dropna(subset=["dt"])
med=gap.groupby("BuoyID").dt.median()
FAST=set(med[med<=3600].index)
print("buoys total %d ; native median interval <=1h: %d"%(D.BuoyID.nunique(),len(FAST)),flush=True)
D=D[D.BuoyID.isin(FAST)]
print("fixes in fast subset",len(D),flush=True)
def build(step_s,brk_s):
    T0=np.datetime64("2016-01-01T00:00:00").astype("datetime64[s]").astype(np.int64)
    T1=np.datetime64("2026-01-01T00:00:00").astype("datetime64[s]").astype(np.int64)
    grid=np.arange(T0,T1,step_s)
    bl=sorted(D.BuoyID.unique()); bx={b:i for i,b in enumerate(bl)}
    re_,rb,rx,ry=[],[],[],[]
    for b,g in D.groupby("BuoyID",sort=False):
        ts=g.t.values.astype("datetime64[s]").astype(np.int64)
        if len(ts)<2: continue
        gx=g.x.values; gy=g.y.values
        lo=np.searchsorted(grid,ts[0]); hi=np.searchsorted(grid,ts[-1],side="right")
        if hi<=lo: continue
        gt=grid[lo:hi]; j=np.clip(np.searchsorted(ts,gt),1,len(ts)-1)
        ok=((gt-ts[j-1])<=brk_s)&((ts[j]-gt)<=brk_s)
        if not ok.any(): continue
        w=(gt-ts[j-1])/np.maximum(ts[j]-ts[j-1],1)
        px=gx[j-1]+w*(gx[j]-gx[j-1]); py=gy[j-1]+w*(gy[j]-gy[j-1])
        re_.append(np.arange(lo,hi,dtype=np.int32)[ok]); rb.append(np.full(int(ok.sum()),bx[b],np.int32))
        rx.append(px[ok]); ry.append(py[ok])
    E=np.concatenate(re_); B=np.concatenate(rb); X=np.concatenate(rx); Y=np.concatenate(ry)
    o=np.argsort(E,kind="stable"); return E[o],B[o],X[o],Y[o],len(bl)
def events(step_h,brk_s,minrun_h,minev_h,tag):
    E,B,X,Y,NB=build(int(step_h*3600),brk_s)
    ue,st=np.unique(E,return_index=True); st=np.append(st,len(E))
    PKl=[];EPl=[];SPl=[]
    for k in range(len(ue)):
        a,b=st[k],st[k+1]
        if b-a<2: continue
        bb=B[a:b]; xx=X[a:b]; yy=Y[a:b]
        s=np.hypot(xx[:,None]-xx[None,:],yy[:,None]-yy[None,:])/1e3
        i,j=np.triu_indices(len(bb),1); sv=s[i,j]
        m=(sv>=20)&(sv<=100)
        if not m.any(): continue
        lo=np.minimum(bb[i[m]],bb[j[m]]).astype(np.int64); hi=np.maximum(bb[i[m]],bb[j[m]]).astype(np.int64)
        PKl.append(lo*NB+hi); EPl.append(np.full(int(m.sum()),ue[k],np.int32)); SPl.append(sv[m].astype(np.float32))
    PK=np.concatenate(PKl);EP=np.concatenate(EPl);SP=np.concatenate(SPl)
    o=np.lexsort((EP,PK)); PK,EP,SP=PK[o],EP[o],SP[o]
    new=np.ones(len(PK),bool); new[1:]=(PK[1:]!=PK[:-1])|((EP[1:]-EP[:-1])!=1)
    rid=np.cumsum(new)-1; cnt=np.bincount(rid); need=int(minrun_h/step_h)
    good=(cnt>=need)[rid]
    r=np.full(len(PK),np.nan); r[1:]=(SP[1:]-SP[:-1])/(step_h/24.0)
    valid=(~new)&good&np.concatenate(([False],good[:-1]))
    THR=float(np.percentile(np.abs(r[valid&(r<0)]),90))
    ok=valid&(r<=-THR); pos=np.where(ok)[0]
    b2=np.ones(len(pos),bool); b2[1:]=(pos[1:]!=pos[:-1]+1)|(new[pos[1:]])
    eid=np.cumsum(b2)-1; ne=eid[-1]+1
    fi=np.zeros(ne,np.int64); fi[eid[b2]]=pos[b2]
    em=np.append(b2[1:],True); li=np.zeros(ne,np.int64); li[eid[em]]=pos[em]
    L=li-fi+1; sel=L>=max(2,int(round(minev_h/step_h)))
    dur=L[sel]*step_h; mag=SP[fi[sel]-1]-SP[li[sel]]
    t0=EP[fi[sel]-1].astype(np.int64)*int(step_h*3600)+int(np.datetime64("2016-01-01T00:00:00").astype("datetime64[s]").astype(np.int64))
    print(f"[{tag}] step {step_h}h THR {THR:.3f} n_ev {len(dur)} pairs {len(np.unique(PK[fi[sel]]))} "
          f"med {np.median(dur):.0f}h p90 {np.percentile(dur,90):.0f}h frac<6h {np.mean(dur<6):.3f} "
          f"mag_med {np.median(mag):.2f}km",flush=True)
    np.savez(f"scratch/P3/step2t_{tag}.npz",dur=dur,mag=mag,THR=THR,t0=t0)
events(1.0,3600,24,2,"native1h")

print("STEP2 DONE",flush=True)
