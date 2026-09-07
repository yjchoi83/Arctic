import numpy as np, pandas as pd, glob, os, json
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
rng=np.random.default_rng(0)
RES=200.0; NODE=25; dx_km=NODE*RES/1e3      # 5 km node spacing
# ---------- A. S1 strait fields -> P1b buoy-pair metric ----------
rows=[]; pairstats=[]
for f in sorted(glob.glob("scratch/P9/fields/pair*.npz")):
    z=np.load(f,allow_pickle=True)
    V=z["V"]; dth=float(z["dth"]); reg=str(z["region"]); sea=str(z["season"]); yr=int(z["year"])
    ok=V[:,5]==1
    if ok.sum()<50: continue
    # node positions (m, EPSG:3413) and displacement (m) over the window
    px=z["x0"]+V[ok,0]*RES; py=z["y1"]-V[ok,1]*RES
    ux=V[ok,2]*RES; uy=-V[ok,3]*RES
    n=len(px)
    # virtual buoy pairs with 20-100 km separation, matching P1b's baseline band
    idx=rng.integers(0,n,size=(20000,2))
    a,b=idx[:,0],idx[:,1]
    sep0=np.hypot(px[b]-px[a],py[b]-py[a])/1e3
    m=(sep0>=20)&(sep0<=100)&(a!=b)
    a,b,sep0=a[m],b[m],sep0[m]
    if len(a)<50: continue
    sep1=np.hypot((px[b]+ux[b])-(px[a]+ux[a]),(py[b]+uy[b])-(py[a]+uy[a]))/1e3
    ds=sep1-sep0                      # negative = convergence (P1b magnitude = -ds)
    rate=ds/(dth/24.0)                # km/day, P1b's r
    pairstats.append(dict(pair=os.path.basename(f),region=reg,season=sea,year=yr,dt_h=round(dth,1),
        n_vpair=len(a),conv_frac=round(float((ds<0).mean()),3),
        mag_med=round(float(np.median(-ds[ds<0])),3) if (ds<0).any() else np.nan,
        mag_p90=round(float(np.percentile(-ds[ds<0],90)),3) if (ds<0).any() else np.nan,
        mag_max=round(float((-ds).max()),3),
        frac_ge3=round(float((-ds>=3).mean()),4),frac_ge5=round(float((-ds>=5).mean()),4),
        rate_p10=round(float(np.percentile(rate,10)),3)))
    rows.append(pd.DataFrame(dict(region=reg,season=sea,year=yr,sep0=sep0,ds=ds,rate=rate,dt_h=dth)))
P=pd.DataFrame(pairstats); P.to_csv("scratch/P9/virtual_pair_stats.csv",index=False)
A=pd.concat(rows,ignore_index=True); A.to_csv("scratch/P9/virtual_pairs_all.csv.gz",index=False,compression="gzip")
print("=== A. S1 strait fields expressed in the P1b buoy-pair metric ===")
print("windows",len(P),"virtual pairs",len(A))
conv=A[A.ds<0]
print("closure (km) over the window: median %.2f p75 %.2f p90 %.2f p99 %.2f max %.2f"%tuple(
    np.percentile(-conv.ds,[50,75,90,99,100])))
print("fraction of virtual pairs reaching >=3 km closure: %.4f ; >=5 km: %.4f"%(
    float((-A.ds>=3).mean()),float((-A.ds>=5).mean())))
print(P.groupby(["region","season"])[["conv_frac","mag_med","mag_p90","frac_ge3"]].mean().round(3).to_string())
