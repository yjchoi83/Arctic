# Stage 4 — Novelty 재검증 B조 (TF02 / TB01 / TC01 / TA03 / TD04)

**API 가용성 (2026-09-04 세션)**: Semantic Scholar = 전 쿼리 HTTP 429(백오프 20 s + 재시도 2회 포함 전부 실패, 유효 결과 0). OpenAlex = HTTP 429 "Insufficient budget"(일일 예산 소진, 리셋 UTC 자정) → 사용 불가. arXiv = 초기 몇 쿼리만 성공하고 이후 HTTP 429 지속, 성공 구간에서도 본 주제군 대상 2024-2026 히트 사실상 0(해양항해·수로측량 주제가 arXiv 색인에 얇음). **따라서 본 재검증의 실질 근거는 Crossref (from-pub-date:2024-01-01)** 이며, 이 점을 각 판정의 신뢰도 한계로 명시한다.

### TF02
- **RQ**: SAR 기반 ice-forced 측방 변위 × 변위 지점의 측량 부적정성을 곱한 2-레이어 노출량이 회랑을 판별력 있게 계층화하고, 기지 좌초 사례가 그 상위 층에 모이는가?
- **쿼리**: 4건(Crossref 4: NWP 측량 adequacy·좌초, unsurveyed waters 회랑 노출, grounding-bathymetry data gaps, ENC adequacy/CATZOC) + arXiv 2건(`all:"survey adequacy"`, `all:"hydrographic survey"` → 0건/429). S2는 429로 전량 실패.
- **주요 히트**
  - `Satellite imagery for hazard detection: Better use of satellite imagery could help prevent groundings in the Canadian Arctic (2025, The International Hydrographic Review) [V 10.58440/ihr-31-2-a13]` — **가장 근접**. 캐나다 북극 **좌초 7개 지점**에 Sentinel-2 자동 shoal detection + SDB를 적용해 "미측량 수역에서 위성으로 사전 탐지가 가능했다"를 사후 입증. 그러나 (i) 해빙 강제 변위(ice-forcing) 축이 전혀 없고, (ii) 회랑 세그먼트 단위 노출량·계층화가 없으며, (iii) SAR가 아닌 광학 SDB이고 결빙기가 아니다 → TF02의 RQ를 답하지 않음.
  - `Navigational Risks in Ice-Prone Areas: A Case Study of the Arctic Northwest Passage (2025, ASCE-ASME J Risk Uncertain Eng Syst A) [V 10.1061/ajrua6.rueng-1446]` — NWP 위험 사례연구. Crossref에 abstract 부재로 측정량 대조 불가 → 원문 확인 전까지 kill 근거로 쓸 수 없음.
- **VERDICT: NARROWED.** 죽지 않는다(측정량·설계 모두 상이). 다만 프레이밍은 두 가지를 반드시 바꿔야 한다: (1) "미측량 수역의 위험은 관측 불가"라는 동기 서술은 IHR 2025가 반증했으므로 폐기하고, 기여를 **"어디를 먼저 측량/경보할 것인가"의 사전(prospective) 우선순위 배분**으로 좁힌다 — IHR 2025는 사후 사례별 탐지이고 우선순위 지도가 아니다. (2) IHR 2025의 좌초 7지점을 사례 대조 집합의 [V] 공급원으로 흡수해 n=4-6의 취약성을 완화한다.

### TB01
- **RQ**: 해협 스케일 navigable-rate에서 PM 대비 SAR의 +57일 격차 중 footprint 평활(Δ_scale) 몫이 절반 이상인가?
- **쿼리**: 3건(Crossref: chokepoint navigable days SAR vs PM, NSR/Vilkitsky 시즌 길이, PM SIC 스케일) + DOI abstract 조회 2건. arXiv `all:"navigable days"` 0건, S2 429.
- **주요 히트**
  - `Pan-Arctic sea ice concentration from SAR and passive microwave (2024, The Cryosphere) [V 10.5194/tc-18-5277-2024]` — S1 고해상 SIC를 pan-Arctic으로 산출하고 PMW와 대조. **retrieval 축은 겹치지만** 계절 navigable-day 회계도, Δ_scale/Δ_retrieval 귀속 분해도 하지 않음.
  - `Enhancing Sea Ice Concentration Resolution in a Northern Sea Route Strait Using a GAN (2025, JGR: Machine Learning) [V 10.1029/2024jh000281]` — NSR 해협에서 PM SIC 초해상. 스케일 문제의 존재는 공인하되, 항행가능일 측정량이나 귀속 실험이 없음.
  - `Sea ice choke points reduce the length of the shipping season in the Northwest Passage (2024, Communications Earth & Environment) [V 10.1038/s43247-024-01477-6]` — chart 유래 RIO로 NWP 구간별 시즌 길이 산출. **"chokepoint가 시즌 길이를 좌우한다"는 명제는 이미 선행**.
  - `Length of Navigation Season in Current Conditions of Climate Change on the Northern Sea Route (2024, TransNav) [V 10.12716/1001.18.03.02]` — NSR 항해 시즌 길이. abstract 부재로 자료·해상도 미확인.
- **VERDICT: NARROWED.** 헤드라인을 "NSR 해협의 항행가능일을 SAR로 새로 센다"에서 **"coarse PM으로 산출된 기존 시즌 통계의 편향을 스케일 성분과 retrieval 성분으로 귀속한다"**로 고정해야 한다. 시즌 길이 산출 자체는 s43247-024-01477-6·TransNav 2024로 선행이고, 고해상 SAR SIC 산출은 tc-18-5277-2024로 선행이다 — TB01에 남는 것은 **오직 Δ 분해(RQ1)와 신뢰도 통계(RQ3)** 이며, RQ2(부호 일관성)는 단독으로 논문을 지탱하지 못한다. 사전등록된 kill 조건(Δ_retrieval 우세)의 중요도가 상승한다.

### TC01
- **RQ**: 사건 24-72 h 전 S1 유래 convergence가 SIC/chart baseline 위에 besetting을 추가 설명하는가(matched case-control)?
- **쿼리**: 4건(Crossref: besetting × convergence case-control, deformation nowcast besetting, NSR ice entrapment 예측, escort/pressure 운용 경보) + arXiv 2건(`all:"besetting"`, `all:"sea ice convergence"` → 0건/429). S2 429.
- **주요 히트**: 2024-2026 구간에서 **besetting을 결과변수로 삼은 관측 기반 case-control 논문은 발견되지 않음**. 인접군은 전부 모델링·시뮬레이션 계열 — `Dynamic risk analysis of escort operations in Arctic waters (2025, Ocean Engineering) [V 10.1016/j.oceaneng.2025.122565]`, `Prediction of ship following behavior in ice-covered waters in the NSR (2024, Ocean Engineering) [V 10.1016/j.oceaneng.2024.116939]`, `Modeling Impact of Sea Ice on Ship and Offshore Structures (2025) [V 10.5957/ssc465]`. 변형장 측면 인접군 `Scale invariance in kilometer-scale sea ice deformation (2025) [V 10.5194/egusphere-2025-311]`, `Community Challenge for Image-Derived Observation of Sea Ice Drift and Deformation (2026) [V 10.5194/egusphere-2026-4668]` — 모두 변형장 자체의 통계·산출 비교이며 선박 결과변수와 연결하지 않음.
- **VERDICT: SURVIVES.** 다만 위 Community Challenge는 drift/deformation 산출의 산출물 간 산포를 정량화하므로, TC01의 convergence 추정 불확실성 처리에서 반드시 인용·반영해야 한다(무시하면 Reviewer-2의 1순위 공격점). 단, Crossref 단독 근거이므로 S2/OpenAlex 복구 후 1회 재확인 권고.

### TA03
- **RQ**: 마지막 SAR 취득 이후 경과시간(Δt)에 따라 hazard 위치오차가 어떻게 커지며, 그 열화가 route/hazard 결정을 뒤집는 knee와 decision half-life는 어디인가?
- **쿼리**: 7건(Crossref 3 + arXiv 4). arXiv는 `all:"sea ice" AND all:"positional uncertainty"`, `all:"ice chart" AND all:"lead time"`, `all:"sea ice drift" AND all:"persistence forecast"`, `all:"sea ice"+route planning+uncertainty` 전부 0건(다중 구절 AND는 arXiv 색인에서 사실상 무의미). S2 429 3회.
- **주요 히트 및 배제 사유**
  - `Arctic sea ice predictability on daily-to-weekly timescales: sensitivity to initial positional errors under different rheology formulations (2026, EGUsphere/TC preprint) [V 10.5194/egusphere-2025-6379]` — **제목만 보면 가장 위협적**이나, 실제로는 결합 빙-해양 모델(aEVP vs BBM)에 합성 변위 섭동을 주입한 10일 앙상블 예측가능성 실험(1997년 1-3월)이다. 관측 나이(observation age)도, 실측 표류 기반 위치오차 예산도, 결정 뒤집힘도 다루지 않음 → **TA03의 RQ와 다름**.
  - `Evaluation and Decision-Making Optimization of Arctic Navigation Meteorological and Sea Ice Information Websites (2024, JMSE) [V 10.3390/jmse12071044]` — "적시성(timeliness)"을 언급하지만 웹사이트 서비스 품질의 지표체계 평가이며, 위치오차의 시간감쇠를 물리적으로 측정하지 않음 → 무관.
  - `Comparative Analysis of Ice Datasets to Inform Decision Support Models for Winter Navigation (2025, OMAE) [V 10.1115/omae2025-156595]` — 데이터셋 간 비교이나 latency/age를 측정량으로 삼지 않음.
- **VERDICT: SURVIVES.** Stage 3에서 [U]로 남았던 "선행 부재" 주장을 **본 세션 Crossref 7쿼리로 재실행하여 동일 RQ의 선행 연구가 없음을 확인**했다. 다만 근거 API가 Crossref 단독이므로 "선행 부재"는 **[V]가 아니라 근거가 보강된 [U]**로 유지한다(§3.1: 부재의 증명은 검색 커버리지에 종속). 원고 전 S2/OpenAlex 복구 시 동일 쿼리 재실행이 여전히 필수 조건이다.

### TD04
- **RQ**: 동일 S1 deformed-ice 산출물을 chart 기준으로 평가할 때와 ICESat-2 ridge 통계 기준으로 평가할 때 skill 격차의 부호와 크기는 얼마인가?
- **쿼리**: 4건(Crossref 3: ICESat-2 ridge × S1 검증, ridge sail density SAR retrieval, chart 순환성·독립 참조 + DOI 정본 조회 1). arXiv `all:"ice ridge"` 429. S2 429.
- **주요 히트**
  - `Sea ice freeboard extrapolation from ICESat-2 to Sentinel-1 (2025, The Cryosphere) [V 10.5194/tc-19-4701-2025]` (Kortum et al.) — **TD04가 인용한 "TC 2025"의 정본 확인 완료**. 초록 원문상 측정량은 **mean freeboard의 2차원 외삽**으로, HV 후방산란 강도로 화소를 정렬한 뒤 누적분포 정합으로 altimetry freeboard를 매핑한다(10-11월 초겨울 한정). **ridge 통계(sail 밀도/간격/p90)도, ice chart 평가도 수행하지 않는다** → TD04의 "측정량이 다르다"는 주장은 **원문 근거로 확인됨**.
  - 선행 프리프린트 `[V 10.5194/egusphere-2024-3351]`, `[V 10.36227/techrxiv.170492478.89653191/v1]` 동일 계열. 그 외 `Sea-ice ridges are a major component of Arctic sea-ice export through the Fram Strait (2025) [V 10.5194/egusphere-2025-5511]` — ridge를 다루나 수송량 연구이며 SAR hazard 산출물 평가가 아님.
- **VERDICT: SURVIVES.** TC 2025 대비 차별성은 [V] 근거로 성립한다. 단 tc-19-4701-2025가 **바로 HV 강도로 freeboard를 설명한다**는 사실이, TD04의 H3 게이트(mean freeboard 통제 후 HV texture의 잔차 skill partial |ρ| ≥ 0.25)를 통과하기 더 어렵게 만든다는 점을 리스크로 승격해야 한다 — 게이트 실패 시 즉시 KILL이라는 Stage 3 구속 조건은 유지가 아니라 강화가 맞다.

## [U] 재검증
- **TF02 / TSB 캐나다 좌초 전수 n** — **[U] 유지**. 본 세션에서 별도 데이터 사냥은 담당 외(다른 에이전트 소관)로 수행하지 않았고, 문헌 API만으로는 전수 카운트를 확정할 수 없음. 명명 4건만 [V] 상태 그대로. 단 IHR 2025 [V 10.58440/ihr-31-2-a13]가 캐나다 북극 좌초 **7지점**을 다루므로, 전수 n 확정과 무관하게 사례 집합을 [V] 근거로 확장할 경로가 새로 생김.
- **TF02 / "TSB occurrence CSV의 미러가 존재하지 않는다"** — **[U] 유지**. Stage 3의 근거는 CKAN 정본 URL 403 + `bst-tsb.gc.ca` 403 관찰이며, 이는 "미러 부재"의 증명이 아니라 "두 경로에서 실패"의 관찰이다. 부재 주장은 원리상 전수 탐색 없이 [V]가 될 수 없으므로 본문에서는 "확인된 두 경로가 차단됨"으로만 서술할 것.
- **TD04 line 57 / 2018-21 ROI의 chart 연속성** — **[U] 유지**. 본 세션은 GEE 및 chart 아카이브 접근이 금지·범위 외였고, 문헌 API로는 특정 ROI·기간의 NIC/AARI 발행 연속성을 확인할 수 없음. W1 착수 전 G10033 인벤토리 직접 조회로만 해소 가능.
- **TD04 / 인용 "TC 2025" = 10.5194/tc-19-4701-2025** — **[V] 승격**. Crossref 정본: Kortum et al., "Sea ice freeboard extrapolation from ICESat-2 to Sentinel-1", *The Cryosphere*, 2025. 측정량 = mean freeboard 2D 외삽(HV 강도 정렬 + 누적분포 정합, 10-11월). ridge 통계·chart 평가 부재 확인 → TD04의 측정량 차별성 성립.
- **TA03 line 40 / "선행 연구 부재"** — **근거 보강된 [U]**. Stage 3의 OpenAlex 429 실패를 본 세션 Crossref 7쿼리로 대체 실행했고 동일 RQ의 선행은 발견되지 않았다. 최근접 후보 [V 10.5194/egusphere-2025-6379]는 모델 초기 위치오차 민감도 실험으로 RQ가 다름을 초록 원문으로 확인. 그러나 S2·OpenAlex가 모두 429였으므로 검색 커버리지가 단일 API에 국한 → **[V]로 승격하지 않는다**.
