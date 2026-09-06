import ee, json, numpy as np, warnings, datetime as dt
warnings.filterwarnings("ignore")
ee.Initialize(project="alpha-earth-app")
roi = ee.Geometry.Rectangle([101.0, 77.4, 105.0, 77.95])
water = ee.Image("NOAA/NGDC/ETOPO1").select("bedrock").lt(-5)   # ocean mask
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
ew = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HH")))
OI = ee.ImageCollection("NOAA/CDR/OISST/V2_1").select("ice")
def owf(img):
    hh = img.select("HH").updateMask(water)
    ow = hh.lt(-18)
    d = ow.reduceRegion(ee.Reducer.mean(), roi, 400, maxPixels=1e9)
    return ee.Feature(None, {"t": img.date().format("YYYY-MM-dd'T'HH"), "ow": d.get("HH")})
def oif(img):
    return ee.Feature(None, {"t": img.date().format("YYYY-MM-dd"),
        "sic": img.updateMask(water).reduceRegion(ee.Reducer.mean(), roi, 25000, maxPixels=1e7).get("ice")})
YRS=[2017,2019,2021,2023,2025]; out={}
for y in YRS:
    a,b=f"{y}-06-15",f"{y}-11-16"
    s=ee.FeatureCollection(ew.filterDate(a,b).map(owf)).getInfo()["features"]
    sar=[(f["properties"]["t"],f["properties"]["ow"]) for f in s if f["properties"].get("ow") is not None]
    o=ee.FeatureCollection(OI.filterDate(a,b).map(oif)).getInfo()["features"]
    pm=[(f["properties"]["t"], (f["properties"].get("sic") or 0.0)/100.0) for f in o]
    out[y]={"sar":sar,"pm":pm}; print(y,len(sar),len(pm),flush=True)
json.dump(out,open("scratch/TB01_p4b.json","w"))
TH=0.30; rows=[]
for y in YRS:
    sar=sorted(out[y]["sar"]); pm=dict(out[y]["pm"])
    ts=[dt.datetime.strptime(t,"%Y-%m-%dT%H") for t,_ in sar]
    gaps=np.diff([t.timestamp() for t in ts])/3600. if len(ts)>1 else np.array([np.nan])
    dayv={}
    for t,ow in sar: dayv.setdefault(t[:10],[]).append(1.0-ow)
    dayice={k:float(np.mean(v)) for k,v in dayv.items()}
    nobs=len(dayice); nav_sar=sum(v<=TH for v in dayice.values())
    nav_pm_all=sum(v<=TH for v in pm.values()); ndays=len(pm)
    m=[(dayice[k],pm[k]) for k in dayice if k in pm]
    nav_pm_obs=sum(b<=TH for a,b in m)
    # bias-corrected extrapolation: SAR nav rate on observed days * full season length
    ext=nav_sar/nobs*ndays if nobs else float("nan")
    rows.append((y,len(sar),nobs,np.median(gaps),np.percentile(gaps,90),nav_sar,nav_pm_obs,nav_pm_all,ndays,ext,
                 float(np.mean([a for a,_ in m])),float(np.mean([b for _,b in m]))))
    print(f"{y} scenes={len(sar)} obsd={nobs} medgap={np.median(gaps):.0f}h p90={np.percentile(gaps,90):.0f}h "
          f"SARnav_obs={nav_sar}/{nobs} PMnav_obs={nav_pm_obs} PMnav_all={nav_pm_all}/{ndays} SARnav_ext={ext:.0f} "
          f"meanIce_SAR={np.mean([a for a,_ in m]):.2f} meanSIC_PM={np.mean([b for _,b in m]):.2f}")
e=[r[9] for r in rows]; p=[r[7] for r in rows]
print(f"SARext mean={np.mean(e):.1f} CV={np.std(e)/np.mean(e):.2f} worst={min(e):.0f} | PM mean={np.mean(p):.1f} CV={np.std(p)/np.mean(p):.2f} worst={min(p)}")
print("PM minus SAR per year:", [f"{p[i]-e[i]:+.0f}" for i in range(len(e))])
