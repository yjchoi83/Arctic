import ee, json, itertools, datetime as dt
ee.Initialize(project="alpha-earth-app")
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
boxes = {"ESS_Chukotka":[150,68,180,76], "Vilkitsky":[95,75,115,79]}
out={}
for name,b in boxes.items():
    roi = ee.Geometry.Rectangle(b)
    ew = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
            .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HH")))
    res={}
    for y,(m0,m1) in [(2016,("11-01","12-31")),(2017,("11-01","12-31")),(2021,("11-01","12-31")),
                      (2023,("11-01","12-31")),(2025,("11-01","12-31")),(2024,("11-01","12-31"))]:
        c = ew.filterDate(f"{y}-{m0}",f"{y}-{m1}")
        feats = c.reduceColumns(ee.Reducer.toList(3),
                  ["system:time_start","relativeOrbitNumber_start","platform_number"]).get("list").getInfo()
        n=len(feats)
        # count same-relative-orbit pairs separated by 1-3 days
        byorb={}
        for t,orb,plat in feats:
            byorb.setdefault(int(orb),[]).append(t/86400000.0)
        pairs=0
        for orb,ts in byorb.items():
            ts=sorted(ts)
            for a,bb in itertools.combinations(ts,2):
                d=bb-a
                if 0.8<=d<=3.2: pairs+=1
        res[y]={"scenes":n,"orbits":len(byorb),"pairs_1_3d":pairs}
        print(name,y,res[y],flush=True)
    out[name]=res
json.dump(out,open("/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/TC01_pairs.json","w"),indent=1)
