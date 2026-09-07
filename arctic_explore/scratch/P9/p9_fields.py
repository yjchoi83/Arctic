import numpy as np, cv2, json, os, sys, glob, zipfile, datetime as dt, csv
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.crs import CRS
from rasterio.transform import from_origin
from pyproj import Transformer
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
SAVE="scratch/P9/fields"; os.makedirs(SAVE,exist_ok=True)
sys.path.insert(0,"scratch/P2"); from regions import regions
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
np.seterr(all='ignore')
RES=200.0; NODE=25; TMPL=25; SRCH=50; PEAK=0.40; RATIO=1.2; MAXOFF=0.8*SRCH
FWD=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
R=regions()
ZIP={os.path.basename(z).split(".")[0]:z for z in glob.glob("scratch/P8/s1/*.zip")}
def grid_for(region):
    w,e,s,n=R[region]
    lo=np.linspace(w,e,40); la=np.linspace(s,n,40)
    X,Y=FWD.transform(np.repeat(lo,40),np.tile(la,40))
    pad=60000
    x0,x1,y0,y1=X.min()-pad,X.max()+pad,Y.min()-pad,Y.max()+pad
    return x0,y1,int((x1-x0)/RES),int((y1-y0)/RES)
def load(scene,x0,y1,W,H):
    z=ZIP.get(scene)
    if z is None: return None
    tif=[m for m in zipfile.ZipFile(z).namelist() if m.endswith('.tiff') and '-hh-' in m]
    if not tif: return None
    DST=from_origin(x0,y1,RES,RES)
    with rasterio.open(f"/vsizip/{z}/{tif[0]}") as src:
        a=src.read(1).astype(np.float32)
        med=np.nanmedian(np.where(a>0,a,np.nan),axis=0); med=np.nan_to_num(med,nan=np.nanmedian(med))
        a=np.where(a>0,a/np.maximum(med[None,:],1e-3),np.nan)
        a=(10*np.log10(a)).astype(np.float32)
        d=np.full((H,W),np.nan,np.float32)
        reproject(a,d,gcps=src.gcps[0],src_crs=CRS.from_epsg(4326),dst_transform=DST,
                  dst_crs=CRS.from_epsg(3413),resampling=Resampling.average,
                  src_nodata=np.nan,dst_nodata=np.nan)
    return d
def u8(a):
    m=np.isfinite(a)
    if m.sum()<100: return None
    lo,hi=np.percentile(a[m],[2,98])
    b=np.clip((a-lo)/max(hi-lo,1e-6),0,1); b[~m]=0
    return (b*255).astype(np.uint8)
def stage1(A,B):
    a=u8(A[::4,::4]); b=u8(B[::4,::4])
    if a is None or b is None: return np.zeros((0,4))
    orb=cv2.ORB_create(nfeatures=20000,fastThreshold=7)
    ka,da=orb.detectAndCompute(a,None); kb,db=orb.detectAndCompute(b,None)
    if da is None or db is None or len(ka)<10 or len(kb)<10: return np.zeros((0,4))
    mm=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da,db,k=2)
    good=[m for m,n in mm if m.distance<0.75*n.distance]
    if len(good)<5: return np.zeros((0,4))
    P=np.array([[ka[m.queryIdx].pt[0]*4,ka[m.queryIdx].pt[1]*4,
                 (kb[m.trainIdx].pt[0]-ka[m.queryIdx].pt[0])*4,
                 (kb[m.trainIdx].pt[1]-ka[m.queryIdx].pt[1])*4] for m in good])
    d=P[:,2:]; med=np.median(d,0); mad=np.median(np.abs(d-med),0)+1e-6
    return P[(np.abs(d-med)<5*mad).all(1)]
def track(A,B):
    P=stage1(A,B); gmed=np.median(P[:,2:],0) if len(P)>=5 else np.array([0.,0.])
    Hh,W=A.shape; h=TMPL//2
    Af=np.nan_to_num(A,nan=np.nanmedian(A)).astype(np.float32)
    Bf=np.nan_to_num(B,nan=np.nanmedian(B)).astype(np.float32)
    va=np.isfinite(A); vb=np.isfinite(B); out=[]
    for yy in range(TMPL+SRCH,Hh-TMPL-SRCH,NODE):
        for xx in range(TMPL+SRCH,W-TMPL-SRCH,NODE):
            if va[yy-h:yy+h+1,xx-h:xx+h+1].mean()<0.99: continue
            t=Af[yy-h:yy+h+1,xx-h:xx+h+1]
            if t.std()<0.3: continue
            if len(P)>=5:
                w=1.0/(np.hypot(P[:,0]-xx,P[:,1]-yy)+1e3)**2; k=np.argsort(-w)[:12]
                gx=np.sum(w[k]*P[k,2])/np.sum(w[k]); gy=np.sum(w[k]*P[k,3])/np.sum(w[k])
            else: gx,gy=gmed
            cy=int(round(yy+gy)); cx=int(round(xx+gx))
            y0,y1_=cy-h-SRCH,cy+h+SRCH+1; x0,x1_=cx-h-SRCH,cx+h+SRCH+1
            if y0<0 or x0<0 or y1_>Hh or x1_>W: continue
            if vb[y0:y1_,x0:x1_].mean()<0.90: continue
            r=cv2.matchTemplate(Bf[y0:y1_,x0:x1_],t,cv2.TM_CCOEFF_NORMED)
            i=np.unravel_index(np.argmax(r),r.shape); pk=float(r[i])
            rr=r.copy(); rr[max(0,i[0]-5):i[0]+6,max(0,i[1]-5):i[1]+6]=-9
            sec=float(rr.max())
            dx=(x0+i[1]+h)-xx; dy=(y0+i[0]+h)-yy
            off=np.hypot(dx-gx,dy-gy)
            ok=int(pk>=PEAK and pk/max(sec,1e-3)>=RATIO and off<=MAXOFF)
            out.append([xx,yy,dx,dy,pk,ok])
    return np.array(out,float),len(P)

# ---------- divergence, events, IABP, quicklooks ----------
from scipy import ndimage as ndi
import pandas as pd
IAB=None
def iabp():
    global IAB
    if IAB is None:
        rows=[]
        for y in (2019,2020,2021):
            f=f"scratch/P1/LEVEL1_{y}.csv"
            hdr=open(f).readline().strip().split(",")
            mn="Min" if "Min" in hdr else "Minute"
            d=pd.read_csv(f,usecols=["BuoyID","Year","Month","Day","Hour",mn,"Lat","Lon"],
                          dtype={"BuoyID":str},low_memory=False).rename(columns={mn:"Min"})
            d=d[(d.Lat>=68)&(d.Lat<=90)].dropna(); rows.append(d)
        d=pd.concat(rows,ignore_index=True)
        d["t"]=pd.to_datetime(dict(year=d.Year.astype(int),month=d.Month.astype(int),day=d.Day.astype(int),
                                   hour=d.Hour.astype(int),minute=d.Min.astype(int)),errors="coerce")
        d=d.dropna(subset=["t"]).sort_values(["BuoyID","t"])
        x,y=FWD.transform(d.Lon.values,d.Lat.values); d["x"]=x; d["y"]=y
        IAB=d
    return IAB
def buoy_check(t0,t1,x0,y1,W,H):
    d=iabp()
    q=d[(d.t>=t0-dt.timedelta(hours=3))&(d.t<=t1+dt.timedelta(hours=3))]
    if not len(q): return None
    cx=x0+W*RES/2; cy=y1-H*RES/2
    q=q[(np.hypot(q.x-cx,q.y-cy)<=100000)]
    if not len(q): return None
    out=[]
    for b,g in q.groupby("BuoyID"):
        g=g.sort_values("t")
        a=g[g.t<=t0+dt.timedelta(hours=3)]; c=g[g.t>=t1-dt.timedelta(hours=3)]
        if not len(a) or not len(c): continue
        out.append((b,float(np.hypot(c.x.iloc[0]-a.x.iloc[-1],c.y.iloc[0]-a.y.iloc[-1])/1e3)))
    return out or None
SEL=json.load(open("scratch/P8/pairs_sel.json"))
os.makedirs("results/P8/quicklooks",exist_ok=True)
rows=[];ev_id=0;summary=[]
for pi,pr in enumerate(SEL):
    reg=pr["region"]; x0,y1,W,Hh=grid_for(reg)
    A=load(pr["a"],x0,y1,W,Hh); B=load(pr["b"],x0,y1,W,Hh)
    if A is None or B is None: print("skip(no file)",pr["a"],flush=True); continue
    V,nf=track(A,B)
    if len(V)==0: print("skip(no nodes)",pr["a"],flush=True); continue
    ok=V[:,5]==1; ns=int(ok.sum())
    t0=dt.datetime.fromisoformat(pr["t0"]); t1=dt.datetime.fromisoformat(pr["t1"])
    dth=(t1-t0).total_seconds()/3600
    summary.append(dict(pair=pi,region=reg,season=pr["season"],year=pr["year"],dt_h=round(dth,1),
                        n_nodes=len(V),n_success=ns,rate=round(ns/len(V),3),n_feat=nf))
    print(f"pair {pi} {reg} {pr['season']} {pr['year']} dt {dth:.1f}h nodes {len(V)} succ {ns} ({ns/len(V):.2f})",flush=True)
    np.savez_compressed(f"{SAVE}/pair{pi:02d}.npz",V=V,x0=x0,y1=y1,W=W,H=Hh,dth=dth,
                        region=reg,season=pr['season'],year=pr['year'],t0=pr['t0'],t1=pr['t1'])
    if ns<30: continue
    # 5 km node grid -> velocity (km/day); pixel row increases downward = -northing
    gx=np.unique(V[:,0]); gy=np.unique(V[:,1])
    U=np.full((len(gy),len(gx)),np.nan); Vv=np.full((len(gy),len(gx)),np.nan)
    ix={v:i for i,v in enumerate(gx)}; iy={v:i for i,v in enumerate(gy)}
    for r_ in V[ok]:
        U[iy[r_[1]],ix[r_[0]]]= r_[2]*RES/1e3/(dth/24)
        Vv[iy[r_[1]],ix[r_[0]]]=-r_[3]*RES/1e3/(dth/24)
    dx_km=NODE*RES/1e3
    dudx=np.full_like(U,np.nan); dvdy=np.full_like(U,np.nan)
    dudx[:,1:-1]=(U[:,2:]-U[:,:-2])/(2*dx_km)
    dvdy[1:-1,:]=(Vv[:-2,:]-Vv[2:,:])/(2*dx_km)   # row index increases southward
    div=dudx+dvdy
    fin=np.isfinite(div)
    if fin.sum()<20: continue
    thr=np.nanpercentile(div[fin],10)
    mask=(div<thr)&fin
    lab,n=ndi.label(mask)
    cell_km2=dx_km*dx_km
    for k in range(1,n+1):
        m=lab==k; area=m.sum()*cell_km2
        if area<100: continue
        conv=float(-np.nanmean(div[m]))            # 1/day, positive = convergence
        mag=conv*(dth/24)*np.sqrt(area)            # km of closure across the feature
        ev_id+=1
        bl=buoy_check(t0,t1,x0,y1,W,Hh)
        rows.append(dict(event=f"E{ev_id:03d}",region=reg,season=pr["season"],year=pr["year"],
            date=t0.date().isoformat(),dt_h=round(dth,1),area_km2=round(area,0),
            conv_per_day=round(conv,4),magnitude_km=round(mag,2),
            mag_class=">=5km" if mag>=5 else (">=3km" if mag>=3 else "<3km"),
            n_success=ns,success_rate=round(ns/len(V),3),
            buoy=("; ".join(f"{b}:{d:.1f}km" for b,d in bl) if bl else "none within 100 km"),
            decision="",auto_note="divergence-threshold detection; not visually scored"))
        # quicklook
        if os.environ.get("NOQL"): continue
        fig,ax=plt.subplots(1,2,figsize=(10,4.6))
        for a_,img,ttl in ((ax[0],A,f"before {t0:%Y-%m-%d %H:%M}"),(ax[1],B,f"after {t1:%Y-%m-%d %H:%M}")):
            a_.imshow(img,cmap="gray",vmin=np.nanpercentile(img,2),vmax=np.nanpercentile(img,98))
            a_.set_title(ttl,fontsize=8); a_.set_xticks([]); a_.set_yticks([])
        ext=[gx.min(),gx.max(),gy.max(),gy.min()]
        im=ax[1].imshow(np.where(mask,div,np.nan),extent=[gx.min(),gx.max(),gy.max(),gy.min()],
                        cmap="autumn_r",alpha=0.65,vmin=thr*2,vmax=thr)
        fig.colorbar(im,ax=ax[1],fraction=0.03,label="divergence (1/day)")
        fig.suptitle(f"E{ev_id:03d} {reg} {pr['season']} {t0:%Y-%m-%d} dt {dth:.0f}h  area {area:.0f} km2  mag {mag:.1f} km",fontsize=9)
        fig.savefig(f"results/P8/quicklooks/E{ev_id:03d}_{reg}_{t0:%Y%m%d}.png",dpi=95,bbox_inches="tight")
        plt.close(fig)
pd.DataFrame(summary).to_csv("scratch/P8/pair_summary.csv",index=False)
if rows:
    with open("results/P8/qc_table.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("PAIRS",len(summary),"EVENTS",len(rows),flush=True)
