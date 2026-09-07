import numpy as np, pandas as pd, os, sys, glob, datetime as dt, json
sys.path.insert(0,"scratch/P3"); from cells import region_cells
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
rng=np.random.default_rng(0)
SEA={"winter":(1,1,3,31),"melt":(6,1,9,30),"freeze-up":(10,1,12,31)}
EP0=dt.datetime(1970,1,1)
# ---- hazard duration distributions from P1b ----
z=np.load("scratch/P3/step2t_native1h.npz")
ed,em,et=z["dur"].astype(float),z["mag"].astype(float),z["t0"].astype(np.int64)
emo=np.array([ (EP0+dt.timedelta(seconds=int(s))).month for s in et ])
def seas(mo): return np.where((mo>=1)&(mo<=3),"winter",np.where((mo>=6)&(mo<=9),"melt",
             np.where(mo>=10,"freeze-up","shoulder")))
esea=seas(emo)
P=pd.read_csv("scratch/P1b/events_persist.csv")
P=P[P.season!="shoulder"].copy(); P["relmag"]=P.magnitude_km/P.sep_start_km
P=P[P.relmag>=0.10]
D_SAMP={}
for mc in (3,5):
    for s in SEA:
        d=ed[(em>=mc)&(esea==s)]
        D_SAMP[("episode",mc,s)]=d if len(d)<=3000 else rng.choice(d,3000,replace=False)
        q=P[(P.magnitude_km>=mc)&(P.season==s)].persist_h.values.astype(float)
        D_SAMP[("state",mc,s)]=q if len(q)<=3000 else rng.choice(q,3000,replace=False)
for k,v in sorted(D_SAMP.items()): print(k,"n",len(v),"med %.1f"%(np.median(v) if len(v) else np.nan),flush=True)
def Hval(gaps,D):
    """H = E_D[ sum_i min(g_i,D) ] / sum_i g_i  (length-biased gap weighting, PLAN A)"""
    if len(gaps)==0 or len(D)==0: return float("nan")
    gs=np.sort(np.asarray(gaps,float)); G=gs.sum()
    if G<=0: return float("nan")
    cs=np.cumsum(gs); Dd=np.asarray(D,float)
    idx=np.searchsorted(gs,Dd,side="right")
    s=np.where(idx>0,cs[np.maximum(idx-1,0)],0.0)+Dd*(len(gs)-idx)
    return float(s.mean()/G)
RC=region_cells(); rows=[]
for name,cl in RC.items():
    nc=len(cl)
    per_cell={}
    for yr in range(2016,2027):
        f=f"scratch/P3/cellacq/{name}_{yr}.npz"
        if not os.path.exists(f): continue
        z=np.load(f,allow_pickle=True)
        ci,t,p,m,o,c=z["ci"],z["t"],z["p"],z["m"],z["o"],z["c"]
        key=np.char.add(np.char.add(p.astype(str),"_"),o.astype(str))
        for k in range(nc):
            sel=ci==k
            if not sel.any(): continue
            tt=t[sel]; cc=c[sel]; kk=key[sel]; pl=p[sel].astype(str); md=m[sel].astype(str)
            order=np.argsort(tt); tt,cc,kk,pl,md=tt[order],cc[order],kk[order],pl[order],md[order]
            # group slices into passes
            gid=np.zeros(len(tt),np.int64)
            for i in range(1,len(tt)):
                gid[i]=gid[i-1] if (kk[i]==kk[i-1] and tt[i]-tt[i-1]<=15*60*1000) else gid[i-1]+1
            ug=np.unique(gid)
            pt=np.array([tt[gid==g].mean() for g in ug])
            pc=np.array([min(1.0,cc[gid==g].sum()) for g in ug])
            pp=np.array([pl[gid==g][0] for g in ug]); pm=np.array([md[gid==g][0] for g in ug])
            per_cell.setdefault(k,{})[yr]=(pt,pc,pp,pm)
    for k,byyr in per_cell.items():
        for yr,(pt,pc,pp,pm) in byyr.items():
            for s,(m0,d0,m1,d1) in SEA.items():
                a=(dt.datetime(yr,m0,d0)-EP0).total_seconds()*1000
                b=(dt.datetime(yr,m1,d1,23,59)-EP0).total_seconds()*1000
                b=min(b,(dt.datetime(2026,9,5)-EP0).total_seconds()*1000)
                if b<=a: continue
                sel=(pt>=a)&(pt<=b)&(pc>=0.5)
                ts=np.sort(pt[sel]); n=len(ts)
                gaps=np.diff(ts)/3.6e6 if n>1 else np.array([])
                win=(b-a)/3.6e6
                rec=dict(region=name,cell=k,year=yr,season=s,n_acq=n,win_h=round(win,1),
                         O24=round(float(gaps[gaps<=24].sum()/win) if n>1 else 0.0,4),
                         O12=round(float(gaps[gaps<=12].sum()/win) if n>1 else 0.0,4),
                         plats="".join(sorted(set(pp[sel].tolist()))))
                for kind in ("episode","state"):
                    for mc in (3,5):
                        rec[f"H_{kind}{mc}"]=round(Hval(gaps,D_SAMP[(kind,mc,s)]),4) if n>1 else 0.0
                rows.append(rec)
C=pd.DataFrame(rows); C.to_csv("scratch/P3/P3_cells.csv",index=False)
print("cell-season-year rows",len(C),flush=True)
def boot(g,col,nb=1000):
    cells=g.cell.unique()
    if len(cells)<2: return (np.nan,np.nan)
    v=[]
    for _ in range(nb):
        pick=rng.choice(cells,len(cells),replace=True)
        v.append(np.nanmean(np.concatenate([g[g.cell==c][col].values for c in pick])))
    return (float(np.nanpercentile(v,2.5)),float(np.nanpercentile(v,97.5)))
agg=[]
for (r,s,y),g in C.groupby(["region","season","year"]):
    d=dict(region=r,season=s,year=y,n_cells=g.cell.nunique(),n_acq_med=float(g.n_acq.median()))
    for col in ("H_episode3","H_episode5","H_state3","H_state5","O24","O12"):
        d[col]=round(float(np.nanmean(g[col])),4)
    lo,hi=boot(g,"H_state3"); d["H_state3_lo"],d["H_state3_hi"]=round(lo,4),round(hi,4)
    agg.append(d)
A=pd.DataFrame(agg); A.to_csv("scratch/P3/P3_region_season_year.csv",index=False)
print(A.groupby("year")[["H_episode3","H_state3","H_state5","O24"]].mean().round(3).to_string())
