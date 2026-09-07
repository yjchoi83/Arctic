# LITERATURE_CLUSTERS — targets, seeds, and what was verified

Verification route: **Crossref** for all journal and conference items, **OpenLibrary** for the two books,
**arXiv** for preprints, and a live URL check for grey literature. **Semantic Scholar was not usable**:
`$S2_API_KEY` is unset in the analysis environment and the unauthenticated `graph/v1/paper/search`
endpoint returned HTTP 429 on every attempt, including after 2 s / 4 s / 8 s exponential backoff.
All raw responses are cached under `scratch/s2cache/`. Nothing here rests on an unverified identifier.

**Total verified: 76** against a target of 45. Per-cluster detail is in `scratch/P11/clusters_1_4.md`,
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
| 8 | Observation gaps propagating into products | 3 | **3** | met |
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
is dated 2025, not 2026. The **InSAR acquisition-gap** seed for cluster 8 could not be found; that cluster
reaches its target of three only by counting a Sentinel-1 decade-scale velocity product paper, and if a
strict gap-quantification claim is required the cluster should be read as **verified 2**. Grey literature
(IMO POLARIS circular, CHNL statistics, Bellona report) is recorded by live-retrieved URL and marked as such.
The two books (Feller, Cox) carry ISBNs read from OpenLibrary rather than DOIs.