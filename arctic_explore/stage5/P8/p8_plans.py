import zipfile,re,glob,os,sys,numpy as np,pandas as pd,datetime as dt
from shapely.geometry import Polygon
from pyproj import Transformer
sys.path.insert(0,"scratch/P2"); from regions import regions
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
T=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
R=regions()
def boxpoly(w,e,s,n):
    lo=np.concatenate([np.linspace(w,e,30),np.full(30,e),np.linspace(e,w,30),np.full(30,w)])
    la=np.concatenate([np.full(30,s),np.linspace(s,n,30),np.full(30,n),np.linspace(n,s,30)])
    x,y=T.transform(lo,la); return Polygon(zip(x,y))
BOX={k:boxpoly(*v) for k,v in R.items()}
AREA={k:v.area for k,v in BOX.items()}
PM=re.compile(r"<Placemark>(.*?)</Placemark>",re.S)
G=lambda tag,s:(re.search(rf'<Data name="{tag}">\s*<value>(.*?)</value>',s,re.S) or [None,None])[1]
CO=re.compile(r"<coordinates>(.*?)</coordinates>",re.S)
seen=set(); rows=[]
for z in sorted(glob.glob("scratch/P8/plans/*.zip")):
    sat=re.search(r"Sentinel-1([ABC])",z).group(1); yr=int(re.search(r"(\d{4})\.zip",z).group(1))
    zf=zipfile.ZipFile(z); nk=0
    for name in zf.namelist():
        s=zf.read(name).decode("utf-8",errors="ignore")
        for p in PM.findall(s):
            dtid=G("DatatakeId",p); t0=G("ObservationTimeStart",p); mode=G("Mode",p)
            if not t0 or not dtid: continue
            key=(sat,dtid,t0)
            if key in seen: continue
            seen.add(key)
            m=CO.search(p)
            if not m: continue
            pts=[]
            for c in m.group(1).split():
                a=c.split(",")
                if len(a)>=2:
                    try: pts.append((float(a[0]),float(a[1])))
                    except ValueError: pass
            if len(pts)<4: continue
            if max(q[1] for q in pts)<60: continue
            x,y=T.transform([q[0] for q in pts],[q[1] for q in pts])
            g=Polygon(zip(x,y))
            if not g.is_valid: g=g.buffer(0)
            if g.is_empty: continue
            for rn,b in BOX.items():
                if not g.intersects(b): continue
                cov=g.intersection(b).area/AREA[rn]
                if cov<0.5: continue
                rows.append((sat,yr,rn,mode,t0,round(cov,3)))
            nk+=1
    print(z.split("/")[-1],"placemarks kept",nk,"rows",len(rows),flush=True)
D=pd.DataFrame(rows,columns=["sat","plan_year","region","mode","t0","cov"])
D["year"]=D.t0.str[:4].astype(int)
D.to_csv("scratch/P8/planned.csv",index=False)
P=D.groupby(["region","year","mode"]).size().rename("planned").reset_index()
P.to_csv("scratch/P8/planned_counts.csv",index=False)
print("total planned region-hits",len(D))
print(P.groupby(["year","mode"]).planned.sum().to_string())
