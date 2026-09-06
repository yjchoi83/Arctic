import ee, json, numpy as np, warnings
warnings.filterwarnings("ignore")
ee.Initialize(project="alpha-earth-app")
roi = ee.Geometry.Rectangle([101.0, 77.3, 105.0, 78.0])   # Vilkitsky Strait
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
ew = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HH")))
OI = ee.ImageCollection("NOAA/CDR/OISST/V2_1").select("ice")
def owf(img):
    ow = img.select("HH").lt(-18)
    return ee.Feature(None, {"t": img.date().format("YYYY-MM-dd'T'HH"),
        "ow": ow.reduceRegion(ee.Reducer.mean(), roi, 400, maxPixels=1e9).get("HH")})
def oif(img):
    return ee.Feature(None, {"t": img.date().format("YYYY-MM-dd"),
        "sic": img.reduceRegion(ee.Reducer.mean(), roi, 25000, maxPixels=1e7).get("ice")})
out={}
for y in [2017,2019,2021,2023,2025]:
    a,b=f"{y}-06-15",f"{y}-11-16"
    try:
        s=ee.FeatureCollection(ew.filterDate(a,b).map(owf)).getInfo()["features"]
        sar=[(f["properties"]["t"],f["properties"].get("ow")) for f in s if f["properties"].get("ow") is not None]
    except Exception as e:
        sar=[]; print(y,"SARERR",str(e)[:120])
    try:
        o=ee.FeatureCollection(OI.filterDate(a,b).map(oif)).getInfo()["features"]
        pm=[(f["properties"]["t"],f["properties"].get("sic")) for f in o]
        pm=[(t,0.0 if v is None else v) for t,v in pm]
    except Exception as e:
        pm=[]; print(y,"PMERR",str(e)[:120])
    out[y]={"sar":sar,"pm":pm}
    print(y,"nscene",len(sar),"npm",len(pm),flush=True)
json.dump(out,open("scratch/TB01_p4.json","w"))
# analysis
import datetime as dt
TH=0.30
for y,d in out.items():
    sar=sorted(d["sar"]); pm=sorted(d["pm"])
    if not sar: continue
    ts=[dt.datetime.strptime(t,"%Y-%m-%dT%H") for t,_ in sar]
    gaps=np.diff([t.timestamp() for t in ts])/3600.
    # per-day SAR ice fraction (mean of scenes that day)
    dayv={}
    for (t,ow) in sar: dayv.setdefault(t[:10],[]).append(1.0-ow)
    dayice={k:np.mean(v) for k,v in dayv.items()}
    nav_obs=sum(1 for v in dayice.values() if v<=TH); nobs=len(dayice)
    pmd={t:(v if v is not None else 0.0) for t,v in pm}
    nav_pm_all=sum(1 for v in pmd.values() if v<=TH)
    # matched-day comparison
    m=[(dayice[k],pmd[k]) for k in dayice if k in pmd]
    agree=sum(1 for a,b in m if (a<=TH)==(b<=TH))
    pm_nav_on_obs=sum(1 for a,b in m if b<=TH)
    print(f"{y}: scenes={len(sar)} obsdays={nobs} medgap_h={np.median(gaps):.0f} p90gap_h={np.percentile(gaps,90):.0f} "
          f"SARnav/obsday={nav_obs}/{nobs} PMnav_alldays={nav_pm_all}/{len(pmd)} "
          f"matched={len(m)} PMnav_on_obs={pm_nav_on_obs} SARnav_on_obs={sum(1 for a,b in m if a<=TH)} agree={agree}")
