"""ARC-P14 shared figure style.

Submission constraints enforced here, not left to each script:
  * 300 dpi
  * width exactly 90 mm (single column) or 190 mm (double column)
  * every text element >= 7 pt at print size
  * one font family (DejaVu Sans) for text AND mathtext
  * viridis for H

Because the width must be exact, `save()` never uses bbox_inches="tight" — that would
re-crop and change the width. Lay panels out with add_axes / GridSpec instead.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image

DPI = 300
MM = 1.0 / 25.4
W1 = 90 * MM          # single column, inches
W2 = 190 * MM         # double column, inches
MIN_PT = 7.0

H_CMAP = "viridis"
H_NORM = Normalize(0, 1)
DIV_CMAP = "RdBu_r"        # diverging, colour-blind safe, no red-green pairing
ACCENT = "#d95f02"         # single accent: requirement lines, hazards
GREY = "0.35"

OUT = "/d/yj_projects/workspace_yj/Arctic/arctic_explore/paper/figures"

BASE = {
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "mathtext.fontset": "dejavusans",
    "font.size": 7.5,
    "axes.titlesize": 8,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.size": 2.0,
    "ytick.major.size": 2.0,
    "lines.linewidth": 1.0,
    "patch.linewidth": 0.5,
    "legend.frameon": False,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
}


def use():
    plt.rcParams.update(BASE)


def figure(width_in, height_in):
    use()
    return plt.figure(figsize=(width_in, height_in), dpi=DPI)


def _texts(fig):
    out = list(fig.texts)
    for ax in fig.axes:
        out += [ax.title, ax.xaxis.label, ax.yaxis.label]
        out += list(ax.texts) + list(ax.get_xticklabels()) + list(ax.get_yticklabels())
        lg = ax.get_legend()
        if lg is not None:
            out += lg.get_texts() + ([lg.get_title()] if lg.get_title() else [])
    return [t for t in out if t is not None and t.get_text().strip()]


def check(fig, target_width_in):
    """Assert every visible text is >= MIN_PT and the figure width is the target."""
    small = sorted({(round(t.get_fontsize(), 2), t.get_text()[:32].replace("\n", " "))
                    for t in _texts(fig) if t.get_fontsize() < MIN_PT})
    if small:
        raise AssertionError(f"{len(small)} text elements below {MIN_PT} pt: {small[:8]}")
    w = fig.get_size_inches()[0]
    assert abs(w - target_width_in) < 1e-6, f"width {w:.5f} in, expected {target_width_in:.5f}"


def save(fig, name, target_width_in):
    check(fig, target_width_in)
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    px = Image.open(path).size
    want = round(target_width_in * DPI)
    assert abs(px[0] - want) <= 1, f"{name}: {px[0]} px wide, expected {want}"
    mm = px[0] / DPI * 25.4
    print(f"  {name:38s} {px[0]:5d} x {px[1]:5d} px  {mm:5.1f} mm @ {DPI} dpi  "
          f"{os.path.getsize(path)/1024:6.0f} kB")
    return path
