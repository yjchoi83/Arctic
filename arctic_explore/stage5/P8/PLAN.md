# ARC-P8 PLAN — P3–P7 배치가 남긴 세 공백 닫기 (실행 전 고정, 2026-09-06)
예산: GEE ≤10 EECU-h(메타데이터), 다운로드 ≤25 GB(S1 EW GRD_MD **최대 20 pair**, CMEMS subset).
자격증명: `copernicusmarine` 로그인 **유효 확인됨**, Earthdata는 `~/.netrc`.

## 1. 닫으려는 공백
(G1) **P7 H9 미검정** — 자격증명이 없어 산출물 전파를 시험하지 못했다.
(G2) **P6의 "배분 문제" 판정이 메타데이터 서술에 머물렀다** — 계획 문서와 램프업 통제가 없었다.
(G3) **겨울 chokepoint 위험이 실제로 존재하는지 미확인** — OSI SAF 62.5 km가 해협을 해상하지 못해
     P4에서 Vilkitsky 유효관측 0건이었다. S1 자체로 위험을 검출해 본 적이 없다.

## 2. Step 1 — 산출물 전파 (G1)
- DMI-ASIP L3 일별 SIC `cmems_obs-si_arc_phy_my_l3_P1D`(2019–2024) + NRT 대응본(2025–26).
- DTU S1 drift `cmems_obs-si_glo_phy-drift-north_my_l4_P1D-m`.
- **가용성 정의**: region 상자 안에서 **유효 화소 비율 ≥ 5 %** 인 날을 "그 지역의 산출일"로 센다.
  region×season×year의 **산출일 수 / 계절 일수** = availability.
- **H9(사전등록)**: availability와 P3의 `H_state3`의 **Spearman ρ ≥ 0.5**(region-year 단위, 계절 통합).
  ρ < 0.5면 **"consequence not demonstrated"를 유지**하고 논문 범위를 observability로 둔다. 재정의하지 않는다.
- MET Norway ice-chart quicklook(Barents/Svalbard, 일별 PNG): **chart 발행 결측일**을 세고
  같은 날의 S1 취득 결측과 사건 수준으로 대조한다. **차트는 고정 일정 발행이므로 이것은 보조 증거이며
  H9의 판정에 쓰지 않는다**(P7에서 이미 밝힌 한계).

## 3. Step 2 — 계획 대 실측, 램프업 통제 (G2)
- sentiwiki document-library에서 **Sentinel-1A/1B/1C acquisition-segment ZIP 2019–2025**를 찾아 받고,
  region×year별 **계획된 EW/IW 커버리지**를 복원해 실제 취득 수와 비교한다. 2025–26은 현행 observation scenario.
- **램프업 통제**: S1C·S1D가 **정규운용(routine operations)** 에 들어간 월 **이후만** 써서 회복적자를 재계산한다.
  사용한 날짜와 **출처를 반드시 명시**하고, 확정 못 하면 그 사실을 적고 보수적(늦은) 날짜를 쓴다.
- **사전등록 판정**: P6의 **"위성 수가 아니라 배분"** 진술은
  **(a) 램프업 통제 후에도 유럽·러시아 구획 적자가 남고 AND (b) 그 구획의 계획 커버리지가 2019–21보다 낮을 때만 유지**한다.
  둘 중 하나라도 아니면 **"unexplained"로 강등**한다. 사후에 조건을 바꾸지 않는다.

## 4. Step 3 — 겨울 chokepoint 물리 실증 (G3)
- 대상: **Vilkitsky, Sannikov/D.Laptev, Long Strait**, **freeze-up·winter 2019–2021**.
- 표본: ASF에서 **EW GRD_MD, 12–72 h 간격, footprint 겹침 ≥ 50 %**(EPSG:3413에서 계산 — 위경도 겹침은
  날짜변경선에서 퇴화한다, Stage 4에서 겪은 오류) **최대 20 pair**.
- 처리: **Stage 4 R1과 동일한 OpenCV matcher·동일 파라미터**(ORB feature tracking → 정규화 상호상관,
  200 m 격자, template 25 px, 탐색창 ±10 km, peak ≥ 0.4, peak/second ≥ 1.2). `sea_ice_drift` 패키지는
  PyPI에 없으므로 재구현임을 결과에 다시 명시한다.
- **divergence**: 성공 벡터를 200 m 격자에서 5 km로 집계해 ∂u/∂x + ∂v/∂y (중심차분).
- **수렴 사건 정의(사전등록)**: 인접 격자 연결요소로 divergence < −(그 pair의 divergence 분포 10퍼센타일)
  이고 **면적 ≥ 100 km²** 인 영역. 사건의 **magnitude** = 그 영역 평균 |수렴| × Δt로 환산한 거리(km);
  가능하면 **≥3 km class**로 필터한다.
- **검증**: 반경 100 km 안의 IABP 부이 실변위와 대조. 부이가 없으면 **"검증 불가"로 적고 지어내지 않는다.**
- **산출**: 관측된 창당 사건율(events per observed window)과, P3의 `H_episode`를 결합한
  **2022–24 미관측 사건 기대수** = (사건율 × 2022–24 창 수) × (1 − H_episode).
- 사건마다 **40 m HH before/after 퀵룩 + divergence 오버레이**를 `results/P8/quicklooks/`에,
  `qc_table.csv`는 `decision` 공란으로.

## 5. 정직성 규칙 (P1–P7과 동일)
사전등록 가설은 실패해도 다시 쓰지 않는다. 표본이 얇으면 얇다고 적고 채우지 않는다.
매처 성공률·부이 대표성·H의 상한 성격 등 **P3–P7에서 살아남은 단서 조항은 전부 유지**한다.
20 pair·해협 3곳·2년은 **통계적 유의성 주장에 못 미친다** — 존재 증명과 크기 추정까지만 한다.
