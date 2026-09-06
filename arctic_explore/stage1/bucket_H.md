# Stage 1 — Bucket H: Environmental safety / oil-in-ice, look-alikes, discharge transparency

Lookups used (4/4, in-session verified [V]):
- OpenAlex "oil in ice field experiment SAR detection" (2015+) — no Arctic oil-in-ice event corpus returned.
- OpenAlex "oil spill detection sea ice Arctic SAR" (2020+) — Firoozy et al. TGRS 2021 (10.1109/tgrs.2021.3123908).
- OpenAlex "controlled oil release experiment sea ice remote sensing trial" (2010+) — only open-water trials
  (Sensors 2017 airborne controlled release) + AMBIO 2017 ice-response review; no enumerable >=10 ice events.
- OpenAlex "oil slick look-alike false alarm dark formation SAR" (2020+) — all Mediterranean/Baltic/aquaculture;
  no Arctic sea-ice look-alike catalog found.

**S15 condition test result: FAILED.** No verifiable corpus of >=10 satellite-observable oil-in-ice events or
ice-condition controlled releases could be assembled in-session. Verified ice-relevant items are a single
mesocosm/tank study (TGRS 2021 [V]) and a response-technology review (AMBIO 2017 [V]); open-water releases
(Sensors 2017 [V]) do not satisfy "in ice". Named field trials (SINTEF/JIP Barents oil-in-ice 2009, NOFO
Oil-on-Water, CRREL tank tests, Norilsk 2020, Kolva 2021) are memory-only [U] and cannot be argued from.
Consequence: detection-benchmark cards that need oil truth are killed; the look-alike / negative-class part
of the bucket survives because its truth data (grease ice, low-wind slicks, ice-edge damping) is abundant.

| ID | Title (<=12 words) | Route/Region | RQ (1 sentence) | Why SAR / which layers | Reference data (named; independence noted) | Closest prior work (title, year, [V]/[U]) | N | R | F | A | V | J | Total | PASS/KILL + reason (<=15 words) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TH01 | S15 Oil-in-ice detection benchmark for Arctic shipping corridors | NSR (Kara-Laptev), Barents, Chukchi | Can C-band SAR reliably separate oil among/under sea ice from ice-intrinsic dark features in operational corridors? | S1 EW/IW HH-HV backscatter + damping contrast; layers: OSI SAF ice type/edge, AMSR2 SIC, S2 optical | Documented spill events + controlled releases; none enumerable in ice at satellite scale (independence moot: no truth set) | Toward the Detection of Oil Spills in Newly Formed Sea Ice Using C-Band Multipolarization Radar, 2021 [V] | 2 | 3 | 1 | 2 | 0 | 2 | 10 | KILL: V=0; S15 event condition fails (<10 verifiable ice events) |
| TH02 | Arctic sea-ice look-alike catalog for SAR slick false alarms | Bering-Chukchi + Barents-Kara corridors | Which ice-related dark formations (grease/nilas, wind-shadow, ice-edge damping) drive false slick alerts, and how separable are they? | S1 EW/IW dark-formation geometry, texture, HH/HV ratio, persistence; layers: ice charts (NIC/AARI/Norwegian Met), AMSR2 SIC, S2/VIIRS optical, ERA5 wind ancillary-only for stratification | Sentinel-2 10 m optical (independent, non-SAR) + VIIRS; ice charts (SAR-interpreted, circular -> supporting only); ERA5 stratification not a research object | Oil spill detection by imaging radars: challenges and pitfalls, 2017 [V]; Med/Baltic look-alike studies 2020-2024 [V], none Arctic-ice | 2 | 3 | 3 | 2 | 2 | 2 | 14 | PASS: Arctic ice look-alike class uncharacterised; optical truth independent |
| TH03 | Detection blind-zone mapping for oil response along Arctic corridors | NSR chokepoints + Bering Strait, MIZ | Where and when does ice cover make SAR slick detection physically unreliable, and how large is the resulting blind zone? | S1 EW coverage + backscatter-contrast statistics conditioned on ice regime; layers: S1_GRD metadata, OSI SAF ice type, AMSR2 SIC, landfast masks | Look-alike/negative-class rates from TH02 + optical confirmations; no positive oil truth (weakness); response-asset reach from EPPR/SAR documents | Oil spill response capabilities for ice-covered Arctic waters (review), 2017 [V] | 2 | 3 | 2 | 2 | 1 | 2 | 12 | PASS (marginal): useful for responders; weak falsifiability without oil truth |
| TH04 | Chronic slick-like feature climatology along Arctic shipping corridors | NSR corridor + Bering approaches (aggregate only) | Has the frequency of slick-like dark features along Arctic corridors changed with traffic growth 2016-2026? | S1 EW repeat coverage, dark-formation detection aggregated to corridor cells; layers: AMSR2 SIC, ice charts, CHNL transit counts as exposure proxy | CHNL transit statistics (independent, non-SAR); S2 optical spot checks; NO AIS, no vessel attribution (ethics: aggregate corridor cells only) | Chronic Oil Pollution from Vessels, Southeastern Baltic Sea, 2021 [V]; Suez-entrance operational mapping, 2020 [V] | 2 | 2 | 3 | 1 | 1 | 2 | 11 | KILL: geographic transfer of established method; no independent pollution truth |
| TH05 | L+C look-alike separability: NISAR and Sentinel-1 over ice | Arctic MIZ where NISAR coverage exists (2026 melt season) | Does adding L-band reduce ice-driven false slick alarms relative to C-band alone in the marginal ice zone? | Frequency-dependent damping/penetration contrast between L (NISAR) and C (S1) on the same dark formations; layers: NISAR L-band dual-pol, S1 EW, S2 optical, AMSR2 | S2 optical class confirmation (independent); NISAR PROVISIONAL products via ASF (PILOT=CATALOG, no Earthdata login) | Coincident L- and S-band ASAR over Arctic sea ice, 2024 [V]; L/C incidence-angle dependency, 2024 [V] | 3 | 2 | 1 | 3 | 2 | 2 | 13 | PASS (conditional): novel sensor insight; coincident L+C pair count unproven |
| TH06 | Oil-in-ice drift and fate forecasting from SAR initial conditions | Kara-Laptev NSR segment | Can SAR-observed slick and ice fields initialise oil trajectory forecasts for Arctic response planning? | S1-derived ice drift + slick outline as model initial condition; layers: OSI SAF drift, ERA5 forcing | Trajectory-model hindcasts vs observed slicks (not applicable) | Various oil-drift modelling studies [U] | 2 | 3 | 2 | 2 | 1 | 2 | 12 | KILL: numerical drift modelling violates NO_METOCEAN hard constraint |

## Notes (Stage 2 verification list)

1. S15 조건은 in-session 문헌 조회로 **불충족**. Stage 2에서 gray literature(NOFO Oil-on-Water 연례 시험,
   SINTEF/JIP Barents 2009 oil-in-ice, ITOPF/GISIS, Norwegian Coastal Administration)로 재시도 1회만 허용;
   그래도 >=10건이 안 나오면 TH01은 영구 KILL로 확정.
2. TH02가 이 버킷의 유일한 확실한 생존자. 검증 포인트: (a) S1 EW 장면에서 grease ice / low-wind dark patch가
   Sentinel-2 동시각(<=3 h offset) 확인 가능한 사례가 계절별로 충분한가, (b) 여름 광학 가용성 편향(겨울 truth 부재).
3. TH02/TH03 모두 ice chart를 truth로 쓰면 §3.5 순환성 위반. 광학·in-situ(ASSIST/Icewatch ice-type 관측)로
   최소 하나의 non-SAR reference를 확보해야 함.
4. ERA5 wind는 stratification 공변량으로만 사용(연구 대상 아님)임을 카드에 명시 유지 — NO_METOCEAN 경계 확인 필요.
5. TH03은 V=1이 약점. Stage 2에서 "blind zone"을 검출 가능성이 아닌 **false-alarm rate 상한**으로 재정의하면
   falsifiable해질 수 있는지 검토.
6. TH05는 NISAR-S1 동시 취득쌍(2026-06~09, MIZ) 실제 개수를 asf_search 메타데이터로 세는 것이 첫 관문(F=1 -> 2 상향 가능성).
7. 윤리/출처: 모든 카드는 corridor cell 단위 집계만, 개별 선박 귀속·제재 추적 없음(§3.10). 공개 데이터만 사용.
8. Journal fit: TH02/TH03 -> Marine Pollution Bulletin, 방법 강조 시 IEEE JSTARS; TH05 -> IEEE TGRS.
