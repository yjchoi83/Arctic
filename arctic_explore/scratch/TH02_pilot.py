import ee, json, sys
ee.Initialize(project='alpha-earth-app')
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
# Bering-Chukchi corridor (Bering Strait -> Chukchi shipping corridor)
roi = ee.Geometry.Rectangle([-172.0, 66.0, -165.0, 70.0])
ew = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HH"))
        .select("HH"))
THR = [-20.0, -22.0, -25.0]
SEASONS = {"winter_JFM":("2023-01-15","2023-03-15"),
           "melt_JJA":("2023-07-01","2023-08-15"),
           "freezeup_OND":("2023-10-15","2023-12-01")}
out={}
for name,(d0,d1) in SEASONS.items():
    col = ew.filterDate(d0,d1)
    n = col.size().getInfo()
    ids = col.limit(6).aggregate_array('system:index').getInfo()
    rows=[]
    for i in ids:
        img = ee.Image(col.filter(ee.Filter.eq('system:index',i)).first())
        g = img.geometry().intersection(roi, 1000)
        d = {}
        for t in THR:
            d[str(t)] = img.lt(t).rename('f')
        stack = ee.Image.cat([d[str(t)].rename('t%d'%abs(int(t))) for t in THR])
        try:
            r = stack.reduceRegion(ee.Reducer.mean(), g, 1000, maxPixels=3e6, bestEffort=True).getInfo()
            npx = img.mask().reduceRegion(ee.Reducer.count(), g, 1000, maxPixels=3e6, bestEffort=True).getInfo()
            r['n_px']=npx.get('HH'); r['id']=i
            rows.append(r); print(name, i[:25], r, flush=True)
        except Exception as e:
            print("ERR", i[:20], str(e)[:100], flush=True)
    out[name]={"n_scenes_total":n,"rows":rows}
json.dump(out, open('/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/TH02_pilot_out.json','w'), indent=1)
print("DONE")
