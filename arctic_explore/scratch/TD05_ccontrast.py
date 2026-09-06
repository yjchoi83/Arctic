import ee, json, numpy as np
ee.Initialize(project="alpha-earth-app")
S1=ee.ImageCollection("COPERNICUS/S1_GRD")
ROIS={"Sannikov":[138,74,145,77],"Chukchi":[-175,70,-168,73]}
SEAS={"melt":("2025-07-15","2025-09-05"),"winter":("2025-02-15","2025-04-05")}
out={}
for rn,b in ROIS.items():
    roi=ee.Geometry.Rectangle(b)
    for sn,(d0,d1) in SEAS.items():
        ew=(S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
              .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HH"))
              .filterDate(d0,d1))
        n=ew.size().getInfo()
        ts=sorted(set(ew.aggregate_array("system:time_start").getInfo()))
        t=np.array(ts)/3.6e6
        g=np.diff(t); g=g[g>0.3]
        sub=ew.sort("system:time_start").toList(min(n,14))
        st=[];mn=[]
        for i in range(min(n,14)):
            im=ee.Image(sub.get(i)).select("HH").clip(roi)
            try:
                r=im.reduceRegion(ee.Reducer.stdDev().combine(ee.Reducer.mean(),None,True),
                                  roi,400,maxPixels=3e6,bestEffort=True).getInfo()
            except Exception as e:
                print("rr fail",rn,sn,i,str(e)[:80]); break
            if r.get("HH_stdDev") is None: continue
            st.append(r["HH_stdDev"]); mn.append(r["HH_mean"])
        k=f"{rn}_{sn}"
        out[k]={"n_scenes":n,"n_acq":len(ts),
                "med_gap_h":round(float(np.median(g)),1) if len(g) else None,
                "frac_gap_le_72h":round(float((g<=72).mean()),2) if len(g) else None,
                "n_eval":len(st),
                "hh_std_dB_med":round(float(np.median(st)),2) if st else None,
                "hh_std_dB_p25p75":[round(float(np.percentile(st,25)),2),round(float(np.percentile(st,75)),2)] if st else None,
                "hh_mean_dB_med":round(float(np.median(mn)),2) if mn else None}
        print(k,out[k],flush=True)
json.dump(out,open("scratch/TD05_ccontrast.json","w"),indent=1)
