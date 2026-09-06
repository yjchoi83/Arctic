import json, math, urllib.parse, urllib.request, numpy as np, pandas as pd, rasterio, io
from rasterio.warp import transform as rtransform
B="https://gis.ngdc.noaa.gov/arcgis/rest/services/"
def get(u,t=60):
    return json.loads(urllib.request.urlopen(u,timeout=t).read().decode())
WP=[(-168.75,65.75),(-168.5,67.0),(-167.5,68.5),(-165.5,70.0),(-161.0,71.3),(-156.5,71.42)]
# densify to 40 segment centroids
pts=[]
for i in range(len(WP)-1):
    for f in np.linspace(0,1,9,endpoint=False):
        pts.append((WP[i][0]+f*(WP[i+1][0]-WP[i][0]), WP[i][1]+f*(WP[i+1][1]-WP[i][1])))
pts=pts[:40]
def km(a,b):
    return 111.19*math.hypot((a[1]-b[1]),(a[0]-b[0])*math.cos(math.radians((a[1]+b[1])/2)))
PORT=[(-165.41,64.50),(-162.60,66.90),(-166.80,68.35),(-160.03,70.64),(-156.79,71.29),(-148.52,70.33),(-173.30,64.42)]
SARB=[(-165.41,64.50),(-162.60,66.90),(-156.79,71.29),(-148.46,70.19)]
def ident(svc,lay,p):
    g=urllib.parse.quote(json.dumps({"x":p[0],"y":p[1]}))
    u=(f"{B}{svc}/MapServer/identify?f=json&geometry={g}&geometryType=esriGeometryPoint&sr=4326"
       f"&layers=all:{lay}&tolerance=2&mapExtent={p[0]-1},{p[1]-1},{p[0]+1},{p[1]+1}&imageDisplay=400,400,96&returnGeometry=false")
    r=get(u).get("results",[])
    return r[0]["attributes"] if r else {}
rows=[]
for i,p in enumerate(pts):
    tid=ident("IHO/GEBCO_TID",0,p).get("UniqueValue.Pixel Value","")
    try: tid=int(tid)
    except: tid=-1
    a=ident("DEM_mosaics/DEM_global_mosaic",0,p)
    dep=[v for k,v in a.items() if "Pixel" in k or "Value" in k]
    try: dep=float(str(dep[0]).split()[0])
    except: dep=np.nan
    d=0.25
    q=(f"{B}web_mercator/nos_hydro_dynamic/MapServer/1/query?f=json&where=1%3D1&outFields=SURVEY_YEAR"
       f"&geometry={p[0]-d},{p[1]-d},{p[0]+d},{p[1]+d}&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&returnGeometry=false")
    try:
        fs=get(q).get("features",[])
        yrs=[f["attributes"].get("SURVEY_YEAR") for f in fs if f["attributes"].get("SURVEY_YEAR")]
        nsurv=len(fs); newest=max(yrs) if yrs else 1900
    except Exception: nsurv,newest=0,1900
    rows.append(dict(seg=i,lon=p[0],lat=p[1],tid=tid,depth=dep,n_survey=nsurv,newest_survey=int(newest),
        dist_refuge_km=min(km(p,q2) for q2 in PORT), dist_sar_km=min(km(p,q2) for q2 in SARB)))
df=pd.DataFrame(rows)
# AMSR2 Bremen SIC hazard frequency
MON={6:"jun",11:"nov"}
hits=np.zeros(len(pts)); tot=0
for y in range(2016,2026):
    for m,dd in ((11,15),(6,25)):
        url=f"https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n6250/{y}/{MON[m]}/Arctic/asi-AMSR2-n6250-{y}{m:02d}{dd}-v5.4.tif"
        try: buf=urllib.request.urlopen(url,timeout=90).read()
        except Exception: continue
        with rasterio.open(io.BytesIO(buf)) as ds:
            xs,ys=rtransform("EPSG:4326",ds.crs,[p[0] for p in pts],[p[1] for p in pts])
            v=np.array([s[0] for s in ds.sample(zip(xs,ys))],dtype=float)
        v[v>100]=np.nan
        hits+= (v>=70).astype(float); tot+=1
df["ice_hazard_freq"]=hits/max(tot,1)
df["n_amsr2_dates"]=tot
df.to_csv("scratch/TF01_segments.csv",index=False)
print(tot, df.shape)
print(df[["seg","lat","tid","depth","n_survey","newest_survey","dist_refuge_km","ice_hazard_freq"]].to_string(index=False))
