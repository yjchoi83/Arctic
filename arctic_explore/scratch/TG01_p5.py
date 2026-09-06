import ee, numpy as np
from scipy.ndimage import rotate
ee.Initialize(project="alpha-earth-app")
S1=ee.ImageCollection("COPERNICUS/S1_GRD")
# boxes: 256x256 @200m = 51 km. A/B = Sannikov Strait corridor (convoy route Nov-Dec 2021),
# C/D = control pack ice off-route, same scene date.
boxes={"A_sannikov_w":[139.0,74.45],"B_sannikov_e":[141.0,74.60],
       "C_ctrl_n":[140.0,75.20],"D_ctrl_e":[142.0,75.10]}
def dxy(lat): return 0.2*256/111.0/np.cos(np.radians(lat)), 0.2*256/111.0
def grab(c,lon,lat,d0,d1):
    hx,hy=dxy(lat); g=ee.Geometry.Rectangle([lon-hx/2,lat-hy/2,lon+hx/2,lat+hy/2])
    im=(c.filterBounds(g).filterDate(d0,d1).select("HH").mosaic().reproject("EPSG:3413",None,200).clip(g))
    r=im.sampleRectangle(region=g,defaultValue=-99,properties=[]).getInfo()
    return np.array(r["properties"]["HH"],dtype=float)
def lcr(a):
    """linear concentration ratio for dark and bright anomaly masks via rotated line integrals"""
    m=(a>-90); v=a.copy(); v[~m]=np.nan
    med=np.nanmedian(v); sd=np.nanstd(v)
    out={}
    for name,mask in [("dark",v<med-1.5*sd),("bright",v>med+1.5*sd)]:
        b=np.nan_to_num(mask.astype(float))
        if b.sum()<50: out[name]=(np.nan,np.nan,b.mean()); continue
        prof=[]
        for th in range(0,180,5):
            R=rotate(b,th,reshape=False,order=0,mode="constant",cval=0)
            n=rotate(np.ones_like(b),th,reshape=False,order=0,mode="constant",cval=0)
            s=R.sum(axis=1)/np.maximum(n.sum(axis=1),1)   # mean along rotated rows
            prof.append(s.max())
        prof=np.array(prof)
        out[name]=(round(float(prof.max()/max(b.mean(),1e-6)),2),int(np.argmax(prof)*5),round(float(b.mean()),4))
    return out
D=[("2021-12-02","2021-12-05"),("2021-11-20","2021-11-23")]
ew=(S1.filter(ee.Filter.eq("instrumentMode","EW")).filter(ee.Filter.listContains("transmitterReceiverPolarisation","HH")))
for d0,d1 in D:
    print("=== window",d0,d1)
    for k,(lon,lat) in boxes.items():
        try:
            a=grab(ew,lon,lat,d0,d1)
            val=a[a>-90]
            if val.size<1000: print(f"  {k}: no data"); continue
            r=lcr(a)
            print(f"  {k}: n={val.size} meanHH={val.mean():.1f}dB sd={val.std():.2f} "
                  f"dark_LCR={r['dark'][0]}@{r['dark'][1]}deg f={r['dark'][2]} "
                  f"bright_LCR={r['bright'][0]}@{r['bright'][1]}deg f={r['bright'][2]}")
        except Exception as e: print(f"  {k}: ERR {type(e).__name__} {str(e)[:90]}")
