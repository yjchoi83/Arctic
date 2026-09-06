import asf_search as asf, numpy as np, json
ROIS={"Sannikov":"POLYGON((138 74,145 74,145 77,138 77,138 74))",
      "Chukchi":"POLYGON((-175 70,-168 70,-168 73,-175 73,-175 70))"}
out={}
for n,w in ROIS.items():
    try:
        r=asf.search(platform=[asf.PLATFORM.NISAR],start="2026-06-17",end="2026-09-04",
                     intersectsWith=w,maxResults=900)
    except Exception as e:
        print(n,"ERR",str(e)[:150]); continue
    t=sorted({g.properties["startTime"] for g in r if str(g.properties.get("processingLevel"))=="GCOV"})
    if len(t)<3: print(n,"few GCOV",len(t),"total",len(r)); 
    tt=np.array([np.datetime64(x[:19]) for x in t]).astype("datetime64[s]").astype(float)/3600
    g=np.diff(tt); g=g[g>0.2]
    out[n]={"n_gcov":len(t),"n_all":len(r),"span":[t[0][:10],t[-1][:10]] if t else None,
            "med_gap_h":round(float(np.median(g)),1) if len(g) else None,
            "frac_gap_le_72h":round(float((g<=72).mean()),2) if len(g) else None,
            "frac_gap_le_24h":round(float((g<=24).mean()),2) if len(g) else None,
            "min_gap_h":round(float(g.min()),1) if len(g) else None}
    print(n,out[n])
json.dump(out,open("scratch/TD05_nisar_gap.json","w"),indent=1)
