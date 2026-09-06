import ee, json
ee.Initialize(project='alpha-earth-app')
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
roi = ee.Geometry.Rectangle([-165.48, 64.435, -165.36, 64.478])
SC = 200
base = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","IW"))
          .filter(ee.Filter.listContains("transmitterReceiverPolarisation","VV")).select("VV"))
out = []
for y in [2018,2019,2020,2021,2022,2023]:
    for orb in [15,117,124,153]:
        c = (base.filterDate(f"{y}-10-01", f"{y+1}-07-15")
                 .filter(ee.Filter.eq("relativeOrbitNumber_start", orb)).sort("system:time_start"))
        n = c.size().getInfo()
        if n < 2: continue
        L = c.toList(n); feats = []
        for i in range(n-1):
            a = ee.Image(L.get(i)); b = ee.Image(L.get(i+1))
            ma = ee.Number(a.reduceRegion(ee.Reducer.mean(), roi, SC, maxPixels=1e7).get("VV"))
            mb = ee.Number(b.reduceRegion(ee.Reducer.mean(), roi, SC, maxPixels=1e7).get("VV"))
            an = a.subtract(ma); bn = b.subtract(mb)
            tex = an.reduceRegion(ee.Reducer.stdDev(), roi, SC, maxPixels=1e7).get("VV")
            chg = bn.subtract(an).abs().reduceRegion(ee.Reducer.mean(), roi, SC, maxPixels=1e7).get("VV")
            feats.append(ee.Feature(None, {"d1": a.date().format("YYYY-MM-dd"), "d2": b.date().format("YYYY-MM-dd"),
                                           "orb": orb, "tex": tex, "chg": chg, "m": ma}))
        r = ee.FeatureCollection(feats).getInfo()
        for f in r["features"]:
            p = f["properties"]; out.append(p)
            print(f'{p["d1"]} -> {p["d2"]} orb{orb} tex={p["tex"]:.2f} chg={p["chg"]:.2f} m={p["m"]:.1f}')
json.dump(out, open("scratch/TI03_p2b.json","w"))
