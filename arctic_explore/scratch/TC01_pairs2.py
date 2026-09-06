import ee, json, numpy as np
ee.Initialize(project="alpha-earth-app")
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
# ~100 km cells at plausible besetting sites (Nov 2021 cluster: ESS + N Chukotka; plus Vilkitsky)
cells = {"ESS_166E_71N":[165,70.5,167,71.5], "Chukotka_178W_69N":[-179,68.5,-177,69.5],
         "Vilkitsky_104E_77.5N":[103,77.2,105,77.8]}
out={}
for name,b in cells.items():
    roi = ee.Geometry.Rectangle(b)
    ew = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
            .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HH")))
    res={}
    for y in [2016,2017,2021,2023,2024,2025]:
        ts = ew.filterDate(f"{y}-11-01",f"{y}-12-31").aggregate_array("system:time_start").getInfo()
        t = np.sort(np.array(ts)/86400000.0)
        if len(t)<2:
            res[y]={"scenes":len(t)}; print(name,y,res[y],flush=True); continue
        g = np.diff(t)
        res[y]={"scenes":int(len(t)),"days_covered":int(len(np.unique(np.floor(t)))),
                "med_gap_h":round(float(np.median(g))*24,1),
                "n_gaps_0.5_3d":int(((g>=0.5)&(g<=3.0)).sum()),
                "max_gap_d":round(float(g.max()),1)}
        print(name,y,res[y],flush=True)
    out[name]=res
json.dump(out,open("/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/TC01_pairs2.json","w"),indent=1)
