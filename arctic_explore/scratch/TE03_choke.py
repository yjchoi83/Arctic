import asf_search as asf, numpy as np, json, collections
CH = {
 "Kara_Gate":      "POLYGON((56 70,60 70,60 71.5,56 71.5,56 70))",
 "Vilkitsky":      "POLYGON((100 76.5,107 76.5,107 78.5,100 78.5,100 76.5))",
 "Sannikov":       "POLYGON((138 74,145 74,145 76.5,138 76.5,138 74))",
 "DmitryLaptev":   "POLYGON((139 72.5,143 72.5,143 74,139 74,139 72.5))",
 "Long_Strait":    "POLYGON((178 69.5,-176 69.5,-176 71.5,178 71.5,178 69.5))",
 "Bering_Strait":  "POLYGON((-172 64,-166 64,-166 67,-172 67,-172 64))",
 "Barrow_Strait":  "POLYGON((-98 73.8,-90 73.8,-90 75,-98 75,-98 73.8))",
 "Transpolar_85N": "POLYGON((-20 84,40 84,40 87,-20 87,-20 84))",
 "Fram_Svalbard":  "POLYGON((5 78,20 78,20 81,5 81,5 78))",
}
out={}; fields_shown=False
for n,w in CH.items():
    try:
        r=asf.search(platform=[asf.PLATFORM.NISAR],start="2026-06-17",end="2026-09-04",
                     intersectsWith=w,maxResults=1200)
    except Exception as e:
        print(n,"ERR",str(e)[:150]); out[n]={"err":str(e)[:100]}; continue
    if not fields_shown and len(r):
        print("FIELDS:",sorted(r[0].properties.keys())); fields_shown=True
    g=[x.properties for x in r if str(x.properties.get("processingLevel"))=="GCOV"]
    pol=collections.Counter(str(p.get("polarization")) for p in g)
    lvl=collections.Counter(str(x.properties.get("processingLevel")) for x in r)
    # distinct pass = (pathNumber or flightDirection) + start time cluster within 25 min
    key=[]
    for p in g:
        t=np.datetime64(p["startTime"][:19]).astype("datetime64[s]").astype(float)/3600.
        key.append((str(p.get("pathNumber")),t))
    key.sort(key=lambda k:k[1])
    passes=[]
    for pth,t in key:
        if passes and passes[-1][0]==pth and t-passes[-1][1]<0.42: passes[-1]=(pth,t)
        else: passes.append((pth,t))
    pt=np.array([t for _,t in passes]); pt.sort()
    d=np.diff(pt)
    # latency
    lat=[]
    for p in g:
        pd_=p.get("processingDate") or p.get("processingTime")
        if pd_ and p.get("stopTime"):
            try:
                a=np.datetime64(str(pd_)[:19]); b=np.datetime64(str(p["stopTime"])[:19])
                lat.append((a-b).astype("timedelta64[h]").astype(float))
            except Exception: pass
    out[n]={"n_all":len(r),"n_gcov":len(g),"levels":dict(lvl),"pol":dict(pol),
        "n_frames_gcov":len(g),"n_distinct_pass":len(passes),
        "span":[min(p["startTime"] for p in g)[:10],max(p["startTime"] for p in g)[:10]] if g else None,
        "pass_gap_median_d":round(float(np.median(d))/24,2) if len(d) else None,
        "pass_gap_min_d":round(float(d.min())/24,2) if len(d) else None,
        "pass_gap_p90_d":round(float(np.percentile(d,90))/24,2) if len(d) else None,
        "n_paths":len(set(k[0] for k in key)),
        "latency_h_median":round(float(np.median(lat)),1) if lat else None,
        "latency_h_p10_p90":[round(float(np.percentile(lat,10)),1),round(float(np.percentile(lat,90)),1)] if lat else None}
    print(n,json.dumps(out[n]))
json.dump(out,open("/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/TE03_choke.json","w"),indent=1)
