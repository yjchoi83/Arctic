exec(open("scratch/TJ02_flip.py").read().split('print("date')[0])
from scipy.stats import rankdata
print("date n2km flip_total flip_resid_qmap corr_spearman",flush=True)
tot=[];res=[];N=[]
for D in ["20251023","20251121","20251218","20260116","20260220","20260320"]:
    Rc,cov,_=chart(D); Rs,_=sar(D)
    if Rs is None: continue
    m=cov&np.isfinite(Rc)&np.isfinite(Rs)
    Ac,As,Am=agg(np.where(m,Rc,np.nan)),agg(np.where(m,Rs,np.nan)),agg(m.astype("f4"))
    k=(Am>0.8)&np.isfinite(Ac)&np.isfinite(As); c=Ac[k]; s=As[k]; n=len(c)
    ft=float((cat(c)!=cat(s)).mean())
    q=(rankdata(s)-0.5)/n; sq=np.sort(c)[np.clip((q*n).astype(int),0,n-1)]   # quantile-map SAR onto chart marginal
    fr=float((cat(c)!=cat(sq)).mean())
    rs=float(np.corrcoef(rankdata(c),rankdata(s))[0,1])
    print(D,n,round(ft,3),round(fr,3),round(rs,3),flush=True)
    tot.append(ft);res.append(fr);N.append(n)
w=np.array(N,float)
print("AREA-WTD total",round(float(np.average(tot,weights=w)),3),"residual(spatial)",round(float(np.average(res,weights=w)),3),
      "calibration_component",round(float(np.average(tot,weights=w)-np.average(res,weights=w)),3),"n_cells",int(w.sum()),flush=True)
