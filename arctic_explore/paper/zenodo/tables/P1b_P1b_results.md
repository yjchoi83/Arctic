# ARC-P1b — hazard-state persistence & detection-floor checks
P1과 동일 자료(IABP LEVEL1 2016–2025, lat ≥ 70 °N). 신규 다운로드 없음, GEE 0회. 스크립트 `p1b_step1–3.py`, 중간산출 `scratch/P1b/`.

## 1. Persistence — 대부분의 이벤트에서 측정량이 **정의되지 않는다**
event 종료 후 separation이 pre-event의 **90 %로 회복**할 때까지 시간(3 h 격자, 미회복 = censored). 재계산 82,439건(P1의 82,440과 1건
차이: 쌍별 run 재구성의 경계 효과). **84.6 %는 종료 시점에 이미 90 % 이상**(magnitude < separation의 10 %)이라 그들의 median 3 h는
회복시간이 아니라 **격자 바닥값**이다. 표는 측정량이 성립하는 `relmag ≥ 10 %`(n = 11,295 = 15.4 %), 괄호는 전체 이벤트 기준.

| group | n | cens | med h | p75 | p90 |
|---|---|---|---|---|---|
| winter | 2,620 | 15 % | 27 | 72 | 261 |
| freeze-up | 2,532 | 19 % | 39 | 123 | 297 |
| melt | 6,143 | 18 % | 12 | 54 | 153 |
| mag ≥ 1 km | 11,295 | 18 % | 21 (3) | 69 (3) | 198 (12) |
| mag ≥ 3 km | 10,870 | 18 % | 24 (3) | 72 (21) | 204 (99) |
| mag ≥ 5 km | 8,373 | 20 % | 33 (15) | 99 (63) | 246 (195) |

→ **episode duration(시간 단위)과 hazard-state persistence(수십 시간~수일)는 다른 측정량**이며 freeze-up이 가장 오래 간다.

## 2. Detection floor — P1의 "median 6 h"는 **검출 바닥이 맞다**
native fix 간격 median ≤ 1 h인 부이 **1,111 / 1,271**(fix 8,399,514), 1 h 격자·브래킷 ±1 h·최소 2 h.

| 구성 | THR km/day | n_ev | med | p90 | **frac < 6 h** | mag med |
|---|---|---|---|---|---|---|
| native 1 h | 4.706 | 137,786 | **2 h** | 7 h | **0.858** | 0.97 km |
| control 3 h (동일 부이) | 3.021 | 59,136 | 6 h | 18 h | 0.000 | 1.86 km |

대조군이 P1을 재현하므로 차이는 부분집합이 아니라 **표본화 간격**이 만든 것이다. 단 magnitude로 거르면 안정된다 — ≥3 km는
med 9 h(1 h) vs 12 h(3 h)·6 h 미만 **9.2 %**, ≥5 km는 12 vs 18 h·**2.1 %**. → **작은 이벤트의 지속시간은 표본화율을 따라갈 뿐
고유 시간척도가 없고, 큰 이벤트만 그것을 갖는다.**

## 3. Observability requirement (단일 T 규칙 대체). 단위 h, `p20 / T_exp80 / p80`
**p20** = 개별 이벤트를 확실히 잡는 T(D ≥ T 비율 80 %); **T_exp80** = 기대 포착률 `mean(min(1,D/T)) ≥ 0.8`인 최대 T = **설계 권장값**;
**p80** = 지시된 문자 그대로의 통계량이며 "80 %를 bracket"하지 **않는다**. persistence는 **Kaplan–Meier**로 censoring 반영.

| measurand | ≥1 km | ≥3 km | ≥5 km |
|---|---|---|---|
| duration, 1 h 표본 | 2 / **3** / 7 (n 66,637) | 7 / **10** / 15 (n 11,984) | 8 / **14** / 21 (n 5,420) |
| duration, 3 h 표본 | 6 / **9** / 12 (n 51,683) | 9 / **14** / 21 (n 17,054) | 12 / **20** / 30 (n 8,303) |
| persistence, relmag ≥10 % | 6 / **16** / 168 (cens 18 %) | 9 / **17** / 174 (18 %) | 12 / **24** / 219 (20 %) |
| persistence, 전체 이벤트 | 3 / 3 / 3 (cens 4 %) | 3 / 5 / 63 (11 %) | 3 / 10 / 156 (17 %) |

**두 measurand의 요구가 다르다**: episode를 잡으려면 **6–12 h**, hazard 상태를 놓치지 않으려면 **24 h급**이면 된다. P2는 이 표를
dt = 6/12/24/48/72/168 h 곡선의 기준선으로 쓰되 **magnitude class를 고정하지 않은 수치는 쓰지 말 것**.

## 4. 한계
persistence는 3 h 격자에서만 계산했다(1 h 재계산 미실시). censoring 18–20 %는 KM으로 다뤘으나 p90(198–246 h)은 꼬리라 불안정.
**relmag 10 % 기준은 사후 도입이며 사전등록되지 않았다.** central Arctic·`other` 표본 편향은 P1과 동일하게 남아 있다.
