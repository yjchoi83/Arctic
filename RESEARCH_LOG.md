# RESEARCH_LOG

## ARC-P1 — hazard-window premise from IABP buoy pairs (2026-09-06)
**Package**: `arctic_explore/stage5/P1/` — PLAN.md (pre-registered), P1_hazard_windows.md,
P1_events.csv (82,440 rows, 5.2 MB), P1_buoy_key.csv. No Earth Engine calls.

**Expected**: 수렴 이벤트의 지속시간이 **일(day) 단위**일 것 — 사전등록 채택 규칙("median ≤ 3 d면 T = 3 d,
아니면 T = p50")이 그 전제 위에 쓰였다. 이벤트 수는 소규모(P1_events.csv가 "small"할 정도)로 예상.

**Observed** (IABP LEVEL1 2016–2025, lat ≥ 70 °N, fix 8.66 M, 부이 1,271 → 쌍 9,884, 이벤트 **82,440**):
- 지속시간 **median 6 h · p75 9 h · p90 18 h**, **T80 = 6 h**. 9개 민감도 조합(밴드 2×3 + 20–100 km p85/p95)
  전부에서 median 6 h 불변.
- **이벤트의 55.9 %가 정확히 6 h** = 정의상 최소값 → 지속시간 분포는 **아래가 절단**되어 있고
  "median 6 h"는 중앙값이 아니라 **검출 바닥**이다.
- 계절 신호는 실재: **winter med 9 h / p90 24 h vs melt med 6 h / p90 12 h**.
- **Laptev/ESS 표본은 얇다**(3계절 합 1,147건, 겨울 17건·쌍 8·부이 14 → 분포 통계 미보고).
  central Arctic이 전체의 55 %인 것은 부이망 배치 편향이지 물리적 사실이 아니다.
- 사후 확인(사전등록 아님): magnitude ≥1 km → med 9 h, ≥3 km → med **15 h**, p90 **36 h**.

**Verdict**: 전제 **기각**. 수렴 이벤트는 일 단위가 아니라 **시간 단위(6–24 h)**다.
사전등록 규칙을 문언대로 적용하면 **T = 3 days**가 되지만 이는 T80 = 6 h와 12배 어긋나고
이벤트의 90 % 이상을 놓친다. 규칙과 데이터가 충돌한다는 사실 자체를 결과로 보고하며,
사후에 유리한 값을 고르지 않았다. 추가로 P1_events.csv는 "small"하지 않다(5.2 MB) — 이벤트 수가
예상보다 3자리수 크기 때문이며, 이는 포맷 문제가 아니라 정보다.

**Next**: (1) **P2는 T = 3 d를 상속하면 안 된다** — 채택 규칙을 재작성할 것.
(2) T를 지속시간만으로 정하지 말고 **hazard magnitude 하한과 함께** 정의할 것(≥3 km면 T는 12–36 h대).
(3) 검출 바닥 문제: 3시간 격자·6 h 최소 조건이 분포를 절단한다 — 1시간 이하 원시 fix를 쓰는 쌍만으로
재실행해 6 h 미만이 실재하는지 확인.
(4) 보간 잡음 검증: 브래킷을 ±3 h → ±1 h로 좁혀 짧고 작은 이벤트가 살아남는지 확인.
(5) Laptev/ESS 겨울(n=17)은 어떤 결론도 지지하지 못한다 — 해당 해역 결론은 P2에서 유보.
