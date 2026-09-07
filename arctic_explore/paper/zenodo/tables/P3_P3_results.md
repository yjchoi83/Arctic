# ARC-P3 — feasibility and the hazard-timescale observability metric H
사전등록 `stage5/PLAN.md`. GEE는 S1 **메타데이터 전용**(1,771개 25 km 셀 × 176 region-year, 실행 ~15분,
EECU 예산 15 h 대비 무시할 수준). 산출 `P3_cells.csv`(56,663 cell-season-year), `P3_region_season_year.csv`.

## 1. Feasibility (요약; 근거표는 `P3_feasibility.md`)
| item | verdict | 영향 |
|---|---|---|
| OSI SAF OSI-405 LR drift (62.5 km, 48 h, 일별) | **available, 무로그인** | **STOP 미발동**, P4 가능 |
| DMI ASIP L3 SIC (`SEAICE_ARC_PHY_AUTO_L3_MYNRT_011_023`) | 존재하나 **계정 필요** | P7 정량검정 차단 |
| DTU S1 drift (`cmems_sat-si_glo_drift_nrt_north_d`) | 존재하나 **계정 필요** | P7 정량검정 차단 |
| OSI SAF **SAR** drift | **부재**(OSI-407 중단, drift_mr은 AVHRR) | S1 의존 산출물 대체 불가 |
| MET Norway ice-chart quicklook PNG (1997–2026) | available, 무로그인 | 래스터 한정 → 정량 전파검증 부족 |
| ESA S1 Acquisition Segments ZIP 2015–2025 | available (2026 없음) | P6-7 계획 대 실측 비교 |
| EODMS RCM | 익명 `wes/rapi/search` 200(부분), STAC 403 | 보조만 |
| Capella / ICEYE 공개 카탈로그 | 접근 200, **북극 커버리지 미판정** | 결론에 사용 안 함 |
| CHNL 통과통계 | **연 단위 HTML만**, 2024 이후 동결 | 월 단위 분석 불가 |

**계정은 만들지 않았다.** DMI ASIP·DTU 차단은 P7에서 "consequence not demonstrated"로 이어진다(§P7).

## 2. H 지표 — 정의와 결과
`H = E_D[ Σ_i min(g_i, D) ] / Σ_i g_i` (PLAN §A, length-biased gap weighting을 닫힌형으로 정리한 것;
`g·min(1,D/g) = min(g,D)`). 폐쇄형이라 정렬+누적합으로 정확히 계산했고 순진한 구현과 1e-12 이내 일치를 확인했다.
D는 P1b: episode(1 h 표본) median **8–12 h**(≥3 km) / **11–15 h**(≥5 km), persistence median
**15–39 h**(≥3 km) / **30–45 h**(≥5 km), 계절별로 분리.

| 기간 | 전 지역 H_ep3 | H_ep5 | H_st3 | H_st5 | chokepoint H_ep3 | H_st3 |
|---|---|---|---|---|---|---|
| pre 2019–21 | 0.267 | 0.336 | 0.562 | 0.610 | 0.200 | 0.504 |
| **during 2022–24** | **0.151** | 0.195 | **0.441** | 0.486 | **0.097** | **0.363** |
| post 2025–26 | 0.245 | 0.309 | 0.532 | 0.585 | 0.176 | 0.467 |

- **episode(D≈10 h)는 어느 시기에도 0.27을 넘지 못한다.** chokepoint는 pre에도 **0.20**, during에는 **0.097** —
  즉 **에피소드 규모 위험 10건 중 9건이 2022–24 NSR chokepoint에서 한 번도 촬영되지 않았다**.
- state(D≈30–45 h)는 pre 0.56 → during 0.44로 떨어지고 2025–26에 0.53으로 **부분 회복**한다.
- 셀 단위 부트스트랩 CI는 **매우 좁다**(예: LongStrait freeze-up 2022 0.464 [0.450, 0.478]). 이는 정밀도가
  아니라 **같은 지역 셀들이 동일 궤도를 공유해 사실상 독립이 아니기 때문**이다 — CI를 신뢰구간으로 읽지 말 것.

## 3. 셀 단위 O(24 h) 대 P2 상자 단위
평균은 거의 같다(셀 0.178 vs 상자 0.169, 평균차 +0.009). 그러나 **512개 region-season-year 중 119건(23 %)에서
0.05 이상 어긋난다**. 방향이 뚜렷한 곳:
- **상자가 과소평가**: LongStrait +0.042, BeringChukchi +0.042, VictoriaStrait +0.045, AKcorr_1/2 +0.025.
  큰 상자의 50 % 조건이 부분 통과 취득을 버려서 생긴다.
- **상자가 과대평가**: GreenlandSea_Fram −0.046. 넓은 상자를 자주 스치는 취득이 개별 셀에는 닿지 않는다.
→ **P2의 chokepoint 결론(요구 상시 미달)은 셀 단위에서도 유지되며 오히려 약간 완화된다**(LongStrait 0.043→0.084,
BeringChukchi 0.007→0.049). 어느 쪽이든 24 h 요구선 0.8과는 한 자릿수 차이다.

## 4. 한계 (모든 H 표에 적용)
(1) **취득 1회 = 관측으로 세므로 H는 상한**이다. drift 산출은 쌍이 필요하다 → P5에서 retrieval success를 곱한다.
(2) D·P는 **IABP 부이쌍(central Arctic 편향)** 분포를 chokepoint에 **외삽**한 것이다.
(3) 위험 발생과 취득계획의 독립을 가정한다. (4) 셀 CI는 궤도 공유로 과소하다(§2).
(5) persistence는 censored 값을 관측 하한 그대로 써서 H_state는 **보수적**(낮게)이다.
