"""ARC-P14 basemap: Natural Earth 50m land + coastline and a graticule, on EPSG:3413.

Vector data are clipped to lat >= 40 in geographic coordinates *before* reprojection, so
nothing from the far hemisphere is pushed through the north polar projection.
Sources cached in scratch/P14/ne/ (ne_50m_land.zip, ne_50m_coastline.zip, naciscdn.org).
"""
import os, pickle
import numpy as np
import geopandas as gpd
from shapely.geometry import box, LineString
from shapely.ops import transform as shp_transform
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__))
NE = os.path.join(HERE, "ne")
CACHE = os.path.join(NE, "ne50_3413.pkl")
FWD = Transformer.from_crs("EPSG:4326", "EPSG:3413", always_xy=True)

LAND_FC = "#eceae5"      # light land fill
COAST_C = "0.42"
GRAT_C = "0.80"


def _load():
    if os.path.exists(CACHE):
        with open(CACHE, "rb") as f:
            return pickle.load(f)
    clip = box(-180, 40, 180, 90)
    out = {}
    for key, fn in (("land", "ne_50m_land.zip"), ("coast", "ne_50m_coastline.zip")):
        g = gpd.read_file(os.path.join(NE, fn))
        g = g[g.intersects(clip)].copy()
        g["geometry"] = g.intersection(clip)
        g = g[~g.is_empty]
        g = g.to_crs("EPSG:3413")
        # reprojection to a polar CRS can leave self-intersections near the pole and the
        # antimeridian; repair once here so every later intersection is safe
        import shapely
        g["geometry"] = shapely.make_valid(g.geometry.values)
        g = g[~g.is_empty]
        out[key] = g
    with open(CACHE, "wb") as f:
        pickle.dump(out, f)
    return out


def graticule(xlim, ylim, dlon=30, dlat=5, n=400):
    """Meridian and parallel segments (in km) inside the axes window."""
    xmin, xmax = min(xlim), max(xlim); ymin, ymax = min(ylim), max(ylim)
    segs = []
    for lon in np.arange(-180, 180, dlon):
        la = np.linspace(40, 89.5, n)
        x, y = FWD.transform(np.full(n, float(lon)), la)
        segs.append(("lon", lon, x / 1e3, y / 1e3))
    for lat in np.arange(45, 90, dlat):
        lo = np.linspace(-180, 180, 4 * n)
        x, y = FWD.transform(lo, np.full(4 * n, float(lat)))
        segs.append(("lat", lat, x / 1e3, y / 1e3))
    keep = []
    for kind, val, x, y in segs:
        m = (x >= xmin - 50) & (x <= xmax + 50) & (y >= ymin - 50) & (y <= ymax + 50)
        if m.sum() < 2:
            continue
        # split at gaps so a line does not jump across the window
        idx = np.where(m)[0]
        for grp in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1):
            if len(grp) >= 2:
                keep.append((kind, val, x[grp], y[grp]))
    return keep


def draw(ax, xlim, ylim, land=True, coast=True, grat=True, lw_coast=0.35,
         dlon=30, dlat=5, zorder=0):
    """Draw land fill, coastline and graticule. xlim/ylim in km, EPSG:3413."""
    d = _load()
    clip = box(min(xlim) * 1e3 - 2e5, min(ylim) * 1e3 - 2e5,
               max(xlim) * 1e3 + 2e5, max(ylim) * 1e3 + 2e5)
    if grat:
        for kind, val, x, y in graticule(xlim, ylim, dlon, dlat):
            ax.plot(x, y, color=GRAT_C, lw=0.3, zorder=zorder, solid_capstyle="butt")
    if land:
        g = d["land"][d["land"].intersects(clip)]
        for geom in g.geometry:
            try:
                gg = geom.intersection(clip)
            except Exception:
                gg = geom.buffer(0).intersection(clip)
            if gg.is_empty:
                continue
            for poly in (gg.geoms if hasattr(gg, "geoms") else [gg]):
                if poly.geom_type != "Polygon":
                    continue
                xs, ys = np.array(poly.exterior.coords).T
                ax.fill(xs / 1e3, ys / 1e3, facecolor=LAND_FC, edgecolor="none",
                        zorder=zorder + 0.1)
    if coast:
        g = d["coast"][d["coast"].intersects(clip)]
        for geom in g.geometry:
            try:
                gg = geom.intersection(clip)
            except Exception:
                continue
            if gg.is_empty:
                continue
            for ln in (gg.geoms if hasattr(gg, "geoms") else [gg]):
                if ln.geom_type != "LineString":
                    continue
                xs, ys = np.array(ln.coords).T
                ax.plot(xs / 1e3, ys / 1e3, color=COAST_C, lw=lw_coast, zorder=zorder + 0.2,
                        solid_capstyle="round")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
