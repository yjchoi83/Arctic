import ee, json, os, numpy as np, datetime as dt, warnings
warnings.filterwarnings("ignore")
ee.Initialize(project="alpha-earth-app")
S1 = ee.ImageCollection("COPERNICUS/S1_GRD").filter(ee.Filter.eq("instrumentMode","EW"))
REG = {  # sector: RU = Russian Arctic, W = Western/allied
 "Kara_Gate":     ([56.0,69.5,61.0,71.5],"RU"),
 "Vilkitsky":     ([98.0,76.5,106.0,78.5],"RU"),
 "Sannikov":      ([136.0,73.5,143.0,76.0],"RU"),
 "Long_Strait":   ([176.0,68.5,179.9,71.0],"RU"),
 "Bering_Strait": ([-172.0,64.0,-166.0,67.0],"W"),
 "Chukchi_appr":  ([-170.0,68.0,-160.0,72.0],"W"),
 "NWP_Barrow":    ([-100.0,73.5,-92.0,75.5],"W"),
 "Barents_Svalb": ([15.0,76.0,30.0,79.5],"W"),
 "Greenland_E":   ([-25.0,68.0,-15.0,73.0],"W"),
}
YEARS = [2019,2021,2023,2025]
OUT = "/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/TE01_coverage.json"
res = json.load(open(OUT)) if os.path.exists(OUT) else {}
def stats(ts, y):
    t = np.array(sorted(set(ts)))/3600000.0
    n_sc = len(t)
    keep = []
    for x in t:
        if not keep or x-keep[-1] > 0.1667: keep.append(x)
    k = np.array(keep)
    ep = dt.datetime(1970,1,1)
    days = set(); days_ond = set(); n_ond = 0
    for x in k:
        d = ep + dt.timedelta(hours=float(x))
        days.add(d.date())
        if d.month >= 10:
            days_ond.add(d.date()); n_ond += 1
    g = np.diff(k) if len(k) > 1 else np.array([])
    # drift pairs: consecutive acquisitions 12-72 h apart
    pairs = int(((g >= 12) & (g <= 72)).sum())
    # Oct-Dec restricted pairs
    kd = [ep+dt.timedelta(hours=float(x)) for x in k]
    go = [ (kd[i+1]-kd[i]).total_seconds()/3600 for i in range(len(kd)-1) if kd[i].month>=10 and kd[i+1].month>=10 ]
    pairs_ond = int(sum(1 for v in go if 12 <= v <= 72))
    ndays = 366 if y%4==0 else 365
    return {"n_scenes":n_sc,"n_acq":len(k),
            "med_gap_h":round(float(np.median(g)),1) if len(g) else None,
            "p90_gap_h":round(float(np.percentile(g,90)),1) if len(g) else None,
            "obs_day_frac":round(len(days)/ndays,3),
            "obs_day_frac_OND":round(len(days_ond)/92.0,3),
            "n_acq_OND":n_ond,"pairs_12_72h":pairs,"pairs_OND":pairs_ond}
for name,(bx,sec) in REG.items():
    roi = ee.Geometry.Rectangle(bx, None, False)
    for y in YEARS:
        key = f"{name}_{y}"
        if key in res: continue
        try:
            ts = S1.filterBounds(roi).filterDate(f"{y}-01-01",f"{y+1}-01-01").aggregate_array("system:time_start").getInfo()
        except Exception as e:
            print(key,"ERR",str(e)[:80],flush=True); continue
        r = stats(ts,y); r["sector"]=sec
        res[key]=r
        json.dump(res,open(OUT,"w"),indent=0)
        print(key,sec,r["n_scenes"],r["obs_day_frac"],r["obs_day_frac_OND"],r["pairs_OND"],flush=True)
print("DONE",len(res))
