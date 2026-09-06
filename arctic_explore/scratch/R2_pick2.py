import asf_search as asf, re, json, datetime as dt, numpy as np
from shapely.geometry import shape
ROIS={"ESib_Laptev":"POLYGON((110 74,180 74,180 78,110 78,110 74))",
      "Beaufort_N":"POLYGON((-160 73,-120 73,-120 78,-160 78,-160 73))",
      "Kara_N":"POLYGON((50 74,110 74,110 78,50 78,50 74))"}
def T(g): return dt.datetime.strptime(g.properties["startTime"][:19],"%Y-%m-%dT%H:%M:%S")
def pol(f):
    m=re.search(r"_(SHSV|DHDH|SH|DH|QQ|NASV|SV|HH|DV)_",f or ""); return m.group(1) if m else "?"
C=[]
for nm,wkt in ROIS.items():
    n=asf.search(platform=[asf.PLATFORM.NISAR],start="2026-06-17",end="2026-09-03",
                 processingLevel=["GCOV"],intersectsWith=wkt,maxResults=3000)
    n=[g for g in n if pol(g.properties.get("fileID"))=="DHDH"]
    s1=asf.search(platform=[asf.PLATFORM.SENTINEL1],start="2026-06-17",end="2026-09-03",
                  beamMode=["EW"],processingLevel=["GRD_MD"],intersectsWith=wkt,maxResults=6000)
    print(nm,"DHDH",len(n),"S1EW",len(s1))
    for a in n:
        la=[c[1] for c in a.geometry["coordinates"][0]]
        if max(la)>78: continue
        ga=shape(a.geometry)
        for b in s1:
            h=abs((T(a)-T(b)).total_seconds())/3600
            if h>6: continue
            ov=ga.intersection(shape(b.geometry)).area/ga.area
            if ov<0.6: continue
            C.append(dict(roi=nm,nid=a.properties["fileID"],nt=T(a).isoformat(),dt_h=round(h,2),ov=round(ov,2),
                          s1=b.properties["sceneName"],st=T(b).isoformat(),
                          lat=(round(min(la),2),round(max(la),2)),
                          ctr=[round(ga.centroid.x,2),round(ga.centroid.y,2)]))
            break
print("candidates",len(C))
json.dump(C,open("scratch/R2_cands2.json","w"),indent=0)
for c in C[:5]: print(" ",c['roi'],c['nt'],c['dt_h'],c['ov'],c['lat'],c['ctr'])
