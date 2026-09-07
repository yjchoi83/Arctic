# NUMBERS_TRACE — every number in MANUSCRIPT.md to its source file and package

Paths are relative to `arctic_explore/`. "scratch" paths are untracked working data (regenerable by the listed
script); "stage5" and "results" paths are committed. Package column gives the ARC package that produced the number.

## Figures

**[P12] Figures renumbered to first-citation order.** Figures 4-8 were out of order: the §4.3 panels were
labelled 7 and 8 while the §4.4-4.6 panels were labelled 4-6. Mapping applied to labels, in-text references,
PNG file names and `scratch/P9/p10_figs.py`: old 7→4, 8→5, 4→6, 5→7, 6→8. Content is unchanged.

| Figure | File | Produced from | Script | Package |
|---|---|---|---|---|
| 1 | `paper/figures/fig01_H_schematic.png` | synthetic illustration only, no data | `scratch/P9/p10_figs.py` | P10 |
| 2 | `paper/figures/fig02_hazard_timescales.png` | `scratch/P3/step2t_native1h.npz`, `scratch/P1b/events_persist.csv` | same | P1b, P3 |
| 3 | `paper/figures/fig03_H_state3_maps.png`, `fig03_H_episode3_maps.png` | `scratch/P3/P3_cells.csv` | same | P3 |
| 4 (was 7) | `paper/figures/fig04_virtual_pairs.png` | `scratch/P9/virtual_pairs_all.csv.gz` | same | P9 |
| 5 (was 8) | `paper/figures/fig05_strait_examples.png` | `results/P8/quicklooks/E00{1,2}_*, E0{10,11}_*`; caption edge-audit values from `results/P9/edge_audit.csv` = `paper/edge_audit.csv` | same | P8, P11 |
| 6 (was 4) | `paper/figures/fig06_design_curve.png` | `scratch/P6/ose_region.csv`, `scratch/P11/ose_region_valid.csv` | same | P6, P11 |
| 7 (was 5) | `paper/figures/fig07_planned_vs_acquired.png` | `scratch/P9/planned_vs_acquired.csv` ← `scratch/P8/planned_vs.csv` + `scratch/P2/P2_tables.csv` | same | P8, P2 |
| 8 (was 6) | `paper/figures/fig08_dtu_availability.png` | `scratch/P8/dtu_availability.csv` | same | P8 |
| A1 | `paper/figures/figA1_contact_sheet.png` | `results/P8/quicklooks/*`, `results/P9/qc_table_p9.csv` | same | P8, P9 |

**[P12-6]** Figure 5 caption edge-audit values, panel order: centroid distance to the overlap boundary
E002 18.9, E001 76.7, E011 46.0, E010 32.4 km; fraction of nodes within 5 km of it 0.000 for all four.

## Tables

| Table | Source | Package |
|---|---|---|
| 1 regions and cells | `scratch/P3/cells.py` (`region_cells()`), `scratch/P2/regions.py` | P2, P3 |
| 2 hazard timescales | `scratch/P9/Hsmall.log` header (episode by class×season); `stage5/P1b/P1b_results.md` §1 (persistence) | P1b, P9 |
| 3 / 3b observability by period and class | `scratch/P3/P3_region_season_year.csv`; `scratch/P9/H_by_class_cells.csv` | P3, P9 |
| 4 observing system experiment | `scratch/P6/ose_region.csv` vs `scratch/P3/P3_region_season_year.csv` | P6 |
| 5 planned vs acquired | `scratch/P8/planned_vs.csv`, `scratch/P8/planned.csv` | P8 |
| 6 threshold sensitivity | `stage5/P9/h9_sensitivity.csv` | P9 |

## Claims and their numbers

### C1 — requirement never met at the chokepoints (§4.1)
| Number | Value | Source | Package |
|---|---|---|---|
| region-season-year cells | 688 total, 512 excluding shoulder | `scratch/P2/P2_tables.csv` | P2 |
| max O(12 h) over the record | 0.278 | same | P2 |
| cells with O(12 h) ≥ 0.5 | 0 | same | P2 |
| chokepoint H_episode / H_state, pre | 0.200 / 0.504 | `scratch/P3/P3_region_season_year.csv` | P3 |
| **[P12-5]** units with H_episode ≥ 0.8 (≥ 3 km) | 0 of 512 overall; 0 of 160 chokepoint | `scratch/P3/P3_region_season_year.csv` | P12 |
| **[P12-5]** max H_episode (≥ 3 km) | 0.640 overall; 0.467 chokepoint | same | P12 |
| **[P12-5]** units with H_state ≥ 0.8 (≥ 3 km) | 25 of 512 overall (Greenland/Fram 13, Baffin 5, Barents 4, Lancaster 3); 0 of 160 chokepoint | same | P12 |
| **[P12-5]** max H_state (≥ 3 km) at chokepoints | 0.793 (Kara Gate) | same | P12 |
| **[P12-5]** "24 h criterion reached in four regions" = **O(24 h) ≥ 0.8** | 38 of 512 main-season units, in those same four regions; 0 chokepoint units; chokepoint max O(24 h) 0.475 | `scratch/P2/P2_tables.csv`, `stage5/P2/P2_results.md` §3 | P2, P12 |
| **[P12-5]** max O(12 h) | 0.278 over the 512 main-season units; 0.320 over all 688 (Baffin Bay 2026 shoulder) | `scratch/P2/P2_tables.csv` | P2, P12 |
| **[P12-5]** superseded (was "maximum over the whole record is 0.278") | 0.278 is the main-season maximum; the all-688 maximum is 0.320 | — | P2 |
| **[P12-5]** unit denominators | H is defined on the 512 main-season units; O(Δt) on all 688 including shoulder | same | P12 |
| episode / state requirement (12 h, 24 h) | derived from Table 2 medians | `stage5/P1b/P1b_results.md` §3 | P1b |

### C2 — the gap widened an existing deficit (§4.2)
| Number | Value | Source | Package |
|---|---|---|---|
| chokepoint H_episode, during | 0.097 | `scratch/P3/P3_region_season_year.csv` | P3 |
| chokepoint H_state, during | 0.363 | same | P3 |
| all-region H_episode / H_state, during | 0.151 / 0.441 | same | P3 |
| retention classes | 9 lost, 7 intermediate, **0 kept** | `scratch/P2/retention.csv` | P2 |
| retention min / max | 0.310 Sannikov / 0.846 Bering–Chukchi | same | P2 |
| dose-response DiD on H_state | −25.7 pp, CI [−49.9, +0.6] | `scratch/P2/did.json` | P2 |

### C3 — chokepoint hazards are real and retrievable (§4.3)
| Number | Value | Source | Package |
|---|---|---|---|
| Vilkitsky valid OSI-405 point-days | 0 of 76,075 | `scratch/P4/div2.log` | P4 |
| Sannikov / Long Strait / Kara Gate divergence-computable | 0.1 / 0.3 / 0.0 % | same | P4 |
| Bering–Chukchi divergence-computable | 6.8 % | same | P4 |
| hazard-observed fraction 2022/23/24 | 0.422 / 0.177 / 0.892 | `scratch/P4/hof.csv` | P4 |
| pairs yielding ≥ 30 vectors | 20 of 20 | `scratch/P8/pair_summary.csv` | P8 |
| mean retrieval success | 0.510 | same | P8 |
| freeze-up range / winter range | 0.377–0.419 / 0.484–0.779 | same | P8 |
| virtual buoy pairs | 240,949 | `scratch/P9/virtual_pairs_all.csv.gz` | P9 |
| fraction passing the buoy rate threshold | 0.50 % | same | P9 |
| closure of those pairs, median / p90 / max | 5.88 / 6.94 / 10.63 km | same | P9 |
| Vilkitsky winter pass fraction | 1.86 % | `scratch/P9/virtual_pair_stats.csv` | P9 |
| events with a buoy within 100 km | 0 of 19 | `results/P9/qc_table_p9.csv` | P8, P9 |
| **[P11-A2]** events flagged EDGE_SUSPECT | 0 of 19 | `results/P9/edge_audit.csv` | P11 |
| **[P11-A2]** centroid distance to overlap boundary | 18.9-135.5 km | same | P11 |
| **[P11-A2]** share of nodes within 5 km of the boundary | 0.000 for all 19 | same | P11 |
| **[P11-A2]** events per pair | 19 events from 5 pairs; 9 from one Sannikov pair | same | P11 |

### C4 — the gap is explained by satellite count (§4.4)
| Number | Value | Source | Package |
|---|---|---|---|
| regions within 10 pp | 15 of 16 | `scratch/P6/ose_region.csv` | P6 |
| Sannikov exception | +12.3 pp | same | P6 |
| **[P11-A1]** admissible combinations after season-matching | 650 of 800 (150 dropped) | `scratch/P11/ose_region_valid.csv` | P11 |
| **[P11-A1]** all regions 1→2, freeze-up / winter / melt | 0.525→0.662 / 0.454→0.598 / 0.351→0.451 | same | P11 |
| **[P11-A1]** chokepoints 1→2, freeze-up / winter / melt | 0.450→0.586 / 0.388→0.527 / 0.287→0.386 | same | P11 |
| **[P11-A1]** season-mean gain 1→2, all / chokepoints | +0.127 / +0.125 | same | P11 |
| **[P11-A1]** combinations reaching 0.8 | 15 of 650 | same | P11 |
| chokepoint maximum | 0.718 | same | P6, P11 |
| **[P11-A1]** 3-platform, melt 2026 only, all / chokepoints | 0.511 (n=9) / 0.429 (n=2) | same | P11 |
| **[P12-consistency]** matched melt-2026 comparison, same nine regions | 1 / 2 / 3 platforms = 0.373 / 0.441 / 0.511 all; 0.293 / 0.353 / 0.429 at the two chokepoints in that set | `scratch/P11/ose_region_valid.csv` | P12 |
| **[P12-consistency]** superseded (§4.4 compared the melt-2026 3-platform value against 0.451 and 0.386) | those are melt-season 2-platform means pooled over all years and all sixteen regions, not the same window or region set; replaced by the matched 0.441 / 0.353 | — | P10 |
| **[P11-A1]** superseded values (were: 0.431/0.563/0.527, 0.372/0.505/0.459, 16 of 800, gain 0.13→0.05) | withdrawn: pooled seasons and included inadmissible 3-platform rows | — | P10 |

### C5 — the recovery shortfall is allocation (§4.5)
| Number | Value | Source | Package |
|---|---|---|---|
| aggregate scene rate vs pre | 88.5 % | `scratch/P2/P2_tables.csv` | P2, P6 |
| ramp-up-controlled EUR / NAM | 77.4 % / 121.1 % | `stage5/P8/P8_step2_plans.md` §2 | P8 |
| **[P11-A6]** planned EUR / NAM, 2025 vs pre | 87.1 % / 123.4 % | `scratch/P11/planned_with_gap.csv` | P11 |
| **[P11-A6]** planned EUR / NAM, gap years 2022-24 vs pre | 49.8 % / 62.0 % | same | P11 |
| **[P11-A6]** Barents planned, gap / 2025 | 42.7 % / 56.8 % | same | P11 |
| **[P11-A6]** Sannikov planned, gap / 2025 | 36.7 % / 89.5 % | same | P11 |
| **[P11-A6]** superseded (was 86.4 % / 122.3 %) | recomputed after adding S1A 2022-24 plan archives | — | P8 |
| **[P12-1]** Barents planned / acquired, 2025 | 56.8 % / 38.3 % | `scratch/P11/planned_with_gap.csv`, `stage5/P8/P8_step2_plans.md` | P11, P8 |
| **[P12-1]** Vilkitsky planned / acquired, 2025 | 147.1 % / 156.1 % | same | P11, P8 |
| **[P12-1]** Long Strait planned, 2025 | 102.9 % | `scratch/P11/planned_with_gap.csv` | P11 |
| **[P12-1]** superseded in text (were: 86.4 % / 122.3 % EUR/NAM; Barents 56 %; Vilkitsky 146 %; Long Strait 113 %) | text now matches Table 5 and `planned_with_gap.csv` everywhere (abstract, §4.5, §7) | — | P8/P10 |
| **[P12-1]** rounding note | Vilkitsky 2025 ratio is 147.1 % from the rounded pre-loss rate of 495 segments/yr printed in Table 5, 147.2 % from the unrounded 494.67; the table value is used throughout | `scratch/P11/planned_with_gap.csv` | P12 |
| S1C routine onset | 2025-04 | `scratch/P8/monthly_platform.csv` | P8 |
| S1D first data | 2026-04 | same | P8 |

### C6 — propagation into an operational product (§4.6)
| Number | Value | Source | Package |
|---|---|---|---|
| ρ with H_state (region-year, n = 112) | 0.711, p = 1.7e-18 | `stage5/P9/h9_sensitivity.csv` | P8, P9 |
| ρ with H_episode | 0.736 | same | P9 |
| within-region median ρ | 0.727 | same | P9 |
| threshold sensitivity 2 / 5 / 10 % | 0.714 / 0.711 / 0.659 | same | P9 |
| availability pre / during / post | 0.152 / 0.031 / 0.033 | `scratch/P8/dtu_availability.csv` | P8 |
| MET Norway issuance days | 248 / 253 / 251 / 250 | `stage5/P8/P8_step1_products.md` §3 | P8 |

## Methods and limitations numbers

| Number | Value | Source | Package |
|---|---|---|---|
| IABP fixes after QC / buoys | 8,661,366 / 1,271 | `scratch/P1/build.log` | P1 |
| buoy pairs in the 20–100 km band | 9,884 | `scratch/P1/pairs.log` | P1 |
| buoy events, 3-h sampling | 82,440 (82,439 on re-derivation) | `stage5/P1/P1_events.csv`, `scratch/P1b/events_persist.csv` | P1, P1b |
| events at the 6 h floor | 55.9 % | `stage5/P1b/P1b_results.md` §1 | P1b |
| events, 1-h subset | 137,786; median 2 h; 85.8 % under 6 h | `scratch/P3/step2t_native1h.npz`, `stage5/P1b/P1b_results.md` §2 | P1b |
| buoys with native interval ≤ 1 h | 1,111 of 1,271 | `stage5/P1b/P1b_results.md` §2 | P1b |
| persistence undefined fraction | 84.6 % | `stage5/P8/`…`P1b_results.md` §1 | P1b |
| rate thresholds 3-h / 1-h | 2.954 / 4.706 km d⁻¹ | `stage5/P1/P1_hazard_windows.md`, `scratch/P1b/step2.log` | P1, P1b |
| cells / regions / cell-season-year rows | 1,771 / 16 / 56,663 | `scratch/P3/cells.py`, `scratch/P3/P3_cells.csv` | P3 |
| √area median vs buoy baseline median | 12.2 km vs 49.4 km; ratio 0.248 | `stage5/P9/P9_step1_magnitude.md` §1 | P9 |
| **[P11-A7]** E chokepoints, winter pre/during/post | 0.345 / 0.236 / 0.293 | `scratch/P11/E_table.csv` | P11 |
| **[P11-A7]** E chokepoints, freeze-up | 0.225 / 0.171 / 0.238 | same | P11 |
| **[P11-A7]** E chokepoints, melt | 0.008 / 0.006 / 0.008 | same | P11 |
| **[P11-A7]** retrieval success winter / freeze-up / melt | 0.628 / 0.392 / 0.020 | `scratch/P8/pair_summary.csv`, `stage5/P5/P5_results.md` | P8, P5 |
| **[P11-A7]** chokepoint H_state3 by season, pre/during/post | see Table 7 | `scratch/P3/P3_region_season_year.csv` | P3 |
| **[P11-A7]** superseded (was 0.18–0.28 winter, pooled) | replaced by season-resolved E table | — | P5 |
| **[P12-3]** E ranges quoted in §5.2 and §6.6 | winter 0.236–0.345, freeze-up 0.171–0.238, melt 0.006–0.008 | `scratch/P11/E_table.csv` (= Table 7) | P11, P12 |
| **[P12-3]** superseded (§5.2 was 0.18–0.28 winter / 0.006–0.009 melt; §6.6 was “order 0.2 winter, 0.01 melt”) | both now read the Table 7 min–max across periods | — | P10 |
| freeze-up retrieval success | 0.392 (0.47 assumption ~19 % high) | `scratch/P8/pair_summary.csv` | P8 |
| **[P12-consistency]** chokepoint H by class (Table 3b) | ≥1 km 0.090/0.044/0.079; 1–3 km 0.063/0.030/0.056; ≥3 km 0.200/0.097/0.176; ≥5 km 0.257/0.127/0.228 | `scratch/P9/H_by_class_cells.csv`, re-aggregated cells → region-season-year → period (45/45/25 units) | P9, P12 |
| **[P12-consistency]** superseded (was 0.081/0.042/0.073, 0.057/0.029/0.051, 0.181/0.093/0.161, 0.233/0.121/0.208) | those were **cell-weighted** means, so Sannikov's 109 cells pulled the ≥3 km row to 0.181 against Table 3's 0.200 for the identical quantity; Table 3b now uses Table 3's two-stage unweighted aggregation and the ≥3 km row matches exactly | — | P9 |
| **[P12-consistency]** 1–3 km chokepoint H during the gap, quoted in §5.2 and §6.8 | 0.030 (was 0.029) | same | P12 |
| Laptev/ESS winter buoy events | 17, from 8 pairs and 14 buoys | `stage5/P1/P1_hazard_windows.md` §2 | P1 |
| central Arctic share of events | 55 % | same | P1 |

## [P12-7] Word budget and trims

| Item | Before | After |
|---|---|---|
| Abstract | 293 | **250** |
| §3.6 (matcher parameters → Supplementary Table S1) | 611 | 449 |
| §4.7 (Bering explanation → two sentences) | 449 | 415 |
| §5.4 (halved) | 358 body | **197 body** |
| Main text, excluding headings, tables, figure captions and back matter | 9,561 | **9,170** |
| Including headings | 9,753 | **9,362** |
| Whole file, including 735 words of tables, 858 of figure captions and 280 of back matter | 11,626 | 11,235 |

Matcher, node-acceptance, pair-selection and event-definition parameters now live in `paper/SUPPLEMENTARY.md`
(Supplementary Table S1); values are unchanged, only relocated.

## Regeneration

`python3 scratch/P9/p10_figs.py` rebuilds every figure in `paper/figures/`. Upstream working data are rebuilt by
`scratch/P1/p1_build.py` → `p1_pairs.py` → `p1_events.py` (P1), `scratch/P1b/p1b_step{1,2,3}.py` (P1b),
`scratch/P2/p2_{fetch,metrics,did}.py` (P2), `scratch/P3/p3_{fetch_geom,cellacq,H,agg}.py` (P3),
`scratch/P4/{dl,p4_div2,p4_hof}.py` (P4), `scratch/P6/p6_ose.py` (P6),
`scratch/P8/p8_{dtu,plans,process}.py` (P8), `scratch/P9/p9_{reconcile,Hsmall,dtu_daily}.py` (P9).

## [P12-8, P12-9] Literature audits

| Audit | Result | File |
|---|---|---|
| 9c, re-verify all 76 references against authenticated Semantic Scholar | 63 clean, 10 flagged and all resolved in favour of the bibliography, 3 not indexed; **one real defect** — truncated title on `karvonen2022baltic`, fixed | `scratch/P12/REF_VERIFY.md`, `scratch/P12/ref_verify.json` |
| 9a, novelty re-search, 21 queries over the three framing claims | **no paper overlaps a core claim**; nearest works are sampling-resolution, mission-status and task-planning papers, all now cited or explained | `scratch/P12/NOVELTY.md`, `scratch/P12/novelty_raw.json` |
| 9b, cluster 8 strict gap-quantification | two strict papers added: `geiger2001resolution`, `covington2022bridging`; cluster 8 goes 3 → 5 and meets its target strictly; bibliography 76 → 78 | same |
| 8, do Fu et al. 2016 and Wulf/Wuite support their sentences | **Fu et al. 2016 yes** (Bayesian besetting-probability model for the Northeast Passage, supports the besetting clause). **Wulf/Wuite no** — OpenAlex abstracts show three Sentinel-1-derived product records that span the 2021 discontinuity but do not document consequences of missing imagery; the §1 sentence was rewritten to claim only that, and the two strict gap papers above now carry the mechanism claim | `scratch/P12/NOVELTY.md` |

