import numpy as np, pandas as pd, os
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
def km(t,ev):
    t=np.asarray(t,float); ev=np.asarray(ev,int)
    o=np.argsort(t); t,ev=t[o],ev[o]
    ut=np.unique(t); S=1.0; xs=[0.0]; ys=[1.0]
    n=len(t)
    for u in ut:
        at=t>=u; ni=at.sum()
        di=int(((t==u)&(ev==1)).sum())
        if ni>0 and di>0: S*=(1-di/ni)
        xs.append(u); ys.append(S)
    return np.array(xs),np.array(ys)
def q_from_S(xs,ys,q):
    i=np.where(ys<=1-q)[0]
    return float(xs[i[0]]) if len(i) else np.nan
def texp_direct(d,frac=0.8):
    best=np.nan
    for T in np.arange(1,745,1.0):
        if np.mean(np.minimum(1.0,d/T))>=frac: best=T
        else: break
    return best
def texp_km(xs,ys,frac=0.8):
    # integral of the right-continuous KM step function
    best=np.nan
    for T in np.arange(1,745,1.0):
        area=0.0
        for k in range(len(xs)-1):
            if xs[k]>=T: break
            area+=ys[k]*(min(xs[k+1],T)-xs[k])
        if xs[-1]<T: area+=ys[-1]*(T-xs[-1])
        if area/T>=frac: best=T
        else: break
    return best
rows=[]
# --- episode duration: native 1h (primary) and 3h control
for tag,lab in (("native1h","duration (1 h sampling)"),("control3h","duration (3 h sampling)")):
    z=np.load(f"scratch/P1b/step2_{tag}.npz"); d,m=z["dur"],z["mag"]
    for lo in (1,3,5):
        s=d[m>=lo]
        if len(s)<20: continue
        rows.append(dict(measurand=lab,mag=f">= {lo} km",n=len(s),
            p20=np.percentile(s,20),Texp80=texp_direct(s.astype(float)),
            p80=np.percentile(s,80),cens="0 %"))
# --- persistence: 3h, Kaplan-Meier (censoring honoured)
D=pd.read_csv("scratch/P1b/events_persist.csv")
S=D[D.season!="shoulder"].copy(); S["relmag"]=S.magnitude_km/S.sep_start_km
for sub,lab in ((S,"persistence (all events)"),(S[S.relmag>=0.10],"persistence (relmag >= 10 %)")):
    for lo in (1,3,5):
        d=sub[sub.magnitude_km>=lo]
        if len(d)<20: continue
        xs,ys=km(d.persist_h.values,1-d.censored.values)
        rows.append(dict(measurand=lab,mag=f">= {lo} km",n=len(d),
            p20=q_from_S(xs,ys,0.20),Texp80=texp_km(xs,ys),p80=q_from_S(xs,ys,0.80),
            cens=f"{100*d.censored.mean():.0f} %"))
T=pd.DataFrame(rows)
T.to_csv("scratch/P1b/obs_table.csv",index=False)
print(T.to_string(index=False))
