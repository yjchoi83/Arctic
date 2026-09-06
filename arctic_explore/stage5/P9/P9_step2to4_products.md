# ARC-P9 steps 2–4 — consequence robustness, products, QC
새 다운로드 없음(DTU는 ARCO 지연로딩). GeoTIFF는 `data/products/`(gitignore, **미커밋**), PNG는 `results/P9/`(커밋).

## Step 2 — H9 임계 민감도
DTU 가용성 정의의 유효화소 임계를 2 / 5 / 10 %로 바꿔 재계산(region-year, n=112):

| valid-pixel 임계 | ρ(availability, H_state3) | p | ρ(H_episode3) | 지역 내 시간축 ρ 중앙값 | 평균 가용성 |
|---|---|---|---|---|---|
| ≥2 % | **0.714** | 9.6e-19 | 0.741 | 0.673 | 0.104 |
| **≥5 %(기본)** | **0.711** | 1.7e-18 | 0.736 | 0.727 | 0.083 |
| ≥10 % | **0.659** | 2.8e-15 | 0.683 | 0.816 | 0.062 |

**세 임계 모두 사전등록 기준 0.5를 넘는다.** 임계를 높일수록 단면 상관은 조금 내려가고
**지역 내 시간축 상관은 올라간다**(0.673 → 0.816) — 엄격한 임계일수록 결측이 S1 취득에 더 민감해지기 때문이다.

> **필수 단서(모든 H9 진술에 병기)**: DTU S1 drift는 **Sentinel-1 입력으로 산출된 제품**이다.
> 따라서 이 상관은 **독립 검증이 아니라 같은 아카이브에서 파생된 두 양의 관계**이며, 인과 방향이 자명한 대신
> "S1과 무관한 제3의 자료로 확인했다"는 주장은 **할 수 없다**. 무계정으로 닿는 S1-비의존 대체물은 존재하지 않고
> (OSI SAF SAR drift 부재), MET Norway 차트는 발행이 고정 일정이라 지표가 되지 못한다(P8 §3).

## Step 3 — 논문용 산출물
| 산출물 | 파일 | 형식 |
|---|---|---|
| H_state·H_episode per 25 km cell, pre/during/post × 3 계절 | `results/P9/H_state3_*.png`, `H_episode3_*.png` (6장) | PNG 커밋 |
| 동일 자료 래스터 | `data/products/H_{state3,episode3}_{season}_{period}.tif` (18장, EPSG:3413 25 km) | **미커밋** |
| 계획 대 실측 장면 수, region별 pre vs post | `results/P9/planned_vs_acquired.png` | PNG 커밋 |
| DTU 가용성 region×year | `results/P9/dtu_availability.png` | PNG 커밋 |
| 해협 divergence 예시 (Vilkitsky 2, Sannikov 2) | `results/P9/example_E00{1,2}_Vilkitsky_*.png`, `example_E0{10,11}_Sannikov_*.png` | PNG 커밋 |

## Step 4 — QC contact sheet
`results/P9/contact_sheet_events.png` — 19개 사건의 before/after + divergence 오버레이를 3열로 배열,
사건별 제목에 지역·날짜·면적·magnitude 표시. **인간 판독용이며 `decision` 열은 공란**이다.
`results/P9/qc_table_p9.csv`는 P8 표에 **P9의 baseline 환산 등급**을 추가한 것:
`mag_buoy_baseline_km`(= mag_S1 ÷ (√area / 49.4 km))과 `mag_class_rescaled`.
환산 결과 **<1 km 10건 · 1–3 km 8건 · ≥5 km 1건** — P8이 "전부 <3 km"로 적었던 집합이
환산 후에는 1건이 ≥5 km로 올라간다(step 1 §1과 일치).
