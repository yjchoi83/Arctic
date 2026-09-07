# ARC-P1 PLAN — hazard-window premise from IABP buoy pairs
작성 2026-09-06, **실행 전**. 이 파일에 적힌 정의는 결과를 보기 전에 고정한 것이며 사후 수정하지 않는다.
Earth Engine은 본 패키지에서 **호출하지 않는다**.

## 1. 질문과 전제
SAR 기반 hazard 갱신 주기 T를 정하려면, 잡아야 할 현상(수렴 이벤트)이 **얼마나 오래 지속되는지**를
먼저 알아야 한다. P1은 그 지속시간 분포를 **SAR와 무관한 in-situ 자료(IABP 부이)**로 측정한다.
부이 쌍의 거리 감소는 SAR에서 독립이므로 §3.5 순환성이 없다.

## 2. 자료 경로
- 원본: `https://iabp.apl.uw.edu/Data_Products/LEVEL1_DATA/LEVEL1_<YYYY>.csv`, YYYY = **2016–2025** (10년). 로그인 불필요.
- 로컬: `arctic_explore/scratch/P1/LEVEL1_<YYYY>.csv`. 2024는 `arctic_explore/scratch/IABP_L1_2024.csv` 재사용.
- 컬럼: `BuoyID,Year,Month,Day,Hour,Min,Sec,Lat,Lon,GPSdelay,BPT,BP,Ts,Ta,Th,Batt`.
- 좌표계: 계산은 전부 **EPSG:3413**(m). 거리 = 유클리드(극지 투영, 100 km 규모에서 오차 무시 가능).

## 3. QC (실행 전 고정)
1. `Lat`/`Lon`이 결측(-999) 또는 범위 밖이면 제거. 2. **Lat ≥ 70 °N만 유지**.
3. 동일 buoy·동일 시각 중복은 첫 값만. 4. 연속 fix 사이 속도 > **120 km/day**면 뒤쪽 fix 제거(전송 오류).
5. 연도 파일 경계에서 부이 궤적을 **BuoyID 기준으로 이어붙인다**.

## 4. 3시간 격자와 쌍 구성
- 각 부이를 **UTC 3시간 격자**(00,03,…,21)에 선형보간. 보간은 **앞뒤 fix가 ±3 h 안에 모두 있을 때만** 수행하고, 아니면 결측.
- 두 부이가 같은 epoch에 모두 존재하면 그 epoch의 **separation s(t)** 를 계산.
- **분석 단위 = run**: `양 부이 존재 AND s(t) ∈ [20, 100] km`인 **연속 epoch 구간**. run 길이 **≥ 8 epoch(24 h)** 만 사용.
- 쌍은 (BuoyID_A < BuoyID_B)로 정렬해 중복 제거.

## 5. 수렴 이벤트 정의 (**결과를 보기 전에 고정**)
- 변화율 `r(t) = [s(t+3h) − s(t)] / 0.125` (km/day). 음수 = 수렴.
- **임계값 THR**: 모든 run·모든 쌍의 `r < 0`을 **한 번에 모아** 그 절댓값의 **90퍼센타일**을 취한다
  (= 전체 음수 rate 분포의 하위 10 % 꼬리). **THR은 한 번만 계산해 동결**하고 계절·해역별로 다시 구하지 않는다.
- **이벤트** = `r(t) ≤ −THR`인 **연속 구간**이 **6 h 이상**(즉 3시간 간격 ≥ 2개) 지속된 것. 중간 완화 허용 안 함(gap 0).
- 기록 항목: `duration_h`, `magnitude_km = s(start) − s(end)`, `mean_rate_km_per_day`,
  `season`, `region`, `pair`, `start_time`, `sep_start_km`.

## 6. 계절·해역 (중간시각·중점 위치 기준)
- 계절: **freeze-up Oct–Dec / winter Jan–Mar / melt Jun–Sep**. **Apr–May는 shoulder**로 분류해 개수만 보고하고 계절 표에는 넣지 않는다.
- 해역(두 부이 중점): `central Arctic` = **lat ≥ 82 °N (우선 적용)**; 그 외 경도로
  `Kara/Barents` 10–100 °E, `Laptev/East Siberian` 100–180 °E, `Chukchi/Beaufort` 180–235 °E(= −180…−125),
  나머지(−125…10, CAA·Greenland·Fram)는 `other`로 보고만 한다.

## 7. T 도출 (**규칙 사전 고정**)
- `T80` = **이벤트의 80 % 이상을 포착하는 관측간격** = 지속시간 분포의 **20퍼센타일**
  (간격 T로 관측할 때 지속 D ≥ T인 이벤트만 확실히 포착된다는 보수적 기준).
- **P2 채택 규칙**: 전체 median duration **≤ 3일이면 T = 3일**, 아니면 **T = p50**.
- `T80`과 채택 T가 다르면 **둘 다 보고**하고 차이를 명시한다(사후에 유리한 쪽을 고르지 않는다).

## 8. 민감도 (사전 지정, 4개 조합 이상)
- 거리 구간: **20–50 km vs 50–100 km** (각각 THR 재계산).
- rate 임계: **p85 / p90 / p95** (각각 THR 재계산, 기본은 p90).

## 9. 정직성 규칙
- 같은 쌍에서 나온 이벤트는 **독립이 아니며**, 한 부이는 여러 쌍에 등장한다. 따라서
  **region–season 칸마다 `n_buoys / n_pairs / n_events`를 모두 보고**하고, **유의성 주장은 하지 않는다**.
- Laptev/ESS 표본이 얇을 것으로 예상된다. 얇으면 얇다고 적고 채우지 않는다.
- n_events < 20인 칸은 **분포 통계(p75/p90)를 보고하지 않고 개수만** 적는다.
