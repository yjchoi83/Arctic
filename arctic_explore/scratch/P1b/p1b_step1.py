import numpy as np, pandas as pd, os, datetime as dt
from pyproj import Transformer
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
g=np.load("scratch/P1/grid.npz",allow_pickle=True)
E,B,X,Y,buoys,grid=g["E"],g["B"],g["X"],g["Y"],g["buoys"],g["grid"]
o=np.lexsort((E,B)); E,B,X,Y=E[o],B[o],X[o],Y[o]
ub,bs=np.unique(B,return_index=True); bs=np.append(bs,len(B))
SER={int(ub[k]):(E[bs[k]:bs[k+1]],X[bs[k]:bs[k+1]].astype(np.float64),Y[bs[k]:bs[k+1]].astype(np.float64))
     for k in range(len(ub))}
z=np.load("scratch/P1/pairs.npz",allow_pickle=True)
PK,EP,SP=z["PK"],z["EP"],z["SP"]; NB=int(z["NB"])
new=np.ones(len(PK),bool); new[1:]=(PK[1:]!=PK[:-1])|((EP[1:]-EP[:-1])!=1)
rid=np.cumsum(new)-1; cnt=np.bincount(rid); good=(cnt>=8)[rid]
r=np.full(len(PK),np.nan); r[1:]=(SP[1:]-SP[:-1])/0.125
valid=(~new)&good&np.concatenate(([False],good[:-1]))
THR=float(np.percentile(np.abs(r[valid&(r<0)]),90))
print("THR",round(THR,3),flush=True)
inv=Transformer.from_crs("EPSG:3413","EPSG:4326",always_xy=True)
def region(lon,lat):
    if lat>=82: return "central Arctic"
    if 10<=lon<100: return "Kara/Barents"
    if 100<=lon<180: return "Laptev/ESS"
    if -180<=lon<-125: return "Chukchi/Beaufort"
    return "other"
def season(mo):
    return "winter" if 1<=mo<=3 else ("melt" if 6<=mo<=9 else ("freeze-up" if mo>=10 else "shoulder"))
rows=[]
for pk in np.unique(PK):
    i,j=int(pk//NB),int(pk%NB)
    ei,xi,yi=SER[i]; ej,xj,yj=SER[j]
    ce,ii,jj=np.intersect1d(ei,ej,assume_unique=True,return_indices=True)
    if len(ce)<3: continue
    sep=np.hypot(xi[ii]-xj[jj],yi[ii]-yj[jj])/1e3
    band=(sep>=20)&(sep<=100)
    idx=np.where(band)[0]
    if len(idx)<8: continue
    brk=np.ones(len(idx),bool); brk[1:]=(ce[idx[1:]]-ce[idx[:-1]])!=1
    run=np.cumsum(brk)-1; rc=np.bincount(run)
    keep=(rc>=8)[run]
    ok=np.zeros(len(idx),bool)
    rr=np.full(len(idx),np.nan)
    rr[1:]=(sep[idx[1:]]-sep[idx[:-1]])/0.125
    vv=(~brk)&keep&np.concatenate(([False],keep[:-1]))
    ok=vv&(rr<=-THR)
    pos=np.where(ok)[0]
    if len(pos)==0: continue
    b2=np.ones(len(pos),bool); b2[1:]=(pos[1:]!=pos[:-1]+1)|(brk[pos[1:]])
    eid=np.cumsum(b2)-1; ne=eid[-1]+1
    fi=np.zeros(ne,np.int64); fi[eid[b2]]=pos[b2]
    em=np.append(b2[1:],True); li=np.zeros(ne,np.int64); li[eid[em]]=pos[em]
    L=li-fi+1; sel=L>=2
    for f,l in zip(fi[sel],li[sel]):
        a=idx[f-1]; b=idx[l]            # full-series indices
        spre=sep[a]; dur=(l-f+1)*3.0; mag=spre-sep[b]
        tgt=0.9*spre
        k=b+1; pers=None; cens=1
        while k<len(ce) and (ce[k]-ce[k-1])==1:
            if sep[k]>=tgt: pers=(ce[k]-ce[b])*3.0; cens=0; break
            k+=1
        if pers is None: pers=(ce[min(k,len(ce)-1)]-ce[b])*3.0
        mid=(a+b)//2
        lon,lat=inv.transform(float((xi[ii[mid]]+xj[jj[mid]])/2),float((yi[ii[mid]]+yj[jj[mid]])/2))
        t0=dt.datetime(1970,1,1)+dt.timedelta(seconds=int(grid[ce[a]]))
        rows.append((buoys[i],buoys[j],t0.strftime("%Y-%m-%dT%H:%M"),dur,round(float(mag),3),
                     round(float(spre),2),round(lat,3),round(lon,3),region(lon,lat),season(t0.month),
                     pers,cens))
D=pd.DataFrame(rows,columns=["buoyA","buoyB","start_utc","duration_h","magnitude_km","sep_start_km",
                             "lat","lon","region","season","persist_h","censored"])
print("events",len(D),"(P1 had 82440)",flush=True)
D.to_csv("scratch/P1b/events_persist.csv",index=False)
S=D[D.season!="shoulder"]
def blk(d,name):
    if len(d)<20: return f"| {name} | {len(d)} | — | — | — | — |"
    u=d[d.censored==0]
    if len(u)<20: return f"| {name} | {len(d)} | {d.censored.mean()*100:.0f} % | — | — | — |"
    q=np.percentile(u.persist_h,[50,75,90])
    return f"| {name} | {len(d)} | {d.censored.mean()*100:.0f} % | {q[0]:.0f} | {q[1]:.0f} | {q[2]:.0f} |"
L=["| group | n_ev | censored | med h | p75 | p90 |","|---|---|---|---|---|---|"]
for s in ["winter","freeze-up","melt"]: L.append(blk(S[S.season==s],f"season {s}"))
for m in [1,3,5]: L.append(blk(S[S.magnitude_km>=m],f"mag >= {m} km"))
for s in ["winter","freeze-up","melt"]:
    for m in [1,3,5]:
        L.append(blk(S[(S.season==s)&(S.magnitude_km>=m)],f"{s} x >= {m} km"))
open("scratch/P1b/persist_tables.md","w").write("\n".join(L))
print("\n".join(L),flush=True)
print("overall censored %.1f %%"%(S.censored.mean()*100))
