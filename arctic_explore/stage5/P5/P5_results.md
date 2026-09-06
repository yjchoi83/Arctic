# ARC-P5 — effective observability E = H × retrieval success
사전등록 `stage5/PLAN.md §D`. 새 자료 없음(P3의 H × Stage 4 R1의 실측 성공률).

## 1. retrieval success 값의 출처와 그 한계
Stage 4 R1(Chukchi, 동일 relative orbit, 얼음 조건부 SIC ≥ 30 %) 실측:
**winter 0.47**(pooled 2,116/4,520), **melt 0.02**(8/492). 이 값들은 **고전 matcher(ORB feature tracking +
정규화 상호상관)** 의 것이고, ROI 1개·2024년 1년·pair 4+4의 소표본이다.
**freeze-up 성공률은 측정된 적이 없다.** 사전등록대로 두 가지를 병기하며 어느 쪽도 기본값으로 숨기지 않는다.
- **(a) 낙관 대입**: freeze-up에 winter 값 0.47을 그대로 쓴다. freeze-up은 신생빙·젖은 표면이 많아
  겨울보다 낮을 개연성이 크므로 이는 **상한**이다.
- **(b) reported**: freeze-up은 **unknown**으로 비워 둔다.

**DL optical-flow 벤치마크(arXiv:2510.26653, RADARSAT-2, 48개 모델, GNSS 부이, EPE 300–400 m)는
3–5월 pack ice만 시험했다.** 따라서 melt·freeze-up에 그 성능을 옮겨 쓸 근거가 없고, 본 표의 melt 0.02를
"DL이면 해결된다"로 반박할 수도 없다 — 그 계절에서 DL은 시험된 적이 없다.

## 2. E 표 (H_state ≥3 km 기준; 괄호는 H_episode ≥3 km)
| 구간 | 계절 | 전 지역 H_state3 | **E_state (a)낙관** | **E_state (b)reported** | E_episode (b) |
|---|---|---|---|---|---|
| pre 2019–21 | winter | 0.596 | 0.280 | **0.280** | 0.143 |
| during 2022–24 | winter | 0.462 | 0.217 | **0.217** | 0.081 |
| post 2025–26 | winter | 0.539 | 0.253 | **0.253** | 0.114 |
| pre | melt | 0.450 | 0.009 | **0.009** | 0.004 |
| during | melt | 0.348 | 0.007 | **0.007** | 0.002 |
| post | melt | 0.454 | 0.009 | **0.009** | 0.004 |
| pre | freeze-up | 0.639 | 0.300 | **unknown** | unknown |
| during | freeze-up | 0.514 | 0.242 | **unknown** | unknown |
| post | freeze-up | 0.674 | 0.317 | **unknown** | unknown |

**NSR chokepoint만**: winter E_state (a/b) pre 0.258 · during **0.177** · post 0.219;
melt 0.008 / **0.006** / 0.008; freeze-up 낙관 0.270 / **0.205** / 0.285.
episode 기준 chokepoint winter E는 pre 0.115 → during **0.053** → post 0.082.

## 3. 읽는 법
- **H와 E의 간극이 이 패키지의 요점이다.** H_state는 0.35–0.67로 "그럴듯"해 보이지만, 실제로 drift를
  산출해 위험을 판정할 확률 E는 **winter에도 0.18–0.28**, **melt에는 0.006–0.009**로 떨어진다.
- **melt에서는 관측 계획을 아무리 늘려도 E가 0.01을 넘지 못한다** — 병목이 위성 수가 아니라
  **C-band 고전 matcher의 융빙기 실패**이기 때문이다(P6의 설계곡선과 직접 대비된다).
- freeze-up은 **가장 중요한 계절인데 성공률이 미측정**이다. 이 공백을 메우는 것이 다음 실험 1순위다.
- E는 여전히 **상한**이다: H가 취득 1회를 관측으로 세고(PLAN 가정 3), R1의 성공률도 단일 ROI 소표본이다.
