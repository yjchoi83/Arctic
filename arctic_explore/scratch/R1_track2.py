import numpy as np, cv2, json
np.seterr(all='ignore')
M=np.load("scratch/R1_grid/_meta.npy",allow_pickle=True).item()
RES=200.0; NODE=25; TMPL=25; PEAK=0.40; RATIO=1.2
def u8(a):
    m=np.isfinite(a); lo,hi=np.percentile(a[m],[2,98])
    b=np.clip((a-lo)/max(hi-lo,1e-6),0,1); b[~m]=0
    return (b*255).astype(np.uint8)
def stage1(A,B):
    a=u8(A[::4,::4]); b=u8(B[::4,::4])
    orb=cv2.ORB_create(nfeatures=20000,fastThreshold=7)
    ka,da=orb.detectAndCompute(a,None); kb,db=orb.detectAndCompute(b,None)
    if da is None or db is None: return np.zeros((0,4))
    mm=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da,db,k=2)
    good=[m for m,n in mm if m.distance<0.75*n.distance]
    if len(good)<5: return np.zeros((0,4))
    P=np.array([[ka[m.queryIdx].pt[0]*4,ka[m.queryIdx].pt[1]*4,
                 (kb[m.trainIdx].pt[0]-ka[m.queryIdx].pt[0])*4,
                 (kb[m.trainIdx].pt[1]-ka[m.queryIdx].pt[1])*4] for m in good])
    d=P[:,2:]; med=np.median(d,0); mad=np.median(np.abs(d-med),0)+1e-6
    return P[(np.abs(d-med)<5*mad).all(1)]
def run(A,B,ICE,SRCH,use_guess):
    P=stage1(A,B) if use_guess else np.zeros((0,4))
    gmed=np.median(P[:,2:],0) if len(P)>=5 else np.array([0.,0.])
    Hh,W=A.shape; h=TMPL//2; MAXOFF=0.8*SRCH
    Af=np.nan_to_num(A,nan=np.nanmedian(A)).astype(np.float32)
    Bf=np.nan_to_num(B,nan=np.nanmedian(B)).astype(np.float32)
    va=np.isfinite(A); vb=np.isfinite(B); out=[]
    for yy in range(TMPL+SRCH,Hh-TMPL-SRCH,NODE):
        for xx in range(TMPL+SRCH,W-TMPL-SRCH,NODE):
            if not ICE[yy,xx]: continue
            if va[yy-h:yy+h+1,xx-h:xx+h+1].mean()<0.99: continue
            t=Af[yy-h:yy+h+1,xx-h:xx+h+1]
            if t.std()<0.3: continue
            if len(P)>=5:
                w=1.0/(np.hypot(P[:,0]-xx,P[:,1]-yy)+1e3)**2; k=np.argsort(-w)[:12]
                gx=np.sum(w[k]*P[k,2])/np.sum(w[k]); gy=np.sum(w[k]*P[k,3])/np.sum(w[k])
            else: gx,gy=gmed
            cy=int(round(yy+gy)); cx=int(round(xx+gx))
            y0,y1=cy-h-SRCH,cy+h+SRCH+1; x0,x1=cx-h-SRCH,cx+h+SRCH+1
            if y0<0 or x0<0 or y1>Hh or x1>W: continue
            if vb[y0:y1,x0:x1].mean()<0.90: continue
            r=cv2.matchTemplate(Bf[y0:y1,x0:x1],t,cv2.TM_CCOEFF_NORMED)
            i=np.unravel_index(np.argmax(r),r.shape); pk=float(r[i])
            rr=r.copy(); rr[max(0,i[0]-5):i[0]+6,max(0,i[1]-5):i[1]+6]=-9
            sec=float(rr.max())
            dx=(x0+i[1]+h)-xx; dy=(y0+i[0]+h)-yy
            off=np.hypot(dx-gx,dy-gy)
            ok=int(pk>=PEAK and pk/max(sec,1e-3)>=RATIO and off<=MAXOFF)
            out.append([xx,yy,dx,dy,pk,sec,off,ok,len(P)])
    return np.array(out,float)
GR={"melt":[("T","20240810T180458","20240812T174832",47.7),("T","20240812T174832","20240813T182941",24.7),
            ("T","20240810T180458","20240813T182941",72.4),("D","20240824T174832","20240825T182942",24.7)],
    "winter":[("T","20240212T180459","20240214T174833",47.7),("T","20240214T174833","20240215T182942",24.7),
              ("T","20240212T180459","20240215T182942",72.4),("D","20240226T174833","20240227T182942",24.7)]}
res=[]
for cfg,(SR,UG) in {"prereg":(50,True),"ctrl_wide":(150,False)}.items():
  for season,prs in GR.items():
    for k,ta,tb,dth in prs:
        A=np.load(f"scratch/R1_grid/{season}_{k}_{ta}.npy"); B=np.load(f"scratch/R1_grid/{season}_{k}_{tb}.npy")
        i1=np.load(f"scratch/asi_{ta[:8]}_{k}.npy"); i2=np.load(f"scratch/asi_{tb[:8]}_{k}.npy")
        ICE=(np.nan_to_num(i1)>=70)&(np.nan_to_num(i2)>=70)
        R=run(A,B,ICE,SR,UG)
        n=len(R); s=int(R[:,7].sum()) if n else 0
        d=np.hypot(R[R[:,7]==1,2],R[R[:,7]==1,3])*RES/1e3 if s else np.array([])
        rec=dict(cfg=cfg,season=season,roi=k,t0=ta[:8],t1=tb[:8],dt_h=dth,
                 ice_area_km2=int(ICE.sum()*RES*RES/1e6),n_valid=n,n_succ=s,
                 rate=round(s/max(n,1),4),nfeat=int(R[0,8]) if n else 0,
                 disp_med_km=round(float(np.median(d)),2) if s else None)
        res.append(rec)
        if cfg=="prereg": np.save(f"scratch/R1v_{season}_{ta[:8]}_{tb[:8]}.npy",R)
        print(f"{cfg:9s} {season:6s} {k} {ta[:8]}->{tb[:8]} {dth:5.1f}h ice{rec['ice_area_km2']:6d}km2 valid{n:5d} succ{s:5d} rate {rec['rate']:.3f} feat{rec['nfeat']:4d} disp {rec['disp_med_km']}")
json.dump(res,open("scratch/R1_results2.json","w"),indent=1)
