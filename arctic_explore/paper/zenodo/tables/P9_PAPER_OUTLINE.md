# PAPER_OUTLINE — Arctic SAR observability
**Target: Remote Sensing of Environment (RSE). Fallback: Cold Regions Science and Technology (CRST).**

## Title
**Hazard-timescale observability of Arctic shipping chokepoints: Sentinel-1 never met the requirement, the 2022–2024
constellation gap widened it, and the shortfall propagated into an operational drift product**

## Abstract (draft, 251 words)
Synthetic aperture radar underpins Arctic navigation support, yet observing capability is normally reported as scene
counts or revisit intervals, which say nothing about whether a hazard is actually caught. We define a hazard-timescale
observability metric, H, as the probability that a randomly occurring convergence event overlaps at least one
acquisition, given the length-biased distribution of acquisition gaps and an independently measured hazard-duration
distribution. Hazard durations come from 82,439 convergence events derived from 2016–2025 IABP buoy pairs; acquisition
gaps come from Sentinel-1 metadata for 1,771 25-km cells across sixteen Arctic regions, 2016–2026. At Northern Sea Route
chokepoints, H for episode-scale hazards was 0.200 before the loss of Sentinel-1B and fell to 0.097 in 2022–2024; the
12-hour episode requirement implied by the buoy record was never met in any of 688 region-season-year cells, and no
chokepoint ever reached the 24-hour state requirement. A remove-one-platform counterfactual reproduces the observed
2022–2024 collapse within 10 percentage points in 15 of 16 regions, so the gap is explained by satellite count; the
incomplete recovery is not. Annual scene volume returned to 88.5 % with three platforms, but ESA acquisition-segment
plans allocate 86 % of pre-loss coverage to the European–Russian sector versus 122 % to North America, and the deficit
persists after controlling for Sentinel-1C ramp-up. Availability of the Copernicus DTU Sentinel-1 drift product tracks
H across region-years (Spearman rho = 0.71). Twenty Sentinel-1 pairs demonstrate that chokepoint convergence is
retrievable in winter and freeze-up, so the hazards are observable in principle and are being missed in practice.

## Sections and the figure/table each uses
1. **Introduction** — observing capability vs. hazard capture; why revisit interval is the wrong measurand.
2. **Data** — Sentinel-1 metadata (Table 1: regions, cells, period); IABP 2016–2025; OSI SAF OSI-405;
   DTU S1 drift; ESA acquisition segments; MET Norway charts. *(Table 1)*
3. **The H metric** — derivation `H = E_D[Σ min(g_i, D)]/Σ g_i`; assumptions and their failure modes. *(Fig. 1 schematic)*
4. **Hazard timescales from buoys** — duration and persistence by magnitude class and season; the detection floor.
   *(Fig. 2 duration/persistence distributions; Table 2 P1b class table)*
5. **Observability 2016–2026** — H per cell, pre/during/post × season. *(Fig. 3 = `H_state3_*.png`, `H_episode3_*.png`;
   Table 3 = `P3_region_season_year.csv`)*
6. **Counterfactual and constellation design** — OSE, H6, design curve. *(Fig. 4 design curve; Table 4 OSE)*
7. **Planned vs acquired, and the recovery deficit** — *(Fig. 5 = `planned_vs_acquired.png`; Table 5 = `planned_vs.csv`)*
8. **Consequence in an operational product** — DTU availability vs H, threshold sensitivity.
   *(Fig. 6 = `dtu_availability.png`; Table 6 = `h9_sensitivity.csv`)*
9. **Physical demonstration at the chokepoints** — 20 pairs, matcher, divergence, events, magnitude reconciliation.
   *(Fig. 7 = `example_E*.png`; Fig. 8 = `contact_sheet_events.png`; Table 7 = `qc_table_p9.csv`)*
10. **Discussion** — what a constellation cannot fix; where the bottleneck is retrieval, not observation.
11. **Limitations** (see below) — **12. Conclusions**.

## The six claims, evidence, and caveats
| # | Claim | Evidence | Caveat carried in the text |
|---|---|---|---|
| C1 | The requirement was **never met** at NSR chokepoints, even before the loss | O(12 h) < 0.5 in **688/688** cells (max 0.278); chokepoint H_episode 0.200 pre; no chokepoint reached 0.8 for the 24 h state requirement | Requirement thresholds derive from the buoy record, not from an operator's stated need |
| C2 | The 2022–2024 loss **widened an existing gap** | chokepoint H_episode 0.200 → **0.097**; H_state 0.504 → 0.363; all-region 0.267 → 0.151 | Region-level DiD is **not estimable** — no untreated control exists (all 16 regions retention < 0.9) |
| C3 | Chokepoint hazards are **real and S1-observable**; low-resolution products cannot resolve them | OSI SAF 62.5 km: **Vilkitsky 0 valid retrievals in 10 y**; S1: 20/20 pairs ≥30 vectors, mean success **0.510**, 19 events | Events are detected, **not validated** — no IABP buoy within 100 km of any of the 19 |
| C4 | Recovery is incomplete because of **allocation**, not satellite count | ramp-up-controlled EUR **77.4 %** vs NAM **121.1 %**; ESA plans EUR **86.4 %** vs NAM **122.3 %** | Narrowed to the **Barents–Kara–Laptev** sub-sector: Vilkitsky is planned at 146 % and acquired at 156 % |
| C5 | The chokepoint requirement is **not attainable** by adding satellites | design curve 1→2 sat +0.13, 2→3 **+0.05**; chokepoint max **0.72** with 3; 16/800 combinations reach 0.8 | Satellite count is confounded with orbit plane; S1C/S1D were still ramping |
| C6 | The shortfall **propagated into an operational product** | DTU S1-drift availability vs H: rho **0.711** (region-year), **0.736** vs H_episode, within-region median **0.727**; robust at 2/5/10 % thresholds | **DTU is derived from Sentinel-1** — a shared-archive relation, not independent confirmation |

## Limitations (dedicated section — none of these may be dropped)
1. **Buoy-to-strait extrapolation.** Hazard durations come from IABP pairs whose network is central-Arctic biased;
   applying that distribution to Vilkitsky/Sannikov/Long Strait is extrapolation, not measurement.
2. **Magnitude-class mismatch.** The S1 event metric uses √area (median 12.2 km) as its baseline, the buoy metric uses
   pair separation (median 49.4 km); they differ by that ratio (0.248). P9 reconciles them with virtual buoy pairs —
   applying the buoy rate threshold to S1 fields yields median 5.9 km closure in 0.50 % of pairs — but the two samples
   are selected differently, and S1's 24–48 h windows time-average the 2–12 h episodes of interest.
3. **Shared-archive dependence.** C6 relates two quantities derived from the same Sentinel-1 archive. No
   Sentinel-1-independent product was reachable: OSI SAF SAR drift does not exist, MET Norway charts are issued on a
   fixed schedule (248/253/251/250 days in 2019/2021/2023/2025, i.e. unchanged through the gap).
4. **KML plans vs acquired scenes.** Acquisition-segment KMLs are *planned datatakes*; they do not guarantee execution
   or downlink. Plans for 2022–2024 were not retrieved, so the planned comparison is pre vs post only.
5. **S1D ramp-up.** S1D first appears 2026-04 with six months of data and no established plateau; the three-satellite
   window covers only melt-season months, so it does not represent routine three-satellite operations.
6. **H is an upper bound.** A single acquisition is counted as an observation, but drift retrieval needs a pair.
   Multiplying by measured retrieval success gives E ≈ 0.18–0.28 (winter), 0.006–0.009 (melt); freeze-up success was
   measured at **0.394** in P8, so P5's 0.47 substitution was ~19 % optimistic.
7. **Cell bootstrap CIs are too narrow** — cells within a region share orbits and are not independent.
8. **Small events need shorter revisit than the headline requirement.** For the 1–3 km class the duration is 2–4 h and
   H falls to **0.029** during 2022–2024; the 12 h requirement is itself a relaxed, ≥3 km-class figure.

## Author to-do before submission
Re-run the novelty search with a Semantic Scholar API key (unavailable in-session; Stage 4 rested on Crossref + arXiv).
Human adjudication of `contact_sheet_events.png` (decision column blank). Decide whether C3's unvalidated events are
presented as a demonstration or moved to an appendix.
