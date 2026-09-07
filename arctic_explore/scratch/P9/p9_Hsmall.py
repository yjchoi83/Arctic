import numpy as np, pandas as pd, os, sys, datetime as dt, glob
sys.path.insert(0,"scratch/P3"); from cells import region_cells
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
rng=np.random.default_rng(0)
SEA={"winter":(1,1,3,31),"melt":(6,1,9,30),"freeze-up":(10,1,12,31)}
EP0=dt.datetime(1970,1,1)
z=np.load("scratch/P3/step2t_native1h.npz")
ed,em,et=z["dur"].astype(float),z["mag"].astype(float),z["t0"].astype(np.int64)
mo=np.array([(EP0+dt.timedelta(seconds=int(s))).month for s in et])
sea=np.where((mo>=1)&(mo<=3),"winter",np.where((mo>=6)&(mo<=9),"melt",np.where(mo>=10,"freeze-up","shoulder")))
CLASSES={"ge1":(1,np.inf),"1to3":(1,3),"ge3":(3,np.inf),"ge5":(5,np.inf)}
D={}
for cn,(lo,hi) in CLASSES.items():
    for s in SEA:
        v=ed[(em>=lo)&(em<hi)&(sea==s)]
        D[(cn,s)]=v if len(v)<=3000 else rng.choice(v,3000,replace=False)
print("P1b 1-h episode durations (median h):")
for cn in CLASSES:
    print("  %-5s"%cn,{s:round(float(np.median(D[(cn,s)])),1) for s in SEA},
          {s:len(D[(cn,s)]) for s in SEA})
def Hval(g,Dd):
    if len(g)==0 or len(Dd)==0: return np.nan
    gs=np.sort(np.asarray(g,float)); G=gs.sum()
    if G<=0: return np.nan
    cs=np.cumsum(gs); dd=np.asarray(Dd,float)
    i=np.searchsorted(gs,dd,side="right")
    return float((np.where(i>0,cs[np.maximum(i-1,0)],0.0)+dd*(len(gs)-i)).mean()/G)
CH=["Vilkitsky","Sannikov_DmLaptev","LongStrait","KaraGate","BeringChukchi"]
RC=region_cells(); rows=[]
for name in CH:
    cl=RC[name]
    for yr in range(2016,2027):
        f=f"scratch/P3/cellacq/{name}_{yr}.npz"
        if not os.path.exists(f): continue
        z2=np.load(f,allow_pickle=True)
        ci,t,p,o,c=z2["ci"],z2["t"],z2["p"].astype(str),z2["o"].astype(str),z2["c"]
        key=np.char.add(np.char.add(p,"_"),o)
        for k in range(len(cl)):
            m=ci==k
            if not m.any(): continue
            tt,cc,kk=t[m],c[m],key[m]
            order=np.argsort(tt); tt,cc,kk=tt[order],cc[order],kk[order]
            gid=np.zeros(len(tt),np.int64)
            for i in range(1,len(tt)):
                gid[i]=gid[i-1] if (kk[i]==kk[i-1] and tt[i]-tt[i-1]<=15*60*1000) else gid[i-1]+1
            ug=np.unique(gid)
            pt=np.array([tt[gid==g].mean() for g in ug]); pc=np.array([min(1.0,cc[gid==g].sum()) for g in ug])
            for s,(m0,d0,m1,d1) in SEA.items():
                a=(dt.datetime(yr,m0,d0)-EP0).total_seconds()*1000
                b=min((dt.datetime(yr,m1,d1,23,59)-EP0).total_seconds()*1000,
                      (dt.datetime(2026,9,5)-EP0).total_seconds()*1000)
                if b<=a: continue
                q=np.sort(pt[(pt>=a)&(pt<=b)&(pc>=0.5)])
                g=np.diff(q)/3.6e6 if len(q)>1 else np.array([])
                r=dict(region=name,cell=k,year=yr,season=s,n_acq=len(q))
                for cn in CLASSES: r["H_"+cn]=Hval(g,D[(cn,s)]) if len(q)>1 else 0.0
                rows.append(r)
    print(name,"done",flush=True)
C=pd.DataFrame(rows); C.to_csv("scratch/P9/H_by_class_cells.csv",index=False)
C["per"]=np.where(C.year.between(2019,2021),"pre",np.where(C.year.between(2022,2024),"during",
        np.where(C.year>=2025,"post","early")))
A=C[C.per!="early"].groupby(["per"])[["H_ge1","H_1to3","H_ge3","H_ge5"]].mean().round(3)
print("\nchokepoint H_episode by magnitude class:"); print(A.to_string())
print("\nby season (during 2022-24):")
print(C[C.per=="during"].groupby("season")[["H_ge1","H_1to3","H_ge3","H_ge5"]].mean().round(3).to_string())
C.groupby(["region","season","year"])[["H_ge1","H_1to3","H_ge3","H_ge5"]].mean().round(4).reset_index().to_csv(
    "scratch/P9/H_by_class_region.csv",index=False)
