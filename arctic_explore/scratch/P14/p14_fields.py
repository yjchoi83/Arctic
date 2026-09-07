"""ARC-P14 items 5 and 8: cache what the strait figures need.

For the five pairs that produced the nineteen candidate events, re-load the HH rasters and
recompute the divergence field, the connected-component labels and the two-scene footprint
overlap polygon, using exactly the P8/P11 definitions. Results go to scratch/P14/fields/.
The tracked node fields themselves are reused from scratch/P9/fields/, so no matching is redone.
"""
import glob, json, os, zipfile
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.crs import CRS
from rasterio.transform import from_origin
from scipy import ndimage as ndi
from shapely.geometry import MultiPoint
from shapely import wkt as shp_wkt
from pyproj import Transformer

os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
np.seterr(all="ignore")
RES, NODE = 200.0, 25
DX_KM = NODE * RES / 1e3
FWD = Transformer.from_crs("EPSG:4326", "EPSG:3413", always_xy=True)
SEL = json.load(open("scratch/P8/pairs_sel.json"))
ZIP = {os.path.basename(z).split(".")[0]: z for z in glob.glob("scratch/P8/s1/*.zip")}
PAIRS = [1, 3, 7, 9, 15]
OUT = "scratch/P14/fields"
os.makedirs(OUT, exist_ok=True)


def load(scene, x0, y1, W, H):
    z = ZIP[scene]
    tif = [m for m in zipfile.ZipFile(z).namelist() if m.endswith(".tiff") and "-hh-" in m][0]
    DST = from_origin(x0, y1, RES, RES)
    with rasterio.open(f"/vsizip/{z}/{tif}") as src:
        a = src.read(1).astype(np.float32)
        med = np.nanmedian(np.where(a > 0, a, np.nan), axis=0)
        med = np.nan_to_num(med, nan=np.nanmedian(med))
        a = np.where(a > 0, a / np.maximum(med[None, :], 1e-3), np.nan)
        a = (10 * np.log10(a)).astype(np.float32)
        d = np.full((H, W), np.nan, np.float32)
        reproject(a, d, gcps=src.gcps[0], src_crs=CRS.from_epsg(4326), dst_transform=DST,
                  dst_crs=CRS.from_epsg(3413), resampling=Resampling.average,
                  src_nodata=np.nan, dst_nodata=np.nan)
    return d


def foot(scene):
    z = ZIP[scene]
    tif = [m for m in zipfile.ZipFile(z).namelist() if m.endswith(".tiff") and "-hh-" in m][0]
    with rasterio.open(f"/vsizip/{z}/{tif}") as s:
        g = s.gcps[0]
    x, y = FWD.transform(np.array([p.x for p in g]), np.array([p.y for p in g]))
    return MultiPoint(list(zip(x, y))).convex_hull


ev = 0
manifest = []
for pi, pr in enumerate(SEL):
    f = f"scratch/P9/fields/pair{pi:02d}.npz"
    if not os.path.exists(f):
        continue
    z = np.load(f, allow_pickle=True)
    V = z["V"]; ok = V[:, 5] == 1
    if ok.sum() < 30:
        continue
    x0, y1 = float(z["x0"]), float(z["y1"])
    W, H = int(z["W"]), int(z["H"])
    dth = float(z["dth"]); reg = str(z["region"])
    gx = np.unique(V[:, 0]); gy = np.unique(V[:, 1])
    U = np.full((len(gy), len(gx)), np.nan); Vv = np.full_like(U, np.nan)
    ix = {v: i for i, v in enumerate(gx)}; iy = {v: i for i, v in enumerate(gy)}
    for r_ in V[ok]:
        U[iy[r_[1]], ix[r_[0]]] = r_[2] * RES / 1e3 / (dth / 24)
        Vv[iy[r_[1]], ix[r_[0]]] = -r_[3] * RES / 1e3 / (dth / 24)
    dudx = np.full_like(U, np.nan); dvdy = np.full_like(U, np.nan)
    dudx[:, 1:-1] = (U[:, 2:] - U[:, :-2]) / (2 * DX_KM)
    dvdy[1:-1, :] = (Vv[:-2, :] - Vv[2:, :]) / (2 * DX_KM)
    div = dudx + dvdy
    fin = np.isfinite(div)
    if fin.sum() < 20:
        continue
    thr = np.nanpercentile(div[fin], 10)
    mask = (div < thr) & fin
    lab, n = ndi.label(mask)
    keep = np.zeros_like(lab)
    ids = []
    for k in range(1, n + 1):
        m = lab == k
        area = m.sum() * DX_KM * DX_KM
        if area < 100:
            continue
        ev += 1
        keep[m] = ev
        ids.append((f"E{ev:03d}", round(float(area), 0)))
    if pi not in PAIRS:
        continue
    A = load(pr["a"], x0, y1, W, H)
    Bs = load(pr["b"], x0, y1, W, H)
    ovl = foot(pr["a"]).intersection(foot(pr["b"]))
    np.savez_compressed(
        f"{OUT}/pair{pi:02d}.npz",
        A=A.astype(np.float16), B=Bs.astype(np.float16),
        div=div.astype(np.float32), lab=keep.astype(np.int16),
        gx=gx, gy=gy, x0=x0, y1=y1, res=RES, dth=dth, thr=thr,
        region=reg, t0=str(z["t0"]), t1=str(z["t1"]),
        overlap_wkt=ovl.wkt, events=json.dumps(ids))
    manifest.append(dict(pair=pi, region=reg, t0=str(z["t0"]), events=ids,
                         overlap_km2=round(ovl.area / 1e6, 0)))
    print(f"pair {pi:2d} {reg:18s} {str(z['t0'])[:10]} events {[a for a,_ in ids]} "
          f"overlap {ovl.area/1e6:,.0f} km2", flush=True)
json.dump(manifest, open(f"{OUT}/manifest.json", "w"), indent=1)
print("total events counted", ev)
