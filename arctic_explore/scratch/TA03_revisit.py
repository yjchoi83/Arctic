import ee, numpy as np, json
ee.Initialize(project="alpha-earth-app")
S1 = ee.ImageCollection("COPERNICUS/S1_GRD").filter(ee.Filter.eq("instrumentMode","EW"))
ROIS = {
 "Vilkitsky": [103.0,77.2,107.0,78.2],
 "Sannikov": [138.0,74.2,142.0,75.2],
 "BeringStr": [-170.5,65.2,-167.5,66.2],
}
YEARS = {"2021":("2021-01-01","2022-01-01"),"2023":("2023-01-01","2024-01-01"),"2026":("2026-01-01","2026-09-01")}
out={}
for rn,bb in ROIS.items():
    roi=ee.Geometry.Rectangle(bb)
    for yn,(d0,d1) in YEARS.items():
        c=S1.filterBounds(roi).filterDate(d0,d1)
        ts=c.aggregate_array("system:time_start").getInfo()
        ts=sorted(set(ts))
        t=np.array(ts)/3600000.0  # hours
        # collapse near-simultaneous frames of same pass (<10 min) into one acquisition
        keep=[t[0]] if len(t) else []
        for x in t[1:]:
            if x-keep[-1]>0.1667: keep.append(x)
        k=np.array(keep)
        gaps=np.diff(k) if len(k)>1 else np.array([])
        out[f"{rn}_{yn}"]={"n_scenes":len(ts),"n_acq":len(k),
          "med_gap_h":round(float(np.median(gaps)),2) if len(gaps) else None,
          "p90_gap_h":round(float(np.percentile(gaps,90)),2) if len(gaps) else None,
          "p99_gap_h":round(float(np.percentile(gaps,99)),2) if len(gaps) else None,
          "max_gap_h":round(float(gaps.max()),2) if len(gaps) else None,
          "frac_gap_gt24h":round(float((gaps>24).mean()),3) if len(gaps) else None,
          "frac_gap_gt48h":round(float((gaps>48).mean()),3) if len(gaps) else None}
        print(f"{rn}_{yn}",out[f"{rn}_{yn}"],flush=True)
json.dump(out,open("scratch/TA03_revisit.json","w"),indent=1)
