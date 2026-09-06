# Stage 1 — Bucket B: Navigability and route feasibility

Lookups used: 4/4 (OpenAlex, from_publication_date 2023-01-01).
New verified work beyond `00_landscape.md`:
- **L17** Corridor-scale sea-ice navigability and its interannual volatility: a multi-model assessment
  of the Arctic Europe–Pacific route (2026, *Frontiers in Marine Science*, 10.3389/fmars.2026.1855356) [V]
  — closest competitor for "navigability + interannual volatility", but **multi-model (simulated) fields**,
  corridor-scale, no observational SAR input and no realised-transit reconciliation.
- **L18** Evolving Arctic maritime hazards: declining sea ice and rising waves in the Northwest Passage
  (2024, *PNAS*, 10.1073/pnas.2400355121) [V] — NWP hazard trends, wave-centric (NO_METOCEAN: cite only).
- Queries for "chokepoint navigability Sentinel-1 Polar Class" and "PM SIC bias in narrow straits vs SAR"
  returned **no on-topic work** → supports gaps 2/6/9 in `00_landscape.md`.

| ID | Title (<=12 words) | Route/Region | RQ (1 sentence) | Why SAR / which layers | Reference data (named; independence noted) | Closest prior work (title, year, [V]/[U]) | N | R | F | A | V | J | Total | PASS/KILL + reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TB01 | S2: Chokepoint navigable-day climatology by Polar Class from Sentinel-1 | Vilkitsky, Sannikov, Long, Bering Straits (NSR) | By how many days per year and per Polar Class do AMSR2/OSI SAF products over- or under-state chokepoint navigability relative to a 40 m Sentinel-1 ice/water + deformed-ice navigability measurand, 2015–2026? | S1 EW HH/HV 40 m resolves narrow straits and coastal flaw leads that 6–25 km passive microwave smears; layers: S1 EW GRDM, AMSR2 SIC, OSI SAF type/edge, POLARIS RIO table | CHNL annual NSR transit counts/dates (realised outcome, fully independent of SAR); Sentinel-2 10 m summer scenes (independent optical); AARI/NIC charts used only as a *dependent* baseline, circularity flagged | L16 Navigability of LNG carriers along the NSR (2024) [V]; L17 Corridor-scale navigability and interannual volatility (2026) [V] | 2 | 3 | 2 | 2 | 2 | 3 | **14** | PASS — new measurand, coarse-product bias quantified against realised transits |
| TB02 | S2: Joint-chokepoint feasibility windows for non-ice-class Busan–Europe transits | Full NSR chain, Bering→Kara; Korea gateway | For how many days per year is the entire NSR chokepoint chain *simultaneously* open-water at SAR resolution for a non-ice-class ship, and how volatile is that window between years? | Feasibility is a joint condition over a chain of narrow gates; only 40 m S1 can test all gates on the same day; layers: S1 EW, AMSR2 SIC (comparison), landfast-ice masks | CHNL transit records with ice class (realised); Bellona Dec-2025 report on 38 sanctioned non-ice-class tankers actually sailing (aggregate only, no vessel attribution); Sentinel-2 optical | L16 (2024) [V]; L17 (2026, multi-model, no observations) [V] | 2 | 3 | 2 | 2 | 2 | 2 | **13** | PASS — joint-chain reliability measurand; falsifiable by realised non-ice-class sailings |
| TB03 | S16: Multiyear-ice inclusion exposure along the Transpolar corridor | Transpolar Sea Route, central Arctic | Does the summer PM-"navigable" Transpolar corridor contain multiyear-ice inclusions invisible at passive-microwave resolution, and how does exposure vary 2016–2026? | S1 EW HH/HV separates MYI floes embedded in low-concentration FYI/open water; layers: S1 EW, ICESat-2 ATL10 freeboard/ridges, CryoSat-2 thickness, OSI SAF type | ICESat-2 ATL10 freeboard and ridge statistics (non-SAR, independent); CryoSat-2 thickness (independent); realised transits essentially absent → validation rests on altimetry | L2 Inter-comparison of Arctic sea ice type products (2023) [V]; L13 Sea Ice Remote Sensing review (2023) [V] | 2 | 2 | 2 | 2 | 2 | 2 | **12** | PASS (marginal) — hazard/thickness link beyond type segmentation; weak operator demand |
| TB04 | S11/gap9: Melt-season uncertainty bounds on SAR-derived navigable windows | Bering–Chukchi and Kara chokepoints | How much does C-band melt-season ice/water ambiguity inflate the error on navigable-day counts, and can the window be reported as a validated bound rather than a point value? | Wet snow and melt ponds collapse C-band contrast exactly in the sailing season; layers: S1 EW HH/HV, incidence-angle metadata, Sentinel-2/VIIRS optical, AMSR2 | Cloud-free Sentinel-2 10 m and VIIRS scenes as independent non-SAR truth; MOSAiC/ASSIST ship observations where coincident; charts excluded from truth | L12 C-band drift/SIC degradation in melt season (2023) [V]; L1 MC-dropout uncertainty in S1 ice segmentation (2023) [V] | 2 | 3 | 2 | 2 | 3 | 2 | **14** | PASS — closes gaps 5+9; uncertainty propagated to a decision-relevant quantity |
| TB05 | Effective navigability: window plus chart adequacy, refuge reach, icebergs | NSR + Canadian Arctic approaches | Does adding chart adequacy, refuge/SAR asset reach and iceberg exposure to the SAR navigable window change which corridor segments are judged feasible? | S1 hazard frequency as one layer among five; layers: S1 EW, IHO C-55 survey status, GEBCO, DMI iceberg charts, SAR-station/icebreaker-base reach | Grounding/besetting records (Clipper Adventurer 2010, Akademik Ioffe 2018, Hudson Strait inventory) — realised but n≈tens; CHNL transits | L14 SAR ice class → POLARIS → route, Barents (2026) [V]; L15 BN navigation risk (2025) [V] | 2 | 2 | 2 | 2 | 1 | 2 | **11** | KILL — composite index, outcome n too small; duplicates bucket F seed S5 |
| TB06 | Auditing published NSR navigability projections against observed Sentinel-1 windows | Pan-NSR, 2015–2026 | Do observed S1-derived chokepoint windows fall inside the ranges projected by published PM/CMIP6 navigability studies? | SAR adds no retrieval advantage here; it is a re-use of TB01 output as an audit series against literature claims | Published projection ranges (literature); TB01 series — no new independent reference of its own | L17 Corridor-scale multi-model navigability (2026) [V]; L16 (2024) [V] | 1 | 2 | 3 | 1 | 2 | 2 | **11** | KILL — hard kill (N<=1 and A<=1); derivative meta-study of TB01 |

## Notes — Stage 2 검증 항목

1. **F 재평가 필수**: GEE noncommercial quota 초과(restricted mode) 상태이므로 TB01/TB02의 2015–2026
   chokepoint 시계열이 `reduceRegion` 소규모 폴리곤으로 실제 완주 가능한지 P2 pilot로 확인. 불가 시 ASF
   메타데이터 + 소수 scene 다운로드로 축소(`PILOT=CATALOG` 가능성).
2. **CHNL 자료 접근성**: transit 건수만 공개인지, 날짜·ice class 단위까지 공개인지 확인. 날짜 단위가
   없으면 TB01/TB02의 V가 2→1로 떨어져 재점수 필요 (Bellona·High North News 보조).
3. **L17 전문 확인**: multi-model 범위에 관측 SAR 비교가 포함되어 있는지 확인. 포함 시 TB02 novelty 재검토.
4. **AARI chart 연속성**: 2022 이후 공개 지속 여부. baseline이 끊기면 dependent baseline 자체가 소멸.
5. **Polar Class → navigability 사상**: POLARIS RIO를 SAR 기반 type/deformation에서 어떻게 도출할지가
   TB01의 핵심 가정. AIRSS/POLARIS 표만으로 40 m 층에 대응되는지 A 버킷과 중복 여부 조율 필요.
6. **TB04 optical coincidence n**: 융빙기 무운량 Sentinel-2 × chokepoint 동시취득 장면 수가 통계적으로
   충분한지(>=30 pair 목표) 카탈로그 조회로 사전 확인.
7. **TB03**: ICESat-2 ATL10 트랙이 Transpolar corridor를 계절별로 충분히 지나는지 확인, 미달 시 KILL 전환.
8. **혼동요인 명시**: incidence angle, wind roughening(개수면 오분류), EW noise-floor scalloping,
   chart-vs-scene time offset — 모든 카드 공통.
