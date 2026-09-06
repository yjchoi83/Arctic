import asf_search as asf, json, itertools, datetime as dt
from shapely.geometry import shape
wkt="POLYGON((-172 69.5,-164 69.5,-164 72.5,-172 72.5,-172 69.5))"
def find(s,e,tag):
    r=asf.geo_search(platform=[asf.PLATFORM.SENTINEL1],processingLevel=['GRD_MD'],beamMode=['EW'],
                     intersectsWith=wkt,start=s,end=e)
    S=[]
    for p in r:
        pr=p.properties
        if 'HH' not in pr['polarization']: continue
        S.append(dict(n=pr['sceneName'],t=dt.datetime.fromisoformat(pr['startTime'][:19]),
                      path=pr['pathNumber'],geom=shape(p.geometry),url=pr['url']))
    out=[]
    for a,b in itertools.combinations(sorted(S,key=lambda x:x['t']),2):
        h=(b['t']-a['t']).total_seconds()/3600
        if not (18<=h<=78): continue
        inter=a['geom'].intersection(b['geom']).area
        f=inter/min(a['geom'].area,b['geom'].area)
        if f<0.45: continue
        out.append(dict(tag=tag,a=a['n'],b=b['n'],dt_h=round(h,1),ovl=round(f,2),
                        t0=a['t'].isoformat(),t1=b['t'].isoformat(),pa=a['path'],pb=b['path']))
    print(tag,"scenes",len(S),"candidate pairs",len(out))
    for o in sorted(out,key=lambda x:-x['ovl'])[:6]:
        print("   ",o['t0'],o['t1'],o['dt_h'],"h ovl",o['ovl'],o['pa'],"->",o['pb'])
    return out
allp=[]
for tag,(s,e) in {"melt23":("2023-07-01","2023-08-31"),"melt24":("2024-07-01","2024-08-31"),
                  "win23":("2023-02-01","2023-03-31"),"win24":("2024-02-01","2024-03-31")}.items():
    allp+=find(s,e,tag)
json.dump(allp,open("scratch/R1_pairs.json","w"),indent=0)
