# LITERATURE_CLUSTERS — targets, seeds, and what was verified

Verification route: **Crossref** for all journal and conference items, **OpenLibrary** for the two books,
**arXiv** for preprints, and a live URL check for grey literature. **[P12] Semantic Scholar is now usable**:
`$S2_API_KEY` is set, and all 76 entries were re-verified through the authenticated
`graph/v1/paper` endpoints at one request per second with exponential backoff — 63 clean, 10 flagged and all
resolved in favour of the bibliography, 3 not indexed, and one real defect corrected (a truncated title on
`karvonen2022baltic`). See `scratch/P12/REF_VERIFY.md`. Raw responses are cached under `scratch/P12/s2cache/`
and the earlier unauthenticated attempts under `scratch/s2cache/`. Nothing here rests on an unverified identifier.

**[P12] Total verified: 78** against a target of 45 (76 plus the two cluster-8 additions below). Per-cluster detail is in `scratch/P11/clusters_1_4.md`,
`clusters_5_8.md` and `clusters_9_12.md`; the section mapping is in `paper/LITERATURE_MAP.md`.

| Cluster | Topic | Target | Verified | Status |
|---|---|---|---|---|
| 1 | Sentinel-1 mission, EW mode, Arctic acquisition | 3-4 | **5** | met |
| 2 | SAR-based sea-ice monitoring and ice-service operations | 5-6 | **12** | met |
| 3 | Sea-ice drift retrieval from SAR | 5-6 | **9** | met |
| 4 | Sea-ice deformation and buoy-based statistics | 5-6 | **8** | met |
| 5 | Navigation hazards, pressured ice, besetting, Polar Code | 5-6 | **7** | met |
| 6 | Observing-system experiments and network design | 4-5 | **5** | met |
| 7 | Passive-microwave drift products and coastal limits | 3-4 | **4** | met |
| 8 | Observation gaps propagating into products | 3 | **5** | met, **strictly** |
| 9 | Length-biased sampling and censored durations | 2-3 | **5** | met |
| 10 | Arctic shipping traffic and policy | 3-4 | **5** | met |
| 11 | Melt-season, noise-floor and incidence-angle limits of C-band | 3 | **6** | met |
| 12 | Deep-learning sea-ice classification and drift | 3 | **7** | met |

## Venue distribution

| Venue | Count | Target |
|---|---|---|
| Remote Sensing of Environment | 9 | >= 8 |
| IEEE TGRS | 6 | >= 6 |
| IEEE JSTARS | 5 | >= 4 |
| The Cryosphere | 13 | >= 6 |
| Annals/J. Glaciology | 2 | remainder |
| JGR Oceans | 7 | remainder |
| Marine Policy | 4 | remainder |
| Cold Reg. Sci. Technol. | 2 | remainder |
| ESSD | 1 | remainder |
| MDPI journal | 3 | <= 5 |
| other | 24 | remainder |

## Discarded and corrected seeds

The ESA **Sentinel-1B end-of-mission announcement** could not be verified as a citable record under any
phrasing tried and **no DOI was invented**; the constellation-gap statement rests instead on the observed
acquisition record and on `potin2019copernicus`. The **Kubat et al. 2016** seed is a conference paper
covering the Canadian Arctic and sub-Arctic generally, not a Hudson Strait journal article. **Ice-FMBench**
is dated 2025, not 2026. **[P12] The cluster-8 shortfall is closed.** The re-search with an authenticated Semantic Scholar key
(21 queries, `scratch/P12/novelty.py`) found two strict gap-quantification papers that the earlier
Crossref-and-arXiv pass had missed: `geiger2001resolution`, which quantifies how temporal and spatial
sampling propagates into derived drift and deformation, and `covington2022bridging`, which quantifies gaps
in a Lagrangian ice-floe record and recovers the missing dynamics. Both are added. `wuite2026velocity`,
`wulf2024panarctic` and `wulf2026decade` are retained but no longer carry the cluster's strict claim: their
abstracts were re-read in P12 and none documents the consequences of missing imagery, so the §1 sentence
citing them was rewritten to say only what they do — span the 2021 discontinuity as product records.
The original **InSAR acquisition-gap** seed was still not found and **no DOI was invented**. Grey literature
(IMO POLARIS circular, CHNL statistics, Bellona report) is recorded by live-retrieved URL and marked as such.
The two books (Feller, Cox) carry ISBNs read from OpenLibrary rather than DOIs.