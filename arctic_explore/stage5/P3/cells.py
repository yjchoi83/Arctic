import numpy as np, sys
sys.path.insert(0,"scratch/P2"); from regions import regions
from pyproj import Transformer
from shapely.geometry import box, Polygon
FWD=Transformer.from_crs("EPSG:4326","EPSG:3413",always_xy=True)
CELL=25000.0
def region_cells():
    out={}
    for name,(w,e,s,n) in regions().items():
        lo=np.linspace(w,e,25); la=np.linspace(s,n,25)
        X,Y=FWD.transform(np.repeat(lo,len(la)),np.tile(la,len(lo)))
        x0,x1,y0,y1=X.min(),X.max(),Y.min(),Y.max()
        cx=np.arange(np.floor(x0/CELL)*CELL,x1+CELL,CELL)
        cy=np.arange(np.floor(y0/CELL)*CELL,y1+CELL,CELL)
        cells=[]
        INV=Transformer.from_crs("EPSG:3413","EPSG:4326",always_xy=True)
        for a in cx:
            for b in cy:
                mx,my=a+CELL/2,b+CELL/2
                lon,lat=INV.transform(mx,my)
                if not (s<=lat<=n): continue
                if w<=e:
                    if not (w<=lon<=e): continue
                else:
                    if not (lon>=w or lon<=e): continue
                cells.append((a,b))
        out[name]=cells
    return out
if __name__=="__main__":
    c=region_cells()
    for k,v in c.items(): print(k,len(v))
    print("TOTAL",sum(len(v) for v in c.values()))
