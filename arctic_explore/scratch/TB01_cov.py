import ee,warnings; warnings.filterwarnings("ignore")
ee.Initialize(project="alpha-earth-app")
S1=ee.ImageCollection("COPERNICUS/S1_GRD")
rois={"Vilkitsky":[101,77.4,105,77.95],"Long":[178,69.6,-178+360,70.6],"Bering":[-170,65.2,-167,66.2]}
for n,b in rois.items():
    r=ee.Geometry.Rectangle(b)
    ew=S1.filterBounds(r).filter(ee.Filter.eq("instrumentMode","EW"))
    print(n,{y:ew.filterDate(f"{y}-06-15",f"{y}-11-16").size().getInfo() for y in range(2015,2027)},flush=True)
