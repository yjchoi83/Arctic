import h5py,numpy as np,rasterio,zipfile,json
from rasterio.warp import reproject,Resampling
from rasterio.crs import CRS
from rasterio.transform import from_origin
np.seterr(all='ignore')
NIS="scratch/R2_data/NISAR_L2_PR_GCOV_029_049_A_037_4005_DHDH_A_20260828T141700_20260828T141732_P05023_N_F_J_001.h5"
S1Z="scratch/R2_data/S1D_EW_GRDM_1SDH_20260828T174021_20260828T174121_004329_007FC1_62A1.zip"
RES=100.0
f=h5py.File(NIS,"r"); g=f["science/LSAR/GCOV/grids/frequencyB"]
x=g["xCoordinates"][:]; y=g["yCoordinates"][:]; sp=abs(x[1]-x[0])
x0,x1=x.min()-sp/2,x.max()+sp/2; y0,y1=y.min()-sp/2,y.max()+sp/2
W=int((x1-x0)/RES); H=int((y1-y0)/RES); DST=from_origin(x0,y1,RES,RES)
SRC=from_origin(x[0]-sp/2,y[0]+sp/2,sp,sp)
S={}
for b in ("HHHH","HVHV"):
    a=g[b][:].astype(np.float32); a[a<=0]=np.nan; a=10*np.log10(a)
    d=np.full((H,W),np.nan,np.float32)
    reproject(a,d,src_transform=SRC,src_crs=CRS.from_epsg(3413),dst_transform=DST,dst_crs=CRS.from_epsg(3413),
              resampling=Resampling.average,src_nodata=np.nan,dst_nodata=np.nan)
    S["L_"+b[:2]]=d
zf=zipfile.ZipFile(S1Z)
for pol in ("hh","hv"):
    t=[n for n in zf.namelist() if n.endswith('.tiff') and f'-{pol}-' in n][0]
    with rasterio.open(f"/vsizip/{S1Z}/{t}") as s:
        a=s.read(1).astype(np.float32)
        med=np.nanmedian(np.where(a>0,a,np.nan),axis=0); med=np.nan_to_num(med,nan=np.nanmedian(med))
        a=np.where(a>0,a/np.maximum(med[None,:],1e-3),np.nan); a=(10*np.log10(a)).astype(np.float32)
        d=np.full((H,W),np.nan,np.float32)
        reproject(a,d,gcps=s.gcps[0],src_crs=CRS.from_epsg(4326),dst_transform=DST,dst_crs=CRS.from_epsg(3413),
                  resampling=Resampling.average,src_nodata=np.nan,dst_nodata=np.nan)
    S["C_"+pol.upper()]=d
m=np.ones((H,W),bool)
for k,v in S.items(): m&=np.isfinite(v)
print("co-registered overlap pixels: %d (%.0f km2), frac of NISAR frame %.2f"%(m.sum(),m.sum()*RES*RES/1e6,m.mean()))
nesz=f["science/LSAR/GCOV/metadata/calibrationInformation/frequencyB/noiseEquivalentBackscatter/HV"][:]
print("NISAR freqB NESZ HV: %.1f .. %.1f dB (median %.1f)"%(10*np.log10(np.nanmin(nesz)),10*np.log10(np.nanmax(nesz)),10*np.log10(np.nanmedian(nesz))))
res={}
for k,v in S.items():
    d=v[m]
    res[k]=dict(n=int(len(d)),p5=round(float(np.percentile(d,5)),2),med=round(float(np.median(d)),2),
                p95=round(float(np.percentile(d,95)),2),sd=round(float(d.std()),2))
    print(f"{k:6s} p5 {res[k]['p5']:7.2f}  med {res[k]['med']:7.2f}  p95 {res[k]['p95']:7.2f}  sd {res[k]['sd']:5.2f} dB")
# local texture (5x5 std) and cross-frequency correlation
import scipy.ndimage as nd
tex={}
for k,v in S.items():
    a=np.where(m,v,np.nan)
    mu=nd.uniform_filter(np.nan_to_num(a),5); mu2=nd.uniform_filter(np.nan_to_num(a)**2,5)
    tex[k]=np.sqrt(np.maximum(mu2-mu**2,0))
    print(f"tex {k:6s} median {np.nanmedian(tex[k][m]):.2f} dB")
sub=np.zeros((H,W),bool); sub[::5,::5]=True; sub&=m
import itertools
for a,b in itertools.combinations(sorted(S),2):
    r=np.corrcoef(S[a][sub],S[b][sub])[0,1]
    print(f"corr {a:6s} {b:6s} {r:+.3f}")
json.dump(res,open("scratch/R2_openwater_stats.json","w"),indent=1)
