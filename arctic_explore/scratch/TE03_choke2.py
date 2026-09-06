import asf_search as asf, numpy as np, json, collections
CH = {
 "Kara_Gate":      "POLYGON((56 70,60 70,60 71.5,56 71.5,56 70))",
 "Vilkitsky":      "POLYGON((100 76.5,107 76.5,107 78.5,100 78.5,100 76.5))",
 "Sannikov":       "POLYGON((138 74,145 74,145 76.5,138 76.5,138 74))",
 "DmitryLaptev":   "POLYGON((139 72.5,143 72.5,143 74,139 74,139 72.5))",
 "Long_Strait":    "POLYGON((178 69.5,-176 69.5,-176 71.5,178 71.5,178 69.5))",
 "Bering_Strait":  "POLYGON((-172 64,-166 64,-166 67,-172 67,-172 64))",
 "Barrow_Strait":  "POLYGON((-98 73.8,-90 73.8,-90 75,-98 75,-98 73.8))",
 "Fram_Svalbard":  "POLYGON((5 78,20 78,20 81,5 81,5 78))",
 "Lat78_82_Kara":  "POLYGON((60 78,90 78,90 82,60 82,60 78))",
 "Transpolar_85N": "POLYGON((-20 84,40 84,40 87,-20 87,-20 84))",
}
out={}
for n,w in CH.items():
    try:
        r=asf.search(platform=[asf.PLATFORM.NISAR],processingLevel=["GCOV"],start="2026-06-17",
                     end="2026-09-04",intersectsWith=w,maxResults=3000)
    except Exception as e:
        print(n,"ERR",str(e)[:120]); continue
    g=[x.properties for x in r]
    if not g:
        out[n]={"n_gcov":0}; print(n,"ZERO"); continue
    mb=collections.Counter(str(p.get("mainBandPolarization")) for p in g)
    sb=collections.Counter(str(p.get("sideBandPolarization")) for p in g)
    fd=collections.Counter(str(p.get("flightDirection")) for p in g)
    lats=[p.get("centerLat") for p in g if p.get("centerLat") is not None]
    key=sorted([(str(p.get("pathNumber")),np.datetime64(p["startTime"][:19]).astype("datetime64[s]").astype(float)/3600.) for p in g],key=lambda k:k[1])
    passes=[]
    for pth,t in key:
        if passes and passes[-1][0]==pth and t-passes[-1][1]<0.42: passes[-1]=(pth,t)
        else: passes.append((pth,t))
    pt=np.sort(np.array([t for _,t in passes])); d=np.diff(pt)
    days=sorted({p["startTime"][:10] for p in g})
    lat=[]
    for p in g:
        try: lat.append((np.datetime64(str(p["processingDate"])[:19])-np.datetime64(str(p["stopTime"])[:19])).astype("timedelta64[m]").astype(float)/60.)
        except Exception: pass
    out[n]={"n_gcov":len(g),"n_pass":len(passes),"n_days":len(days),
      "span":[days[0],days[-1]],"n_paths":len(set(k[0] for k in key)),
      "mainpol":dict(mb),"sidepol":dict(sb),"dir":dict(fd),
      "centerLat":[round(min(lats),1),round(max(lats),1)] if lats else None,
      "gap_med_d":round(float(np.median(d))/24,2) if len(d) else None,
      "gap_p90_d":round(float(np.percentile(d,90))/24,2) if len(d) else None,
      "gap_max_d":round(float(d.max())/24,2) if len(d) else None,
      "obs_days_frac":round(len(days)/((np.datetime64(days[-1])-np.datetime64(days[0])).astype(int)+1),2),
      "lat_med_h":round(float(np.median(lat)),1) if lat else None,
      "lat_p90_h":round(float(np.percentile(lat,90)),1) if lat else None}
    print(n,json.dumps(out[n]))
json.dump(out,open("scratch/TE03_choke2.json","w"),indent=1)
