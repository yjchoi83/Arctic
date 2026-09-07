import numpy as np, pandas as pd, os, json, datetime as dt
from pyproj import Transformer
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
z=np.load("scratch/P1/pairs.npz",allow_pickle=True)
PK,EP,SP,MX,MY=z["PK"],z["EP"],z["SP"],z["MX"],z["MY"]; NB=int(z["NB"]); grid=z["grid"]; buoys=z["buoys"]
inv=Transformer.from_crs("EPSG:3413","EPSG:4326",always_xy=True)
def region(lon,lat):
    r=np.full(len(lat),"other",object)
    m=(lon>=10)&(lon<100); r[m]="Kara/Barents"
    m=(lon>=100)&(lon<180); r[m]="Laptev/ESS"
    m=(lon>=-180)&(lon<-125); r[m]="Chukchi/Beaufort"
    r[lat>=82]="central Arctic"
    return r
def season(mo):
    s=np.full(len(mo),"shoulder",object)
    s[(mo>=1)&(mo<=3)]="winter"; s[(mo>=6)&(mo<=9)]="melt"; s[(mo>=10)&(mo<=12)]="freeze-up"
    return s
def analyze(lo,hi,pct,tag,dump=None):
    m=(SP>=lo)&(SP<=hi)
    pk,ep,sp,mx,my=PK[m],EP[m],SP[m],MX[m],MY[m]
    new=np.ones(len(pk),bool); new[1:]=(pk[1:]!=pk[:-1])|((ep[1:]-ep[:-1])!=1)
    rid=np.cumsum(new)-1
    cnt=np.bincount(rid); keep=cnt>=8
    good=keep[rid]
    r=np.full(len(pk),np.nan); r[1:]=(sp[1:]-sp[:-1])/0.125
    valid=(~new)&good&np.concatenate(([False],good[:-1]))
    neg=r[valid&(r<0)]
    THR=float(np.percentile(np.abs(neg),pct))
    ok=valid&(r<=-THR)
    pos=np.where(ok)[0]
    if len(pos)==0: return dict(tag=tag,THR=THR,n_events=0)
    brk=np.ones(len(pos),bool)
    brk[1:]=(pos[1:]!=pos[:-1]+1)|(new[pos[1:]])
    eid=np.cumsum(brk)-1
    ne=eid[-1]+1
    first=np.zeros(ne,np.int64); last=np.zeros(ne,np.int64)
    np.minimum.at(first,eid,0); first=np.full(ne,-1,np.int64)
    order=np.arange(len(pos))
    fi=np.zeros(ne,np.int64); fi[eid[brk]]=pos[brk]
    li=np.zeros(ne,np.int64)
    endmask=np.append(brk[1:],True)
    li[eid[endmask]]=pos[endmask]
    L=(li-fi+1)
    sel=L>=2
    fi,li,L=fi[sel],li[sel],L[sel]
    dur=L*3.0
    mag=sp[fi-1]-sp[li]
    rate=mag/(dur/24.0)
    midrec=((fi-1+li)//2)
    lon,lat=inv.transform(mx[midrec].astype(float),my[midrec].astype(float))
    tm=np.array([dt.datetime.utcfromtimestamp(int(grid[e])) for e in ep[midrec]])
    mo=np.array([t.month for t in tm]); yr=np.array([t.year for t in tm])
    reg=region(np.asarray(lon),np.asarray(lat)); sea=season(mo)
    a=pk[fi]//NB; b=pk[fi]%NB
    df=pd.DataFrame(dict(pair=[f"{buoys[i]}_{buoys[j]}" for i,j in zip(a,b)],
        start_utc=[dt.datetime.utcfromtimestamp(int(grid[e])).strftime("%Y-%m-%dT%H:%M") for e in ep[fi-1]],
        duration_h=dur, magnitude_km=np.round(mag,3), mean_rate_km_day=np.round(rate,3),
        sep_start_km=np.round(sp[fi-1],2), lat=np.round(lat,3), lon=np.round(lon,3),
        region=reg, season=sea, year=yr))
    if dump: df.to_csv(dump,index=False)
    nb=len(set(list(a)+list(b)))
    return dict(tag=tag,THR=round(THR,3),n_events=len(df),n_pairs=int(len(np.unique(pk[fi]))),
                n_buoys=nb,med_dur=float(np.median(dur)),p20=float(np.percentile(dur,20)),
                p75=float(np.percentile(dur,75)),p90=float(np.percentile(dur,90)),df=df)
base=analyze(20,100,90,"base_20-100_p90",dump="stage5/P1/P1_events.csv")
print("BASE",{k:v for k,v in base.items() if k!="df"},flush=True)
out=[{k:v for k,v in base.items() if k!="df"}]
for lo,hi in [(20,50),(50,100)]:
    for p in (85,90,95):
        r=analyze(lo,hi,p,f"{lo}-{hi}_p{p}")
        out.append({k:v for k,v in r.items() if k!="df"}); print(out[-1],flush=True)
for p in (85,95):
    r=analyze(20,100,p,f"20-100_p{p}")
    out.append({k:v for k,v in r.items() if k!="df"}); print(out[-1],flush=True)
json.dump(out,open("scratch/P1/variants.json","w"),indent=1,default=float)
print("EVENTS DONE",flush=True)
