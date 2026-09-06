import glob,os,zipfile,numpy as np,rasterio
from rasterio.warp import reproject, Resampling
from rasterio.crs import CRS
from rasterio.transform import from_origin
from pyproj import Transformer
from shapely.geometry import MultiPoint
RES=200.0
tr=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
Z={os.path.basename(z).split("_")[4][:15]:z for z in glob.glob("scratch/R1_data/*.zip")}
def tif(z): return [n for n in zipfile.ZipFile(z).namelist() if n.endswith('.tiff') and '-hh-' in n][0]
H={}
for t,z in Z.items():
    with rasterio.open(f"/vsizip/{z}/{tif(z)}") as s: g=s.gcps[0]
    x,y=tr.transform(np.array([p.x for p in g]),np.array([p.y for p in g]))
    H[t]=MultiPoint(list(zip(x,y))).convex_hull
G={"melt":["20240810T180458","20240812T174832","20240813T182941","20240824T174832","20240825T182942"],
   "winter":["20240212T180459","20240214T174833","20240215T182942","20240226T174833","20240227T182942"]}
def bbox(polys):
    p=polys[0]
    for q in polys[1:]: p=p.intersection(q)
    x0,y0,x1,y1=p.bounds
    pad=3000
    return x0+pad,y0+pad,x1-pad,y1-pad
# common ROIs from the melt group (identical relative orbits in winter)
ROI={"T":bbox([H[t] for t in G["melt"][:3]]),"D":bbox([H[t] for t in G["melt"][3:]])}
os.makedirs("scratch/R1_grid",exist_ok=True)
meta={}
for k,(x0,y0,x1,y1) in ROI.items():
    W=int((x1-x0)/RES); Hh=int((y1-y0)/RES)
    meta[k]=dict(x0=x0,y1=y1,res=RES,W=W,H=Hh)
    print(k,"grid",W,"x",Hh,"= %.0f x %.0f km"%(W*RES/1e3,Hh*RES/1e3))
np.save("scratch/R1_grid/_meta.npy",meta,allow_pickle=True)
for season,ts in G.items():
    for i,t in enumerate(ts):
        k="T" if i<3 else "D"
        out=f"scratch/R1_grid/{season}_{k}_{t}.npy"
        if os.path.exists(out): continue
        m=meta[k]; DST=from_origin(m['x0'],m['y1'],RES,RES)
        with rasterio.open(f"/vsizip/{Z[t]}/{tif(Z[t])}") as src:
            a=src.read(1).astype(np.float32)
            col=np.where(a>0,a,np.nan)
            med=np.nanmedian(col,axis=0); med=np.nan_to_num(med,nan=np.nanmedian(med))
            a=np.where(a>0,a/np.maximum(med[None,:],1e-3),np.nan)
            with np.errstate(divide='ignore',invalid='ignore'): a=(10*np.log10(a)).astype(np.float32)
            dst=np.full((m['H'],m['W']),np.nan,np.float32)
            reproject(a,dst,gcps=src.gcps[0],src_crs=CRS.from_epsg(4326),
                      dst_transform=DST,dst_crs=CRS.from_epsg(3413),
                      resampling=Resampling.average,src_nodata=np.nan,dst_nodata=np.nan)
        np.save(out,dst); print(season,k,t,"valid %.3f"%np.isfinite(dst).mean())
