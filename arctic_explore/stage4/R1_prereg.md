# R1 사전등록 (TD05 re-pilot) — 실행 **전** 작성, 2026-09-04

## 0. 왜 사전등록인가
Stage 2의 TD05 근거는 전부 **카탈로그 메타데이터 + IABP 부이 변위**였고 SAR 화소 매칭은 한 번도 돌지 않았다
(D1의 evidence-provenance = `metadata + in-situ`). 즉 "융빙기 C-band drift 추적이 실패한다"는 전제는
아직 **측정된 적이 없다**. R1은 그 전제를 소규모로 실측한다. 결과를 보고 기준을 정하면 무의미하므로
아래 기준을 실행 전에 고정한다.

## 1. 설계
- ROI: Chukchi Sea (대략 lon 190-202E / -170..-158, lat 68-74), 단일 relative orbit의 중첩 footprint.
- 자료: Sentinel-1 EW GRD_MD, HH 편파, ASF 다운로드(~/.netrc Earthdata).
- 표본: **melt (Jul-Aug) pair >=3, winter (Feb-Mar) pair >=3**, pair 간격 1-3 일.
  연쇄 취득(A-B, B-C)으로 pair를 구성해 총 scene 수를 예산(<=12 scenes, R2 몫 포함) 안에 유지한다.
- matcher: 오픈소스 `sea_ice_drift` (Korosov & Rampal 2017, 10.3390/rs9030258) 알고리즘 =
  **feature tracking(ORB) + pattern matching(정규화 상호상관)**. 패키지 설치가 실패하면
  동일 2단 알고리즘을 OpenCV로 재구현하고 **재구현임을 결과 파일에 명시**한다(패키지 원본과 동일하다고 주장하지 않음).
- 양 계절에 **완전히 동일한 파라미터**(탐색창, 격자, 품질필터)를 적용한다. 계절별 튜닝 금지.

## 2. 측정량 (사전 정의)
- 격자: 중첩영역 내 **5 km 간격 노드**. 육지·정착빙 마스크 밖 노드만 사용.
- **success (이진)**: 해당 노드에서 pattern matching 상관 피크가 품질필터
  (peak correlation >= 0.4, peak/second-peak >= 1.2, 변위 <= 탐색창의 80 %)를 통과하면 1.
- **success rate** = success 노드 수 / 유효 노드 수. pair별로 산출하고 계절별로 pair 평균 ± 범위 보고.
- 진리값: pair의 두 취득 시각 사이에 ROI 안에 있는 **IABP 부이**의 실변위(선형 보간).
  공동위치(부이 위치 반경 10 km 내 성공 벡터)가 있으면 벡터 오차(km)를 보고.
  공동위치가 0건이면 **"진리값 없음"으로 명시하고 오차는 보고하지 않는다**(대체 진리값을 지어내지 않음).

## 3. PASS / KILL 기준 (사전 고정)
Δ = (winter mean success rate) − (melt mean success rate), 단위 %p.

| 조건 | 판정 | 의미 |
|---|---|---|
| Δ >= +15 %p | **PASS** | TD05 H1의 방향과 크기가 소규모에서 재현. Tier 1 단독 논문 전제 성립 → GO 유지 |
| +5 <= Δ < +15 %p | **NARROWED** | 방향은 맞으나 크기 미달 → GO 유지하되 제목/측정량을 "실패율"이 아니라 "조건부 성능 저하"로 재조준하고 본 파일럿 수치를 명시 |
| −5 < Δ < +5 %p | **KILL-PREMISE** | 융빙기 실패 전제가 소규모에서 성립하지 않음 → TD05는 GO에서 강등, Tier 1 단독 논문 주장 철회 |
| Δ <= −5 %p | **KILL-PREMISE (역전)** | 전제가 반대 방향 → 동일 강등, 단 "융빙기가 오히려 낫다"는 음성 결과 자체는 short-form 후보로 남김 |

**무효(kill 아님) 조건**: 두 계절 **모두** 유효 노드 대비 success rate < 0.10 이거나 pair당 성공 벡터 < 50개면
matcher/전처리 문제이지 계절 효과가 아니다 → 판정 `INCONCLUSIVE`, TD05는 Stage 3 상태 유지, 재파일럿 필요로 기록.

## 4. 이 파일럿이 보일 수 없는 것 (사전 명시)
- pair 3+3, ROI 1개, 연도 1-2개 → **통계적 유의성 주장 불가**. fold spread도 궤적 단위로 정의되지 않는다.
- 계절 차이에는 wet snow·개활수 wind roughening·입사각·IPF 버전이 교락되어 있고, 소표본에서는 분리 불가.
- 따라서 R1의 산출은 **효과의 존재 여부와 대략적 크기**이며, TD05 본 연구의 결론을 대체하지 않는다.
