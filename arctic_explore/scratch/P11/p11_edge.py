import numpy as np, pandas as pd, glob, os, json, zipfile, rasterio, sys
from scipy import ndimage as ndi
from shapely.geometry import Polygon, Point
from pyproj import Transformer
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
FWD=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
RES=200.0; NODE=25; dx_km=NODE*RES/1e3
SEL=json.load(open("scratch/P8/pairs_sel.json"))
ZIP={os.path.basename(z).split(".")[0]:z for z in glob.glob("scratch/P8/s1/*.zip")}
def foot(scene):
    z=ZIP.get(scene)
    if z is None: return None
    tif=[m for m in zipfile.ZipFile(z).namelist() if m.endswith('.tiff') and '-hh-' in m][0]
    with rasterio.open(f"/vsizip/{z}/{tif}") as s: g=s.gcps[0]
    x,y=FWD.transform(np.array([p.x for p in g]),np.array([p.y for p in g]))
    from shapely.geometry import MultiPoint
    return MultiPoint(list(zip(x,y))).convex_hull
rows=[]; ev=0
for pi,pr in enumerate(SEL):
    f=f"scratch/P9/fields/pair{pi:02d}.npz"
    if not os.path.exists(f): continue
    z=np.load(f,allow_pickle=True)
    V=z["V"]; x0=float(z["x0"]); y1=float(z["y1"]); dth=float(z["dth"]); reg=str(z["region"])
    ok=V[:,5]==1
    if ok.sum()<30: continue
    fa,fb=foot(pr["a"]),foot(pr["b"])
    if fa is None or fb is None: continue
    ovl=fa.intersection(fb)
    if ovl.is_empty: continue
    bnd=ovl.boundary
    gx=np.unique(V[:,0]); gy=np.unique(V[:,1])
    U=np.full((len(gy),len(gx)),np.nan); Vv=np.full((len(gy),len(gx)),np.nan)
    ix={v:i for i,v in enumerate(gx)}; iy={v:i for i,v in enumerate(gy)}
    for r_ in V[ok]:
        U[iy[r_[1]],ix[r_[0]]]= r_[2]*RES/1e3/(dth/24)
        Vv[iy[r_[1]],ix[r_[0]]]=-r_[3]*RES/1e3/(dth/24)
    dudx=np.full_like(U,np.nan); dvdy=np.full_like(U,np.nan)
    dudx[:,1:-1]=(U[:,2:]-U[:,:-2])/(2*dx_km)
    dvdy[1:-1,:]=(Vv[:-2,:]-Vv[2:,:])/(2*dx_km)
    div=dudx+dvdy; fin=np.isfinite(div)
    if fin.sum()<20: continue
    thr=np.nanpercentile(div[fin],10); mask=(div<thr)&fin
    lab,n=ndi.label(mask)
    for k in range(1,n+1):
        m=lab==k; area=m.sum()*dx_km*dx_km
        if area<100: continue
        ev+=1
        ii,jj=np.where(m)
        px=x0+gx[jj]*RES; py=y1-gy[ii]*RES
        cx,cy=px.mean(),py.mean()
        d_centroid=Point(cx,cy).distance(bnd)/1e3
        d_pix=np.array([Point(a,b).distance(bnd) for a,b in zip(px,py)])/1e3
        near=float((d_pix<=5).mean())
        rows.append(dict(event=f"E{ev:03d}",pair=pi,region=reg,season=pr["season"],year=pr["year"],
            date=pr["t0"][:10],area_km2=round(area,0),
            centroid_dist_km=round(float(d_centroid),2),
            frac_pix_within_5km=round(near,3),
            EDGE_SUSPECT=bool(near>0.50),
            inside_overlap=bool(ovl.contains(Point(cx,cy))),
            overlap_area_km2=round(ovl.area/1e6,0)))
D=pd.DataFrame(rows); D.to_csv("scratch/P11/edge_audit.csv",index=False)
print("events audited",len(D))
print(D[["event","region","date","area_km2","centroid_dist_km","frac_pix_within_5km","EDGE_SUSPECT","inside_overlap"]].to_string(index=False))
print("\nEDGE_SUSPECT:",int(D.EDGE_SUSPECT.sum()),"of",len(D),"| passing:",int((~D.EDGE_SUSPECT).sum()))
print("outside overlap polygon:",int((~D.inside_overlap).sum()))
print("\nclustering by pair:"); print(D.groupby(["pair","region","date"]).size().rename("n_events").to_string())
