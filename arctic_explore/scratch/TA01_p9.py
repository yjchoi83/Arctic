import ee, json, numpy as np, geopandas as gpd, heapq, sys
from rasterio.features import rasterize
from rasterio.transform import from_origin
ee.Initialize(project="alpha-earth-app")
LO,LA,HO,HA = 100.0,77.15,106.0,78.30
SC = 400.0
# --- grid in EPSG:3413-like local metric: use simple lon/lat -> m
mlat=111320.0; mlon=111320.0*np.cos(np.deg2rad(77.7))
nx=int((HO-LO)*mlon/SC); ny=int((HA-LA)*mlat/SC)
print("grid",ny,nx,ny*nx)
tr = from_origin(LO,HA,(HO-LO)/nx,(HA-LA)/ny)
# --- chart baseline (NIC SIGRID-3 weekly)
g = gpd.read_file("scratch/TA01_data/nh_20251121.shp").to_crs(4326)
g = g.cx[LO-0.5:HO+0.5, LA-0.3:HA+0.3].copy()
land = rasterize([(x,1) for x in g[g.POLY_TYPE=="L"].geometry], out_shape=(ny,nx), transform=tr, fill=0).astype(bool)
def riv_chart(r):
    if r.POLY_TYPE!="I": return 3.0
    thi,fyi,myi = [float(r[k] or 0)/10.0 for k in ("thi","fyi","myi")]
    ct = float(r.tc_mid or 0)/10.0
    ow = max(0.0, 1-ct)
    return 3*ow + 2*thi + (-1)*fyi + (-2)*myi
ice = g[g.POLY_TYPE.isin(["I","W"])]
rio_c = rasterize([(x.geometry, riv_chart(x)) for _,x in ice.iterrows()], out_shape=(ny,nx),
                  transform=tr, fill=3.0, dtype="float32")
# --- SAR field
roi = ee.Geometry.Rectangle([LO,LA,HO,HA],None,False)
col = (ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(roi)
       .filter(ee.Filter.eq("instrumentMode","EW"))
       .filter(ee.Filter.listContains("transmitterReceiverPolarisation","HV"))
       .filterDate("2025-11-18","2025-11-25"))
print("S1 EW scenes:", col.size().getInfo())
SSC=600.0
img = col.select(["HH","HV"]).mosaic().reproject("EPSG:4326", None, SSC/mlat*111320.0)
arr = img.sampleRectangle(region=roi, defaultValue=-99).getInfo()["properties"]
hh = np.array(arr["HH"],dtype="float32"); hv = np.array(arr["HV"],dtype="float32")
print("sar arr", hh.shape)
# resample SAR to chart grid
from scipy.ndimage import zoom
zy,zx = ny/hh.shape[0], nx/hh.shape[1]
hh = zoom(hh,(zy,zx),order=0); hv = zoom(hv,(zy,zx),order=0)
rio_s = np.full((ny,nx),3.0,dtype="float32")
valid = hh>-90
rio_s[valid & (hv<-28)] = 3.0            # open water / calm
rio_s[valid & (hv>=-28)&(hv<-24)] = 2.0  # new/young ice
rio_s[valid & (hv>=-24)&(hv<-20)] = -1.0 # level FYI
rio_s[valid & (hv>=-20)] = -2.0          # deformed FYI / MYI
np.save("scratch/TA01_rio_chart.npy",rio_c); np.save("scratch/TA01_rio_sar.npy",rio_s)
# --- A*
def astar(rio):
    cost = np.where(rio>=0, 1.0+0.5*(3-rio), 1.0+3.0*(-rio)**1.5)
    cost = np.where(land, 1e9, cost)
    blocked = land | (rio<=-2.0)
    s=(ny//2,0); t=(ny//2,nx-1)
    for p in (s,t):
        pass
    D={s:0.0}; prev={}; pq=[(0.0,s)]; seen=set()
    while pq:
        f,u=heapq.heappop(pq)
        if u in seen: continue
        seen.add(u)
        if u==t: break
        y,x=u
        for dy in(-1,0,1):
            for dx in(-1,0,1):
                if dy==0 and dx==0: continue
                v=(y+dy,x+dx)
                if not(0<=v[0]<ny and 0<=v[1]<nx) or blocked[v]: continue
                w=cost[v]*np.hypot(dy,dx)
                nd=D[u]+w
                if nd<D.get(v,1e18):
                    D[v]=nd; prev[v]=u
                    heapq.heappush(pq,(nd+np.hypot(t[0]-v[0],t[1]-v[1]),v))
    if t not in D: return None,None
    p=[t]
    while p[-1]!=s: p.append(prev[p[-1]])
    return np.array(p[::-1]), D[t]
import time; t0=time.time()
res={}
for nm,r in (("chart",rio_c),("sar",rio_s)):
    pth,c = astar(r)
    if pth is None: res[nm]=None; print(nm,"BLOCKED"); continue
    seg=np.hypot(np.diff(pth[:,0])*SC, np.diff(pth[:,1])*SC).sum()/1000
    res[nm]=dict(len_km=round(float(seg),1), cost=round(float(c),1),
                 rio_mean=round(float(r[pth[:,0],pth[:,1]].mean()),2),
                 rio_min=float(r[pth[:,0],pth[:,1]].min()), path=pth)
    print(nm, {k:v for k,v in res[nm].items() if k!="path"})
if res["chart"] is not None and res["sar"] is not None:
    A,B=res["chart"]["path"],res["sar"]["path"]
    def div(A,B):
        d=[np.min(np.hypot((A[i,0]-B[:,0])*SC,(A[i,1]-B[:,1])*SC)) for i in range(len(A))]
        return np.mean(d)/1000, np.max(d)/1000
    m,M=div(A,B); m2,M2=div(B,A)
    print("divergence_km mean/max:", round(max(m,m2),2), round(max(M,M2),2))
    for nm,other in (("chart_on_sar",(rio_s,A)),("sar_on_chart",(rio_c,B))):
        r,p=other; print(nm,"RIO_mean",round(float(r[p[:,0],p[:,1]].mean()),2),"RIO_min",float(r[p[:,0],p[:,1]].min()))
print("runtime_s",round(time.time()-t0,1))
