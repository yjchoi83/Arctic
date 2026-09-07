import asf_search as asf, numpy as np, json, itertools, datetime as dt, sys
from shapely.geometry import Polygon
from pyproj import Transformer
sys.path.insert(0,"scratch/P2"); from regions import regions
T=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
R=regions(); CH=["Vilkitsky","Sannikov_DmLaptev","LongStrait"]
def p3413(geo):
    cs=geo["coordinates"][0]
    x,y=T.transform([c[0] for c in cs],[c[1] for c in cs])
    p=Polygon(zip(x,y)); return p if p.is_valid else p.buffer(0)
def boxpoly(w,e,s,n):
    lo=np.concatenate([np.linspace(w,e,30),np.full(30,e),np.linspace(e,w,30),np.full(30,w)])
    la=np.concatenate([np.full(30,s),np.linspace(s,n,30),np.full(30,n),np.linspace(n,s,30)])
    x,y=T.transform(lo,la); return Polygon(zip(x,y))
WIN=[(y,a,b) for y in (2019,2020,2021) for a,b in [(f"{y}-01-01",f"{y}-03-31"),(f"{y}-10-01",f"{y}-12-31")]]
out=[]
for r in CH:
    w,e,s,n=R[r]; B=boxpoly(w,e,s,n); AB=B.area
    wkt=f"POLYGON(({w} {s},{e} {s},{e} {n},{w} {n},{w} {s}))"
    for yr,a,b in WIN:
        try:
            res=asf.geo_search(platform=[asf.PLATFORM.SENTINEL1],processingLevel=['GRD_MD'],
                               beamMode=['EW'],intersectsWith=wkt,start=a,end=b)
        except Exception as ex:
            print(r,a,"ERR",str(ex)[:80]); continue
        S=[]
        for p in res:
            pr=p.properties
            if 'HH' not in (pr.get('polarization') or ''): continue
            g=p3413(p.geometry); cov=g.intersection(B).area/AB
            if cov<0.30: continue
            S.append(dict(n=pr['sceneName'],t=dt.datetime.strptime(pr['startTime'][:19],"%Y-%m-%dT%H:%M:%S"),
                          g=g,cov=cov,sz=pr.get('bytes')))
        S.sort(key=lambda z:z['t'])
        for i,j in itertools.combinations(range(len(S)),2):
            h=(S[j]['t']-S[i]['t']).total_seconds()/3600
            if h<12 or h>72: continue
            ov=S[i]['g'].intersection(S[j]['g']).area/min(S[i]['g'].area,S[j]['g'].area)
            if ov<0.5: continue
            out.append(dict(region=r,year=yr,season="winter" if a.endswith("01-01") else "freeze-up",
                            a=S[i]['n'],b=S[j]['n'],t0=S[i]['t'].isoformat(),t1=S[j]['t'].isoformat(),
                            dt_h=round(h,1),ovl=round(ov,2),cov_a=round(S[i]['cov'],2),cov_b=round(S[j]['cov'],2)))
        print(r,a[:7],"scenes",len(S),"pairs so far",len(out),flush=True)
json.dump(out,open("scratch/P8/pairs_all.json","w"),indent=0)
print("TOTAL candidate pairs",len(out))
import collections
print(collections.Counter((o['region'],o['season']) for o in out))
