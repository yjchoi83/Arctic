import ee; ee.Initialize(project='alpha-earth-app')
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
sites = {"Nome":[-165.47,64.44,-165.30,64.52], "Utqiagvik":[-156.90,71.30,-156.55,71.42]}
for n,b in sites.items():
    roi = ee.Geometry.Rectangle(b)
    c = S1.filterBounds(roi)
    for mode in ["IW","EW"]:
        cc = c.filter(ee.Filter.eq("instrumentMode",mode))
        tot = cc.size().getInfo()
        print(n, mode, "total", tot)
        if tot:
            print("  by winter:", {y: cc.filterDate(f"{y}-09-01", f"{y+1}-08-31").size().getInfo() for y in range(2016,2026)})
            print("  relorbits:", sorted(set(cc.filterDate("2019-09-01","2020-08-31").aggregate_array("relativeOrbitNumber_start").getInfo())))
