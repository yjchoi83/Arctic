# Hazard-timescale observability of Arctic shipping chokepoints — data and code deposit

Supporting dataset for the manuscript

> **Hazard-timescale observability of Arctic shipping chokepoints: what Sentinel-1 could and could not see**

## Citation

**The author line must be completed before deposit.** It is left blank here on purpose: this repository's
git identity (`yjchoi83`) is not a verified personal name, and a citation with a guessed author is worse than
one with an explicit gap. Fill in `[AUTHOR]` and, once Zenodo has minted it, the concept DOI.

```
[AUTHOR], 2026. Hazard-timescale observability of Arctic shipping chokepoints: what Sentinel-1
    could and could not see — data and code. Zenodo. https://doi.org/10.5281/zenodo.[ID]
```

BibTeX:

```bibtex
@dataset{arctic_observability_2026,
  author    = {[AUTHOR]},
  title     = {Hazard-timescale observability of Arctic shipping chokepoints:
               what Sentinel-1 could and could not see --- data and code},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.[ID]},
  url       = {https://github.com/yjchoi83/Arctic}
}
```

Cite the manuscript itself for the findings; cite this deposit for the gridded products and the code.

## What is here

| Folder | Contents |
|---|---|
| `products/` | 18 gridded observability rasters, GeoTIFF |
| `tables/` | 41 result tables and result documents from the analysis packages |
| `code/` | figure-generating and reference-rendering code |
| `MANIFEST.txt` | every file with its size and a sha256 prefix |

### `products/` — the gridded H fields

`H_{metric}_{season}_{period}.tif`, where metric is `episode3` or `state3` (the ≥ 3 km magnitude class),
season is `winter`, `melt` or `freeze-up`, and period is `pre2019-21`, `during2022-24` or `post2025-26`.
Two metrics × three seasons × three periods = 18 rasters.

- CRS **EPSG:3413** (NSIDC polar stereographic north), 25 km pixels, 178 × 161, `float32`, nodata `NaN`.
- Pixel value is **H**, the probability on 0–1 that a randomly occurring convergence hazard of the stated
  class overlaps at least one qualifying Sentinel-1 acquisition. 1 means every hazard is caught.
- Only the 1,771 cells of the sixteen study regions carry values; everything else is nodata.
- `H_episode` uses the convergence-episode duration; `H_state` uses hazard-state persistence. See §3.1 of the
  manuscript for the estimator and §6 for what H does not account for — in particular, **H is an upper bound**,
  because one acquisition inside a hazard window is counted as an observation whereas drift retrieval needs a
  pair.

### `tables/` — result tables

Flattened from the analysis packages, prefixed with the package that produced them (`P1_`, `P2_`, … `P9_`).
The CSVs are the machine-readable results; the `*_results.md` files are the per-package write-ups that state
what each column means and which claims rest on it. `paper/NUMBERS_TRACE.md` in the source repository maps
every number in the manuscript to a file here.

### `code/`

| File | Purpose |
|---|---|
| `p10_figs.py` | rebuilds every manuscript figure from the committed tables |
| `p13_fig03.py` | Figure 3 standalone, the merged H map panels |
| `p13_graphical_abstract.py` | the 1600 × 900 graphical abstract |
| `cells.py`, `regions.py` | region boxes and the 25 km cell grid, imported by the above |
| `bib.py`, `render_refs.py`, `make_rse.py` | render the reference list into `MANUSCRIPT_RSE.md` |
| `p13_zenodo.py` | rebuilds this deposit folder and its manifest |

Run from the repository root, not from inside this folder: the scripts set their own working directory and
read the untracked working data under `arctic_explore/scratch/`, which is regenerable by the pipeline recorded
in `paper/NUMBERS_TRACE.md` but is not part of this deposit.

## Provenance of the inputs

Sentinel-1 acquisition metadata via the Copernicus programme; International Arctic Buoy Programme Level 1
archive; EUMETSAT OSI SAF OSI-405; Copernicus Marine `cmems_obs-si_glo_phy-drift-north_my_l4_P1D-m` and
`cmems_obs-si_arc_phy_my_l3_P1D`; ESA acquisition-segment archives from the Copernicus SentiWiki document
library; Norwegian Meteorological Institute ice-chart quicklook archive. No third-party data are
redistributed here — only derived products and code.

## Licence

Proposed: **CC BY 4.0** for `products/` and `tables/`, **MIT** for `code/`. Confirm before deposit.

## Note on duplication

`products/` is copied from `arctic_explore/data/products/` and `tables/` from `arctic_explore/stage5/`.
This folder is a packaging convenience; the source tree remains authoritative. Rebuild with
`python3 scratch/P13/p13_zenodo.py`.
