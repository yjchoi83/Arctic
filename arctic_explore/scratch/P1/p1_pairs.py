import numpy as np, os
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
d=np.load("scratch/P1/grid.npz",allow_pickle=True)
E,B,X,Y=d["E"],d["B"],d["X"],d["Y"]; NB=len(d["buoys"])
ue,st=np.unique(E,return_index=True); st=np.append(st,len(E))
PK=[];EP=[];SP=[];MX=[];MY=[]
for k in range(len(ue)):
    a,b=st[k],st[k+1]
    if b-a<2: continue
    bb=B[a:b]; xx=X[a:b].astype(np.float64); yy=Y[a:b].astype(np.float64)
    dx=xx[:,None]-xx[None,:]; dy=yy[:,None]-yy[None,:]
    s=np.hypot(dx,dy)/1e3
    i,j=np.triu_indices(len(bb),1)
    sel=(s[i,j]>=20)&(s[i,j]<=100)
    if not sel.any(): continue
    i2,j2=i[sel],j[sel]
    lo=np.minimum(bb[i2],bb[j2]).astype(np.int64); hi=np.maximum(bb[i2],bb[j2]).astype(np.int64)
    PK.append(lo*NB+hi); EP.append(np.full(sel.sum(),ue[k],np.int32)); SP.append(s[i2,j2].astype(np.float32))
    MX.append(((xx[i2]+xx[j2])/2).astype(np.float32)); MY.append(((yy[i2]+yy[j2])/2).astype(np.float32))
PK=np.concatenate(PK);EP=np.concatenate(EP);SP=np.concatenate(SP);MX=np.concatenate(MX);MY=np.concatenate(MY)
o=np.lexsort((EP,PK)); PK,EP,SP,MX,MY=PK[o],EP[o],SP[o],MX[o],MY[o]
print("pair-epoch records",len(PK),"unique pairs",len(np.unique(PK)),flush=True)
np.savez_compressed("scratch/P1/pairs.npz",PK=PK,EP=EP,SP=SP,MX=MX,MY=MY,NB=NB,grid=d["grid"],buoys=d["buoys"])
print("PAIRS DONE",flush=True)
