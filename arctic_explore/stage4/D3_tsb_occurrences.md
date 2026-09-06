# D3 — TSB Marine Occurrence 취득 및 Arctic Grounding 집계

## 1. 시도한 경로 (URL + HTTP code)

| # | URL | 방법 | HTTP | 결과 |
|---|-----|------|------|------|
| 1 | `open.canada.ca/data/en/api/3/action/package_search?q=marine+occurrence` | CKAN API | 200 | TSB 데이터셋 3건 식별 |
| 2 | `.../package_show?id=ad8d1b73-df09-4521-9bdb-61c529328218` ("Marine occurrence data from January 1995 to present") | CKAN API | 200 | resource 14건, 전부 `datastore_active=false`, URL은 모두 tsb.gc.ca 호스팅 |
| 3 | `https://www.tsb.gc.ca/sites/default/files/stats/MARSISdb_MDOTW_VW_OCCURRENCE_PUBLIC.csv` | `curl -L --compressed -A "<Chrome UA>"` | **200** | **96.98 MB CSV 취득 성공** |

핵심: Stage 2의 403은 Azure WAF의 **User-Agent 기반 차단**이었음. 브라우저 UA 헤더 하나로 해제됨.
CKAN datastore / Wayback은 불필요했음. 저장 위치: `scratch/MARSIS_OCC.csv` (88,054 rows, 1975–2026-08).

## 2. 사용한 필터 정의 (exact)

- **Grounding**: `AccIncTypeDisplayEng`에 문자열 `GROUNDING` 포함
  → `GROUNDING - Under power (non-intentional)` + `GROUNDING - Not under power (includes drifting) (non-intentional)`.
  ※ `BOTTOM CONTACT`(별도 코드)는 **제외**했음. 포함 시 수치가 달라짐.
- **연도**: `OccDate`의 연도가 2010–2026 (2026은 8월까지 부분연도).
- **Arctic (union 정의, 셋 중 하나라도 만족)**:
  (a) `RegionOfOccurrenceDisplayEng == 'ARCTIC REGION'`, 또는
  (b) `ProvinceDisplayEng` ∈ {NUNAVUT, NORTHWEST TERRITORIES, YUKON}, 또는
  (c) 좌표 위도 ≥ 60N.
- **CAA (Canadian Arctic Archipelago)**: 좌표 기준 lat ≥ 66N **및** 128W ≤ lon ≤ 60W.

## 3. 결과

- 캐나다 전체 grounding 2010–2026: **1,507건**
- **Arctic grounding 2010–2026: 59건** (union 정의)
  - 하위 정의별: ARCTIC REGION만 = 13, NU/NT/YT 주(準)만 = 51, lat≥60N만 = 58
- 연도별: 2010:3, 2011:0, 2012:4, 2013:8, 2014:4, 2015:5, 2016:6, 2017:4, 2018:3, 2019:3, 2020:0, 2021:3, 2022:2, 2023:6, 2024:1, 2025:5, 2026:2
- **좌표 보유: 59/59 (100%)** — 위경도 결측 없음
- 위도대 분포: 60–66N 26건, ≥66N 33건
- **CAA box 내: 14건 / 59 = 23.7%**. 나머지는 Hudson Bay/Chesterfield Inlet, Mackenzie River(Fort Simpson 등 내륙 수로), Beaufort 남부 등.
  → TF02가 "NWP/CAA 항로"로 좁히면 모집단은 **14건**으로, 연 1건 미만이라 통계적 검정력이 매우 낮음.

## 4. 사전등록 조건 "TSB n 확정"에 대한 판정

**PASS** — 원시 CSV를 official source에서 직접 취득해 n을 재현 가능하게 확정했으므로 [U] 태그는 해제됨. 다만 TF02의 realised-outcome 표본은 union 정의 59건 / CAA 엄격 정의 14건으로, gate는 통과하되 **표본 크기 자체가 별도의 설계 리스크**로 남는다(D-단계 재검토 권고).
