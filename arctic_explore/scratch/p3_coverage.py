import ee, json, warnings
warnings.filterwarnings("ignore")
ee.Initialize(project="alpha-earth-app")
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
regions = {
 "Kara_Gate":      [56.0, 69.5, 61.0, 71.5],
 "Vilkitsky":      [98.0, 76.5, 106.0, 78.5],
 "Sannikov":       [136.0, 73.5, 143.0, 76.0],
 "Long_Strait":    [176.0, 68.5, 183.0, 71.0],
 "Bering_Strait":  [-172.0, 64.0, -166.0, 67.0],
 "Chukchi_appr":   [-170.0, 68.0, -160.0, 72.0],
 "NWP_Barrow_Str": [-100.0, 73.5, -92.0, 75.5],
 "Barents_Svalb":  [15.0, 76.0, 30.0, 79.5],
 "Greenland_E":    [-25.0, 68.0, -15.0, 73.0],
 "Transpolar":     [80.0, 84.0, 120.0, 88.0],
}
out = {}
for name, bx in regions.items():
    roi = ee.Geometry.Rectangle(bx, None, False)
    base = S1.filterBounds(roi)
    row = {}
    for y in range(2016, 2027):
        d0, d1 = f"{y}-01-01", f"{y+1}-01-01"
        c = base.filterDate(d0, d1)
        ew = c.filter(ee.Filter.eq("instrumentMode", "EW")).size()
        iw = c.filter(ee.Filter.eq("instrumentMode", "IW")).size()
        row[y] = ee.Dictionary({"EW": ew, "IW": iw})
    out[name] = ee.Dictionary(row)
res = ee.Dictionary(out).getInfo()
json.dump(res, open("scratch/p3_coverage.json", "w"), indent=0)
print("region," + ",".join(str(y) for y in range(2016, 2027)) + "  (EW/IW)")
for n, r in res.items():
    print(n + "," + ",".join(f"{r[str(y)]['EW']}/{r[str(y)]['IW']}" for y in range(2016, 2027)))
