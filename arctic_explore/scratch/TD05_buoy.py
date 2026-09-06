import urllib.request,re,numpy as np,json,random
base="https://iabp.apl.uw.edu/WebData/"
idx=urllib.request.urlopen(base,timeout=60).read().decode(errors="ignore")
files=[f for f in re.findall(r'href="([0-9]+\.dat)"',idx)]
print("dat files listed:",len(files))
random.seed(0); samp=files if len(files)<=120 else random.sample(files,120)
ROI=(100,200,70,79)  # lon 100E..160W(=200), lat 70-79  Laptev-ESib-Chukchi
def inroi(la,lo):
    lo=np.where(lo<0,lo+360,lo)
    return (lo>=ROI[0])&(lo<=ROI[1])&(la>=ROI[2])&(la<=ROI[3])
stat={"melt":{"buoys":set(),"d":[]},"winter":{"buoys":set(),"d":[]}}
nb=0
for f in samp:
    try: raw=urllib.request.urlopen(base+f,timeout=25).read().decode(errors="ignore")
    except Exception: continue
    L=raw.strip().split("\n")
    if len(L)<50: continue
    h=L[0].split()
    try:
        iy,ih,imn,ila,ilo=[h.index(k) for k in ("Year","Hour","Min","Lat","Lon")]
        idoy=h.index("DOY") if "DOY" in h else h.index("Doy")
    except Exception: continue
    T=[];LA=[];LO=[];DOY=[]
    for ln in L[1:]:
        p=ln.split()
        if len(p)<=max(iy,idoy,ih,ila,ilo): continue
        try:
            t=float(p[iy])*8760+float(p[idoy])*24+float(p[ih])+float(p[imn])/60
            la=float(p[ila]);lo=float(p[ilo]);dy=float(p[idoy])
        except Exception: continue
        if la<60 or la>90: continue
        T.append(t);LA.append(la);LO.append(lo);DOY.append(dy)
    if len(T)<50: continue
    T=np.array(T);LA=np.array(LA);LO=np.array(LO);DOY=np.array(DOY); nb+=1
    j=np.searchsorted(T,T+48); j=np.clip(j,0,len(T)-1)
    ok=np.abs(T[j]-(T+48))<7.2
    if ok.sum()<5: continue
    la1,lo1=LA[ok],LO[ok]; la2,lo2=LA[j][ok],LO[j][ok]; dy=DOY[ok]
    reg=inroi(la1,lo1)
    dyy=(la2-la1)*111.32; dxx=(lo2-lo1)*111.32*np.cos(np.radians((la1+la2)/2))
    dd=np.hypot(dxx,dyy)
    good=reg&(dd<300)
    melt=good&(dy>=166)&(dy<=258)      # 15 Jun - 15 Sep
    wint=good&((dy>=32)&(dy<=105))     # 1 Feb - 15 Apr
    for k,m in (("melt",melt),("winter",wint)):
        if m.sum():
            stat[k]["buoys"].add(f); stat[k]["d"].extend(dd[m].tolist())
print("buoys parsed",nb)
out={}
for k,v in stat.items():
    a=np.array(v["d"])
    out[k]={"n_buoys":len(v["buoys"]),"n_samples":len(a),
            "med_km_48h":round(float(np.median(a)),2) if len(a) else None,
            "p90_km":round(float(np.percentile(a,90)),2) if len(a) else None,
            "p95_km":round(float(np.percentile(a,95)),2) if len(a) else None}
    print(k,out[k])
json.dump(out,open("scratch/TD05_buoy.json","w"),indent=1)
