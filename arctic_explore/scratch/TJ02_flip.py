import ee, time, numpy as np, geopandas as gpd
from rasterio.features import rasterize
from rasterio.transform import from_origin
from scipy.ndimage import zoom
T0=time.time(); ee.Initialize(project="alpha-earth-app")
LO,LA,HO,HA=101.0,77.40,105.0,78.10; SC=400.
mlat=111320.; mlon=111320.*np.cos(np.deg2rad(77.75))
nx=int((HO-LO)*mlon/SC); ny=int((HA-LA)*mlat/SC)
tr=from_origin(LO,HA,(HO-LO)/nx,(HA-LA)/ny)
RIV={'ow':3.,'thi':2.,'fyi':0.,'myi':-3.}      # POLARIS PC6 (MSC.1/Circ.1519), 4-class collapse
def cat(r): return np.where(r>=0,0,np.where(r>=-10,1,2))   # 0 normal 1 elevated 2 special
def chart(date):
    g=gpd.read_file(f"scratch/TA01_data/nh_{date}.shp").to_crs(4326).cx[LO-.6:HO+.6,LA-.3:HA+.3]
    cov=rasterize([(x,1) for x in g.geometry],out_shape=(ny,nx),transform=tr,fill=0).astype(bool)
    def rio(r):
        if r.POLY_TYPE!="I": return 30. if r.POLY_TYPE=="W" else 30.
        t,f,m=[max(0.,float(r[k] or 0))/100. for k in ("thi","fyi","myi")]
        ow=max(0.,1-float(r.tc_mid or 0)/100.); s=ow+t+f+m
        if s<=0: return 30.
        ow,t,f,m=[v/s for v in (ow,t,f,m)]
        return 10*(RIV['ow']*ow+RIV['thi']*t+RIV['fyi']*f+RIV['myi']*m)
    ice=g[g.POLY_TYPE.isin(["I","W"])]
    R=rasterize([(x.geometry,rio(x)) for _,x in ice.iterrows()],out_shape=(ny,nx),transform=tr,fill=np.nan,dtype="float32")
    return R,cov,len(ice)
roi=ee.Geometry.Rectangle([LO,LA,HO,HA],None,False)
def sar(date,shift=0.):
    d=np.datetime64(f"{date[:4]}-{date[4:6]}-{date[6:]}")
    c=(ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(roi)
       .filter(ee.Filter.eq("instrumentMode","EW"))
       .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HV"))
       .filterDate(str(d-np.timedelta64(3,'D')),str(d+np.timedelta64(4,'D'))))
    n=c.size().getInfo()
    if n==0: return None,0
    a=ee.Image(c.first()).select("HV").reproject("EPSG:3413",None,SC).sampleRectangle(region=roi,defaultValue=-99).getInfo()["properties"]["HV"]
    hv=np.array(a,"f4"); hv=zoom(hv,(ny/hv.shape[0],nx/hv.shape[1]),order=0)
    v=hv>-90; R=np.full((ny,nx),np.nan,"f4"); h=hv-shift
    R[v&(h<-28)]=10*RIV['ow']; R[v&(h>=-28)&(h<-24)]=10*RIV['thi']
    R[v&(h>=-24)&(h<-20)]=10*RIV['fyi']; R[v&(h>=-20)]=10*RIV['myi']
    return R,n
def agg(A,k=5):
    m=A[:ny//k*k,:nx//k*k].reshape(ny//k,k,nx//k,k)
    return np.nanmean(m,axis=(1,3))
print("date npoly nS1 n_px flip_px n_2km flip_2km flip_lo flip_hi cat_chart% cat_sar%",flush=True)
rows=[]
for D in ["20251023","20251121","20251218","20260116","20260220","20260320"]:
    Rc,cov,npoly=chart(D); Rs,n1=sar(D)
    if Rs is None: print(D,"NO_S1",flush=True); continue
    m=cov&np.isfinite(Rc)&np.isfinite(Rs)
    fp=float((cat(Rc[m])!=cat(Rs[m])).mean()); npx=int(m.sum())
    Ac,As,Am=agg(np.where(m,Rc,np.nan)),agg(np.where(m,Rs,np.nan)),agg(m.astype("f4"))
    m2=(Am>0.8)&np.isfinite(Ac)&np.isfinite(As)
    f2=float((cat(Ac[m2])!=cat(As[m2])).mean())
    band=[]
    for sh in (-2.,2.):
        Rs2,_=sar(D,sh); A2=agg(np.where(m,Rs2,np.nan))
        band.append(float((cat(Ac[m2])!=cat(A2[m2])).mean()))
    cc=np.bincount(cat(Ac[m2]),minlength=3)/m2.sum(); cs=np.bincount(cat(As[m2]),minlength=3)/m2.sum()
    print(D,npoly,n1,npx,round(fp,3),int(m2.sum()),round(f2,3),round(min(band),3),round(max(band),3),
          cc.round(2),cs.round(2),flush=True)
    rows.append((f2,min(band),max(band),int(m2.sum())))
w=np.array([r[3] for r in rows],float); print("AREA-WEIGHTED flip_2km",round(float(np.average([r[0] for r in rows],weights=w)),3),
      "band",round(float(np.average([r[1] for r in rows],weights=w)),3),round(float(np.average([r[2] for r in rows],weights=w)),3),
      "n_dates",len(rows),"n_cells_2km",int(w.sum()),"runtime",round(time.time()-T0,1),flush=True)
