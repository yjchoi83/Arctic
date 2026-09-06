import h5py,numpy as np,rasterio,zipfile,json
from rasterio.warp import reproject,Resampling
from rasterio.crs import CRS
from rasterio.transform import from_origin
np.seterr(all='ignore')
NIS="scratch/R2_data/NISAR_L2_PR_GCOV_026_022_A_040_2005_DHDH_A_20260721T172217_20260721T172226_P05023_N_P_J_001.h5"
S1Z="scratch/R2_data/S1C_EW_GRDM_1SDH_20260721T184459_20260721T184605_008645_011217_FAB7.zip"
RES=100.0
f=h5py.File(NIS,"r"); g=f["science/LSAR/GCOV/grids/frequencyB"]
x=g["xCoordinates"][:]; y=g["yCoordinates"][:]
x0,x1=x.min()-40,x.max()+40; y0,y1=y.min()-40,y.max()+40
W=int((x1-x0)/RES); H=int((y1-y0)/RES); DST=from_origin(x0,y1,RES,RES)
SRC=from_origin(x[0]-40,y[0]+40,80.0,80.0)
out={}
for b in ("HHHH","HVHV"):
    a=g[b][:].astype(np.float32); a[a<=0]=np.nan
    a=10*np.log10(a)
    d=np.full((H,W),np.nan,np.float32)
    reproject(a,d,src_transform=SRC,src_crs=CRS.from_epsg(3413),dst_transform=DST,
              dst_crs=CRS.from_epsg(3413),resampling=Resampling.average,src_nodata=np.nan,dst_nodata=np.nan)
    out["L_"+b]=d; print("L",b,"valid %.2f median %.1f dB"%(np.isfinite(d).mean(),np.nanmedian(d)))
zf=zipfile.ZipFile(S1Z)
for pol in ("hh","hv"):
    t=[n for n in zf.namelist() if n.endswith('.tiff') and f'-{pol}-' in n][0]
    with rasterio.open(f"/vsizip/{S1Z}/{t}") as s:
        a=s.read(1).astype(np.float32)
        col=np.where(a>0,a,np.nan); med=np.nanmedian(col,axis=0)
        med=np.nan_to_num(med,nan=np.nanmedian(med))
        a=np.where(a>0,a/np.maximum(med[None,:],1e-3),np.nan)
        a=(10*np.log10(a)).astype(np.float32)
        d=np.full((H,W),np.nan,np.float32)
        reproject(a,d,gcps=s.gcps[0],src_crs=CRS.from_epsg(4326),dst_transform=DST,
                  dst_crs=CRS.from_epsg(3413),resampling=Resampling.average,src_nodata=np.nan,dst_nodata=np.nan)
    out["C_"+pol.upper()]=d; print("C",pol,"valid %.2f"%np.isfinite(d).mean())
with rasterio.open("scratch/asi_20260721.tif") as s:
    a=s.read(1).astype(np.float32); a[a>100]=np.nan
    d=np.full((H,W),np.nan,np.float32)
    reproject(a,d,src_transform=s.transform,src_crs=s.crs,dst_transform=DST,dst_crs=CRS.from_epsg(3413),
              resampling=Resampling.average,src_nodata=np.nan,dst_nodata=np.nan)
out["SIC"]=d
print("SIC mean %.1f  frac>15 %.2f  frac<15 %.2f"%(np.nanmean(d),np.nanmean(d>15),np.nanmean(d<15)))
np.savez_compressed("scratch/R2_stack.npz",**out,meta=np.array([x0,y1,RES,W,H]))
print("grid",W,H)
