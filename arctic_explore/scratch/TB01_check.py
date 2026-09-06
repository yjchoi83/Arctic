import ee
ee.Initialize(project="alpha-earth-app")
for cid in ["NOAA/CDR/OISST/V2_1"]:
    try:
        c=ee.ImageCollection(cid)
        im=c.filterDate("2023-08-01","2023-08-03").first()
        print(cid, im.bandNames().getInfo(), im.date().format().getInfo())
    except Exception as e:
        print(cid,"ERR",str(e)[:200])
