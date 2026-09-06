import ee; ee.Initialize(project="alpha-earth-app")
S1=ee.ImageCollection("COPERNICUS/S1_GRD")
rois={"Sannikov":[137,74.0,143,75.4],"ESS_beset":[160,70.0,168,72.5]}
for n,b in rois.items():
    roi=ee.Geometry.Rectangle(b)
    ew=(S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HH"))
        .filterDate("2021-11-01","2021-12-16"))
    f=ew.reduceColumns(ee.Reducer.toList(2),["system:time_start","relativeOrbitNumber_start"]).getInfo()["list"]
    print(n,"EW_HH scenes:",len(f))
    ds=sorted(set(__import__("datetime").datetime.utcfromtimestamp(t/1000).strftime("%m-%d") for t,_ in f))
    print("  days:",len(ds),ds[:14])
    print("  orbits:",sorted(set(int(o) for _,o in f)))
# S2 seasonal availability over Sannikov
S2=ee.ImageCollection("COPERNICUS/S2_HARMONIZED").filterBounds(ee.Geometry.Rectangle(rois["Sannikov"]))
for m in range(1,13):
    c=S2.filter(ee.Filter.calendarRange(m,m,"month")).filterDate("2019-01-01","2026-01-01")
    n=c.size().getInfo()
    sz=c.aggregate_mean("MEAN_SOLAR_ZENITH_ANGLE").getInfo() if n else None
    print("S2 month",m,"n=",n,"meanSZA=",None if sz is None else round(sz,1))
