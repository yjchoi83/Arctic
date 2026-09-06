# ARC-P3…P7 BATCH SUMMARY (2026-09-06)
예산: GEE **S1 메타데이터 전용**(~25분, 15 h 대비 무시), 다운로드 **2.3 GB / 5 GB**(OSI SAF 3,043일 + quicklook 5 MB).
픽셀 판독 없음, charting layer 범위 밖. 사전등록 `stage5/PLAN.md`, `P{3..7}/P*_results.md`, `results/maps/`.

## 논문 진술 (요구된 6개 항목)
**1. NSR chokepoint에서 요구는 한 번도 충족된 적이 없다.**
P1b가 정한 요구(episode 12 h, hazard state 24 h) 대비 — O(12 h)는 688개 region-season-year 셀 **전부에서
미충족**(최댓값 0.278). 25 km 셀 단위 H로 보면 chokepoint의 `H_episode(≥3 km)`는 **손실 이전에도 0.200**,
`H_state`는 0.504였다. 2016–2026 어느 해에도 24 h 요구선(0.8)에 도달한 chokepoint는 없다.

**2. 위성 손실은 이미 있던 격차를 더 벌렸다.**
chokepoint `H_episode` 0.200 → **0.097**(2022–24) → 0.176, `H_state` 0.504 → **0.363** → 0.467. 즉 **에피소드 규모
위험 10건 중 9건이 2022–24에 한 번도 촬영되지 않았다.** 전 지역도 0.267 → 0.151 → 0.245. P2의 DiD는 **미처치
대조군 부재**(16개 지역 전부 retention < 0.9)로 사전등록 형태 추정 불가, 대체 대비는 −25.7 pp [−49.9, +0.6].

**3. 2022–24 hazard-observed fraction.**
NSR chokepoint 4곳에서는 **측정 자체가 불가능**하다 — OSI SAF 62.5 km에서 **Vilkitsky는 10년간 유효 관측 0건**,
Sannikov·Long Strait·Kara Gate는 divergence 계산가능 비율 0.0–0.3 %(대부분 interpolated). 유일하게 가능한
Bering–Chukchi 접근로에서 freeze-up 값은 **2022 0.422 / 2023 0.177 / 2024 0.892** → **H8(매년 <0.25) 기각**.
기간 평균(24 h)은 pre 0.652 → during 0.475 → post 0.677.

**4. 회복은 불완전하고, 이유는 위성 수가 아니다.**
연간 장면 수는 pre의 **88.5 %**(2기→3기인데도). 부족은 **유럽·러시아 구획에 집중** — Barents **46.6 %**,
Sannikov **63.5 %**, Fram 73.6 %, Kara Gate 75.1 % vs 북미·베링 101–141 %. **H6는 지지**(16개 중 15개에서
A-only 반사실이 관측 2022–24를 10 pp 이내 재현, 대부분 ±3 pp)이며, **유일한 예외 Sannikov(+12.3 pp)**는
그 해역의 실제 취득이 1위성 기대치보다도 적었음을 뜻한다. → **서술적 판정: 취득 계획(지리적 배분)의 문제.**
ESA observation scenario 대조는 URL 확보 실패로 **수행하지 못했다**(2026 파일은 존재하지 않음).

**5. 최소 위성 수: NSR chokepoint에서는 "not attainable".**
설계곡선 H_state: 1기 0.28–0.37, 2기 0.41–0.51, 3기 **0.459**(chokepoint 최댓값 0.72). 800개 조합 중 0.8 도달은
**16개(2 %)**, 전부 Fram·Barents 등 대형 고위도 해역. 한계이득 1→2 +0.13, 2→3 **+0.05**로 체감.

**6. 산출물이 영향받았는가 — 미검정.**
DMI-ASIP·DTU S1 drift는 CMEMS에 **존재하나 자격증명이 없어 접근 불가**, OSI SAF SAR drift는 **존재하지 않는다**.
**H9는 기각이 아니라 검정 불가**이며, "영향이 없었다"로 읽으면 안 된다. 논문 범위를 observability로 좁힌다.

## 가장 중요한 단서 조항
- **H는 상한이다**: 취득 1회를 관측으로 세지만 drift 산출은 쌍이 필요하다. 실효값 E = H × retrieval success는
  winter **0.18–0.28**, **melt 0.006–0.009**로 떨어진다. **melt에서는 위성을 늘려도 E가 0.01을 넘지 못한다**
  — 병목이 관측이 아니라 C-band 고전 matcher다. **freeze-up 성공률은 측정된 적이 없다**(낙관 대입과 unknown 병기).
- hazard 지속시간 분포 D·P는 **IABP 부이쌍(central Arctic 편향)** 을 chokepoint로 **외삽**한 것이다.
- 셀 부트스트랩 CI가 좁은 것은 정밀도가 아니라 **같은 지역 셀이 궤도를 공유**하기 때문이다.
- P4의 QC 퀵룩은 요청 10–15건 대비 **5건**(전부 Long Strait 2025)만 성립했고, 예산 때문에 40 m 화소가 아니라
  **ASF browse JPEG**를 저장했다(auto_note는 UNSCORED). Sannikov는 단일 취득은 있어도 **쌍이 없어** 0건이었다.
