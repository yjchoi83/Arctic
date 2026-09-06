import ee, json
ee.Initialize(project="alpha-earth-app")
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
roi = ee.Geometry.Rectangle([-170.0,65.0,-167.0,66.5])  # Bering Strait chokepoint
ew = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
      .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HV"))
      .filterDate("2024-03-01","2024-03-31"))
print("n_scenes_Mar2024:", ew.size().getInfo())
im = ee.Image(ew.first())
p = im.toDictionary().getInfo()
for k in sorted(p): 
    v=p[k]
    print(k,"=",str(v)[:90])
print("BANDS:", im.bandNames().getInfo())
