import asf_search as asf, collections
WKT="POLYGON((110 72,180 72,180 78,110 78,110 72))"  # Laptev-E.Siberian-Chukchi NSR legs
try:
    r=asf.search(platform=[asf.PLATFORM.NISAR],start="2026-06-17",end="2026-09-04",
                 intersectsWith=WKT,maxResults=300)
    print("NISAR n=",len(r))
    c=collections.Counter((str(g.properties.get("processingLevel")),str(g.properties.get("beamModeType"))) for g in r)
    print(dict(c))
    ts=sorted(g.properties.get("startTime") for g in r)
    if ts: print("first",ts[0],"last",ts[-1])
except Exception as e:
    print("NISAR ERR",type(e).__name__,str(e)[:200])
