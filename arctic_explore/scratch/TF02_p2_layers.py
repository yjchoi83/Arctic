import json,urllib.request,urllib.parse,math,time
TID="https://gis.ngdc.noaa.gov/arcgis/rest/services/IHO/GEBCO_TID/MapServer/identify"
NOS="https://gis.ngdc.noaa.gov/arcgis/rest/services/web_mercator/nos_hydro_dynamic/MapServer/%d/query"
def get(u):
    r=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    return json.load(urllib.request.urlopen(r,timeout=60))
def tid(lon,lat):
    q=dict(geometry=json.dumps({"x":lon,"y":lat}),geometryType="esriGeometryPoint",sr=4326,
           layers="all",tolerance=1,mapExtent=f"{lon-1},{lat-1},{lon+1},{lat+1}",
           imageDisplay="400,400,96",returnGeometry="false",f="json")
    try:
        r=get(TID+"?"+urllib.parse.urlencode(q))["results"]
        return int(r[0]["attributes"]["UniqueValue.Pixel Value"]) if r else None
    except Exception as e: return None
# NWP corridor waypoints (Bering approach -> Gulf of Boothia), AIS-free: published route geometry
WP=[(-168.5,65.8),(-166.0,68.9),(-160.0,71.0),(-152.0,71.3),(-141.0,70.6),(-133.0,70.2),
    (-125.0,70.3),(-118.0,69.0),(-112.0,68.3),(-106.0,68.6),(-101.0,69.2),(-96.0,69.6),
    (-92.0,70.3),(-89.5,71.5)]
def interp(wp,n):
    segs=[];tot=len(wp)-1
    for i in range(tot):
        a,b=wp[i],wp[i+1]
        for k in range(n):
            t=k/n; segs.append((a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t))
    segs.append(wp[-1]); return segs
segs=interp(WP,3)
print("segments:",len(segs))
rows=[]
for lon,lat in segs:
    rows.append((lon,lat,tid(lon,lat)))
DIRECT=set(range(10,18))
ok=[r for r in rows if r[2] is not None]
print("TID retrieved:",len(ok),"/",len(rows))
from collections import Counter
print("TID codes:",Counter(r[2] for r in ok).most_common())
meas=sum(1 for r in ok if r[2] in DIRECT)
print("direct-measurement segments: %d (%.0f%%)"%(meas,100*meas/len(ok)))
# grounding positions (dated, georeferenced, charting-attributed)
GR=[("Clipper Adventurer 2010-08-27",-112.65,68.15),
    ("Akademik Ioffe 2018-08-24",-89.75,69.60),
    ("Nanny 2010-10-.. Simpson Str",-96.5,68.6),
    ("Hanseatic 1996-08-29 Simpson Str",-96.6,68.55)]
print("--- grounding-point TID")
for n,lo,la in GR: print(" ",n,"TID=",tid(lo,la))
# NOAA NOS survey coverage over Chukchi/Beaufort AK segment
for L,nm in [(0,"BAGs"),(1,"digital soundings"),(2,"no digital soundings")]:
    u=(NOS%L)+"?where=1%3D1&geometry=-170,66,-140,73&geometryType=esriGeometryEnvelope&inSR=4326"\
      "&spatialRel=esriSpatialRelIntersects&returnCountOnly=true&f=json"
    try: print("NOS",nm,"polys in AK Arctic bbox:",get(u).get("count"))
    except Exception as e: print("NOS",nm,"ERR",e)
