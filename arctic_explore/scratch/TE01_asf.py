import asf_search as asf, json
BOX = {"Vilkitsky":[98.0,76.5,106.0,78.5],"Sannikov":[136.0,73.5,143.0,76.0],
       "Long_Strait":[176.0,68.5,179.9,71.0],"NWP_Barrow":[-100.0,73.5,-92.0,75.5]}
JOBS = [("Vilkitsky",2021),("Vilkitsky",2023),("Vilkitsky",2025),("Sannikov",2025),
        ("Long_Strait",2023),("NWP_Barrow",2023)]
def wkt(b):
    x0,y0,x1,y1=b
    return f"POLYGON(({x0} {y0},{x1} {y0},{x1} {y1},{x0} {y1},{x0} {y0}))"
out={}
for name,y in JOBS:
    try:
        r=asf.geo_search(platform=[asf.PLATFORM.SENTINEL1],processingLevel=['GRD_MD'],
            beamMode=['EW'],intersectsWith=wkt(BOX[name]),
            start=f"{y}-01-01T00:00:00Z",end=f"{y}-12-31T23:59:59Z",maxResults=6000)
        plats={}
        for s in r:
            p=s.properties.get('platform','?'); plats[p]=plats.get(p,0)+1
        out[f"{name}_{y}"]={"n":len(r),"by_platform":plats}
    except Exception as e:
        out[f"{name}_{y}"]={"err":str(e)[:120]}
    print(name,y,out[f"{name}_{y}"],flush=True)
json.dump(out,open("/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/TE01_asf.json","w"),indent=0)
