# Stage 1 — Bucket G: Traffic and activity WITHOUT AIS (safety/transparency framing)

Lookups used: 4/4 (OpenAlex, from_publication_date 2022-01-01).
Query results: no paper found on (a) icebreaker/convoy channel detection in SAR, (b) AIS-free Arctic
corridor traffic proxies, (c) SAR port-activity monitoring in the Arctic. Only adjacent hits:
ship–iceberg discrimination (Remote Sensing 2022, MDPI), generic SAR ocean reviews (JSTARS 2023),
maritime small-object detection (Appl Ocean Res 2024). Treated as evidence of an open niche, not proof.

| ID | Title (<=12 words) | Route/Region | RQ (1 sentence) | Why SAR / which layers | Reference data (named; independence noted) | Closest prior work (title, year, [V]/[U]) | N | R | F | A | V | J | Total | PASS/KILL + reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TG01 | S9: Convoy channel detection in Sentinel-1 as AIS-free traffic proxy | NSR: Kara–Laptev, Vilkitsky & Sannikov Straits | Can refrozen icebreaker channels detected in S1 EW yield a monthly corridor-activity index that tracks independently reported NSR transit counts? | Channels are linear low-backscatter/refrozen features only 40 m EW HH/HV resolves; layers: S1 EW GRDM, OSI SAF drift (channel advection), AMSR2 SIC for regime stratification | CHNL (Nord Univ.) annual NSR transit statistics [non-SAR, independent]; Sentinel-2 10 m summer scenes [independent optical]; Rosatom public convoy announcements [independent]; AIS validation-only, never required | None found for SAR convoy-channel detection; nearest is SAR ship–iceberg discrimination, 2022 [V] (different measurand) | 3 | 3 | 2 | 2 | 2 | 3 | 15 | PASS — fills blackout transparency gap with independent transit-count validation |
| TG02 | Aggregate ship-detection density as corridor hazard exposure, no AIS | Bering Strait & Chukchi Sea (Korea gateway) | Does the aggregate spatial density of SAR ship detections, crossed with SAR hazard-ice frequency, identify corridor segments where traffic and hazard ice coincide? | S1 EW/IW CFAR-type detections plus SAR-derived hazard frequency; layers: S1 GRD, IMO Bering two-way routes, AMSR2 SIC | Sentinel-2 10 m same-day detections [independent optical]; US free Bering AIS as validation-only cross-check; IMO route geometry [independent] | SAR ship detection literature is saturated (§4.3) [V, from prompt]; aggregate exposure framing not found | 2 | 3 | 2 | 2 | 2 | 2 | 13 | PASS — detection is old, aggregate exposure measurand is not |
| TG03 | Port and anchorage activity proxy from Sentinel-1 IW time series | Sabetta, Dudinka, Pevek, Nome | Can S1 IW target counts inside port/anchorage polygons plus landfast breakup dates reconstruct annual port operating windows without AIS? | IW 10 m resolves berths and anchored vessels; layers: S1 IW GRD backscatter, S1 landfast-ice backscatter/coherence proxy, shoreline mask | Sentinel-2 / VHR Google Earth port imagery [independent optical]; CHNL destinational-traffic tallies [independent]; published port operating notices where available | No Arctic SAR port-activity study found in lookups; only coastal-erosion PlanetScope work, 2024 [V] | 2 | 2 | 2 | 1 | 2 | 2 | 11 | PASS (low) — plausible but reference records for Russian ports are thin |
| TG04 | Composite corridor exposure index from channels, hazards and assets | Pan-NSR corridor segments | Can a per-segment composite of channel-derived activity, hazard frequency and distance to response assets rank corridor risk exposure? | Would integrate S1 hazard layers with TG01 channel products | CHNL transits; incident news catalog — but no outcome dataset scoped | Overlaps seed S5 (bucket F) and L15 Bayesian index, 2025 [V] | 2 | 2 | 2 | 1 | 1 | 2 | 10 | KILL — composite index without outcome validation/sensitivity; duplicates bucket F S5 |
| TG05 | Sanctioned shadow-fleet tanker detection on NSR without AIS | NSR, Kara–Laptev | Can SAR detect and characterise sanctioned non-ice-class tankers transiting the NSR during the data blackout? | S1 EW detections plus ice-class-inferred hazard exposure | Bellona report Dec 2025 (100 sanctioned vessels) [U] | AIS-centric dark-vessel literature (§4.3) [V] | 2 | 2 | 2 | 2 | 1 | 2 | 11 | KILL — individual-vessel sanction attribution; violates ethics scope and AIS_POLICY |
| TG06 | S1B gap degrades AIS-free traffic observability, 2019–2026 | Pan-Arctic, NSR + Bering focus | How much did the 2022–2024 single-satellite gap reduce the detectability and revisit of AIS-free traffic proxies, and did 1C/1D restore it? | Pure S1_GRD metadata audit (mode, pol, orbit) — no imagery download, fits restricted GEE quota; layers: COPERNICUS/S1_GRD metadata, corridor polygons | Copernicus/ASF acquisition records [independent of the proxy itself]; CHNL transit counts as the activity denominator [independent]; ESA mission notices | Seed S6 (bucket E) covers monitoring gap generally; no traffic-observability treatment found [V-null] | 2 | 2 | 3 | 2 | 2 | 2 | 13 | PASS — cheap, falsifiable, sets detection-capability floor for TG01/TG02 |

## Ethics / provenance (one line per card)

- **TG01**: Aggregate monthly corridor-activity counts only, from public Copernicus S1 and public CHNL/Rosatom statements; no vessel identity, no naval assets, no attribution to individual ships; beneficiary is Arctic ice services and IMO Polar Code monitoring.
- **TG02**: Detection density is binned to corridor segments and reported as aggregate exposure; no track reconstruction, no identity, no naval or military vessels; AIS used only to check the aggregate, never released per-detection.
- **TG03**: Port polygons are civilian commercial ports; outputs are seasonal operating-window statistics, not vessel-level anchorage logs; no military basing inference; public Copernicus and Sentinel-2 imagery only.
- **TG04**: (killed) Would have been aggregate-only; no ethics obstacle, killed on scientific grounds.
- **TG05**: (killed) Attribution of sanction status to individual hulls is explicitly out of scope; not pursued in any form.
- **TG06**: Uses satellite acquisition metadata only, no vessel observations at all; beneficiary is ESA/Copernicus and polar monitoring policy.

## Notes (Stage 2 verification list)

1. TG01 핵심 미검증 가정: refrozen convoy channel이 S1 EW HH/HV에서 며칠 동안 backscatter 대비를 유지하는가. Vilkitsky 겨울 장면 2–3쌍으로 육안 확인 필요 (P2/P3 metadata 우선, GEE restricted mode 고려).
2. TG01/TG02 검증 데이터 접근성: CHNL transit statistics의 연·월 해상도와 공개 연도 범위를 확인해야 함 (gray literature, WebFetch 1회).
3. Channel과 자연 lead/crack의 구분 가능성이 최대 confounder — linearity, 폭 일정성, drift 정합성으로 분리 가능한지 Stage 2에서 정량 확인.
4. TG02: Sentinel-2 동시각 매칭 장면 수(여름, 결빙 corridor)가 실제로 확보되는지 카탈로그 조회 필요; 부족하면 V 하락.
5. TG03: Sabetta/Pevek 항만 운영 기록의 공개 여부 확인 실패 시 TG03은 Stage 1.5로 강등.
6. TG06: S1_GRD metadata 조회는 quota 부담 낮음 — 가장 먼저 실행할 pilot.
7. Confounders 공통: EW noise-floor scalloping, incidence-angle 의존성, wind roughening (open water false alarms), melt season 대비 저하.
8. Reviewer-2 예상 (TG01): "AIS 없이 만든 traffic proxy의 절대 정확도를 어떻게 보증하나?" → 답: CHNL 총량 대비 상관·편향만 주장하고, 절대 계수는 주장하지 않음.
9. Reviewer-2 예상 (TG02): "ship detection은 새롭지 않다" → 답: 기여는 detection이 아니라 corridor-level exposure measurand.
10. Journal 후보: TG01 → Cold Regions Science and Technology 또는 Marine Policy(SSCI); TG02 → Ocean & Coastal Management; TG06 → Environmental Research Letters.
