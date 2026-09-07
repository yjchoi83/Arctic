# Supplementary material

Companion to `paper/MANUSCRIPT.md`. Provenance for every value is in `paper/NUMBERS_TRACE.md`.

## Supplementary Figure S1. H_state maps

**Figure S1.** H_state per 25 km cell on EPSG:3413, for the ≥ 3 km magnitude class, by season (rows)
and period (columns), on the same Natural Earth 50 m coastline, land fill and graticule as Figure 3(b),
with the five-region chokepoint group outlined. Colour is viridis from 0 to 1, where 1 means every
hazard is caught, and the 0.8 requirement is marked on the scale. This is the state-metric companion to
the main-text H_episode maps of Figure 3(b); the two are also tabulated cell by cell in Figure 4.
`figS1_H_state_maps.png`

## Supplementary Table S1. Sentinel-1 pair-processing and matcher parameters

Parameters of the two-stage ice-motion matcher of Section 3.6, and of the pair selection and event
definition that surround it. Values are those used earlier in this work for a Chukchi melt-versus-winter
comparison and were **not retuned per season or per strait**. The scheme is a reimplementation of the
two-stage design of Korosov and Rampal (2017) and is not claimed to be identical to the `sea_ice_drift`
package, which is not distributed through the Python Package Index.

| Stage | Parameter | Value |
|---|---|---|
| Pair selection | mode / product | Extra Wide, ground-range-detected |
| | acquisition separation | 12–72 h |
| | footprint overlap | ≥ 50 % of the smaller scene, computed in EPSG:3413 |
| | region-box coverage, each scene | ≥ 30 % |
| | balancing | round-robin across the six region-season combinations |
| Radiometry | band | HH |
| | across-track gradient | divided by the per-column median, expressed in relative dB |
| Geometry | reprojection source | scene ground-control points |
| | common grid | 200 m, EPSG:3413, region box with a 60 km margin |
| Stage 1, feature tracking | detector / descriptor | oriented FAST and rotated BRIEF (ORB) |
| | image decimation | 4× |
| | matching | Hamming distance with a ratio test |
| | outlier rejection | median absolute deviation on the displacement field |
| Stage 2, pattern matching | node grid | 5 km |
| | template size | 25 pixels |
| | search window | ± 10 km about the stage-1 prediction |
| | initialisation | stage-1 coarse displacement field |
| Node acceptance | correlation peak | ≥ 0.40 |
| | peak to next highest local maximum | ≥ 1.20 |
| | displacement magnitude | ≤ 80 % of the search radius |
| Node attempted (success-rate denominator) | template validity, image 1 | fully within valid data |
| | search-window validity, image 2 | ≥ 90 % valid |
| | template contrast | standard deviation > 0.3 dB |
| Derived fields | velocity units | km d⁻¹; northing sign inverted relative to pixel row index |
| | divergence | centred differences on the 5 km node grid |
| Candidate events | threshold | divergence below the 10th percentile of that pair's own distribution (relative, not absolute strain) |
| | minimum area | 100 km² |
| | magnitude scale | square root of component area (see Section 3.3) |
| | edge audit | flagged edge-suspect if > 50 % of nodes lie within 5 km of the two-scene overlap boundary (Appendix A) |
| Virtual buoy pairs | separation band | 20–100 km, matching the real-buoy band of Section 3.2 |
| | sampling | random node pairs on the accepted-node fields |
| | count | 240,949 pairs across the twenty windows |
| | rate threshold applied | 4.706 km d⁻¹, from the one-hourly buoy archive (Section 3.2) |

## Supplementary Note S1. Bibliography verification

All in-text citations resolve to keys in `paper/references.bib`, which holds **76 entries, every one verified
in-session** by retrieval of its DOI through Crossref, by OpenLibrary for the two books, by arXiv for the one
preprint, or by a live URL check for the two grey-literature items (the IMO POLARIS circular and the Bellona
report), which carry no DOI and are marked as such. Nothing in the bibliography rests on an unverified
identifier, and no DOI was inferred or constructed. Rendering the list for submission (Section *Data
availability*) confirmed that **all 74 in-text citation instances resolve to a key**, and removed two duplicate
keys that pointed at the DOIs already present under another key.

The 76 entries standing before this package were subsequently **re-verified against an authenticated Semantic Scholar search** (`x-api-key`,
one request per second, exponential backoff). Sixty-three matched without qualification. Ten were flagged and all
ten resolve in favour of the bibliography: six are Semantic Scholar recording the Copernicus discussion-paper or
online-first year rather than the year of record, each settled against Crossref `issued`; three are index defects
on the two books and on the Kaplan–Meier paper, for which the bibliography carries the better identifier; one was
an author-string split. Three are not indexed at all, being the two grey-literature items and, at the time of the
run, the arXiv preprint, which has since been resolved by identifier. **One real defect was found and corrected**:
the title of `karvonen2022baltic` was truncated and now reads in full. The audit is recorded in
`scratch/P12/REF_VERIFY.md`.

Cluster composition, per-cluster targets and the section in which each cluster is cited are given in
`paper/LITERATURE_CLUSTERS.md` and `paper/LITERATURE_MAP.md`. Rendering instructions for the two journal styles
are in `paper/build.md`.
