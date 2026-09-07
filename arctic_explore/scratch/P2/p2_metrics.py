import json,glob,os,numpy as np,pandas as pd,datetime as dt,sys
sys.path.insert(0,"scratch/P2"); from regions import regions
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
DT=[6,12,24,48,72,168]
SEA={"winter":(1,1,3,31),"shoulder":(4,1,5,31),"melt":(6,1,9,30),"freeze-up":(10,1,12,31)}
COV=float(os.environ.get("COVTHR","0.5"))
rows=[];curves=[]
allmax=0
raw={}
for f in glob.glob("scratch/P2/raw/*.json"):
    b=os.path.basename(f)[:-5]; name,yr=b.rsplit("_",1)
    d=json.load(open(f))
    if d: allmax=max(allmax,max(r[0] for r in d))
    raw[(name,int(yr))]=d
DATA_END=dt.datetime(1970,1,1)+dt.timedelta(milliseconds=allmax)
print("data end",DATA_END.isoformat(),flush=True)
def passes(d):
    """group slices into passes: same platform+pass, gap < 15 min; coverage = min(1, sum)"""
    if not d: return np.zeros(0),np.zeros(0),[]
    a=sorted(d,key=lambda r:r[0])
    out=[];cur=[a[0]]
    for r in a[1:]:
        if r[1]==cur[-1][1] and r[2]==cur[-1][2] and (r[0]-cur[-1][0])<=15*60*1000: cur.append(r)
        else: out.append(cur); cur=[r]
    out.append(cur)
    t=np.array([np.mean([x[0] for x in g]) for g in out])
    c=np.array([min(1.0,sum(x[4] or 0 for x in g)) for g in out])
    p=[g[0][1] for g in out]
    return t,c,p
for (name,yr),d in sorted(raw.items()):
    t,c,p=passes(d)
    for sea,(m0,d0,m1,d1) in SEA.items():
        s=dt.datetime(yr,m0,d0); e=dt.datetime(yr,m1,d1,23,59)
        e=min(e,DATA_END)
        if e<=s: continue
        frac_win=(e-s).total_seconds()/((dt.datetime(yr,m1,d1,23,59)-s).total_seconds())
        ms=(s-dt.datetime(1970,1,1)).total_seconds()*1000; me=(e-dt.datetime(1970,1,1)).total_seconds()*1000
        sel=(t>=ms)&(t<=me)&(c>=COV)
        tt=np.sort(t[sel]); pp=np.array(p)[ (t>=ms)&(t<=me)&(c>=COV) ]
        n=len(tt); dur_h=(me-ms)/3.6e6
        gaps=np.diff(tt)/3.6e6 if n>1 else np.array([])
        rec=dict(region=name,year=yr,season=sea,n_acq=n,window_h=round(dur_h,1),
                 partial=int(frac_win<0.8),
                 med_gap_h=round(float(np.median(gaps)),2) if len(gaps) else None,
                 p90_gap_h=round(float(np.percentile(gaps,90)),2) if len(gaps) else None,
                 drift_pairs=int(np.sum((np.abs(tt[:,None]-tt[None,:])/3.6e6>=12)&
                                        (np.abs(tt[:,None]-tt[None,:])/3.6e6<=72))//2) if n>1 else 0)
        for plat in ["A","B","C","D"]:
            rec["n_S1"+plat]=int(np.sum(pp==plat))
        for x in DT:
            o=float(np.sum(gaps[gaps<=x])/dur_h) if len(gaps) else 0.0
            rec[f"O{x}"]=round(min(o,1.0),4)
            curves.append(dict(region=name,year=yr,season=sea,dt_h=x,O=round(min(o,1.0),4),n_acq=n))
        rows.append(rec)
T=pd.DataFrame(rows); C=pd.DataFrame(curves)
suf="" if COV==0.5 else f"_cov{int(COV*100)}"
T.to_csv(f"scratch/P2/P2_tables{suf}.csv",index=False); C.to_csv(f"scratch/P2/P2_curves{suf}.csv",index=False)
print("cells",len(T),"regions",T.region.nunique(),flush=True)
print(T[T.season=="freeze-up"].groupby("year")[["n_acq","O24"]].mean().round(3).to_string())
