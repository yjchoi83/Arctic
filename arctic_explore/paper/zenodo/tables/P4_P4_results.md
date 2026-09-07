# ARC-P4 — chokepoint hazard record from an S1-independent source (OSI SAF OSI-405)
사전등록 `stage5/PLAN.md §C`. 자료 3,043개 일별 파일(2016–2025, Apr–May 제외), **2.3 GB**, 무로그인.

## 1. 핵심 결과: **NSR chokepoint에는 S1-독립 hazard 기록이 존재하지 않는다**
OSI-405는 62.5 km 격자다. 해협 셀은 대부분 **land / close-to-coast / no-ice로 마스크**된다.
`status_flag`가 유효(20/21/22/30)인 비율과, 중심차분으로 **divergence까지 계산 가능한** 비율:

| chokepoint | OSI 격자점 | point-days | valid flag | **divergence 계산가능** | 유효분 중 interpolated |
|---|---|---|---|---|---|
| **Vilkitsky** | 7 | 76,075 | **0 (0.0 %)** | **0 (0.0 %)** | — |
| Sannikov/D.Laptev | 25 | 331,687 | 30,119 (9.1 %) | **399 (0.1 %)** | 25,357 / 30,119 |
| Long Strait | 12 | 139,978 | 35,639 (25.5 %) | **384 (0.3 %)** | 34,157 / 35,639 |
| Kara Gate | 8 | 73,032 | 1,750 (2.4 %) | **26 (0.0 %)** | 1,154 / 1,750 |
| Bering–Chukchi(접근로) | 35 | 492,966 | 89,462 (18.1 %) | **33,489 (6.8 %)** | 27,452 / 89,462 |

**Vilkitsky는 10년치 전체에서 유효 관측이 단 하나도 없다** — 62.5 km 격자에서 해협이 통째로 육지로 분류된다.
나머지 3개 해협도 divergence 계산가능 비율이 0.0–0.3 %이고, 유효값의 대부분이 **interpolated(flag 22)** 라
독립 관측이라 부르기 어렵다. divergence는 4-이웃이 모두 필요해 손실이 한 번 더 일어난다(neighbour-fail
Sannikov 29,719 / LongStrait 35,255).

## 2. H8 판정
> **H8: NSR chokepoint의 2022–2024 freeze-up hazard-observed fraction이 매 연도 0.25 미만.**
> **판정: 4개 NSR chokepoint에서는 검정 불가**(수렴일 자체가 산출되지 않음).
> 유일하게 검정 가능한 **Bering–Chukchi 접근로에서는 기각** — 2022 **0.422**, 2023 **0.177**, 2024 **0.892**로
> 0.25 미만인 해는 2023 한 해뿐이다.

기후값은 사전등록대로 셀별 2016–2025 divergence의 **10퍼센타일을 한 번만** 계산해 동결했다(`climatology.csv`).
Bering–Chukchi 수렴일 3,365건, 기간별 hazard-observed fraction(24 h / 12 h):
pre 2019–21 **0.652 / 0.381** → during 2022–24 **0.475 / 0.246** → post 2025–26 **0.677 / 0.383**.
다른 세 해협은 수렴일이 KaraGate 3건·LongStrait 39건·Sannikov 42건뿐이며 **전부 2025년**이라 기간 비교가 불가능하다.

## 3. QC 퀵룩 (요청 10–15건 대비 **5건**)
수렴일 중 **S1 쌍이 24 h 이내**인 경우만 대상으로 했다. 대상 후보는 22개 날짜(LongStrait 13, Sannikov 9)였으나
쌍 조건을 통과한 것은 **5건, 전부 Long Strait 2025년**이다. Sannikov는 **단일 취득은 24 h 안에 있어도
쌍이 24 h 안에 존재하지 않는다** — PLAN §A 가정 3("취득 1회 ≠ drift 산출")이 실제 자료에서 확인된 것이다.
Vilkitsky는 §1대로 수렴일이 0건이라 대상 자체가 없다.

`results/P4/qc_table.csv` (5행, `decision` 열 공란), `results/P4/quicklooks/` (10 JPEG, 5.1 MB).
**예산 관련 이탈(공개)**: 40 m EW HH 화소 crop 대신 **ASF browse JPEG**를 저장했다. 전체 장면 24개는
~6 GB로 5 GB 예산을 초과하며, OSI SAF에 이미 2.3 GB를 썼다. 따라서 `auto_note`는 자동 판독을 하지 않고
**"UNSCORED — browse JPEG only"**로 채웠다. 육안 판정은 사람이 `decision` 열에 채우는 것을 전제로 한다.

## 4. 한계
(1) 62.5 km는 폭 20–50 km의 해협을 원리적으로 해상하지 못한다 — 본 절의 결과는 OSI-405의 한계이지
해협에 수렴이 없다는 뜻이 **아니다**. (2) 유효값의 다수가 interpolated다. (3) 수렴일 정의(셀별 p10)는
표본이 적은 해협에서 불안정하다. (4) Bering–Chukchi는 NSR chokepoint가 아니라 접근로이며 P2/P3에서
AKcorr_*와 공간 중복이 있다.
