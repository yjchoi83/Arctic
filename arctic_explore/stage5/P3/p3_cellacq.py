import json,glob,os,sys,numpy as np
sys.path.insert(0,"scratch/P3"); sys.path.insert(0,"scratch/P2")
from cells import region_cells, CELL
from pyproj import Transformer
from shapely.geometry import box, Polygon, MultiPolygon
from shapely.strtree import STRtree
from shapely.ops import unary_union
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
FWD=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
RC=region_cells(); OUT="scratch/P3/cellacq"; os.makedirs(OUT,exist_ok=True)
def poly3413(coords):
    def ring(r):
        lo=[c[0] for c in r]; la=[c[1] for c in r]
        x,y=FWD.transform(lo,la); return list(zip(x,y))
    try:
        if not coords: return None
        if isinstance(coords[0][0][0],(int,float)):
            p=Polygon(ring(coords[0]))
        else:
            p=unary_union([Polygon(ring(c[0])) for c in coords if len(c[0])>=4])
        return p if p.is_valid else p.buffer(0)
    except Exception: return None
for name,cl in RC.items():
    boxes=[box(a,b,a+CELL,b+CELL) for a,b in cl]
    tree=STRtree(boxes); A=CELL*CELL
    for yr in range(2016,2027):
        src=f"scratch/P3/geom/{name}_{yr}.json"; dst=f"{OUT}/{name}_{yr}.npz"
        if os.path.exists(dst) or not os.path.exists(src): continue
        d=json.load(open(src))
        ci=[];tt=[];pp=[];mm=[];oo=[];cc=[]
        for rec in d:
            t,plat,mode,orb,g=rec
            p=poly3413(g)
            if p is None or p.is_empty: continue
            for k in tree.query(p):
                inter=boxes[k].intersection(p).area/A
                if inter<=0.01: continue
                ci.append(k);tt.append(t);pp.append(plat or "?");mm.append(mode or "?")
                oo.append(orb or "?");cc.append(inter)
        np.savez_compressed(dst,ci=np.array(ci,np.int32),t=np.array(tt,np.int64),
            p=np.array(pp),m=np.array(mm),o=np.array(oo),c=np.array(cc,np.float32),
            ncell=len(cl))
        print(name,yr,"pairs",len(ci),flush=True)
print("CELLACQ DONE",flush=True)
