# FIGURE_LIST — ARC-P14

Every figure is PNG at **300 dpi**, width exactly **90 mm** (single column) or **190 mm** (double column), one font family (DejaVu Sans for text and mathtext), all text **≥ 7 pt at print size**, viridis for H, and a single diverging map (RdBu, negative = convergence) for divergence.

Enforced mechanically rather than by eye: `scratch/P14/figstyle.py` asserts the saved pixel width against the target and refuses to write a figure containing any text below 7 pt. Widths are exact because no figure is saved with `bbox_inches="tight"`, which would re-crop it.

| Fig. | File | Pixels | Size (mm) | Column | kB | Caption, first sentence |
|---|---|---|---|---|---|---|
| 1 | `fig01_H_schematic.png` | 2244 × 765 | 190 × 65 | double | 137 | Construction of the observability metric H. (a) A sequence of acquisitions defines gaps g_i. |
| 2 | `fig02_hazard_timescales.png` | 2244 × 825 | 190 × 70 | double | 158 | Hazard timescales measured from buoy pairs, independent of Sentinel-1. |
| 3a | `fig03a_overview.png` | 2244 × 1443 | 190 × 122 | double | 651 | Observability across the study domain, for the ≥ 3 km magnitude class. |
| 3b | `fig03b_H_episode_maps.png` | 2244 × 2302 | 190 × 195 | double | 1590 | ″ |
| 3c | `fig03c_chokepoint_strip.png` | 1062 × 1875 | 90 × 159 | single | 385 | ″ |
| 4 | `fig04_H_heatmap.png` | 2244 × 1876 | 190 × 159 | double | 517 | H by region and season-period, values printed in each cell. |
| 5 | `fig05_virtual_pairs.png` | 1062 × 975 | 90 × 83 | single | 110 | Strait drift fields expressed in the buoy-pair metric. |
| 6 | `fig06_strait_examples.png` | 2244 × 2467 | 190 × 209 | double | 4359 | Retrieved divergence fields at two straits, for four of the nineteen candidate convergence components of Appendix A: E002 and E001 at Vilkitsky on 5 January 2019, 125 km² each, and E011 and E010 at Sannikov on 13 January 2019, 100 and 400 km². |
| 7 | `fig07_design_curve.png` | 2244 × 765 | 190 × 65 | double | 137 | Constellation design curve within matched season windows, one panel per season. |
| 8 | `fig08_planned_vs_acquired.png` | 2244 × 1065 | 190 × 90 | double | 129 | European Space Agency planned acquisition segments against acquired scenes, per region, on a logarithmic axis. |
| 9 | `fig09_dtu_availability.png` | 1062 × 945 | 90 × 80 | single | 105 | Availability of the DTU Sentinel-1 drift product per region-year, defined as the fraction of days with at least 5 % valid pixels; chokepoint-group regions in bold red. |
| A1 | `figA1_contact_sheet.png` | 2244 × 2909 | 190 × 246 | double | 5722 | Contact sheet of the nineteen candidate strait convergence events, for human adjudication; the decision box on each panel is deliberately blank, as is the decision column of the accompanying table. |
| S1 | `figS1_H_state_maps.png` | 2244 × 2302 | 190 × 195 | double | 1593 | H_state per 25 km cell on EPSG:3413, for the ≥ 3 km magnitude class, by season (rows) |

**13 files, 15.2 MB total.**

## Numbering change in P14

Figure 4 is new — the H heatmap — and it belongs in §4.2, so the figures after it are renumbered to keep citation order:

| New | Was | File then → now |
|---|---|---|
| 3 | 3 | `fig03_H_maps.png` → `fig03a_overview.png`, `fig03b_H_episode_maps.png`, `fig03c_chokepoint_strip.png` |
| 4 | — (new) | — → `fig04_H_heatmap.png` |
| 5 | 4 | `fig04_virtual_pairs.png` → `fig05_virtual_pairs.png` |
| 6 | 5 | `fig05_strait_examples.png` → `fig06_strait_examples.png` |
| 7 | 6 | `fig06_design_curve.png` → `fig07_design_curve.png` |
| 8 | 7 | `fig07_planned_vs_acquired.png` → `fig08_planned_vs_acquired.png` |
| 9 | 8 | `fig08_dtu_availability.png` → `fig09_dtu_availability.png` |
| S1 | part of 3 | `fig03_H_state3_maps.png` → `figS1_H_state_maps.png` |

Figures 1, 2 and A1 keep their numbers. Every in-text reference and caption in `MANUSCRIPT.md` and `SUPPLEMENTARY.md` was updated to match.

## Regeneration

    python3 scratch/P14/f01.py            # Fig. 1
    python3 scratch/P14/f02.py            # Fig. 2
    python3 scratch/P14/f03a.py           # Fig. 3(a)
    python3 scratch/P14/f03b.py           # Fig. 3(b)
    python3 scratch/P14/f03b.py --state   # Fig. S1
    python3 scratch/P14/f03c.py           # Fig. 3(c)
    python3 scratch/P14/f04.py            # Fig. 4
    python3 scratch/P14/f05.py            # Fig. 5
    python3 scratch/P14/f06.py            # Fig. 6
    python3 scratch/P14/f07.py            # Fig. 7
    python3 scratch/P14/f08.py            # Fig. 8
    python3 scratch/P14/f09.py            # Fig. 9
    python3 scratch/P14/fA1.py            # Fig. A1
    python3 scratch/P14/mklist.py         # this file

Figures 6 and A1 read `scratch/P14/fields/`, rebuilt by `scratch/P14/p14_fields.py` from the forty Sentinel-1 scenes in `scratch/P8/s1/` and the tracked node fields in `scratch/P9/fields/`; it reproduces the nineteen events and their overlap areas exactly. Shared modules: `figstyle.py` (style plus the width and font assertions), `basemap.py` (Natural Earth 50 m land and coastline, cached in `scratch/P14/ne/`), `regmap.py` (region boxes and cells), `straitpanel.py` (the Figure 6 and A1 panel).
