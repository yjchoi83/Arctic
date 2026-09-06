# ARC-P2 PLAN — observation deficit, observability curves, difference-in-differences
작성 2026-09-06, **실행 전 고정**. 자료는 **Sentinel-1 메타데이터 전용**(GEE `COPERNICUS/S1_GRD`,
`size()` / `aggregate_array`). **픽셀 접근 없음.** EECU 예산 ≤ 12 h.

## 0. 실행 전에 발견한 라벨 오류 (그대로 보고)
브리프의 "the 40 NWP segments from Stage 2"를 열어 보니 좌표가 **(−168.75, 65.75) → (−159.5, 71.34)**,
즉 **Bering Strait → Chukchi → Point Barrow의 알래스카 회랑**이다. Northwest Passage(캐나다 북극군도)가
아니다. Stage 2가 NOAA **NOS**(미국) 측량 폴리곤을 쓰면서 "NWP"로 이름 붙인 것이 원인으로 보인다.
- 지시대로 40 세그먼트를 **6개 sector로 집계**하되 이름은 **`AKcorr_*` (Bering–Chukchi–Beaufort 알래스카 회랑)**로 단다.
- 이 회랑은 브리프가 따로 요구한 **Bering/Chukchi 지역과 공간적으로 겹친다** → 두 집합을 **독립 표본으로 쓰지 않으며**,
  DiD의 region-year 블록 부트스트랩에서 겹침을 명시한다.
- 진짜 NWP가 패키지에서 통째로 빠지므로 **CAA 2개 지역(Lancaster Sound, Victoria Strait)을 추가**하고
  "브리프 외 추가"로 표시한다.

## 1. 지역 (모두 위경도 상자, EPSG:4326)
NSR chokepoint: `KaraGate` 57–60.5 E / 70.0–71.0 N · `Vilkitsky` 100–106 E / 77.3–78.4 N ·
`Sannikov_DmLaptev` 137–145 E / 72.7–75.2 N · `LongStrait` 175–180 E / 69.5–71.0 N.
접근로: `BeringChukchi` −172…−166 / 65.5–69.0 N.
알래스카 회랑 `AKcorr_1…6`: 40 세그먼트를 7·7·7·7·6·6개씩 6 sector로 나누고 각 sector의 bounding box를
**위도 ±0.5°, 경도 ±1.0°** 확장.
후보 대조군: `Barents_Svalbard` 15–35 E / 74–78 N · `GreenlandSea_Fram` −10…5 / 76–80 N ·
`BaffinBay` −65…−55 / 70–75 N. 추가(브리프 외): `LancasterSound` −90…−80 / 73.5–75 N ·
`VictoriaStrait` −105…−96 / 68–70.5 N.
**대조군은 가정이 아니라 §3의 retention 수치로 확정**하며, 후보 전부의 retention을 공개한다.

## 2. 취득 정의와 지표
- 기간 2016-01-01 … 2026-09-01, `instrumentMode ∈ {EW, IW}`, GRD, 편파 무관.
- **coverage** = `area(scene ∩ region) / area(region)`. **coverage ≥ 0.5인 장면만 "취득"으로 센다.**
  브리프의 "footprint overlap ≥ 50 %"를 **지역 기준**으로 조작화한 것이다(chokepoint는 장면보다 작고,
  장면–장면 겹침을 위경도에서 계산하면 날짜변경선에서 퇴화한다 — Stage 4에서 실제로 겪은 오류).
- 계절: freeze-up Oct–Dec / winter Jan–Mar / melt Jun–Sep. **Apr–May는 shoulder로 따로 보고.**
- region × season × year마다: 플랫폼별(S1A/B/C/D) 장면 수, 연속 취득 간격의 **median·p90**,
  **drift pair 수** = 간격이 **12–72 h**인 취득 쌍(양쪽 coverage ≥ 0.5).
- **O(dt)** = 계절 구간에서 "간격 ≤ dt인 연속 취득쌍이 덮는 시간의 합" / "계절 총 시간".
  dt = 6, 12, 24, 48, 72, 168 h. 계절 경계 밖으로 넘는 구간은 잘라서 더한다.

## 3. Treatment (사전 고정)
`retention = (2022–2024 장면 수) / (2019–2021 장면 수)`, 지역별.
**lost = retention < 0.5**, **kept = retention ≥ 0.9**, 그 사이(0.5–0.9)는 **intermediate로 별도 보고**하고
DiD 주분석에서 제외한다. 대조군 목록은 이 계산 결과로 결정한다.

## 4. DiD (사전 고정)
- 결과변수: **O(24 h)** (P1b의 hazard-state 요구, ≥3 km class) 및 **O(12 h)** (episode 요구).
- 구간: **pre 2019–2021 / during 2022–2024 / post 2025–2026** (1C 정기운용 2025-04부터, 1D 포함).
- 추정: `DiD = (lost_during − lost_pre) − (kept_during − kept_pre)`, region-year 셀 단위.
- **블록 부트스트랩 1,000회**, 블록 = **region**(같은 지역의 연도는 함께 재표집). 95 % CI.
- **H1**: lost의 O(24 h) 하락이 kept보다 **≥ 20 pp** 크고 CI가 0을 포함하지 않는다.
- **H2**: lost가 2025–2026에 pre 수준의 **10 pp 이내**로 회복한다.
- 두 판정 모두 보고하며, 실패해도 재정의하지 않는다.

## 5. 요구 오버레이
region × season별 O(dt) 곡선에 P1b 요구선을 얹는다: **12 h = episode**, **24 h = hazard state**.
연도별로 `met (O ≥ 0.8)` / `partial (0.5 ≤ O < 0.8)` / `not met (O < 0.5)`로 분류해 보고한다.
(0.8은 P1b의 "80 % bracket" 기준과 맞춘 값이며 여기서 사전 고정한다.)

## 6. 정직성 규칙
- 지역은 상자 근사이며 실제 해협 형상이 아니다. coverage 임계 0.5는 상자 크기에 민감하다 → 민감도로 0.3/0.7 병기.
- AKcorr_*와 BeringChukchi는 겹친다(§0). Vilkitsky·Long Strait 등은 위성 궤도 배치상 서로 독립이 아니다.
- retention은 **장면 수** 기준이며 관측 품질이 아니다.
- 지역 수가 적어(≈15) 부트스트랩 CI는 넓을 것으로 예상한다. 좁게 나오면 그것 자체를 의심해 보고한다.
