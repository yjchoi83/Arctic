# ARC-P2 — observation deficit, observability curves, difference-in-differences
자료: GEE `COPERNICUS/S1_GRD` **메타데이터 전용**(픽셀 접근 없음). 16 지역 × 2016-01…2026-09, EW+IW GRD,
176 region-year 조회, 실행 ~6분 — **EECU는 예산 12 h 대비 무시할 수준**. 688 region×season×year 셀.
산출 `P2_tables/curves/cells/retention.csv`, 사전등록 `PLAN.md`.

**PLAN 대비 이탈 1건(공개)**: GRD는 한 pass가 여러 slice로 분할되어 slice 단위 coverage로는 큰 지역이 영원히
50 %에 못 미친다 → 동일 platform·pass·15분 이내 slice를 **한 취득으로 묶고 coverage 합산**(≤1.0). **라벨 오류
(PLAN §0)**: 브리프의 "40 NWP segments"는 실제로 **Bering→Point Barrow 알래스카 회랑**이고 Northwest Passage가
아니다 → `AKcorr_1…6`로 개명, BeringChukchi와 중복 명시, 진짜 CAA 2개 지역 추가.

## 1. Retention (2022–24 장면 수 / 2019–21) 과 대조군
**lost (<0.5, 9개)**: Sannikov_DmLaptev 0.310 · VictoriaStrait 0.329 · LongStrait 0.365 · LancasterSound 0.428 ·
KaraGate 0.438 · Barents_Svalbard 0.455 · Vilkitsky 0.457 · GreenlandSea_Fram 0.471 · AKcorr_6 0.481.
**intermediate (0.5–0.9, 7개)**: BaffinBay 0.508 · AKcorr_5 0.663 · AKcorr_4 0.675 · AKcorr_3 0.679 ·
AKcorr_1 0.780 · AKcorr_2 0.822 · BeringChukchi 0.846.
**kept (≥0.9): 0개.**

> **대조군 목록: 없음.** 후보 3개(Barents 0.455, Fram 0.471, Baffin 0.508)를 포함해 **16개 지역 전부가
> 최소 15 % 이상을 잃었다.** S1B 상실은 지역별 자연실험이 아니라 **북극 전역 동시충격**이었고,
> 사전등록한 DiD의 **미처치 대조군은 존재하지 않는다**. 이는 TE01의 "자연실험" 프레이밍에 직접 타격이다.

## 2. DiD — 사전등록 형태로는 추정 불가, 용량반응으로 대체(사후 명시)
결과변수는 region-year 셀(계절 3개 window 가중평균), 블록 부트스트랩 1,000회(블록 = region). 대조군이 없으므로
**lost vs intermediate(고용량 vs 저용량)** 대비를 **사후 분석임을 명시하고** 산출한다 — 양쪽 모두 처치를 받았으므로
**진짜 효과를 과소추정**한다.

| 결과 | lost pre→during→post | intermediate pre→during→post | DiD (95 % CI) |
|---|---|---|---|
| **O(24 h)** | 0.393 → **0.025** → 0.229 | 0.117 → 0.006 → 0.134 | **−25.7 pp [−49.9, +0.6]** |
| **O(12 h)** | 0.012 → 0.000 → 0.007 | 0.016 → 0.000 → 0.036 | +0.4 pp [−2.4, +4.3] |

- **H1: 평가 불가(사전등록 형태) / 미충족(대체 대비)** — kept 그룹이 없어 지정 대비를 만들 수 없고, 대체 대비는
  −25.7 pp로 20 pp를 넘지만 **CI가 0을 포함**한다.
- **H2 판정: 기각.** lost의 2025–26은 pre 대비 **−16.4 pp [−31.1, −4.6]** — 10 pp 이내 회복이 아니며 CI가 0을 제외한다.
  O(12 h)의 H2는 −0.5 pp로 "충족"처럼 보이나 **애초에 pre 수준이 0.012라서 그런 것**이므로 성공으로 읽으면 안 된다.
- **설계 위협(중대)**: 용량 그룹이 위도·기저관측력과 **공선**이다 — retention vs 위도 Spearman **ρ = −0.556 (p .025)**,
  vs pre-O24 **ρ = −0.461 (p .073)**. pre 수준이 0.393 대 0.117로 달라 **평행추세 가정이 성립하지 않는다.**
  고위도일수록 궤도가 겹쳐 기저 O24가 높았고, 그래서 위성 하나를 잃을 때 더 많이 무너졌다.

## 3. 요구 오버레이 (P1b: episode 12 h, hazard state 24 h; met O≥0.8 / partial 0.5–0.8 / not met <0.5)
| 연도 | 2016–18 | 2019–21 | **2022–24** | 2025 | 2026* |
|---|---|---|---|---|---|
| O(24 h) met / partial | 9 / 11 | 22 / 10 | **0 / 0** | 4 / 2 | 3 / 3 |
| O(12 h) met / partial | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
`*2026`은 melt 계절이 잘린 부분 셀 포함(688셀 중 16셀 partial flag).

- **12 h episode 요구는 688셀 전부에서 한 번도 충족된 적이 없다**(O12 max 0.278) → S1 단독으로 **도달 불가**.
- 24 h 요구를 한 번이라도 충족한 지역은 **4개뿐**: GreenlandSea_Fram(2016–2026 20셀), LancasterSound(7),
  Barents_Svalbard(9, 2018–21만), BaffinBay(2, 2025–26). **2022·2023·2024는 전 지역 0셀.**
- **결정적**: **NSR chokepoint 5곳은 어느 해에도 24 h 요구를 충족한 적이 없다** —
  pre 기간 평균 O24가 Vilkitsky 0.061 · Sannikov 0.048 · LongStrait 0.084 · KaraGate 0.312 · BeringChukchi 0.002.
  즉 **운용상 가장 중요한 해협들은 S1B 상실 이전에도 관측요구를 만족한 적이 없다.**

## 4. 민감도 (coverage 임계 0.3 / 0.5 / 0.7)
kept 지역 수 **0 / 0 / 0**, O12 최댓값 **0.356 / 0.278 / 0.189**(어디서도 0.5 미달),
chokepoint pre-O24 평균 **0.178 / 0.101 / 0.098**. **주요 결론 3개는 임계에 무관하게 유지된다.**

## 5. 한계
지역은 상자 근사이고 O(dt)는 상자 크기·형상에 민감하다(큰 고위도 상자가 유리). AKcorr_*와 BeringChukchi는 공간
중복이라 부트스트랩 블록이 완전 독립이 아니다. retention은 **장면 수**이지 관측 품질이 아니다. 지역 16개는 블록
부트스트랩에 적어 O(24 h) CI 폭 50 pp는 그 결과이지 정밀도가 아니다. 2026은 8월까지다. **픽셀은 읽지 않았다.**
