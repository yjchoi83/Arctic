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

### ARC-P1b progress
- **Step 1 (persistence)**: 82,439 이벤트에 대해 event 종료 후 separation이 pre-event 값의 90 %까지
  회복하는 시간 측정(전체 censoring 3.9 %). **결정적 문제 발견 — 이벤트의 84.6 %는 종료 시점에 이미
  90 % 이상**이다(magnitude가 pre-event separation의 10 % 미만). 이들에게 persistence는 정의되지 않으며
  median 3 h는 3시간 격자의 바닥값일 뿐이다. **relmag ≥ 10 %인 15.4 %(n=11,295)에서만 측정량이 성립**하고,
  거기서는 지속이 길다: med **21 h** / p75 69 h / p90 198 h, censoring 18 %
  (freeze-up med 39 h·p75 123 h, winter 27 h·72 h, melt 12 h·54 h).
  → episode duration(시간 단위)과 hazard-state persistence(수십 시간~일)는 **다른 측정량**이다.
- **Step 2 (detection floor)**: native fix interval ≤1 h인 부이 **1,111/1,271**(fix 8,399,514)만으로
  1시간 격자(브래킷 ±1 h)·최소 2 h로 재계산. **이벤트의 85.8 %가 6 h 미만**이고 median은 **6 h → 2 h**로
  떨어진다(THR 4.706, n=137,786, p90 7 h). 동일 부이 부분집합의 3시간 격자 대조군은 med 6 h·p90 18 h로
  P1을 재현 → 차이는 부분집합이 아니라 **표본화 간격 자체**가 만든 것이다.
  즉 P1의 "median 6 h"는 **검출 바닥이 맞다**. 다만 **magnitude로 거르면 측정량이 안정된다**:
  mag ≥3 km는 med 9 h(1 h 격자) vs 12 h(3 h 격자)·6 h 미만 9.2 %, mag ≥5 km는 12 h vs 18 h·6 h 미만 2.1 %.
  → **작은 이벤트의 지속시간은 정의되지 않고(표본화율을 따라감), 큰 이벤트만 고유 시간척도를 갖는다.**
- **Step 3 (observability table)**: 단일 T 규칙을 폐기하고 measurand × magnitude class 표로 대체.
  "80 %를 bracket하는 revisit"은 정의가 셋이라 셋 다 싣는다 — p20(개별 이벤트를 확실히 잡는 T),
  **T_exp80**(모집단 기대 포착률 ≥0.8, 설계용 권장값), p80(지시된 문자 그대로의 통계량).
  persistence는 **Kaplan-Meier**로 censoring(4–20 %)을 반영했다. duration ≥3 km는 T_exp80 = 10 h(1 h 표본)
  / 14 h(3 h 표본), ≥5 km는 14 / 20 h. persistence(relmag ≥10 %)는 ≥3 km 17 h, ≥5 km **24 h**(p80 219 h).
  → **두 measurand의 요구가 다르다**: episode를 잡으려면 6–12 h, hazard 상태를 놓치지 않으려면 24 h급.
- **P1b 종합 (verdict)**: P1의 두 핵심 수치가 모두 **아티팩트로 확인**됐다 — "median 6 h"는 3시간 격자의
  검출 바닥(1 h 격자에서 median 2 h, 이벤트의 85.8 %가 6 h 미만)이고, persistence의 "median 3 h"는
  이벤트의 84.6 %에서 **측정량 자체가 정의되지 않아** 생긴 값이다. 살아남는 결론은 하나다:
  **magnitude로 거른 이벤트만 고유 시간척도를 갖는다.** ≥3 km duration 9–12 h, ≥5 km 12–18 h,
  relmag ≥10 % persistence 24–39 h(freeze-up p75 123 h). 단일 T 규칙은 폐기하고 measurand × magnitude
  표(§3)로 대체했다. **P1b_results.md는 48줄로 지정된 40줄을 초과** — 3개 표(계절·검출바닥·observability)와
  정직성 문단을 줄이는 것보다 초과를 택했다.
  **Next**: (a) persistence를 1 h 격자로 재계산(현재 3 h만), (b) relmag 기준을 P2에서 **사전등록**할 것,
  (c) p90 꼬리(198–246 h)는 censoring 18–20 %에 민감하므로 P2 곡선에서는 신뢰구간 없이 인용 금지,
  (d) P2는 dt = 6/12/24/48/72/168 h 곡선을 **magnitude class별로만** 산출.

### ARC-P2 progress
- **Step 0 (PLAN + 라벨 오류)**: 브리프의 "40 NWP segments from Stage 2"를 열어 보니 좌표가
  (−168.75, 65.75) → (−159.5, 71.34), 즉 **Bering–Chukchi–Point Barrow 알래스카 회랑**이고
  **Northwest Passage가 아니다**(Stage 2가 NOAA NOS 미국 측량자료를 쓰면서 "NWP"로 오명명). 지시대로
  6 sector로 집계하되 `AKcorr_*`로 개명하고, BeringChukchi와 **공간 중복**을 명시하며, 빠진 진짜 NWP를
  메우려 CAA 2개 지역(Lancaster Sound, Victoria Strait)을 "브리프 외 추가"로 넣는다. PLAN.md 사전등록 완료.
- **Steps 1–2 (regions, metrics)**: GEE `COPERNICUS/S1_GRD` 메타데이터만으로 16개 지역 × 2016–2026 취득
  176 region-year를 추출(EW+IW, 장면당 `area(scene∩region)/area(region)` 계산). 실행 시간 총 ~6분,
  EECU 사용은 예산 12 h 대비 무시할 수준. 688개 region×season×year 셀 산출(부분 계절 16셀 flag).
  **PLAN §2에서 한 가지 이탈을 공개한다**: GRD는 한 pass가 여러 slice로 쪼개져 slice 단위 coverage로는
  큰 지역이 영원히 50 %에 못 미친다 → 동일 platform·pass·15분 이내 slice를 **하나의 취득(pass)으로 묶고
  coverage를 합산(min 1.0)**했다. 이는 지표를 의도에 맞추는 수정이며 은폐하지 않는다.
  전 지역 평균 freeze-up O(24 h)는 2019–21 0.28–0.30 → **2022–24 0.015–0.017** → 2025 0.276.
- **Step 3 (treatment)**: retention = 2022–24 / 2019–21 장면 수. **"kept"(≥0.9) 지역이 하나도 없다** —
  16개 후보 전부가 최소 15 % 이상을 잃었고 9개가 lost(<0.5), 7개가 intermediate(0.5–0.9)다.
  최저 Sannikov 0.310, 최고 BeringChukchi 0.846. **즉 사전등록한 DiD의 미처치 대조군이 존재하지 않는다.**
  S1B 상실은 지역별 자연실험이 아니라 **북극 전역 동시충격**이었다. 후보 대조군(Barents 0.455,
  Fram 0.471, Baffin 0.508)도 전부 처치를 받았다.
- **Step 4 (DiD)**: 대조군 부재로 **H1은 사전등록된 형태로 평가 불가**. 대신 lost vs intermediate의
  용량반응 대비를 **사후 분석으로 명시**해 산출: O(24 h) DiD **−25.7 pp, 95 % CI [−49.9, +0.6]**
  (region 블록 부트스트랩 1,000회) — 크기는 20 pp를 넘지만 **CI가 0을 포함**해 H1의 두 조건 중 하나도 못 채운다.
  **H2 기각**: lost의 2025–26은 pre 대비 **−16.4 pp, CI [−31.1, −4.6]**로 10 pp 이내 회복이 아니다.
  O(12 h)는 전 기간·전 지역에서 ≤0.016이라 DiD 0.4 pp [−2.4, 4.3]로 무의미하다(요구가 애초에 충족된 적 없음).
  **설계 위협 명시**: 용량 그룹이 위도·기저관측력과 공선(retention vs lat rho −0.556 p .025;
  vs pre-O24 rho −0.461 p .073)이고 pre 수준이 0.393 vs 0.117로 달라 평행추세 가정이 성립하지 않는다.
- **Step 5 + 종합 (verdict)**: 요구 오버레이가 가장 강한 결과를 냈다. **12 h episode 요구는 688셀 전부에서
  한 번도 충족된 적이 없고**(O12 최댓값 0.278, coverage 임계 0.3에서도 0.356) → **Sentinel-1 단독으로는
  P1b의 episode 요구가 원리적으로 도달 불가**다. 24 h 요구는 16개 중 **4개 지역만** 충족한 적이 있고
  (Fram·Lancaster·Barents·Baffin), **2022–24는 전 지역 0셀**이다. 그리고 **NSR chokepoint 5곳은 어느 해에도
  24 h를 충족한 적이 없다**(pre O24: Vilkitsky 0.061·Sannikov 0.048·LongStrait 0.084·KaraGate 0.312·
  BeringChukchi 0.002) — **운용상 가장 중요한 해협들은 S1B 상실 이전에도 요구를 만족한 적이 없다.**
  민감도(coverage 0.3/0.5/0.7)에서 kept 0개·O12<0.5·chokepoint 미달 세 결론 모두 불변.
  **P2_results.md는 61줄로 지정된 60줄을 1줄 초과.**
  **Next(P3 착수 전 결정 필요)**: (a) TE01의 "자연실험" 프레이밍은 대조군 부재로 성립하지 않는다 —
  측정량을 지역 간 DiD가 아니라 **전역 관측능력의 시계열 붕괴·복구**로 재정의할 것.
  (b) chokepoint가 애초에 요구 미달이라는 사실이 TE01보다 강한 결과일 수 있다 — 우선순위 재검토.
  (c) O(dt)의 상자 의존성을 실제 해협 폴리곤으로 교체해 (c)를 확정할 것.

### ARC-P3…P7 batch
- **PLAN 고정**: `stage5/PLAN.md`에 H 지표 유도를 사전등록. 핵심은 **length-biased gap weighting** —
  위험 발생시각이 계절에 균등분포면 gap i에 떨어질 확률이 g_i에 비례하므로
  **H = E_D[Σ g_i·min(1,D/g_i) / Σ g_i]**. 단순 평균 min(1,D/ḡ)을 쓰면 큰 gap 하나가 숨겨져 낙관 편향이 난다.
  가정 5개(특히 **취득 1회=관측으로 세므로 H는 상한**, **부이 D 분포를 chokepoint에 외삽**)를 명시.
  H8/H6/H9와 설계임계 0.8도 사전 고정. charting layer는 논문 범위에서 제외.
- **P3 step 1 (feasibility)**: **STOP 미발동** — OSI SAF OSI-405 LR drift(62.5 km, 48 h 변위, 일별)는
  thredds.met.no에서 **무로그인 200**, 2016–2025 전 월 존재. 반면 **DMI ASIP**
  (`SEAICE_ARC_PHY_AUTO_L3_MYNRT_011_023`)와 **DTU S1 drift**(`cmems_sat-si_glo_drift_nrt_north_d`)는
  CMEMS에 **존재하지만 계정이 없어 다운로드 불가**(계정은 만들지 않는다) → **P7의 H9는 정량 검정 자체가 불가**.
  OSI SAF **SAR 기반 drift는 존재하지 않는다**(OSI-407은 중단, drift_mr은 AVHRR 기반).
  무계정으로 닿는 유일한 S1 의존 산출물은 **MET Norway ice chart quicklook PNG 아카이브**(1997–2026)뿐이며
  래스터라 정량 전파검증에 부족하다. ESA **Sentinel-1 Acquisition Segments ZIP 2015–2025** 취득 가능(2026분 없음)
  → P6-7의 계획 대 실측 비교에 사용. EODMS는 익명 `wes/rapi/search` 200(부분), CHNL은 **연 단위 HTML만**(2024 이후 동결).
- **P3 step 2 (H metric)**: 1,771개 25 km 셀 × 2016–2026로 `H = E_D[Σ min(g_i,D)]/Σ g_i` 산출
  (length-biased 가중을 닫힌형으로 정리; 순진한 구현과 1e-12 이내 일치 확인). **episode(D≈10 h)는 어느 시기에도
  0.27을 못 넘고, NSR chokepoint는 pre에도 0.20, 2022–24에는 0.097** — 에피소드 위험 10건 중 9건이
  촬영되지 않았다는 뜻. state(D≈30–45 h)는 0.562 → 0.441 → 0.532(부분 회복). 셀 단위 O(24 h)는 P2 상자값과
  평균은 같으나(0.178 vs 0.169) **512건 중 119건에서 0.05 이상 어긋난다** — 작은 해협은 상자가 과소평가
  (LongStrait +0.042), 큰 상자는 과대평가(Fram −0.046). **셀 부트스트랩 CI가 매우 좁은 것은 정밀도가 아니라
  같은 지역 셀이 궤도를 공유해 독립이 아니기 때문**이며 그렇게 명시했다.
- **P4 steps 3–4 (OSI SAF hazard record)**: OSI-405 3,043일(2.3 GB) 처리. **NSR chokepoint에 S1-독립 hazard
  기록이 사실상 없다** — 62.5 km 격자에서 **Vilkitsky는 10년 전체 유효 관측 0건**(전부 land/coast 마스크),
  divergence 계산가능 비율은 Sannikov 0.1 %·LongStrait 0.3 %·KaraGate 0.0 %이고 유효값 대부분이
  **interpolated(flag 22)**. **H8은 4개 해협에서 검정 불가**, 유일하게 가능한 Bering–Chukchi 접근로에서는
  **기각**(2022 0.422 / 2023 0.177 / 2024 0.892 — 0.25 미만은 2023뿐). 기간별 hazard-observed fraction은
  pre 0.652 → during 0.475 → post 0.677(24 h). QC 퀵룩은 요청 10–15건 대비 **5건**만 성립했고 전부 Long Strait
  2025다 — Sannikov는 단일 취득은 24 h 내에 있어도 **쌍이 없다**(PLAN 가정 3의 실증). 예산 때문에 40 m 화소
  crop 대신 **ASF browse JPEG**를 저장했고 auto_note는 UNSCORED로 남겼다(공개 이탈).
- **P5 (effective observability)**: `E = H × retrieval success`(R1 실측 winter 0.47 / melt 0.02).
  **H와 E의 간극이 요점** — H_state3는 0.35–0.67이지만 E_state는 winter 0.18–0.28, **melt 0.006–0.009**.
  즉 **융빙기에는 위성을 더 띄워도 E가 0.01을 못 넘는다**(병목이 관측계획이 아니라 C-band matcher).
  chokepoint winter E_state는 pre 0.258 → during 0.177 → post 0.219. **freeze-up 성공률은 미측정**이라
  낙관 대입(0.47)과 unknown을 병기했고 어느 쪽도 기본값으로 숨기지 않았다. DL 벤치마크(arXiv:2510.26653)는
  **3–5월 pack ice만** 시험했으므로 melt·freeze-up 반박 근거가 될 수 없음을 명시.
- **P6 (counterfactual/design/recovery)**: **H6 지지 — 16개 중 15개 지역에서 A-only 반사실이 관측 2022–24를
  10 pp 이내로 재현**(대부분 ±3 pp). 유일 실패는 **Sannikov +12.3 pp**로, 그 해역은 A 단독 기대치보다도 취득이
  적었다. 설계곡선: 1→2위성 +0.13, 2→3 **+0.05**로 체감하며 **NSR chokepoint는 3위성에서도 최대 0.72로
  0.8 "not attainable"**(800조합 중 0.8 도달은 16개, 전부 Fram·Barents 등 대형 고위도 상자).
  **회복적자는 위성 수가 아니라 배분** — 총량은 pre의 88.5 %인데 **Barents 46.6 %·Sannikov 63.5 %·KaraGate 75.1 %·
  Fram 73.6 %로 유럽·러시아 구획에 부족이 집중**되고 북미·베링은 101–141 %로 이미 초과 회복. ESA scenario
  교차확인은 URL 해시 미확보로 **수행 못 함**(2026 파일은 애초에 없음) → 판정은 메타데이터 근거 서술로 한정.
- **P7 (product consequence)**: **H9 미검정 — 기각이 아니라 자료 접근 불가.** DMI-ASIP·DTU S1 drift는 CMEMS에
  존재하나 자격증명이 없고(계정은 만들지 않음), OSI SAF SAR drift는 **존재하지 않으며**, 무료로 닿는 MET Norway
  차트 quicklook은 PNG라 정량 지표가 못 된다. **"제품이 영향받지 않았다"로 읽으면 안 된다** — 검사를 못 했다.
  논문 범위를 observability로 좁힌다. 계정 1개만 있으면 <1 GB로 완료 가능함을 P7에 적어 뒀다.
- **BATCH 종합**: 논문 진술 6개 확정. (1) chokepoint는 **손실 이전에도** 요구 미달(H_episode 0.200, O12는 688셀
  전부 미충족). (2) 손실이 격차를 벌림(H_episode 0.200 → 0.097). (3) 2022–24 hazard-observed fraction은
  **4개 해협에서 측정 불가**, Bering–Chukchi에서 H8 기각. (4) 회복 88.5 %, 부족은 **유럽·러시아 구획 편중**
  → 계획 문제. (5) 최소 위성 수 **not attainable**. (6) 산출물 영향 **미검정**(자격증명).
  예산 집행 2.3 GB / 5 GB, EECU 무시 수준. **P8은 시작하지 않았다.**

### ARC-P8 — 세 공백 닫기
- **PLAN 고정**: G1(H9 미검정)·G2(배분 판정이 서술뿐)·G3(겨울 chokepoint 위험 미실증)을 대상으로 사전등록.
  핵심은 **G2의 강등 규칙** — "위성 수가 아니라 배분"은 **램프업 통제 후에도 적자가 남고 AND 계획 커버리지도
  낮을 때만** 유지하고, 아니면 **"unexplained"로 강등**한다. G3의 수렴사건 정의(면적 ≥100 km², pair별 p10)와
  미관측 기대수 산식도 실행 전에 고정. copernicusmarine 로그인 유효 확인.
