# 02_stage2_feasibility — Stage 2 결과 (16 토픽, 2026-09-04)

원본: `stage2/<ID>.md`. 파일럿 스크립트/데이터: `scratch/<ID>_*`.
환경 제약: GEE `alpha-earth-app`는 **restricted mode**(noncommercial quota 초과) — 메타데이터와
소규모 reduceRegion(>=200 m)만 사용. `~/.netrc` 없음 -> EARTHDATA_LOGIN=false -> NISAR/ASF는 `PILOT=CATALOG`.

## 판정 요약

| ID | 주제 (축약) | Stage1 | Stage2 | 판정 | 핵심 파일럿 수치 |
|---|---|---|---|---|---|
| TC01 | Convergence/pressure nowcast + besetting case-control (S3) | 16 | **16** | PASS | 2021-11~12 East Siberian 100 km 셀: EW 43 scenes/40 d, median revisit 23.9 h, **usable 0.5-3 d drift pairs 38**. 대조: 2023 Vilkitsky 동기간 9 scenes, **pairs 0** |
| TA01 | SAR-resolution POLARIS가 최적경로를 바꾸는가 (S1) | 15 | **16** | PASS | Vilkitsky 2025-11-21: chart 7 polygons vs SAR **45,784 cells @400 m**; route divergence mean 6.9 km / max 10.8 km; chart route의 **19.9 % 길이가 SAR 기준 negative-RIO** |
| TA03 | Hazard positional staleness / lead-time | 15 | **16** | PASS(조건) | median 연속취득 간격 Vilkitsky 72/96/48 h (2021/2023/2026); IABP 표류 96 h median **22.0 km** (p95 60.3) vs 해협폭 ~55 km |
| TD01 | Melt-season L+C separability (S4) | 15 | **16** | PASS(조건) | NISAR **GCOV 2291 frames** (3 ROI, 2026-06-17~09-01, 64 days, 65.6-77.7N); **NISAR x S1 EW <=6 h = 563** (<=3 h 25); dual-pol은 Chukchi 49 / Laptev 177 / **Barents 0** |
| TD05 | L-band가 융빙기 drift 회수를 복원하는가 | 15 | **16** | PASS | IABP 48 h 변위 melt n=4,468 median **19.58 km** vs winter n=7,662 **11.08 km** (1.77x); melt기 S1 pair 가용성은 오히려 양호(Chukchi median gap 23.8 h) |
| TE01 | S1B gap 자연실험 (S6) | 14 | **16** | PASS | freeze-up 12-72 h drift pair: **110 (2021) -> 23 (2023, -79 %) -> 121 (2025)**; Vilkitsky 2023 freeze-up **pairs 0**, 관측일 비율 30.4 % -> 13.0 % -> 59.8 % |
| TE02 | EW noise floor / incidence angle artefact budget | 15 | **16** | PASS(조건) | HV across-swath gradient **-11.40 dB** (IPF 002.84) -> **-1.45 dB** (IPF 003.71), 잔여 scalloping 9.72 dB p-p; **hazard threshold flip rate 25.89 %** (near swath 44.2 %) |
| TF02 | 결빙이 선박을 미측량 해역으로 밀어내는가 (S7) | 15 | **16** | PASS | NWP 40 segments 중 **28 %만 직접측량 bathymetry**; 알려진 좌초 4건 전부 직접측량 코드 밖; NOAA NOS survey polygons 129건 취득 성공 |
| TB01 | Chokepoint navigability + reliability (S2) | 14 | **15** | PASS(조건) | Vilkitsky: coarse PM가 항해가능일을 **+23~+103 d/season (mean +57)** 과대평가, 5/5 시즌 부호 일치; n=265 scenes, 관측일 192 |
| TJ02 | POLARIS RIO: SAR vs chart | 14 | **15** | PASS(병합) | RIO decision-category **flip rate 59.9 % of area** (58-62 %), n=6 dates, 6,500 cells @2 km. 단 area-weighted rho(chart, SAR) = **-0.12** -> 현재는 분류기 실패를 측정 중 |
| TD04 | ICESat-2 ridge stats를 SAR 독립 기준으로 | 16 | **15** | PASS(조건) | Vilkitsky 2023 Oct-Nov: ATL10 141 granules vs S1 EW 32 scenes, dt<=3 h **18 pairs** (상한); 2025 EW 32->**202**로 회복 -> 실질 30-90 coincidences |
| TI03 | Landfast onset/breakup = 항만 운영창 신뢰도 (S8) | 14 | **14** | PASS(재설정) | Nome 6 시즌: onset 12-08~10-14 (spread **55 d**), clearance spread 39 d; open-water window 132-221 d, mean 172, **CV 20 %**, worst year 132 d |
| TG01 | Convoy channel = AIS-free traffic proxy (S9) | 15 | **12** | **KILL** | corridor 선형이방성 LCR 4.7-9.0 < control 10.9-47.0 (판별 실패); Sentinel-2 74-75N **Nov-Jan 0 scenes** -> 극야 양성 라벨 부재 |
| TH02 | Arctic sea-ice look-alike catalog | 14 | **11** | **KILL** | false-alarm-prone area OND **11.21 %** but per-scene 0-49.7 %; 라벨 독립성 FAIL(S2는 Oct-Feb 부재, chart는 순환); Espeseth JSTARS 2020이 핵심 질문에 이미 답함 |
| TF01 | Incident-fitted multi-layer index (S5) | 14 | **11** | **KILL** | segment 귀속 가능 사고 **n = 0-6** vs 가중치 6개; Dirichlet-100 rank stability rho median 0.717 (p05 0.413), **40 segment 중 32개가 decile 이동**; top-5 중복 median 2/5 |

## KILL 3건의 의미 (soften 하지 않음)
- **TF01 (S5)**: §3.6이 예고한 지점에서 정확히 사망. 다층 합성지수는 "가중치 적합"도 "검증"도 불가 —
  사고 표본이 segment 해상도로 존재하지 않는다. Fu et al. (Cold Reg Sci Technol 2021, 10.1016/j.coldregions.2021.103238)
  [V]가 AIS+위성 빙권 자료로 적합했을 때 **sea area 자체가 유의하지 않았다**는 점이 결정타.
  => PRIORITY_PROBLEMS의 "multi-layer route safety index"는 이번 탐색에서 **연구주제로 성립하지 않음**.
- **TG01 (S9)**: 데이터는 충분하나 극야에 독립적 양성 라벨이 존재하지 않는다. AIS를 배제한 설계에서는
  precision/recall을 정의할 수 없다 -> 정의상 반증 불가.
- **TH02**: bucket H 전멸. S15(oil-in-ice)는 사건 수 조건 실패, TH02는 라벨 계절과 신호 계절이 상호배타.

## Stage 3 진출 (10건) 및 병합 처분
진출: **TC01, TA01, TA03, TB01, TD01, TD04, TD05, TE01, TE02, TF02**
- **TJ02 -> TA01 병합**: 담당 subagent 자체 판정이 "default MERGE" (동일 ROI/chart/S1/RIO surface,
  TA01은 1-D 경로 판독, TJ02는 2-D 면적 판독 -> salami risk). RIO flip rate 59.9 %와 불확실성 밴드는
  TA01 제안서의 area-readout 구성요소로 편입.
- **TE03 -> TD01 병합**: 담당 subagent 판정 "short-form only, fold into TD01". 단 TE03의 독립 성과는
  보존: chokepoint 관측일 비율 0.79-0.83, **북위 ~78N 이북 granule 0건**(Transpolar/Fram/북부 Kara는
  season 1에서 관측 불가), dual-pol 비율 12-38 %, **acquisition->availability latency median 123 h
  (5.1 d)** -> 전술 routing 불가, 계절 통계·물리 검증만 가능.
- **TI03 유보(Stage 3 미진출, 예비군)**: Stage 2 PASS이나 원 프레이밍이 사망하고 N=1로 하락.
  Bahr/Mahoney/Eicken ERL 2024 (10.1088/1748-9326/ad1c7b) [V]가 Nome 포함 알래스카 38개 지역의
  MODIS landfast breakup date를 이미 발표했고, amplitude-only로는 landfast와 표류빙을 분리할 수 없음이
  파일럿에서 확인됨(corr(texture, |delta|) = 0.67). GO 수가 6 미만일 때만 승격.

## 공통 인프라 판정 (모든 토픽 공유)
| 자원 | 판정 | 근거 |
|---|---|---|
| GEE `COPERNICUS/S1_GRD` | 사용가능, 아카이브 대표성 확인 | 6 region-year에서 **ASF 카탈로그의 93-102 %** — "GEE가 CDSE를 과소대표한다"는 위협 기각 |
| NSIDC G10033 NIC weekly SIGRID-3 | 로그인 없이 다운로드, 2026-08-27까지 최신 | TA01/TJ02/TB01/TF02 chart baseline 확보. 단 배포본은 `tc_*, thi, fyi, myi, fast`만 포함 -> **partial concentration 없음** |
| POLARIS | **reduced 4-class RIO만 가능** (SAR·chart 양쪽 모두) | TB01·TJ02 독립 확인; full POLARIS는 raw SIGRID-3 필요, CIS archive 403 |
| NOAA NOS hydrographic survey coverage | 사용가능 (geojson, 129 polygons) | TF02. CHS 엔드포인트는 전부 실패 -> 캐나다 북극은 GEBCO_2024 TID로 대체 |
| IABP buoys | 로그인 불필요, 4,335 `.dat` | TC01/TA03/TD05의 비순환 검증축 |
| NISAR (ASF) | 카탈로그 풍부, **픽셀은 Earthdata 로그인 필수** | 무료 가입으로 해소 가능 — Stage 3 전 최우선 조치 |
| Sentinel-2 광학 검증 | **74-75N에서 Nov-Jan 0 scenes**, Feb 사용불가(SZA 83도) | TG01 사망 원인, TH02 사망 원인, TI03·TF02 제약 |
| TSB Canada occurrence CSV | **HTTP 403 (Azure WAF)** | 좌초 사건 n 확정 불가 -> TF02는 exposure map 프레이밍으로 후퇴 |

## 전 토픽 공통 위험 3가지
1. **분류기 부재**: TJ02가 보여준 rho = -0.12는 crude HH/HV threshold의 공간적 기술이 0에 가깝다는 뜻.
   TA01/TB01/TJ02/TE02는 모두 **훈련된 ice/water(+type) 분류기를 전제조건**으로 삼아야 하며,
   AI4Arctic/ASIP 라벨은 chart 유래라 §3.5 순환성을 완전히 해소하지 못한다.
2. **Incidence-angle artefact가 모든 hazard layer를 오염**: TE02의 flip rate 25.89 %는 TA01·TB01·TJ02의
   측정량에 그대로 전파된다. 정규화가 선택이 아니라 필수.
3. **Outcome 표본의 공간해상도**: besetting은 sub-basin(~1000 km), grounding은 n=4-6.
   segment 단위 통계모형은 불가하며, 사례 일치(case agreement) 수준의 검증이 상한.
