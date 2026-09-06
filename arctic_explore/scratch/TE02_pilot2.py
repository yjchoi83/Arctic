import ee, numpy as np, pandas as pd
ee.Initialize(project="alpha-earth-app")
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
roi = ee.Geometry.Rectangle([95.0,75.0,110.0,78.5])   # Vilkitsky/Kara-Laptev chokepoint, winter landfast+pack
def get(y0,y1):
    return (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode","EW"))
            .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HV"))
            .filterDate(y0,y1).sort("system:time_start"))
rows=[]
for era,(d0,d1) in [("2018",("2018-03-01","2018-03-20")),("2024",("2024-03-01","2024-03-20"))]:
    c=get(d0,d1); ids=c.aggregate_array("system:index").getInfo()
    print(era,"scenes:",len(ids))
    for sid in ids[:3]:
        img=ee.Image(c.filter(ee.Filter.eq("system:index",sid)).first())
        ipf=img.get("GRD_Post_Processing_software_version").getInfo()
        s=img.select(["HH","HV","angle"]).sample(region=roi,scale=200,numPixels=2000,seed=7,dropNulls=True)
        f=s.getInfo()["features"]
        for x in f:
            p=x["properties"]; p.update(scene=sid,ipf=ipf,era=era); rows.append(p)
        print("  ",sid[:32],"IPF",ipf,"n=",len(f))
df=pd.DataFrame(rows).dropna(); df.to_csv("scratch/TE02_samples2.csv",index=False)
print("TOTAL n =",len(df),"| IPF:",sorted(df.ipf.unique()))
print("angle %.1f-%.1f"%(df.angle.min(),df.angle.max()))
for era,g in df.groupby("era"):
    print(f"-- era {era} (IPF {sorted(g.ipf.unique())}) n={len(g)} angle {g.angle.min():.1f}-{g.angle.max():.1f}")
    for pol in ["HH","HV"]:
        b,a=np.polyfit(g.angle,g[pol],1); span=g.angle.max()-g.angle.min()
        print(f"   {pol}: {b:+.3f} dB/deg -> {b*span:+.2f} dB across swath; mean {g[pol].mean():.2f}, sd {g[pol].std():.2f}")
    # sub-swath binned means (2 deg bins) -> residual scalloping amplitude after linear detrend
    for pol in ["HH","HV"]:
        b,a=np.polyfit(g.angle,g[pol],1); r=g[pol]-(b*g.angle+a)
        bm=r.groupby(pd.cut(g.angle,np.arange(np.floor(g.angle.min()),g.angle.max()+2,2))).mean().dropna()
        print(f"   {pol} residual per-2deg-bin: {bm.min():+.2f} .. {bm.max():+.2f} dB (peak-to-peak {bm.max()-bm.min():.2f} dB)")
# era-difference at matched angle (IPF drift proxy)
for pol in ["HH","HV"]:
    m=df.groupby(["era",pd.cut(df.angle,np.arange(19,48,3))],observed=True)[pol].mean().unstack(0).dropna()
    if m.shape[1]==2:
        d=(m["2024"]-m["2018"]); print(f"IPF-era diff {pol}: mean {d.mean():+.2f} dB, range {d.min():+.2f}..{d.max():+.2f} dB over {len(d)} angle bins")
# flip rate, full swath
for pol,thr in [("HV",-28.0),("HH",-18.0)]:
    b,a=np.polyfit(df.angle,df[pol],1); nrm=df[pol]-b*(df.angle-35.0)
    r=(df[pol]<thr).values; n=(nrm<thr).values
    print(f"{pol} thr {thr}: raw {r.mean():.3f} norm {n.mean():.3f} FLIP {(r!=n).mean()*100:.2f}%")
    for lab,mm in [("near<25",df.angle<25),("far>40",df.angle>40)]:
        if mm.sum()>50: print(f"    {lab}: n={mm.sum()} flip {(r[mm.values]!=n[mm.values]).mean()*100:.1f}%")
