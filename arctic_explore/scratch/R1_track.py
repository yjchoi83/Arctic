import numpy as np, cv2, json, os, itertools
np.seterr(all='ignore')
META=np.load("scratch/R1_grid/_meta.npy",allow_pickle=True).item()
RES=200.0; NODE=25          # 5 km node spacing (px)
TMPL=25                     # 5 km template
SRCH=50                     # +-10 km around first guess
PEAK=0.40; RATIO=1.2; MAXOFF=0.8*SRCH
def u8(a):
    m=np.isfinite(a)
    lo,hi=np.percentile(a[m],[2,98])
    b=np.clip((a-lo)/max(hi-lo,1e-6),0,1); b[~m]=0
    return (b*255).astype(np.uint8), m
def stage1(A,B):
    a,_=u8(A[::4,::4]); b,_=u8(B[::4,::4])
    orb=cv2.ORB_create(nfeatures=20000,fastThreshold=7)
    ka,da=orb.detectAndCompute(a,None); kb,db=orb.detectAndCompute(b,None)
    if da is None or db is None or len(ka)<10 or len(kb)<10: return np.zeros((0,4)),0
    bf=cv2.BFMatcher(cv2.NORM_HAMMING)
    mm=bf.knnMatch(da,db,k=2)
    good=[m for m,n in mm if m.distance<0.75*n.distance]
    if len(good)<5: return np.zeros((0,4)),len(good)
    P=np.array([[ka[m.queryIdx].pt[0],ka[m.queryIdx].pt[1],
                 kb[m.trainIdx].pt[0]-ka[m.queryIdx].pt[0],
                 kb[m.trainIdx].pt[1]-ka[m.queryIdx].pt[1]] for m in good])*4.0
    P[:,:2]/=1.0
    d=P[:,2:]; med=np.median(d,0); mad=np.median(np.abs(d-med),0)+1e-6
    keep=(np.abs(d-med)<5*mad).all(1)
    return P[keep],len(good)
def guess(P,x,y,gmed):
    if len(P)<5: return gmed
    w=1.0/(np.hypot(P[:,0]-x,P[:,1]-y)+1e3)**2
    k=np.argsort(-w)[:12]
    return np.array([np.sum(w[k]*P[k,2])/np.sum(w[k]),np.sum(w[k]*P[k,3])/np.sum(w[k])])
def track(A,B):
    P,ng=stage1(A,B)
    gmed=np.median(P[:,2:],0) if len(P)>=5 else np.array([0.,0.])
    Hh,W=A.shape
    Af=np.nan_to_num(A,nan=np.nanmedian(A)).astype(np.float32)
    Bf=np.nan_to_num(B,nan=np.nanmedian(B)).astype(np.float32)
    va=np.isfinite(A); vb=np.isfinite(B)
    res=[]
    h=TMPL//2
    for yy in range(TMPL+SRCH, Hh-TMPL-SRCH, NODE):
        for xx in range(TMPL+SRCH, W-TMPL-SRCH, NODE):
            t=Af[yy-h:yy+h+1, xx-h:xx+h+1]
            if va[yy-h:yy+h+1, xx-h:xx+h+1].mean()<0.99: continue
            if t.std()<0.3: continue
            gx,gy=guess(P,xx,yy,gmed)
            cy=int(round(yy+gy)); cx=int(round(xx+gx))
            y0,y1=cy-h-SRCH, cy+h+SRCH+1; x0,x1=cx-h-SRCH, cx+h+SRCH+1
            if y0<0 or x0<0 or y1>Hh or x1>W: continue
            if vb[y0:y1,x0:x1].mean()<0.90: continue
            res.append([xx,yy,gx,gy,y0,x0])
            S=Bf[y0:y1,x0:x1]
            r=cv2.matchTemplate(S,t,cv2.TM_CCOEFF_NORMED)
            i=np.unravel_index(np.argmax(r),r.shape); pk=r[i]
            rr=r.copy(); rr[max(0,i[0]-5):i[0]+6, max(0,i[1]-5):i[1]+6]=-9
            sec=rr.max()
            dx=(x0+i[1]+h)-xx; dy=(y0+i[0]+h)-yy
            off=np.hypot(dx-gx,dy-gy)
            ok=(pk>=PEAK) and (pk/max(sec,1e-3)>=RATIO) and (off<=MAXOFF)
            res[-1]=[xx,yy,dx,dy,float(pk),float(sec),float(off),int(ok)]
    return np.array(res,float),len(P),ng
GROUPS={
 "melt":  [("T","20240810T180458","20240812T174832",47.7),("T","20240812T174832","20240813T182941",24.7),
           ("T","20240810T180458","20240813T182941",72.4),("D","20240824T174832","20240825T182942",24.7)],
 "winter":[("T","20240212T180459","20240214T174833",47.7),("T","20240214T174833","20240215T182942",24.7),
           ("T","20240212T180459","20240215T182942",72.4),("D","20240226T174833","20240227T182942",24.7)]}
out=[]
for season,prs in GROUPS.items():
    for k,ta,tb,dth in prs:
        A=np.load(f"scratch/R1_grid/{season}_{k}_{ta}.npy"); B=np.load(f"scratch/R1_grid/{season}_{k}_{tb}.npy")
        R,nf,ng=track(A,B)
        n=len(R); s=int(R[:,7].sum()) if n else 0
        d=np.hypot(R[R[:,7]==1,2],R[R[:,7]==1,3])*RES/1e3 if s else np.array([])
        rec=dict(season=season,roi=k,t0=ta,t1=tb,dt_h=dth,n_valid=n,n_success=s,
                 rate=round(s/max(n,1),4),n_feat=int(nf),n_orb_good=int(ng),
                 disp_med_km=round(float(np.median(d)),2) if s else None,
                 disp_p95_km=round(float(np.percentile(d,95)),2) if s else None,
                 peak_med=round(float(np.median(R[:,4])),3) if n else None)
        out.append(rec); np.save(f"scratch/R1_vec_{season}_{ta}_{tb}.npy",R)
        print(season,k,ta[:8],"->",tb[:8],dth,"h  valid",n,"succ",s,"rate %.3f"%rec['rate'],
              "feat",nf,"disp_med",rec['disp_med_km'])
json.dump(out,open("scratch/R1_results.json","w"),indent=1)
