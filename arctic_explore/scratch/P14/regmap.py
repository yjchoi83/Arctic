"""ARC-P14: region-box geometry on EPSG:3413, shared by the Figure 3 panels."""
import sys, os
import numpy as np
from pyproj import Transformer

A = "/d/yj_projects/workspace_yj/Arctic/arctic_explore"
sys.path.insert(0, os.path.join(A, "scratch/P2"))
sys.path.insert(0, os.path.join(A, "scratch/P3"))
from regions import regions          # noqa: E402
from cells import region_cells, CELL  # noqa: E402

FWD = Transformer.from_crs("EPSG:4326", "EPSG:3413", always_xy=True)
R = regions()
RC = region_cells()

CH = ["KaraGate", "Vilkitsky", "Sannikov_DmLaptev", "LongStrait", "BeringChukchi"]
CHSET = set(CH)
AK = [f"AKcorr_{i}" for i in range(1, 7)]
CONTRAST = ["Barents_Svalbard", "GreenlandSea_Fram", "BaffinBay", "LancasterSound",
            "VictoriaStrait"]
ORDER = CH + AK + CONTRAST

NAME = {"KaraGate": "Kara Gate", "Vilkitsky": "Vilkitsky", "Sannikov_DmLaptev": "Sannikov / Dm. Laptev",
        "LongStrait": "Long Strait", "BeringChukchi": "Bering–Chukchi",
        "Barents_Svalbard": "Barents / Svalbard", "GreenlandSea_Fram": "Greenland Sea / Fram",
        "BaffinBay": "Baffin Bay", "LancasterSound": "Lancaster Sound",
        "VictoriaStrait": "Victoria Strait",
        **{f"AKcorr_{i}": f"AK{i}" for i in range(1, 7)}}
SHORT = {"KaraGate": "KG", "Vilkitsky": "VS", "Sannikov_DmLaptev": "SD", "LongStrait": "LS",
         "BeringChukchi": "BC"}


def box_xy(region, n=80):
    """Region box outline in km, EPSG:3413, edges densified so the projection is honest."""
    w, e, s, nn = R[region]
    lo = np.concatenate([np.linspace(w, e, n), np.full(n, e), np.linspace(e, w, n), np.full(n, w)])
    la = np.concatenate([np.full(n, s), np.linspace(s, nn, n), np.full(n, nn), np.linspace(nn, s, n)])
    x, y = FWD.transform(lo, la)
    return x / 1e3, y / 1e3


def centroid(region):
    x, y = box_xy(region)
    return float(x.mean()), float(y.mean())


def cell_xy(region):
    a = np.array(RC[region], float)
    return a[:, 0] / 1e3, a[:, 1] / 1e3


def region_extent(region, pad_km=40):
    x, y = cell_xy(region)
    c = CELL / 1e3
    return (x.min() - pad_km, x.max() + c + pad_km), (y.min() - pad_km, y.max() + c + pad_km)


def all_extent(pad_km=0):
    xs, ys = [], []
    for r in ORDER:
        x, y = box_xy(r)
        xs += [x.min(), x.max()]; ys += [y.min(), y.max()]
    return (min(xs) - pad_km, max(xs) + pad_km), (min(ys) - pad_km, max(ys) + pad_km)
