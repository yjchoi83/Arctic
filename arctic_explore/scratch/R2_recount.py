import asf_search as asf, re, json, datetime as dt, numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
from pyproj import Transformer
tr=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
def poly(g):
    cs=g["coordinates"][0]
    x,y=tr.transform([c[0] for c in cs],[c[1] for c in cs])
    p=Polygon(zip(x,y))
    return p if p.is_valid else p.buffer(0)
def T(g): return dt.datetime.strptime(g.properties["startTime"][:19],"%Y-%m-%dT%H:%M:%S")
def pol(f):
    m=re.search(r"_(SHSV|DHDH|SH|DH|QQ|NASV|SV|HH|DV)_",f or ""); return m.group(1) if m else "?"
ROIS={"ESib_Laptev":"POLYGON((110 74,180 74,180 78,110 78,110 74))",
      "Beaufort_N":"POLYGON((-160 73,-120 73,-120 78,-160 78,-160 73))",
      "Kara_N":"POLYGON((50 74,110 74,110 78,50 78,50 74))",
      "Chukchi":"POLYGON((-172 70,-160 70,-160 74,-172 74,-172 70))"}
tot={"nisar_gcov":0,"dhdh":0,"time6h_roi":0,"true_ovl50":0}
best=[]
for nm,wkt in ROIS.items():
    n=asf.search(platform=[asf.PLATFORM.NISAR],start="2026-06-17",end="2026-09-03",
                 processingLevel=["GCOV"],intersectsWith=wkt,maxResults=4000)
    s1=asf.search(platform=[asf.PLATFORM.SENTINEL1],start="2026-06-17",end="2026-09-03",
                  beamMode=["EW"],processingLevel=["GRD_MD"],intersectsWith=wkt,maxResults=8000)
    S=[(T(b),poly(b.geometry),b.properties["sceneName"]) for b in s1]
    tot["nisar_gcov"]+=len(n)
    nd=[a for a in n if pol(a.properties.get("fileID"))=="DHDH"]
    tot["dhdh"]+=len(nd)
    t6=o5=0
    for a in nd:
        la=[c[1] for c in a.geometry["coordinates"][0]]
        if max(la)>78: continue
        ta=T(a); ga=poly(a.geometry); hit_t=False; hit_o=False
        for tb,gb,nmb in S:
            h=abs((ta-tb).total_seconds())/3600
            if h>6: continue
            hit_t=True
            f=ga.intersection(gb).area/max(ga.area,1)
            if f>=0.5:
                hit_o=True
                best.append(dict(roi=nm,nid=a.properties["fileID"],nt=ta.isoformat(),s1=nmb,
                                 st=tb.isoformat(),dt_h=round(h,2),ovl=round(f,2),
                                 lat=[round(min(la),2),round(max(la),2)]))
        t6+=hit_t; o5+=hit_o
    tot["time6h_roi"]+=t6; tot["true_ovl50"]+=o5
    print(f"{nm}: GCOV {len(n)} DHDH {len(nd)} | <=6h&sameROI {t6} | TRUE overlap>=50% {o5}")
print("TOTAL",tot)
json.dump({"tot":tot,"pairs":best},open("scratch/R2_recount.json","w"),indent=1)
