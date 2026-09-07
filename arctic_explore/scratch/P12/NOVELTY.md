# ARC-P12 item 9a/9b — authenticated Semantic Scholar novelty and cluster-8 re-search

Authenticated `graph/v1/paper/search` (`x-api-key`, ≤ 1 req/s, exponential backoff to 90 s). 21 queries,
`scratch/P12/novelty.py`; raw hits in `scratch/P12/novelty_raw.json`; run log `scratch/P12/novelty.log`.
Unique titles returned: 42 for the metric framing, 57 for the Sentinel-1B gap, 62 for plan allocation,
91 for cluster 8.

## 9a — does any paper overlap a core claim?

**No.** All three framing claims survive.

| Core claim | Nearest indexed work | Why it does not overlap |
|---|---|---|
| A hazard-timescale observability metric H: the probability a randomly occurring hazard overlaps ≥ 1 acquisition, given the length-biased gap distribution and a measured duration distribution | Geiger and Drinkwater (2001), *Impact of Temporal-Spatio Resolution on Sea-Ice Drift and Deformation*; Kaminski et al. (2015, 2018) Arctic Mission Benefit Analysis | Geiger and Drinkwater quantify how sampling resolution degrades a *retrieved field*, not the probability that an *event* is caught; Kaminski et al. score product impact on forecast skill, with no hazard-duration distribution and no gap-length biasing. Both are cited. |
| The Sentinel-1B loss and the incomplete recovery are separable, and the 2022–2024 period is explained by platform count | Potin et al., *Copernicus Sentinel-1 Constellation Mission Operations Status* (2019); Howell et al. (2022) on Sentinel-1 + RCM motion | Mission-status papers predate the failure and report capacity, not consequence. Nothing in the index treats the Sentinel-1B failure as a measured shock to observing capability. |
| The 2025–2026 shortfall is an allocation decision visible in the acquisition plans before execution | *Sentinel-1A observation scenario simulations — Initial operations phase* (IGARSS 2014); *Sentinel-1 Mission operations concept* (IGARSS 2012); TerraSAR-X strategic mission planning (2004); *A Multi-Objective Modeling Method of Multi-Satellite Imaging Task Planning* (2020) | These describe planning *systems and simulators*, and the optimisation literature designs schedules. None audits a published plan archive against the acquired archive to expose a regional allocation asymmetry. |

Nothing found that reports a probability-of-catching metric, a Sentinel-1B consequence quantification, or a
plan-versus-acquired regional audit. **No claim in the manuscript needs weakening on novelty grounds.** The
bound is the usual one: a negative search constrains what the index holds, not what exists.

## 9b — cluster 8, strict gap-quantification

The earlier pass recorded cluster 8 as reaching three entries "only by counting a Sentinel-1 decade-scale
velocity product paper", and as **verified 2** on a strict reading. Two genuinely strict papers were found and
both are now in the bibliography.

| Added | Why it is strict |
|---|---|
| `geiger2001resolution` — Geiger and Drinkwater, *Impact of Temporal-Spatio Resolution on Sea-Ice Drift and Deformation*, Springer, 2001, `10.1007/978-94-015-9735-7_34` | Quantifies how temporal and spatial sampling resolution propagates into the drift and deformation derived from it — the same mechanism H measures, one level upstream. |
| `covington2022bridging` — Covington, Chen and Wilhelmus, *Bridging Gaps in the Climate Observation Network*, J. Adv. Model. Earth Syst. 14, 2022, `10.1029/2022MS003218` | Treats gaps in a Lagrangian ice-floe observation record as a measurable deficit and recovers the missing dynamics; the closest existing treatment of observation gaps as a quantity. |

Considered and rejected: `10.5194/tc-18-1259-2024` (von Albedyll et al., lead fractions from SAR divergence
during MOSAiC) — highly relevant to the divergence retrieval of §3.6 but not a gap paper;
`10.5194/TC-15-3101-2021` (Harmony bi-static sea-ice dynamics) — a future-mission sampling argument, not a
quantification of an existing gap.

**The three incumbents were re-read and demoted, not removed.** OpenAlex abstracts for `wulf2024panarctic`
(ASIP pan-Arctic SIC methodology), `wulf2026decade` (DMI-ASIP 2014–2024 SIC record) and `wuite2026velocity`
(ten years of Sentinel-1 polar ice velocity) show that **none documents the consequences of missing imagery**.
They are Sentinel-1-derived product records that happen to span the discontinuity. The §1 sentence that had
claimed "downstream consequences of missing imagery have begun to be documented" was therefore rewritten to
say only that, which is also what item 8 of this package required.
