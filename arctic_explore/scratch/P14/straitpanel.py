"""ARC-P14 items 5 and 8: one strait panel, shared by Figure 6 and Figure A1.

Each panel is cropped to the two-scene footprint overlap, shows the retrieved divergence as a
semi-transparent raster over the after-scene HH, outlines the connected component, and carries
a graticule and a 50 km scale bar. The before-scene appears as a small thumbnail.
"""
import json
import numpy as np
from shapely import wkt as shp_wkt
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
from matplotlib.colors import Normalize
import figstyle as F
import basemap as B

DIV_LIM = 0.10                       # per day; common to every panel
DIV_NORM = Normalize(-DIV_LIM, DIV_LIM)
FIELDS = "scratch/P14/fields"


def load(pair):
    z = np.load(f"{FIELDS}/pair{pair:02d}.npz", allow_pickle=True)
    d = {k: z[k] for k in z.files}
    d["events"] = json.loads(str(z["events"]))
    d["overlap"] = shp_wkt.loads(str(z["overlap_wkt"]))
    return d


def crop_box(d, pad_km=6):
    """Bounding box of the two-scene overlap, clipped to the raster, in km."""
    x0, y1, res = float(d["x0"]), float(d["y1"]), float(d["res"])
    H, W = d["A"].shape
    ex = (x0 / 1e3, (x0 + W * res) / 1e3, (y1 - H * res) / 1e3, y1 / 1e3)
    bx0, by0, bx1, by1 = [v / 1e3 for v in d["overlap"].bounds]
    return (max(ex[0], bx0 - pad_km), min(ex[1], bx1 + pad_km),
            max(ex[2], by0 - pad_km), min(ex[3], by1 + pad_km))


def _img_extent(d):
    x0, y1, res = float(d["x0"]), float(d["y1"]), float(d["res"])
    H, W = d["A"].shape
    return [x0 / 1e3, (x0 + W * res) / 1e3, (y1 - H * res) / 1e3, y1 / 1e3]


def _node_extent(d):
    x0, y1, res = float(d["x0"]), float(d["y1"]), float(d["res"])
    gx, gy = d["gx"], d["gy"]
    return [(x0 + gx.min() * res) / 1e3, (x0 + gx.max() * res) / 1e3,
            (y1 - gy.max() * res) / 1e3, (y1 - gy.min() * res) / 1e3]


def panel(ax, d, event, box=None, thumb=True, scalebar=True, title=None,
          grat_lon=2, grat_lat=0.5, label_fs=7):
    """Draw one event panel on ax. `event` is an id such as 'E010'."""
    if box is None:
        box = crop_box(d)
    xl, xr, yb, yt = box
    A = np.asarray(d["A"], np.float32); Bs = np.asarray(d["B"], np.float32)
    div = d["div"]; lab = d["lab"]
    ev_id = int(event[1:])

    # clip everything to the two-scene overlap: the panel shows the overlap and nothing else
    ring = np.array(d["overlap"].exterior.coords) / 1e3
    clip = PathPatch(MPath(ring), transform=ax.transData, facecolor="none", edgecolor="none")
    ax.add_patch(clip)

    m = np.isfinite(Bs)
    lo, hi = np.percentile(Bs[m], [2, 98]) if m.sum() > 100 else (-25, 5)
    im1 = ax.imshow(Bs, extent=_img_extent(d), cmap="gray", vmin=lo, vmax=hi,
                    origin="upper", interpolation="nearest", zorder=1)
    im1.set_clip_path(clip)

    ne = _node_extent(d)
    dv = np.where(np.isfinite(div), div, np.nan)
    im2 = ax.imshow(dv, extent=ne, cmap=F.DIV_CMAP, norm=DIV_NORM, origin="upper",
                    alpha=0.70, interpolation="nearest", zorder=2)
    im2.set_clip_path(clip)

    # component outline, drawn on the node grid
    mask = (lab == ev_id).astype(float)
    if mask.any():
        ny, nx = mask.shape
        xs = np.linspace(ne[0], ne[1], nx)
        ys = np.linspace(ne[3], ne[2], ny)
        for cs, col, lwv in ((None, "white", 1.9), (None, "black", 0.9)):
            c = ax.contour(xs, ys, mask, levels=[0.5], colors=col, linewidths=lwv, zorder=4)
            for coll in c.collections if hasattr(c, "collections") else [c]:
                try:
                    coll.set_clip_path(clip)
                except Exception:
                    pass

    for kind, val, gxs, gys in B.graticule((xl, xr), (yb, yt), grat_lon, grat_lat):
        ln, = ax.plot(gxs, gys, color="white", lw=0.35, alpha=0.75, zorder=3)
        ln.set_clip_path(clip)

    ax.plot(*np.array(d["overlap"].exterior.coords).T / 1e3, color=F.ACCENT, lw=0.7,
            ls=(0, (3, 2)), zorder=6)

    if scalebar:
        sx, sy = xl + 0.06 * (xr - xl), yb + 0.055 * (yt - yb)
        ax.plot([sx, sx + 50], [sy, sy], color="white", lw=2.6, solid_capstyle="butt", zorder=8)
        ax.plot([sx, sx + 50], [sy, sy], color="black", lw=1.4, solid_capstyle="butt", zorder=9)
        ax.text(sx + 25, sy + 0.022 * (yt - yb), "50 km", fontsize=label_fs, ha="center",
                va="bottom", color="black", zorder=9,
                path_effects=[pe.withStroke(linewidth=1.8, foreground="white")])

    if thumb:
        ins = ax.inset_axes([0.700, 0.688, 0.288, 0.288], zorder=10)
        ins.set_facecolor("white")
        ma = np.isfinite(A)
        alo, ahi = np.percentile(A[ma], [2, 98]) if ma.sum() > 100 else (-25, 5)
        ins.imshow(A, extent=_img_extent(d), cmap="gray", vmin=alo, vmax=ahi,
                   origin="upper", interpolation="nearest")
        ins.set_xlim(xl, xr); ins.set_ylim(yb, yt)
        ins.set_xticks([]); ins.set_yticks([])
        for sp in ins.spines.values():
            sp.set_color("0.15"); sp.set_linewidth(0.6)
        ins.text(0.5, 0.982, "before", transform=ins.transAxes, fontsize=label_fs,
                 color="black", ha="center", va="top",
                 path_effects=[pe.withStroke(linewidth=1.9, foreground="white")])
        iring = PathPatch(MPath(ring), transform=ins.transData, facecolor="none",
                          edgecolor="none")
        ins.add_patch(iring)
        for im in ins.images:
            im.set_clip_path(iring)

    ax.set_xlim(xl, xr); ax.set_ylim(yb, yt)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("0.4"); s.set_linewidth(0.5)
    if title:
        ax.set_title(title, fontsize=label_fs + 0.5, pad=2)
    return ax
