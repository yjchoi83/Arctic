import numpy as np, pandas as pd, os, sys, datetime as dt, itertools, json
sys.path.insert(0,"scratch/P3"); from cells import region_cells
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
rng=np.random.default_rng(0)
SEA={"winter":(1,1,3,31),"melt":(6,1,9,30),"freeze-up":(10,1,12,31)}
EP0=dt.datetime(1970,1,1)
z=np.load("scratch/P3/step2t_native1h.npz")
P=pd.read_csv("scratch/P1b/events_persist.csv"); P=P[P.season!="shoulder"].copy()
P["relmag"]=P.magnitude_km/P.sep_start_km; P=P[P.relmag>=0.10]
DS={s:(lambda v: v if len(v)<=3000 else rng.choice(v,3000,replace=False))(
        P[(P.magnitude_km>=3)&(P.season==s)].persist_h.values.astype(float)) for s in SEA}
def Hval(gaps,D):
    if len(gaps)==0 or len(D)==0: return np.nan
    gs=np.sort(np.asarray(gaps,float)); G=gs.sum()
    if G<=0: return np.nan
    cs=np.cumsum(gs); Dd=np.asarray(D,float)
    idx=np.searchsorted(gs,Dd,side="right")
    return float((np.where(idx>0,cs[np.maximum(idx-1,0)],0.0)+Dd*(len(gs)-idx)).mean()/G)
RC=region_cells(); rows=[]
YEARS=list(range(2019,2022))+list(range(2025,2027))
for name,cl in RC.items():
    for yr in YEARS:
        f=f"scratch/P3/cellacq/{name}_{yr}.npz"
        if not os.path.exists(f): continue
        z2=np.load(f,allow_pickle=True)
        ci,t,pl,md,ob,cv=z2["ci"],z2["t"],z2["p"].astype(str),z2["m"].astype(str),z2["o"].astype(str),z2["c"]
        plats=sorted(set(pl))
        subsets=[]
        for r in range(1,len(plats)+1):
            for c in itertools.combinations(plats,r): subsets.append(c)
        for k in range(len(cl)):
            sel=ci==k
            if not sel.any(): continue
            tt,cc,pp,oo=t[sel],cv[sel],pl[sel],ob[sel]
            for sub in subsets:
                m2=np.isin(pp,sub)
                if not m2.any(): continue
                t2,c2,p2,o2=tt[m2],cc[m2],pp[m2],oo[m2]
                order=np.argsort(t2); t2,c2,p2,o2=t2[order],c2[order],p2[order],o2[order]
                key=np.char.add(np.char.add(p2,"_"),o2)
                gid=np.zeros(len(t2),np.int64)
                for i in range(1,len(t2)):
                    gid[i]=gid[i-1] if (key[i]==key[i-1] and t2[i]-t2[i-1]<=15*60*1000) else gid[i-1]+1
                ug=np.unique(gid)
                pt=np.array([t2[gid==g].mean() for g in ug])
                pc=np.array([min(1.0,c2[gid==g].sum()) for g in ug])
                for s,(m0,d0,m1,d1) in SEA.items():
                    a=(dt.datetime(yr,m0,d0)-EP0).total_seconds()*1000
                    b=min((dt.datetime(yr,m1,d1,23,59)-EP0).total_seconds()*1000,
                          (dt.datetime(2026,9,5)-EP0).total_seconds()*1000)
                    if b<=a: continue
                    q=np.sort(pt[(pt>=a)&(pt<=b)&(pc>=0.5)])
                    g=np.diff(q)/3.6e6 if len(q)>1 else np.array([])
                    rows.append(dict(region=name,cell=k,year=yr,season=s,subset="".join(sub),
                                     nsat=len(sub),H_state3=Hval(g,DS[s]) if len(q)>1 else 0.0))
    print(name,"done",flush=True)
D=pd.DataFrame(rows); D.to_csv("scratch/P6/ose_cells.csv",index=False)
A=D.groupby(["region","season","year","subset","nsat"],as_index=False).H_state3.mean()
A.to_csv("scratch/P6/ose_region.csv",index=False)
print("rows",len(D),"agg",len(A),flush=True)
