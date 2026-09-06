import urllib.request,re,numpy as np,json
from pyproj import Transformer
M=np.load("scratch/R1_grid/_meta.npy",allow_pickle=True).item()
inv=Transformer.from_crs("EPSG:3413","EPSG:4326",always_xy=True)
box={}
for k,m in M.items():
    xs=[m['x0'],m['x0']+m['W']*m['res']]; ys=[m['y1']-m['H']*m['res'],m['y1']]
    lo,la=inv.transform([xs[0],xs[1],xs[0],xs[1]],[ys[0],ys[0],ys[1],ys[1]])
    box[k]=(min(lo),max(lo),min(la),max(la)); print(k,"lon %.2f..%.2f lat %.2f..%.2f"%box[k])
base="https://iabp.apl.uw.edu/WebData/"
idx=urllib.request.urlopen(base,timeout=60).read().decode(errors="ignore")
files=re.findall(r'href="([0-9]+\.dat)"',idx)
print("buoy files",len(files))
WIN=[("winter",2024,43,58),("melt",2024,223,239)]   # DOY ranges covering the pairs
hits={"winter":[],"melt":[]}
for i,f in enumerate(files):
    try: raw=urllib.request.urlopen(base+f,timeout=20).read().decode(errors="ignore")
    except Exception: continue
    L=raw.strip().split("\n")
    if len(L)<20: continue
    h=L[0].split()
    try:
        iy=h.index("Year");ila=h.index("Lat");ilo=h.index("Lon")
        idoy=h.index("DOY") if "DOY" in h else h.index("Doy")
    except Exception: continue
    for ln in L[1:]:
        p=ln.split()
        if len(p)<=max(iy,idoy,ila,ilo): continue
        try: y=int(float(p[iy]));dy=float(p[idoy]);la=float(p[ila]);lo=float(p[ilo])
        except Exception: continue
        for tag,yy,d0,d1 in WIN:
            if y!=yy or not(d0<=dy<=d1): continue
            for k,(a,b,c,d) in box.items():
                if a<=lo<=b and c<=la<=d: hits[tag].append((f,dy,la,lo,k))
    if i%200==0: print("  scanned",i,"hits w/m",len(hits['winter']),len(hits['melt']),flush=True)
for t in hits: print(t,"records",len(hits[t]),"buoys",len(set(x[0] for x in hits[t])))
json.dump({k:v[:2000] for k,v in hits.items()},open("scratch/R1_iabp.json","w"))
