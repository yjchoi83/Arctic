import pandas as pd, numpy as np, os, sys, datetime as dt, urllib.request, csv
import asf_search as asf
sys.path.insert(0,"scratch/P3"); from cells import region_cells, CELL
from pyproj import Transformer
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
OUT="results/P4/quicklooks"; os.makedirs(OUT,exist_ok=True)
inv=Transformer.from_crs("EPSG:3413","EPSG:4326",always_xy=True)
RC=region_cells()
C=pd.read_csv("scratch/P4/convergence_days.csv")
C=C[(C.region.isin(["Vilkitsky","Sannikov_DmLaptev","LongStrait"]))&(C.obs24)]
C=C.sort_values("div")           # strongest convergence first
print("candidate events",len(C),"by region:",C.groupby('region').size().to_dict(),flush=True)
rows=[];n=0
seen=set()
for _,r in C.iterrows():
    if n>=14: break
    key=(r.region,r.date)
    if key in seen: continue
    a,b=RC[r.region][int(r.cell)]
    lon,lat=inv.transform(a+CELL/2,b+CELL/2)
    t=dt.datetime.utcfromtimestamp(r.tmid)
    wkt=f"POINT({lon:.3f} {lat:.3f})"
    try:
        res=asf.geo_search(platform=[asf.PLATFORM.SENTINEL1],processingLevel=['GRD_MD'],beamMode=['EW'],
                           intersectsWith=wkt,start=(t-dt.timedelta(hours=36)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                           end=(t+dt.timedelta(hours=36)).strftime("%Y-%m-%dT%H:%M:%SZ"))
    except Exception as e:
        print("asf err",str(e)[:80]); continue
    sc=sorted([p for p in res if 'HH' in (p.properties.get('polarization') or '')],
              key=lambda p:p.properties['startTime'])
    if len(sc)<2: continue
    ts=[dt.datetime.strptime(p.properties['startTime'][:19],"%Y-%m-%dT%H:%M:%S") for p in sc]
    best=None
    for i in range(len(sc)-1):
        for j in range(i+1,len(sc)):
            h=(ts[j]-ts[i]).total_seconds()/3600
            if h<=0 or h>24: continue
            span=max(abs((ts[i]-t).total_seconds()),abs((ts[j]-t).total_seconds()))/3600
            if span>30: continue
            brackets=ts[i]<=t<=ts[j]
            score=(0 if brackets else 1,span)
            if best is None or score<best[0]: best=(score,i,j,h)
    if best is None: continue
    _,i,j,dt_h=best; p0,p1=sc[i],sc[j]
    seen.add(key); n+=1
    ev=f"{r.region}_{r.date}"
    got=[]
    for tag,p in (("before",p0),("after",p1)):
        u=(p.properties.get('browse') or [None])[0]
        if not u: continue
        fn=f"{OUT}/{ev}_{tag}.jpg"
        try:
            urllib.request.urlretrieve(u,fn); got.append(tag)
        except Exception: pass
    rows.append(dict(event=ev,region=r.region,date=r.date,div=round(float(r["div"]),4),
                     p10=round(float(r.p10),4),pair_dt_h=round(dt_h,1),
                     scene_before=p0.properties['sceneName'],scene_after=p1.properties['sceneName'],
                     quicklooks=";".join(got),decision="",
                     auto_note="visible ridging/lead closure: UNSCORED - browse JPEG only"))
    print(n,ev,"dt %.1f h"%dt_h,got,flush=True)
with open("results/P4/qc_table.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("wrote",len(rows),"events",flush=True)
