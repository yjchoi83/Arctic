import ee, datetime as dt, json
ee.Initialize(project='alpha-earth-app')
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
roi = ee.Geometry.Rectangle([-165.48, 64.435, -165.36, 64.478])  # Nome port approach, all water
base = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","IW"))
          .filter(ee.Filter.listContains("transmitterReceiverPolarisation","VV")).select("VV"))
SC = 200
def norm(img):  # remove scene-level offset so mixed orbits are comparable
    m = ee.Number(img.reduceRegion(ee.Reducer.mean(), roi, SC, maxPixels=1e7).get("VV"))
    return img.subtract(m).rename("VVn").set("m", m, "t", img.date().millis())
out = []
for y in [2018, 2019, 2020, 2021, 2022, 2023]:
    s0 = dt.date(y, 10, 1); n = 36
    feats = []
    for i in range(n):
        a = s0 + dt.timedelta(days=8*i); b = a + dt.timedelta(days=16)
        w = base.filterDate(str(a), str(b))
        wn = w.map(norm)
        sd = wn.reduce(ee.Reducer.stdDev()).reduceRegion(ee.Reducer.mean(), roi, SC, maxPixels=1e7).get("VVn_stdDev")
        mn = ee.List(w.map(norm).aggregate_array("m"))
        feats.append(ee.Feature(None, {"d": str(a), "sd": sd, "n": w.size(), "mean": mn.reduce(ee.Reducer.mean())}))
    r = ee.FeatureCollection(feats).getInfo()
    rows = [f["properties"] for f in r["features"]]
    out.append({"season": f"{y}-{y+1}", "rows": rows})
    print(f"--- {y}-{y+1}")
    for p in rows:
        print(f'  {p["d"]} n={p.get("n")} sd={None if p.get("sd") is None else round(p["sd"],2)} mean={None if p.get("mean") is None else round(p["mean"],1)}')
json.dump(out, open("scratch/TI03_p2.json","w"))
