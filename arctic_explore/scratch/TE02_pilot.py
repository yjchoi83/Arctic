import ee, numpy as np, pandas as pd
ee.Initialize(project="alpha-earth-app")
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
roi = ee.Geometry.Rectangle([-172.0,64.5,-166.0,68.5])   # Bering Strait / S. Chukchi chokepoint
ew = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
      .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HV"))
      .filterDate("2024-02-15","2024-03-31")
      .sort("system:time_start"))
ids = ew.aggregate_array("system:index").getInfo()
print("scenes avail:", len(ids))
rows=[]
for sid in ids[:6]:
    img = ee.Image(ew.filter(ee.Filter.eq("system:index", sid)).first())
    ipf = img.get("GRD_Post_Processing_software_version").getInfo()
    dt  = ee.Date(img.get("system:time_start")).format("YYYY-MM-dd").getInfo()
    samp = img.select(["HH","HV","angle"]).sample(
        region=roi, scale=200, numPixels=1500, seed=42, dropNulls=True, geometries=False)
    f = samp.getInfo()["features"]
    for x in f:
        p=x["properties"]; p["scene"]=sid; p["ipf"]=ipf; p["date"]=dt; rows.append(p)
    print(sid, dt, "IPF", ipf, "n=", len(f))
df = pd.DataFrame(rows).dropna()
df.to_csv("scratch/TE02_samples.csv", index=False)
print("TOTAL n =", len(df), "| IPF versions:", sorted(df.ipf.unique()))
print("angle range: %.1f - %.1f deg"%(df.angle.min(), df.angle.max()))
for pol in ["HH","HV"]:
    b,a = np.polyfit(df.angle, df[pol], 1)
    span = df.angle.max()-df.angle.min()
    print(f"{pol}: slope {b:+.3f} dB/deg -> {b*span:+.2f} dB across {span:.1f} deg swath; mean {df[pol].mean():.2f}")
    # per-scene fold spread
    sl=[np.polyfit(g.angle,g[pol],1)[0] for _,g in df.groupby("scene") if len(g)>100]
    print(f"   per-scene slope spread: {min(sl):+.3f} .. {max(sl):+.3f} dB/deg (n_scenes={len(sl)})")
# ---- hazard threshold flip test (low-backscatter / open-water-or-smooth-ice class) ----
for pol,thr in [("HV",-28.0),("HH",-18.0)]:
    b,a = np.polyfit(df.angle, df[pol], 1)
    norm = df[pol] - b*(df.angle - 35.0)          # normalise to 35 deg reference
    raw_cls  = (df[pol] < thr).values
    norm_cls = (norm   < thr).values
    flip = (raw_cls != norm_cls).mean()
    print(f"{pol} thr={thr} dB: raw class frac {raw_cls.mean():.3f}, angle-normalised {norm_cls.mean():.3f}, FLIP RATE {flip*100:.2f}%")
    # flip rate restricted to near/far swath edges
    for lab,m in [("near(<27deg)",df.angle<27),("far(>41deg)",df.angle>41)]:
        if m.sum()>50: print(f"    {lab}: n={m.sum()}, flip {(raw_cls[m.values]!=norm_cls[m.values]).mean()*100:.1f}%")
