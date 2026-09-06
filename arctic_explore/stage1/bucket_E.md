# Stage 1 — Bucket E: Sensor and coverage science

4 OpenAlex lookups used (2026-09-04, from_publication_date 2022-01-01):
"Sentinel-1B failure coverage impact monitoring" (no relevant hit — supports the coverage gap),
"Sentinel-1 EW noise floor thermal noise removal sea ice HV", "NISAR L-band sea ice coverage
acquisition plan" (no relevant hit), "operational sea ice chart latency timeliness SAR ice service".
Newly verified [V] beyond 00_landscape: E-a "Automatic Detection of Low-Backscatter Targets in the
Arctic Using Wide Swath Sentinel-1 Imagery" (2022, IEEE JSTARS, 10.1109/jstars.2022.3214069);
E-b "Generating Accurate De-Noising Vectors for Sentinel-1: 10 Years of Continuous Improvements"
(2025, Remote Sensing, 10.3390/rs17203474); E-c "Improving satellite-based monitoring of the polar
regions: Identification of research and capacity gaps" (2023, Frontiers in Remote Sensing,
10.3389/frsen.2023.952091).

| ID | Title (<=12 words) | Route/Region | RQ (1 sentence) | Why SAR / which layers | Reference data (named; independence noted) | Closest prior work (title, year, [V]/[U]) | N | R | F | A | V | J | Total | PASS/KILL + reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TE01 | S6: Sentinel-1B gap as natural experiment on Arctic monitoring capability | Pan-Arctic route corridors; NSR chokepoints (Vilkitsky, Sannikov, Long Strait) + Bering/Chukchi | How much did the 2022-2024 single-satellite gap degrade chokepoint hazard revisit and drift-pair availability, and did 1C/1D restore it? | S1_GRD metadata only (mode/pol/orbit/time) gives per-cell revisit and short-repeat-pair counts, the exact quantity drift/deformation and hazard nowcasts consume | OSI SAF ice-drift product coverage/quality flags (independent processing chain); CIS/NIC/AARI chart issue dates (independent of S1 counts); AMSR2 SIC as an always-available fallback baseline | E-c "Improving satellite-based monitoring of the polar regions" 2023 [V] (names capacity gaps, does not quantify the S1B gap) | 3 | 2 | 3 | 2 | 2 | 2 | 14 | PASS — unquantified coverage shock; metadata-only, quota-safe |
| TE02 | EW noise floor, incidence angle and IPF drift in hazard layers | Kara/Laptev landfast reference sites + Bering/Chukchi corridors | How much chokepoint hazard-layer variance and apparent interannual trend is artefact of EW sub-swath noise, incidence angle and IPF denoising-vector versions rather than ice change? | HV EW noise floor and sub-swath scalloping directly set the detectability of leads, low-backscatter smooth ice and open water; uses S1 GRD + IPF version and incidence-angle metadata | Quasi-static landfast-ice polygons as an invariance control; ascending/descending overlaps at differing incidence angle; Sentinel-2 / MODIS ice-water truth; CIS charts as dependent (SAR-derived) baseline only | E-b "Generating Accurate De-Noising Vectors for Sentinel-1" 2025 [V]; E-a "Automatic Detection of Low-Backscatter Targets" 2022 [V]; L1 MC-dropout uncertainty 2023 [V] | 2 | 2 | 3 | 3 | 2 | 3 | 15 | PASS — artefact budget for hazard products; TGRS-shaped |
| TE03 | NISAR first-season Arctic observability and L+C coincidence audit | Arctic route corridors; NSR + Bering/Chukchi/Barents | What fraction of Arctic chokepoints does NISAR actually observe in its first public season, at what repeat and polarisation, and how many <6 h L+C coincidences with S1 exist? | Establishes whether L-band sea-ice science over routes is observationally possible at all; asf_search catalog metadata + S1 catalog intersection, no imagery needed | ASF/Earthdata NISAR catalog vs the published NISAR observation plan (independent documents); S1 catalog from CDSE/GEE (independent mission) | L8 "NISAR sea ice motion validation: preliminary results" 2026 [V] (drift validation only, no coverage audit) | 3 | 2 | 3 | 2 | 2 | 2 | 14 | PASS — PILOT=CATALOG, no login needed; gates bucket-D S4 |
| TE04 | Acquisition coverage of Russian Arctic waters 2019-2026 | NSR: Kara, Laptev, East Siberian, Chukchi seas | Did Sentinel-1 acquisition density over Russian Arctic waters change after 2022 relative to comparable Western Arctic waters, and what does that mean for route transparency? | Only the SAR archive can show whether the observing capacity behind an information vacuum (NSR traffic data withheld) shrank; S1_GRD scene-count metadata by sea and season | ESA observation-scenario / mission-plan documents (independent statements of intent); Canadian/Norwegian Arctic waters as a control region; CHNL transit statistics for exposure context | E-c 2023 [V]; no verified study of post-2022 Arctic acquisition change (searched, none found) | 3 | 2 | 3 | 1 | 2 | 2 | 13 | PASS(weak) — low A (metadata audit); merge candidate with TE01 |
| TE05 | Acquisition-to-usable-hazard latency versus ice-drift decorrelation time | NSR chokepoints + Bering Strait | How often does a chokepoint hazard update reach a user before ice drift has displaced the hazard field beyond its own resolution? | Defines an actionable-observation-window measurand: publication latency + revisit compared against drift speed, using S1 metadata timestamps and drift fields | OSI SAF / IABP buoy drift speeds (independent, non-SAR) set the decorrelation clock; CIS/NIC chart issue-to-validity times as an operational comparison | No verified study found linking SAR latency to drift decorrelation; L4 daily-risk routing 2025 [V] assumes daily updates without latency analysis | 2 | 3 | 2 | 2 | 2 | 2 | 13 | PASS(weak) — F risk: historical publication timestamps may be unrecoverable |
| TE06 | Sentinel-1C/1D onboard AIS payload for Arctic coverage-gap filling | Pan-Arctic | Can the 1C/1D AIS payload compensate for SAR revisit gaps in route monitoring? | Would rely on AIS as the primary observable, not on SAR hazard retrieval | AIS itself (not independent; validation-only under policy) | n/a | 1 | 1 | 3 | 1 | 0 | 1 | 7 | KILL — AIS-centric, violates HARD_CONSTRAINT; V=0 |

## Notes (Stage 2 verification)

- TE01/TE04: GEE `COPERNICUS/S1_GRD` metadata-only counting이 restricted-mode quota 안에서 실제로
  돌아가는지 먼저 확인. 안 되면 CDSE OData catalog로 대체 (scene count query, 이미지 없음).
- TE01: OSI SAF drift product이 S1을 입력으로 쓰는 구간이 있는지 확인 — 있으면 independence 주장이
  약해지므로 chart issue date + AMSR2로 reference를 옮겨야 함.
- TE02: IPF version별 denoising vector 변경 이력(ESA release notes)과 GRD 메타데이터의 IPF 필드
  가용성 확인. landfast reference polygon은 CIS/NorMet chart 또는 coherence 기반으로 정의.
- TE03: `asf_search`로 로그인 없이 NISAR granule 검색이 실제로 되는지, 첫 공개분(2026-06-17 이후)의
  Arctic granule 수가 유의미한지 확인. granule 수가 적으면 TE03은 Stage 2에서 KILL 후보.
- TE04: ESA post-2022 Arctic observation scenario 문서 존재 여부(gray literature 1 query). 없으면
  "정책 변화" 해석은 못 하고 서술적 통계로만 남음 -> TE01로 흡수 권장.
- TE05: CDSE/ASF에 과거 publication timestamp가 남아 있는지가 핵심. processingDate만 있으면
  latency proxy로만 쓸 수 있고 F는 2 이하로 유지.
- 공통: 이 버킷의 카드들은 모두 descriptive audit 성향이 강함. Reviewer-2는 "so what"을 물을 것이므로
  Stage 2에서 각 카드가 어떤 downstream 결정(chart 갱신 주기, routing update rate)을 바꾸는지
  한 문장으로 고정해야 함.
