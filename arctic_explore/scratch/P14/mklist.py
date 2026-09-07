"""ARC-P14 item 9: write paper/figures/FIGURE_LIST.md from the figures on disk and the
captions in MANUSCRIPT.md / SUPPLEMENTARY.md."""
import re, pathlib
from PIL import Image

A = pathlib.Path("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
FIGDIR = A / "paper/figures"
DPI = 300

ORDER = [
    ("1",  ["fig01_H_schematic.png"],       "MANUSCRIPT.md", "**Figure 1.**",  "—"),
    ("2",  ["fig02_hazard_timescales.png"], "MANUSCRIPT.md", "**Figure 2.**",  "—"),
    ("3",  ["fig03a_overview.png", "fig03b_H_episode_maps.png", "fig03c_chokepoint_strip.png"],
                                            "MANUSCRIPT.md", "**Figure 3.**",  "3, rebuilt"),
    ("4",  ["fig04_H_heatmap.png"],         "MANUSCRIPT.md", "**Figure 4.**",  "new in P14"),
    ("5",  ["fig05_virtual_pairs.png"],     "MANUSCRIPT.md", "**Figure 5.**",  "4"),
    ("6",  ["fig06_strait_examples.png"],   "MANUSCRIPT.md", "**Figure 6.**",  "5"),
    ("7",  ["fig07_design_curve.png"],      "MANUSCRIPT.md", "**Figure 7.**",  "6"),
    ("8",  ["fig08_planned_vs_acquired.png"], "MANUSCRIPT.md", "**Figure 8.**", "7"),
    ("9",  ["fig09_dtu_availability.png"],  "MANUSCRIPT.md", "**Figure 9.**",  "8"),
    ("A1", ["figA1_contact_sheet.png"],     "MANUSCRIPT.md", "**Figure A1.**", "A1"),
    ("S1", ["figS1_H_state_maps.png"],      "SUPPLEMENTARY.md", "**Figure S1.**", "part of 3"),
]
SRC = {f: (A / "paper" / f).read_text() for f in {o[2] for o in ORDER}}


def first_sentence(doc, marker):
    line = [l for l in SRC[doc].split("\n") if l.startswith(marker)][0]
    body = re.sub(r"\*\*|`", "", line[len(marker):].strip())
    m = re.search(r"(?<=[a-z0-9)%²⁻¹])\.\s", body + " ")
    return (body[:m.end() - 1] if m else body).strip()


rows, total = [], 0.0
for num, files, doc, marker, was in ORDER:
    s1 = first_sentence(doc, marker)
    for k, f in enumerate(files):
        path = FIGDIR / f
        px = Image.open(path).size
        mm = (px[0] / DPI * 25.4, px[1] / DPI * 25.4)
        kb = path.stat().st_size / 1024
        total += kb
        col = "single" if round(mm[0]) == 90 else ("double" if round(mm[0]) == 190 else "?")
        rows.append((f"{num}{'abc'[k] if len(files) > 1 else ''}", f, px, mm, col, kb,
                     s1 if k == 0 else "″", was if k == 0 else ""))

out = ["# FIGURE_LIST — ARC-P14", "",
       "Every figure is PNG at **300 dpi**, width exactly **90 mm** (single column) or **190 mm** "
       "(double column), one font family (DejaVu Sans for text and mathtext), all text **≥ 7 pt at "
       "print size**, viridis for H, and a single diverging map (RdBu, negative = convergence) for "
       "divergence.", "",
       "Enforced mechanically rather than by eye: `scratch/P14/figstyle.py` asserts the saved pixel "
       "width against the target and refuses to write a figure containing any text below 7 pt. Widths "
       "are exact because no figure is saved with `bbox_inches=\"tight\"`, which would re-crop it.", "",
       "| Fig. | File | Pixels | Size (mm) | Column | kB | Caption, first sentence |",
       "|---|---|---|---|---|---|---|"]
for num, f, px, mm, col, kb, s1, was in rows:
    out.append(f"| {num} | `{f}` | {px[0]} × {px[1]} | {mm[0]:.0f} × {mm[1]:.0f} | {col} | "
               f"{kb:.0f} | {s1} |")
out += ["", f"**{len(rows)} files, {total/1024:.1f} MB total.**", "",
        "## Numbering change in P14", "",
        "Figure 4 is new — the H heatmap — and it belongs in §4.2, so the figures after it are "
        "renumbered to keep citation order:", "",
        "| New | Was | File then → now |", "|---|---|---|",
        "| 3 | 3 | `fig03_H_maps.png` → `fig03a_overview.png`, `fig03b_H_episode_maps.png`, `fig03c_chokepoint_strip.png` |",
        "| 4 | — (new) | — → `fig04_H_heatmap.png` |",
        "| 5 | 4 | `fig04_virtual_pairs.png` → `fig05_virtual_pairs.png` |",
        "| 6 | 5 | `fig05_strait_examples.png` → `fig06_strait_examples.png` |",
        "| 7 | 6 | `fig06_design_curve.png` → `fig07_design_curve.png` |",
        "| 8 | 7 | `fig07_planned_vs_acquired.png` → `fig08_planned_vs_acquired.png` |",
        "| 9 | 8 | `fig08_dtu_availability.png` → `fig09_dtu_availability.png` |",
        "| S1 | part of 3 | `fig03_H_state3_maps.png` → `figS1_H_state_maps.png` |",
        "",
        "Figures 1, 2 and A1 keep their numbers. Every in-text reference and caption in "
        "`MANUSCRIPT.md` and `SUPPLEMENTARY.md` was updated to match.", "",
        "## Regeneration", "",
        "    python3 scratch/P14/f01.py            # Fig. 1",
        "    python3 scratch/P14/f02.py            # Fig. 2",
        "    python3 scratch/P14/f03a.py           # Fig. 3(a)",
        "    python3 scratch/P14/f03b.py           # Fig. 3(b)",
        "    python3 scratch/P14/f03b.py --state   # Fig. S1",
        "    python3 scratch/P14/f03c.py           # Fig. 3(c)",
        "    python3 scratch/P14/f04.py            # Fig. 4",
        "    python3 scratch/P14/f05.py            # Fig. 5",
        "    python3 scratch/P14/f06.py            # Fig. 6",
        "    python3 scratch/P14/f07.py            # Fig. 7",
        "    python3 scratch/P14/f08.py            # Fig. 8",
        "    python3 scratch/P14/f09.py            # Fig. 9",
        "    python3 scratch/P14/fA1.py            # Fig. A1",
        "    python3 scratch/P14/mklist.py         # this file",
        "",
        "Figures 6 and A1 read `scratch/P14/fields/`, rebuilt by `scratch/P14/p14_fields.py` from the "
        "forty Sentinel-1 scenes in `scratch/P8/s1/` and the tracked node fields in "
        "`scratch/P9/fields/`; it reproduces the nineteen events and their overlap areas exactly. "
        "Shared modules: `figstyle.py` (style plus the width and font assertions), `basemap.py` "
        "(Natural Earth 50 m land and coastline, cached in `scratch/P14/ne/`), `regmap.py` (region "
        "boxes and cells), `straitpanel.py` (the Figure 6 and A1 panel).", ""]
(FIGDIR / "FIGURE_LIST.md").write_text("\n".join(out))
print("\n".join(out[8:23]))
print(f"\n{len(rows)} files, {total/1024:.1f} MB")
