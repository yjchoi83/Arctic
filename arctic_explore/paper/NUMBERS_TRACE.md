# NUMBERS_TRACE — every number in MANUSCRIPT.md to its source file and package

Paths are relative to `arctic_explore/`. "scratch" paths are untracked working data (regenerable by the listed
script); "stage5" and "results" paths are committed. Package column gives the ARC package that produced the number.

## Figures

| Figure | File | Produced from | Script | Package |
|---|---|---|---|---|
| 1 | `paper/figures/fig01_H_schematic.png` | synthetic illustration only, no data | `scratch/P9/p10_figs.py` | P10 |
| 2 | `paper/figures/fig02_hazard_timescales.png` | `scratch/P3/step2t_native1h.npz`, `scratch/P1b/events_persist.csv` | same | P1b, P3 |
| 3 | `paper/figures/fig03_H_state3_maps.png`, `fig03_H_episode3_maps.png` | `scratch/P3/P3_cells.csv` | same | P3 |
| 4 | `paper/figures/fig04_design_curve.png` | `scratch/P6/ose_region.csv` | same | P6 |
| 5 | `paper/figures/fig05_planned_vs_acquired.png` | `scratch/P9/planned_vs_acquired.csv` ← `scratch/P8/planned_vs.csv` + `scratch/P2/P2_tables.csv` | same | P8, P2 |
| 6 | `paper/figures/fig06_dtu_availability.png` | `scratch/P8/dtu_availability.csv` | same | P8 |
| 7 | `paper/figures/fig07_virtual_pairs.png` | `scratch/P9/virtual_pairs_all.csv.gz` | same | P9 |
| 8 | `paper/figures/fig08_strait_examples.png` | `results/P8/quicklooks/E00{1,2}_*, E0{10,11}_*` | same | P8 |
| A1 | `paper/figures/figA1_contact_sheet.png` | `results/P8/quicklooks/*`, `results/P9/qc_table_p9.csv` | same | P8, P9 |

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
| regions ever meeting the 24 h criterion | 4, none a chokepoint | `stage5/P2/P2_results.md` §3 | P2 |
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

### C4 — the gap is explained by satellite count (§4.4)
| Number | Value | Source | Package |
|---|---|---|---|
| regions within 10 pp | 15 of 16 | `scratch/P6/ose_region.csv` | P6 |
| Sannikov exception | +12.3 pp | same | P6 |
| design curve, all regions, 1/2/3 platforms | 0.431 / 0.563 / 0.527 | same | P6 |
| design curve, chokepoints | 0.372 / 0.505 / 0.459 | same | P6 |
| combinations reaching 0.8 | 16 of 800 | same | P6 |
| chokepoint maximum | 0.718 | same | P6 |
| marginal gain 1→2, 2→3 | +0.13, +0.05 | same | P6 |

### C5 — the recovery shortfall is allocation (§4.5)
| Number | Value | Source | Package |
|---|---|---|---|
| aggregate scene rate vs pre | 88.5 % | `scratch/P2/P2_tables.csv` | P2, P6 |
| ramp-up-controlled EUR / NAM | 77.4 % / 121.1 % | `stage5/P8/P8_step2_plans.md` §2 | P8 |
| planned EUR / NAM | 86.4 % / 122.3 % | `scratch/P8/planned_vs.csv` | P8 |
| Barents planned / acquired | 56.0 % / 38.3 % | same, `stage5/P8/P8_step2_plans.md` | P8 |
| Vilkitsky planned / acquired | 146 % / 156.1 % | same | P8 |
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
| effective observability winter / melt | 0.18–0.28 / 0.006–0.009 | `stage5/P5/P5_results.md` §2 | P5 |
| freeze-up retrieval success | 0.392 (0.47 assumption ~19 % high) | `scratch/P8/pair_summary.csv` | P8 |
| chokepoint H by class (Table 3b) | see Table 3b | `scratch/P9/H_by_class_cells.csv` | P9 |
| Laptev/ESS winter buoy events | 17, from 8 pairs and 14 buoys | `stage5/P1/P1_hazard_windows.md` §2 | P1 |
| central Arctic share of events | 55 % | same | P1 |

## Regeneration

`python3 scratch/P9/p10_figs.py` rebuilds every figure in `paper/figures/`. Upstream working data are rebuilt by
`scratch/P1/p1_build.py` → `p1_pairs.py` → `p1_events.py` (P1), `scratch/P1b/p1b_step{1,2,3}.py` (P1b),
`scratch/P2/p2_{fetch,metrics,did}.py` (P2), `scratch/P3/p3_{fetch_geom,cellacq,H,agg}.py` (P3),
`scratch/P4/{dl,p4_div2,p4_hof}.py` (P4), `scratch/P6/p6_ose.py` (P6),
`scratch/P8/p8_{dtu,plans,process}.py` (P8), `scratch/P9/p9_{reconcile,Hsmall,dtu_daily}.py` (P9).
