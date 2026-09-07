# ARC-P8 step 3 — 겨울 chokepoint 물리 실증 (P4의 G3 닫기)
Vilkitsky·Sannikov/D.Laptev·Long Strait, freeze-up·winter 2019–2021.
**20 pair**(EW GRD_MD, 12–72 h, EPSG:3413 겹침 ≥50 %), 40 scene **9.2 GB**. 매처는 **Stage 4 R1과 동일
파라미터**의 OpenCV 재구현(`sea_ice_drift`는 PyPI에 없다 — 동일하다고 주장하지 않는다).

## 1. **해협에서 겨울·결빙기 C-band 추적은 작동한다** (P4가 답하지 못한 질문)
| region | season | n_pair | success rate | 평균 노드 |
|---|---|---|---|---|
| Vilkitsky | freeze-up | 4 | **0.377** | 1,068 |
| Vilkitsky | winter | 4 | **0.623** | 1,123 |
| Sannikov | freeze-up | 3 | **0.385** | 1,203 |
| Sannikov | winter | 3 | **0.779** | 2,453 |
| Long Strait | freeze-up | 3 | **0.419** | 2,015 |
| Long Strait | winter | 3 | **0.484** | 2,088 |

**20 pair 전부 유효 벡터 ≥30개**, 전체 평균 **0.510**(최소 0.27, 최대 0.87).
OSI SAF가 62.5 km에서 이 해협들을 통째로 마스크했던 것(P4: Vilkitsky 유효관측 0건)과 정반대로,
**S1 자체는 같은 해협에서 수천 개의 drift 벡터를 낸다.** 해협 위험이 관측 불가능한 것이 아니라
**저해상 산출물이 해상하지 못했던 것**이다.

> **P5의 공백을 메운다**: 결빙기 retrieval success가 **처음 측정**되어 **0.377–0.419 (평균 0.394)** 다.
> 겨울(평균 0.629)보다 확실히 낮다. P5가 낙관 대입으로 쓴 **0.47은 약 19 % 과대**였다.

## 2. 수렴 사건 — 검출되지만 **전부 ≥3 km 미만**
사전등록 정의(divergence < pair별 p10, 연결영역 **면적 ≥100 km²**)로 **19건** 검출.
전부 **winter**이고 **Sannikov 13건·Vilkitsky 6건**, Long Strait 0건, freeze-up 0건
(결빙기는 성공률이 낮아 divergence 장이 성기다 — §1의 0.38–0.42).

| 지표 | 값 |
|---|---|
| 면적 | median 150 km², max 700 km² |
| magnitude | median **0.28 km**, p90 0.53, max **1.39 km** |
| **magnitude class** | **≥3 km: 0건 / 19건 (전부 <3 km)** |
| 관측된 창당 사건율(전 등급) | **0.95 events / observed window** (n=20) |
| ≥3 km 사건율 | **0/20 → rule of three 95 % 상한 0.15 / window** |

**사전등록한 ≥3 km class 실증은 실패했다** — 20개 창에서 0건이므로 "≥3 km 미관측 사건 기대수"는
**계산하지 않는다**(0에서 외삽하지 않는다).

## 3. 미관측 비율 — 등급을 고정하지 않은 진술
관측된 사건 = 실제 사건 × H_episode 이므로, 실제/관측 = 1/H.
chokepoint freeze-up+winter의 `H_episode3`는 **pre 0.196 → during 0.084**.
> 관측 1건당 실제 발생은 **2019–21에 약 5.1건, 2022–24에 약 11.9건**.
> 즉 에피소드 규모 수렴의 **미관측 비율이 80 % → 92 %** 로 올라간다.
절대 건수는 창 수 추정이 프록시라 제시하지 않는다. §2의 사건율 0.95/window는 **<3 km 등급**의 값이고
H_episode3는 **≥3 km** 기준이라 두 수를 곱해 절대수를 만들면 등급이 어긋난다 — 그래서 비율만 보고한다.

## 4. 부이 검증 — **불가능했다**
19개 사건 전부 **반경 100 km 안에 IABP 부이가 없다**(±3 h → ±12 h로 완화해도 동일). 2019–21
freeze-up+winter에 Sannikov 100 km 내 부이 **0기**, Vilkitsky **1기(375 fixes)**, Long Strait 6기지만
사건 시각과 겹치지 않았다. **검증하지 못했다고 적고 대체 진리값을 만들지 않는다.**

## 5. 산출물
`results/P8/quicklooks/` 19개 PNG(before/after + divergence 오버레이), `results/P8/qc_table.csv`
(19행, `decision` 공란, `auto_note`는 "divergence-threshold detection; not visually scored").

## 6. 한계
20 pair·해협 3곳·2 계절·3년은 **존재 증명과 크기 추정까지**다. 사건 정의의 p10 임계는 pair마다 상대적이라
절대 강도를 비교할 수 없다. magnitude는 `평균수렴률 × Δt × √면적`으로 정의했고 P1b의 부이쌍 baseline
(20–100 km)과 **정확히 같은 양이 아니다** — 등급 비교는 근사다. 결빙기 사건 0건은 위험이 없어서가 아니라
**매처 성공률이 낮아 divergence 장을 만들지 못해서**일 수 있다(교락).
