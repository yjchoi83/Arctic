# Stage 1 — Bucket A. Safe routing and decision support

Lookups used: 4 OpenAlex queries (uncertainty-aware ice routing; SAR channel/convoy route validation;
S1 high-res ice route optimisation; Arctic places of refuge / corridors). New [V] beyond §4.3 / 00_landscape:
L17 = "Integrating spatio-temporal analysis for assessing the effectiveness of POLARIS in Arctic shipping
traffic" (2026, Transport Policy, doi:10.1016/j.tranpol.2026.104096) [V]. No paper found for
uncertainty-propagated route-risk bounds, nor for routing validated against SAR-detected channels.

| ID | Title (<=12 words) | Route/Region | RQ (1 sentence) | Why SAR / which layers | Reference data (named; independence noted) | Closest prior work (title, year, [V]/[U]) | N | R | F | A | V | J | Total | PASS/KILL + reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TA01 | S1 SAR-resolution POLARIS risk surfaces change optimal Arctic routes (S1) | NSR Kara–Laptev (Vilkitsky) + Chukchi/Bering | Do 40 m Sentinel-1 EW hazard fields yield different optimal routes and residual risk than chart/passive-microwave POLARIS surfaces, and are the SAR-derived routes closer to realised transits? | S1 EW HH/HV 40 m ice/water + deformed-vs-level hazard layer converted to RIO surface; charts and AMSR2 as coarse baselines | SAR-detected convoy/icebreaker channels (AIS-free, Sentinel-2 10 m confirmation), CHNL transit statistics, besetting/incident records (Lynx 2025, Hudson Strait inventory, TSB) — all independent of ice charts | SAR ice class -> POLARIS -> route, Barents (2026, MDPI Sustainability) [V]; Incremental route planning daily risk (2025, Ocean Eng) [V]; POLARIS effectiveness vs traffic (2026, Transport Policy) [V] | 2 | 3 | 2 | 3 | 2 | 3 | 15 | PASS: resolution-effect on routes with realised-channel/incident validation is open |
| TA02 | Uncertainty-aware ice routing: propagating SAR retrieval uncertainty into route-risk bounds (S17) | Kara Sea + Bering/Chukchi | Does propagating pixel-level SAR classification uncertainty into path costs produce route-risk bounds that are calibrated against observed hazardous encounters, and does it shift chosen routes? | MC-dropout / ensemble uncertainty on S1 EW ice classification; incidence-angle and season strata as uncertainty drivers | IABP buoy drift and deformation, Sentinel-2 scenes for melt/roughness truth, besetting/incident catalog for calibration; charts used only as coarse baseline (declared circular) | Model Ensemble With Dropout for Uncertainty in Sea Ice Segmentation (2023, TGRS) [V] — pixel uncertainty only, never propagated to routes; no routing-uncertainty paper found in-session | 3 | 2 | 2 | 2 | 2 | 3 | 14 | PASS (conditional on TA01): novel measurand, calibration is the risk |
| TA03 | Lead-time value of sub-daily SAR revisit for dynamic rerouting (S1/S6) | Pan-NSR + Bering Strait approaches | How much does SAR revisit frequency (single-satellite 2022-2024 vs two-satellite 2019-2021 and 2025-2026) change hazard latency and the risk of routes replanned on stale ice information? | S1_GRD metadata (mode, orbit, timestamp) gives per-region revisit; hazard fields recomputed at different staleness to measure decision degradation | S1_GRD scene-count metadata (non-circular), CHNL transits by season, chart revision timestamps (NIC/AARI/DMI), documented besetting events during the gap | Arctic weather routing review (2023, Front Mar Sci) [V] flags input-resolution gap; no quantification of revisit/latency on route risk found | 2 | 3 | 3 | 2 | 2 | 3 | 15 | PASS: cheap metadata natural experiment, clear operator value |
| TA04 | Channel-reuse routing: detected refrozen leads as low-cost route segments | Kara–Laptev NSR convoy corridors | Does routing preferentially along SAR-detected icebreaker channels reduce modelled transit risk, and how long do such channels remain reusable as a function of ice regime? | S1 EW backscatter contrast and coherence-like persistence to detect and age channels; hazard field as background cost | Sentinel-2 optical channel confirmation, Rosatom/announced convoy dates, CHNL counts; no AIS in the method (AIS validation-only if used at all) | S9-adjacent channel-detection work is bucket G; no routing study using detected channels as cost layer found in-session | 2 | 2 | 2 | 2 | 2 | 2 | 12 | PASS (marginal): value depends on channel-detection reliability |
| TA05 | Bering Strait two-way corridor geometry versus observed SAR hazard field | Bering Strait / Chukchi (Korea gateway) | Does the observed 2016-2026 SAR hazard-frequency field support the geometry of the IMO 2018 two-way routes and precautionary areas, or are hazard hotspots systematically off-corridor? | Multi-year S1 EW hazard-frequency climatology at 40 m inside/outside routeing measures; landfast and drift-ice edge layers | IMO routeing measures (documented), USCG/NOAA charts and survey adequacy, grounding/incident records; hazard field itself independent of the corridor design | Marine spatial planning in Canadian Arctic low-impact shipping corridors (2023, Ocean Yearbook) [V] — governance, not observational hazard | 2 | 3 | 2 | 2 | 1 | 2 | 12 | PASS (weak V): few incidents in region; falsification path thin |
| TA06 | Expert-weighted multi-criteria NSR route risk index (AHP/fuzzy) | Pan-NSR | Can an AHP/fuzzy composite of ice, distance and infrastructure criteria rank NSR route segments by risk? | Would use SAR only as one convenience layer among many | Expert elicitation only; no independent outcome data proposed | Navigation Risk Assessment of Arctic Shipping Routes Based on Bayesian Networks (2025, JMSE) [V]; XGBoost Arctic navigation risk (2023, Risk Analysis) [V] | 1 | 2 | 3 | 1 | 0 | 1 | 8 | KILL: V=0, composite without outcome validation; §4.3 saturated |

## Additional kills (not carried as cards)
- AIS-driven route-deviation / risk learning for the NSR: KILL — AIS-centric, violates AIS_POLICY.
- Ship resistance / ice-load simulation coupled routing: KILL — numerical modelling (NO_METOCEAN-adjacent), no SAR advantage.

## Notes (Stage 2에서 검증할 것)
1. TA01의 핵심 리스크는 "realised route" 증거 확보. CHNL transit 통계 접근성과 besetting/grounding 사건이
   10건 이상 지리·시간 좌표로 특정되는지 먼저 확인해야 함. 실패 시 TA01의 V는 2->1로 떨어짐.
2. L14(MDPI Sustainability 2026)가 SAR->POLARIS->route를 이미 수행. 반드시 (a) 해상도 대조 실험,
   (b) 실현경로/사고 검증 두 축으로 차별화해야 하며, 단순 지역 변경은 novelty 아님.
3. TA01/TA02 hazard field는 ice *type* 분류가 아니라 hazard measurand로 정의해야 §4.3 포화를 피함
   (deformed vs level, ridge/pressure proxy). Stage 2에서 measurand 정의를 문서화할 것.
4. GEE noncommercial quota 초과 상태 -> 대형 export 금지. TA03은 metadata-only라 이 제약에 가장 강함;
   Stage 2 첫 pilot으로 TA03을 돌리는 것이 비용 대비 효율적.
5. TA02는 §6 규정상 S1(=TA01) 통과 조건부. 또한 uncertainty bound의 calibration 대상(사건 표본 수)이
   충분한지 TA01과 같은 확인 절차를 공유함.
6. TA04는 Sentinel-2 여름 한정 검증이라 결빙기 channel persistence 검증 수단이 불확실. Stage 2에서
   S1 시계열만으로 channel age를 정의할 수 있는지 확인 필요.
7. TA05는 IMO 2018 two-way routes 및 precautionary areas의 정확한 좌표 공개본 확인 필요(§4.2 verify 표시).
8. Journal fit: TA01/TA04 -> Ocean Engineering / Cold Regions Sci Tech, TA02 -> RESS 또는 TGRS,
   TA03 -> Environmental Research Letters / Journal of Navigation, TA05 -> Ocean & Coastal Management.
   MDPI 전 계열 제외 유지.
