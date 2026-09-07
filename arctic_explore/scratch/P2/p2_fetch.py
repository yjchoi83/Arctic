import ee, json, os, sys, time
sys.path.insert(0,"scratch/P2")
from regions import regions
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
ee.Initialize()
R=regions(); OUT="scratch/P2/raw"; os.makedirs(OUT,exist_ok=True)
S1=ee.ImageCollection("COPERNICUS/S1_GRD")
for name,(w,e,s,n) in R.items():
    geom=ee.Geometry.Rectangle([w,s,e,n],None,False)
    A=geom.area(10000)
    for yr in range(2016,2027):
        f=f"{OUT}/{name}_{yr}.json"
        if os.path.exists(f): continue
        t0=time.time()
        col=(S1.filterDate(f"{yr}-01-01",f"{min(yr+1,2027)}-01-01")
               .filter(ee.Filter.inList("instrumentMode",["EW","IW"]))
               .filterBounds(geom))
        def m(img):
            cov=img.geometry().intersection(geom,10000).area(10000).divide(A)
            return ee.Feature(None,{"t":img.get("system:time_start"),
                                    "p":img.get("platform_number"),
                                    "o":img.get("orbitProperties_pass"),
                                    "m":img.get("instrumentMode"),"c":cov})
        fc=ee.FeatureCollection(col.map(m))
        try:
            d=fc.reduceColumns(ee.Reducer.toList(5),["t","p","o","m","c"]).get("list").getInfo()
        except Exception as ex:
            print(name,yr,"ERR",str(ex)[:120],flush=True); continue
        json.dump(d,open(f,"w"))
        print(f"{name} {yr} n={len(d)} {time.time()-t0:.0f}s",flush=True)
print("FETCH DONE",flush=True)
