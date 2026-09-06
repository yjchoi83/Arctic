import ee, json, time, numpy as np, geopandas as gpd, heapq
from rasterio.features import rasterize
from rasterio.transform import from_origin
from scipy.ndimage import zoom
T0=time.time(); ee.Initialize(project="alpha-earth-app")
LO,LA,HO,HA = 101.0,77.40,105.0,78.10
SC=400.0; mlat=111320.0; mlon=111320.0*np.cos(np.deg2rad(77.75))
nx=int((HO-LO)*mlon/SC); ny=int((HA-LA)*mlat/SC); print("grid",ny,nx,ny*nx,flush=True)
tr=from_origin(LO,HA,(HO-LO)/nx,(HA-LA)/ny)
g=gpd.read_file("scratch/TA01_data/nh_20251121.shp").to_crs(4326).cx[LO-.6:HO+.6, LA-.3:HA+.3].copy()
cov=rasterize([(x,1) for x in g.geometry],out_shape=(ny,nx),transform=tr,fill=0).astype(bool)
land=~cov  # chart has no land polys; uncovered = land/unmapped
def riv(r):
    if r.POLY_TYPE!="I": return 3.0
    thi,fyi,myi=[float(r[k] or 0)/100. for k in ("thi","fyi","myi")]
    ow=max(0.,1-float(r.tc_mid or 0)/100.)
    return 3*ow+2*thi-1*fyi-2*myi
ice=g[g.POLY_TYPE.isin(["I","W"])]
rio_c=rasterize([(x.geometry,riv(x)) for _,x in ice.iterrows()],out_shape=(ny,nx),transform=tr,fill=3.,dtype="float32")
print("chart polys",len(ice),"land_frac",round(land.mean(),3),"RIO uniq",np.unique(rio_c).round(2)[:8],flush=True)
roi=ee.Geometry.Rectangle([LO,LA,HO,HA],None,False)
col=(ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(roi)
     .filter(ee.Filter.eq("instrumentMode","EW"))
     .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HV"))
     .filterDate("2025-11-19","2025-11-24"))
ids=col.aggregate_array("system:index").getInfo(); print("S1 EW scenes",len(ids),ids[:3],flush=True)
img=ee.Image(col.first()).select(["HH","HV"]).reproject("EPSG:3413",None,SC)
a=img.sampleRectangle(region=roi,defaultValue=-99).getInfo()["properties"]
hh=np.array(a["HH"],"f4"); hv=np.array(a["HV"],"f4"); print("sar",hh.shape,"t",round(time.time()-T0,1),flush=True)
hv=zoom(hv,(ny/hv.shape[0],nx/hv.shape[1]),order=0)
rio_s=np.full((ny,nx),3.,"f4"); v=hv>-90
print("sar_valid_frac",round(float(v.mean()),3),"hv_pcts",np.percentile(hv[v],[5,25,50,75,95]).round(1),flush=True)
rio_s[v&(hv<-28)]=3.; rio_s[v&(hv>=-28)&(hv<-24)]=2.; rio_s[v&(hv>=-24)&(hv<-20)]=-1.; rio_s[v&(hv>=-20)]=-2.
np.save("scratch/TA01_rio_chart.npy",rio_c); np.save("scratch/TA01_rio_sar.npy",rio_s)
def astar(rio):
    cost=np.where(rio>=0,1.+0.5*(3-rio),1.+3.*np.abs(np.minimum(rio,0))**1.5); blk=land|(rio<=-2.)
    s=(ny//2,0); t=(ny//2,nx-1)
    if blk[s] or blk[t]: return None,None
    D={s:0.}; pv={}; pq=[(0.,s)]; sn=set()
    while pq:
        f,u=heapq.heappop(pq)
        if u in sn: continue
        sn.add(u)
        if u==t: break
        y,x=u
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                if dy==dx==0: continue
                vv=(y+dy,x+dx)
                if not(0<=vv[0]<ny and 0<=vv[1]<nx) or blk[vv]: continue
                nd=D[u]+cost[vv]*np.hypot(dy,dx)
                if nd<D.get(vv,1e18): D[vv]=nd; pv[vv]=u; heapq.heappush(pq,(nd+np.hypot(t[0]-vv[0],t[1]-vv[1]),vv))
    if t not in D: return None,None
    p=[t]
    while p[-1]!=s: p.append(pv[p[-1]])
    return np.array(p[::-1]),D[t]
R={}
for nm,r in (("chart",rio_c),("sar",rio_s)):
    p,c=astar(r)
    if p is None: print(nm,"BLOCKED",flush=True); continue
    R[nm]=p; L=np.hypot(np.diff(p[:,0])*SC,np.diff(p[:,1])*SC).sum()/1000
    print(nm,"len_km",round(L,1),"cost",round(c,1),"RIO_mean",round(float(r[p[:,0],p[:,1]].mean()),2),
          "RIO_min",float(r[p[:,0],p[:,1]].min()),flush=True)
if len(R)==2:
    A,B=R["chart"],R["sar"]
    d=lambda X,Y:[np.min(np.hypot((X[i,0]-Y[:,0])*SC,(X[i,1]-Y[:,1])*SC)) for i in range(len(X))]
    d1,d2=d(A,B),d(B,A)
    print("divergence_km mean",round(max(np.mean(d1),np.mean(d2))/1000,2),"max",round(max(np.max(d1),np.max(d2))/1000,2),flush=True)
    print("chart_route_on_SAR: RIO_mean",round(float(rio_s[A[:,0],A[:,1]].mean()),2),"RIO_min",float(rio_s[A[:,0],A[:,1]].min()),
          "| sar_route_on_CHART: RIO_mean",round(float(rio_c[B[:,0],B[:,1]].mean()),2),flush=True)
    print("frac_chart_route_in_SAR_highrisk",round(float((rio_s[A[:,0],A[:,1]]<0).mean()),3),flush=True)
print("runtime_s",round(time.time()-T0,1),flush=True)
