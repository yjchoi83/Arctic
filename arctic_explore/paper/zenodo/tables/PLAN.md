# ARC-P3…P7 PLAN — 실행 전 고정 (2026-09-06)
자료: Sentinel-1 **메타데이터 전용**(GEE, EECU ≤15 h) + OSI SAF drift + (가능시) DMI-ASIP/DTU.
다운로드 ≤5 GB. **charting layer(구 TF02)는 이 논문에서 제외**한다.
STOP: **OSI SAF drift와 DMI-ASIP이 둘 다 불가일 때만** 중단.

## A. 핵심 지표 H 의 유도 (P3-2)
셀·계절·연도마다 S1 취득 시각열 t_1<…<t_n 에서 **gap** g_i = t_{i+1} − t_i 를 얻는다(G).
위험은 지속시간 D(에피소드) 또는 P(상태)를 갖고 계절 안에서 **발생 시각이 균등분포**라고 둔다.
그러면 위험 시작점이 gap i 안에 떨어질 확률은 **g_i 에 비례**한다(length-biased sampling).
gap g 안에서 시작한 지속 D 의 위험이 **적어도 한 번 취득과 겹칠 확률은 min(1, D/g)**.
따라서
> **H = E_D [ Σ_i g_i · min(1, D/g_i) / Σ_i g_i ]**
`H_episode`는 D = P1b의 **1 h 표본 episode duration**, `H_state`는 P = P1b의 **persistence
(relmag ≥ 10 %)**, 각각 **magnitude class ≥3 km, ≥5 km**와 계절별로 따로 계산한다.

**가정(위반 시 결과가 어떻게 틀리는지 함께 명시)**
1. 위험 발생시각과 위성 취득계획이 **독립**. S1 배경임무는 고정계획이므로 대체로 성립하나,
   계절적 계획 변경이 있으면 H는 낙관 쪽으로 편향된다.
2. D·P는 P1b의 **부이쌍(20–100 km)** 분포를 셀의 위험 모집단으로 대표시킨다. 부이망은
   central Arctic 편향이므로(P1 §3) chokepoint에 그대로 옮기는 것은 **외삽**이다. 명시한다.
3. **취득 1회면 "관측됐다"고 센다.** drift 산출은 실제로 **쌍**이 필요하므로 H는 **상한**이다.
   쌍 요구는 P5의 retrieval success로 별도 곱한다.
4. 셀 gap은 **cell coverage ≥ 0.5**인 취득만으로 만든다(P2와 동일 조작화, 상자 크기 의존성 제거 목적).
5. 계절 경계에서 잘린 gap은 계절 안쪽 길이로만 센다.

집계: 25 km 셀 → region×season×year 평균, **블록 부트스트랩 1,000회, 블록 = 셀**. 95 % CI.
P2의 상자 단위 O(24 h)와 셀 단위 값을 나란히 보고하고 **차이가 나는 지점을 명시**한다.

## B. 지역·격자
P2의 16개 지역(NSR chokepoint 4 + BeringChukchi + AKcorr 1–6 + Barents/Fram/Baffin + CAA 2)을 그대로 쓰고,
각 지역을 **EPSG:3413에서 25 km 격자**로 분할한다. 셀은 지역 상자 안에 중심이 들어오는 것만.

## C. P4 — S1 비의존 hazard 기록
OSI SAF **OSI-405 low-res drift(62.5 km, 2일 변위, 일별)** 2016–2025.
셀별로 **divergence** = ∂u/∂x + ∂v/∂y (중심차분, 62.5 km 격자).
**convergence day** = 그 셀의 **기후값 10퍼센타일 미만**인 날. 기후값은 **셀별로 2016–2025 전체에서 한 번만**
계산해 동결한다(계절·연도별로 다시 구하지 않는다).
**hazard-observed fraction** = convergence day 중 그 셀 위에 **24 h 이내 S1 취득**이 있는 비율(12 h도 병기).
- **H8**: NSR chokepoint의 **2022–2024 freeze-up** hazard-observed fraction이 **매 연도 0.25 미만**.

## D. P5 — effective observability
`E = H × retrieval success`. Stage 4 R1 실측: **winter 0.47, melt 0.02**(얼음조건부 SIC≥30 %).
**freeze-up은 측정된 적이 없다** → 두 가지를 모두 보고: (a) winter 값 대입(낙관 가정, 명시),
(b) **unknown**으로 남김. 어느 쪽도 기본값으로 숨기지 않는다.
DL optical-flow 벤치마크(arXiv:2510.26653)는 **3–5월 pack ice만** 시험했으므로 melt·freeze-up에
그대로 적용할 수 없음을 결과에 적는다.

## E. P6 — 반사실·설계곡선·회복적자
- **OSE(remove-one-platform)**: 2019–2021과 2025–2026에서 플랫폼을 하나씩 제거해 H_state 재계산.
- **H6**: 2019–2021의 **1위성 반사실**이 관측된 2022–2024 H_state를 **지역별 10 pp 이내**로 재현한다.
- 설계곡선: 플랫폼 조합으로 **1·2·3위성** H_state를 만들고 **0.8을 넘는 최소 위성 수**를 보고,
  없으면 **"not attainable"**로 적는다.
- 회복적자: 2025–26 대 2019–21을 **플랫폼·모드(EW/IW)·지역**으로 분해. ESA observation scenario를
  얻으면 러시아 북극 EW 계획 2021 대 2025–26을 비교한다. **위성 수 부족인지 계획 변경인지 서술적으로만** 판정.

## F. P7 — 산출물 영향
DMI-ASIP L3 일별 SIC와 DTU S1-drift의 region×season×year 가용성(2019–2025)을 H_state와 대조.
- **H9**: 두 계열의 **Spearman ρ ≥ 0.5**(region-year 단위). **실패 시 "consequence not demonstrated"로
  적고 논문 범위를 observability로 좁힌다** — 재정의하지 않는다.

## G. 정직성·중단 규칙
자격증명이 없으면 "unavailable (no credentials)"로 적고 **계정을 만들지 않는다**.
사전등록 가설은 실패해도 다시 쓰지 않는다. 부이 분포의 외삽(가정 2)과 취득 1회 근사(가정 3)는
모든 H 표에 각주로 반복한다. 지역 16개·셀 수십 개 규모라 CI는 넓을 것으로 예상한다.
