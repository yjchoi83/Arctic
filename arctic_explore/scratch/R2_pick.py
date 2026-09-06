import asf_search as asf, re, json, datetime as dt
from shapely.geometry import shape
wkt="POLYGON((-172 70,-160 70,-160 74,-172 74,-172 70))"
n=asf.search(platform=[asf.PLATFORM.NISAR],start="2026-06-17",end="2026-09-30",
             processingLevel=["GCOV"],intersectsWith=wkt,maxResults=2000)
s1=asf.search(platform=[asf.PLATFORM.SENTINEL1],start="2026-06-17",end="2026-09-30",
              beamMode=["EW"],processingLevel=["GRD_MD"],intersectsWith=wkt,maxResults=4000)
def T(g): return dt.datetime.strptime(g.properties["startTime"][:19],"%Y-%m-%dT%H:%M:%S")
def pol(f): 
    m=re.search(r"_(SHSV|DHDH|SH|DH|QQ|NASV|SV|HH|DV)_",f or ""); return m.group(1) if m else "?"
cands=[]
for a in n:
    ga=shape(a.geometry); la=[c[1] for c in a.geometry["coordinates"][0]]
    if max(la)>78: continue
    for b in s1:
        h=abs((T(a)-T(b)).total_seconds())/3600
        if h>6: continue
        gb=shape(b.geometry); ov=ga.intersection(gb).area/ga.area
        if ov<0.5: continue
        cands.append(dict(dt_h=round(h,2),ov=round(ov,2),npol=pol(a.properties.get("fileID")),
            nid=a.properties.get("fileID"),nt=T(a).isoformat(),sz=a.properties.get("bytes"),
            s1=b.properties["sceneName"],st=T(b).isoformat(),s1pol=b.properties["polarization"],
            latmax=round(max(la),2)))
cands.sort(key=lambda x:(x['npol']!='DH',x['dt_h'],-x['ov']))
print("NISAR",len(n),"S1",len(s1),"candidates",len(cands))
for c in cands[:6]: print(" ",c['npol'],c['nt'],"| S1",c['st'],"| dt",c['dt_h'],"h ov",c['ov'],"latmax",c['latmax'],"sz",c['sz'])
json.dump(cands[:20],open("scratch/R2_cands.json","w"),indent=1)
