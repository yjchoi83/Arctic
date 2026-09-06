# 04_final_ranking — 최종 순위·프로그램 지도·kill 로그 (2026-09-04)

## 0. 결론 요약
60개 후보 -> Stage 1 16건 진출 -> Stage 2 13 PASS / 3 KILL -> Stage 3 제안서 10건.
Stage 3 subagent의 무조건 GO는 **2건**(TD05, TE01)으로 목표 6건에 미달했다. §8의 규정
("If <6 GO, promote CONDITIONAL-GO with conditions stated; report the shortfall")에 따라
아래 **승격 기준**을 적용해 GO를 7건으로 확정하고, 미달 사실과 기준을 함께 공개한다.

**승격 기준 (사후 합리화가 아니라 사전 적용한 단일 규칙)**:
> gate의 성패와 무관하게 **양쪽 분기 모두에서 발표 가능한 결과가 남는가**.
> 남으면 GO(조건 명시), gate 실패 시 주제가 소멸하면 CONDITIONAL-GO 유지.

이 기준으로 TD01, TE02, TA01, TF02, TB01이 승격됐고, TC01·TA03·TD04는 CONDITIONAL-GO로 남았다
(각각 outcome 카탈로그 부재 시 소멸, C1 실패 시 즉시 TE01 흡수, H3 실패 시 TC 2025와 측정량 동일화).

## 1. GO 리스트 (7건, 순위순)

| # | ID | 기여 한 줄 | Journal (primary) | Evidence provenance | 조건 | 실패 분기의 잔존 논문 |
|---|---|---|---|---|---|---|
| 1 | **TE01** | S1B 공백을 자연실험으로 삼아, 위성 손실이 북극 항로 hazard 관측가능성(freeze-up drift-pair 가용성)을 얼마나 붕괴시켰는지 최초로 정량화 | Cold Reg Sci Technol | metadata-is-the-method | 없음 | — (무조건 GO) |
| 2 | **TD05** | 융빙기 C-band 해빙 drift 추적 실패율을 부이로 현장검증해 최초 산출하고, L-band가 이를 복원하는지 쌍대 비교 | IEEE TGRS | metadata + in-situ (화소 미처리) | melt-season tracking-failure pilot (R1) | — (무조건 GO) |
| 3 | **TD01** | NISAR 첫 시즌 L+C 동시쌍으로 융빙기 ice/water·변형빙 분리도의 L-band 기여를 측정하고, 관측 불가 영역을 확정 | IEEE TGRS | metadata → 실화소 필요 | W1 내 무료 Earthdata 계정 + GCOV 1 frame 다운로드 | observability short-form (IEEE GRSL) — 78N 이북 공백·123 h latency는 그 자체로 발표 가치 |
| 4 | **TE02** | SAR hazard layer의 겉보기 신호 중 계측 아티팩트 비율을 예산화하고, 그것이 운항 판정을 뒤집는 비율(25.9 %)로 환산 | IEEE TGRS | real SAR pixels | W1-2 landfast polygon 면적 >=1,500 km2, asc/desc pair >=60 | IPF-drift 단독 short-form (JSTARS) |
| 5 | **TA01** | 40 m SAR hazard field가 chart 기반 대비 최적항로와 잔여위험을 바꾸는지를, 해상도 효과와 분류오차를 분리해 검정 | Cold Reg Sci Technol | real SAR pixels + GIS | W5 분류기 rho >= +0.4 (held-out 해협·시즌) | 판정 불확실성/negative-result 논문 (RESS) |
| 6 | **TF02** | 결빙이 선박을 미측량 해역으로 밀어내는 노출을 가중치 없는 곱 형태로 정의하고 측량적정성 레이어와 교차 | Cold Reg Sci Technol | GIS layers | AUC >=0.75, stratum <=25 %, TSB n 확정 | corridor 측량공백 지도 (28 % 수치는 gate와 무관하게 성립) |
| 7 | **TB01** | 해협 규모 navigable-day/rate 측정량을 정의하고 PM 과대평가(+57 d/season)를 scale 대 retrieval로 귀속 분해 | Remote Sens Environ | real SAR pixels + GIS | W8 Delta_scale/Delta_total CI 하한 > 0.5 | C-band navigable-day 오차예산 (CRST) |

## 2. CONDITIONAL-GO (3건, 승격 보류)

| ID | 조건 | 실패 시 |
|---|---|---|
| TC01 | W3까지 sigma<=50 km/<=24 h besetting 사건 n>=20 (사건 전 24-72 h pair 보유 n>=12) 확보 | 주제 소멸. 대안: outcome을 호송지연 proxy로 교체하거나 TE01/TD05에 흡수 |
| TA03 | W9까지 decision flip-rate 곡선이 Delta t에 대해 비평탄(24 vs 96 h >=20 pp, 4/5 해협 부호 일치) | **즉시 NO-GO**, TE01 §3으로 흡수 (담당 subagent 자체 사전등록) |
| TD04 | W9 H3: 평균 freeboard 통제 후 HV texture 잔여 partial \|rho\| >= 0.25 | 측정량이 TC 2025 (10.5194/tc-19-4701-2025)와 동일해져 kill |

## 3. 다양성 점검 (GO 7건 기준)
- **Bucket**: A(TA01), B(TB01), D(TD01, TD05), E(TE01, TE02), F(TF02), G(TE01 부수), I(TF02 부수),
  J(TA01 부수) -> **8/10 bucket**. 요구치 >=4 충족.
- **Route**: NSR chokepoints(Vilkitsky/Sannikov/Long Strait — TE01, TB01, TA01, TE02),
  Bering-Chukchi(TD05, TD01), Northwest Passage(TF02), Barents-Laptev(TD01, TD05).
  -> **4개 항로군**. 요구치 >=2 충족.
- **공백**: bucket C(ice hazard measurand)와 H(환경안전)는 GO에 없다. C는 TC01이 CONDITIONAL로
  대표하고, **H는 전멸**했다(S15 사건 수 조건 실패 + TH02 라벨 계절 배타성). 이는 축소가 아니라
  탐색 결과다.

## 4. 첫 프로젝트: **TE01**
근거: (a) 유일하게 외부 차단요인이 0 — GEE 메타데이터만 사용하고 로그인이 불필요하다.
(b) 파일럿이 이미 effect size(110->23->121), 독립 교차검증(GEE = ASF의 93-102 %), 반사실
(위성별 분해)까지 확보해 남은 작업이 확장과 집필에 가깝다. (c) 산출물이 **인프라**다 — 커버리지·
재방문·drift-pair 통계는 TA03·TB01·TD05·TC01이 모두 소비하므로, 이것을 먼저 끝내면 나머지 6건의
전제가 동시에 해소된다. 병행 권장: **W1에 무료 Earthdata + CDSE 계정 발급** (TD01·TE02·TD05의
조건을 한 번에 해제하는 최소 비용 조치).

## 5. 토픽별 피벗 2개
| ID | Pivot A | Pivot B |
|---|---|---|
| TE01 | 1C/1D 복원 이후의 회복 곡선만으로 "미래 결측 대비 설계" 논문화 | 커버리지 충격을 ice chart 갱신빈도 변화로 환산해 Marine Policy 계열로 |
| TD05 | Tier 1만으로 C-band 융빙기 실패율 단독 논문 | drift 대신 lead/polynya 지속성 추적 실패율로 측정량 교체 |
| TD01 | observability/latency 단독 short-form (GRSL) | freeze-up 2026-27 데이터 대기 후 재실행 (계절 교체) |
| TE02 | IPF 버전 드리프트만으로 product-stability 논문 | flip rate를 TA01/TB01의 불확실성 입력으로 제공하는 방법론 노트 |
| TA01 | 해상도 효과 대신 **판정 불확실성 전파**를 주제로 RESS | routing 대신 corridor 설계(Bering 양방향 항로) 평가로 전환 |
| TF02 | 좌초 검증을 버리고 순수 측량공백 노출 지도(Marine Geodesy) | ICESat-2 ATL03 photon bathymetry로 공백 일부를 실제 보강하는 retrieval 논문 |
| TB01 | DMI-ASIP을 주 retrieval로 삼고 S1 자체 검색은 검증용으로 | navigable-day 대신 **연간 신뢰도(worst-year)** 단독 측정량으로 축소 |
| TC01 | outcome을 쇄빙선 지원요청/호송지연 proxy로 교체 | deformation observability 논문으로 축소해 TE01과 병합 |
| TA03 | TE01 §3으로 흡수 | staleness를 chart 갱신주기 문제로 재정의(운영기관 대상) |
| TD04 | RDA product를 쓰는 순수 SAR-altimetry 교차검증 | ridge 대신 lead fraction을 측정량으로 |

## 6. 프로그램 지도 (4개 논문 클러스터)
1. **C1 관측능력·아티팩트 기반 (upstream)** — TE01 + TE02 (+TA03 조건부).
   "무엇을 볼 수 있는가, 그리고 그중 얼마가 계측 인공물인가." 나머지 전부의 전제를 공급한다.
2. **C2 융빙기·L+C 검색 물리** — TD05 + TD01 (+TD04 조건부).
   "C-band가 실패하는 계절에 L-band와 고도계가 무엇을 복원하는가."
3. **C3 항해가능성과 판정 효과** — TB01 + TA01 (+TC01 조건부).
   "관측 해상도가 항해가능일·최적항로·위험판정을 실제로 바꾸는가."
4. **C4 해도적정성과 회랑 노출** — TF02 단독.
   "결빙이 선박을 미측량 해역으로 밀어낼 때 무엇이 노출되는가." 수로국 대상 유일 트랙.

의존 순서: C1 -> (C2 || C3) -> C4. C1의 산출물 없이 C3의 측정량은 아티팩트에 오염된다.

## 7. Kill 로그 (총 21건)

### Stage 2에서 사망 (3건 — 파일럿 증거 기반)
- **TF01 / seed S5 (다층 route safety·reliability index)**: segment 귀속 가능 사고 **n = 0-6** vs
  가중치 6개; Dirichlet-100에서 rank rho median 0.717(p05 0.413), **40 segment 중 32개 decile 이동**;
  top-5 중복 median 2/5. 가중치 적합도 검증도 불가. Fu et al. (Cold Reg Sci Technol 2021) [V]가
  AIS+위성으로 적합했을 때 sea area가 유의하지 않았다는 사실이 결정타.
  => CONFIG의 PRIORITY_PROBLEMS 중 "multi-layer route safety index"는 **연구주제로 성립하지 않는다**.
- **TG01 / seed S9 (convoy channel = AIS-free traffic proxy)**: 데이터는 충분(ESS ROI 77 scenes/34 d)하나
  선형이방성이 판별에 실패(corridor LCR 4.7-9.0 < control 10.9-47.0)하고, **Sentinel-2가 74-75N에서
  Nov-Jan 0 scenes** — AIS를 배제한 설계에서 극야 양성 라벨이 존재하지 않아 precision/recall을
  정의할 수 없다. 반증 불가 -> kill.
- **TH02 (Arctic look-alike catalog)**: 라벨 계절과 신호 계절이 상호배타(S2는 Oct-Feb 부재, chart는
  순환). Espeseth et al., IEEE JSTARS 2020 (10.1109/jstars.2020.3017278) [V]가 핵심 질문에 이미
  더 나은 데이터로 답했고 S1 EW는 NESZ가 더 나쁘다. **bucket H 전멸.**

### Stage 1에서 사망 (18건 — 사유별)
- **HARD_CONSTRAINT 위반 (4)**: TE06 (S1C/1D AIS payload — AIS-centric), TG05 (개별 제재선박 귀속 —
  윤리·AIS), TH06 (oil drift/fate 수치모델 — NO_METOCEAN), TI06 (wave/storm 구동 — NO_METOCEAN).
- **Outcome 검증·민감도 없는 합성지수 (6)**: TA06(AHP/fuzzy), TB05, TF05, TF06, TG04, TJ05.
- **RQ가 이미 답해짐 §3.2 (6)**: TC06/TD03(iceberg detection, RSE 2024), TC05(MYI = ice-type 포화),
  TB06(projection 감사), TH04(look-alike 지리적 이식), TJ06(npj 2023이 AIS로 해결).
- **F=0 / V=0 (2)**: TI01 / seed S12 (SAR wave-kinematics bathymetry — SLC·파랑스펙트럼 파이프라인
  부재), TH01 / seed S15 (oil-in-ice — **검증 가능한 사건 10건 조건 불충족**).

### 유보 (Stage 2 PASS이나 Stage 3 미진출)
- **TI03 / seed S8 (landfast = 항만 운영창 신뢰도)**: Nome 6시즌 CV 20 %, worst year 132 d 등
  좋은 수치를 냈으나 (a) Bahr/Mahoney/Eicken **ERL 2024** (10.1088/1748-9326/ad1c7b) [V]가 Nome 포함
  38개 알래스카 지역의 MODIS landfast breakup date를 이미 발표했고, (b) 파일럿에서 amplitude-only로는
  landfast와 표류빙을 분리할 수 없음이 확인됨(corr(texture, |delta|) = 0.67, 겨울에도 하락 없음).
  SLC/coherence 접근이 확보되면 승격 후보 1순위.

## 8. seed 처분 (§6 대비표)
| Seed | 처분 | 근거 |
|---|---|---|
| S1 (SAR POLARIS routing) | **GO** (TA01) | 조건부, 해상도 효과 분리가 관건 |
| S2 (chokepoint navigability) | **GO** (TB01) | RSE 2026에 방향은 부분 선점 -> 측정량·귀속으로 재진술 |
| S3 (convergence nowcast) | CONDITIONAL (TC01) | 사건 georeferencing이 병목 |
| S4 (NISAR L+C) | **GO** (TD01) + GO (TD05) | 데이터 존재 확인, 로그인만 필요 |
| S5 (다층 지수) | **KILL** (TF01) | 사고 표본 부재 |
| S6 (S1B gap) | **GO** (TE01) | 최우선 프로젝트 |
| S7 (chart adequacy x ice) | **GO** (TF02) | AIS-free 정의 확립 |
| S8 (landfast port window) | 유보 (TI03) | ERL 2024 선점 + amplitude 한계 |
| S9 (convoy channel) | **KILL** (TG01) | 극야 라벨 부재 |
| S10 (iceberg) | KILL (TC06/TD03) | RSE 2024가 해결 |
| S11 (rotten ice) | 미진출 (TC03, HOLD) | — |
| S12 (SAR bathymetry) | **KILL** (TI01) | F=0 |
| S13 (port subsidence) | 미진출 (TI02, HOLD) | — |
| S14 (SAR response gap) | KILL (TF05) / HOLD (TJ01) | outcome 부족 |
| S15 (oil-in-ice) | **KILL** (TH01) | 사건 수 조건 실패 |
| S16 (MYI Transpolar) | KILL (TC05) / HOLD (TB03) | ice-type 포화 |
| S17 (uncertainty routing) | TA01에 흡수 | 단독 논문으로는 얇음 |

## 9. 남은 리스크 (프로그램 전체)
1. **훈련된 분류기가 3건(TA01, TB01, TC01)의 공통 전제**이며 아직 존재하지 않는다.
   TJ02의 rho = -0.12가 그 증거다. AI4Arctic/ASIP 라벨은 chart 유래라 §3.5 순환성을 완전히 깨지 못한다.
2. **Outcome 데이터의 구조적 부족**: besetting은 sub-basin(~1000 km), grounding은 n=4-6,
   TSB CSV는 403. 이 프로그램에서 "사고 예측 모형"은 어떤 토픽에서도 불가능하며, 도달 가능한 상한은
   노출 지도 + 사례 일치다. 이를 인정한 것이 TF02가 살아남고 TF01이 죽은 이유다.
3. **계정 하나가 3건의 조건을 동시에 쥐고 있다**: 무료 Earthdata/CDSE 계정 발급이 TD01·TE02·TD05
   Tier 2의 gate를 한 번에 해제한다. W1 최우선 조치.
