import urllib.request, numpy as np, io, json
BUOYS=["301434060952820","301434061840390","301434061843360","301434061848380",
       "301434060402490","301434060406500","301434061846300","301434061841390"]
LAGS=[6,12,24,48,72,96,168]
res={L:[] for L in LAGS}; nb=0
for b in BUOYS:
    try:
        raw=urllib.request.urlopen(f"https://iabp.apl.uw.edu/WebData/{b}.dat",timeout=60).read().decode(errors="ignore")
    except Exception as e:
        print("fail",b,e); continue
    lines=raw.strip().split("\n"); hdr=lines[0].split()
    try:
        iy,ih,ihr,ilat,ilon=[hdr.index(k) for k in ("Year","Hour","Min","Lat","Lon")]
        idoy=hdr.index("DOY") if "DOY" in hdr else hdr.index("Doy")
    except Exception as e:
        print("hdr",b,hdr[:8]); continue
    T=[];LA=[];LO=[]
    for ln in lines[1:]:
        p=ln.split()
        if len(p)<=max(iy,idoy,ih,ilat,ilon): continue
        try:
            t=float(p[iy])*8760+float(p[idoy])*24+float(p[ih])+float(p[ihr])/60
            la=float(p[ilat]); lo=float(p[ilon])
        except: continue
        if abs(la)>90 or la<65: continue
        T.append(t);LA.append(la);LO.append(lo)
    if len(T)<50: continue
    T=np.array(T);LA=np.array(LA);LO=np.array(LO); nb+=1
    for L in LAGS:
        # for each point find the sample closest to t+L (within 10%)
        j=np.searchsorted(T,T+L)
        j=np.clip(j,0,len(T)-1)
        ok=np.abs(T[j]-(T+L))<0.15*L
        if ok.sum()<5: continue
        la1,lo1,la2,lo2=LA[ok],LO[ok],LA[j][ok],LO[j][ok]
        dy=(la2-la1)*111.32
        dx=(lo2-lo1)*111.32*np.cos(np.radians((la1+la2)/2))
        d=np.hypot(dx,dy)
        res[L].extend(d[d<500].tolist())
print("buoys used",nb)
out={}
for L in LAGS:
    a=np.array(res[L])
    if len(a)<10: out[L]=None; continue
    out[L]={"n":len(a),"med_km":round(float(np.median(a)),2),"p90_km":round(float(np.percentile(a,90)),2),
            "p95_km":round(float(np.percentile(a,95)),2),"mean_km":round(float(a.mean()),2)}
    print(L,"h ->",out[L])
json.dump(out,open("scratch/TA03_drift.json","w"),indent=1)
