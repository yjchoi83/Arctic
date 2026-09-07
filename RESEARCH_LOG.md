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
- **P8 step 1 (H9 재검정)**: 자격증명으로 **DTU S1 drift**(`cmems_obs-si_glo_phy-drift-north_my_l4_P1D-m`)를
  ARCO 지연로딩해 region×season×year 가용성 산출. **H9 지지 — region-year Spearman ρ = 0.711 (p 1.7e-18)**,
  H_episode3와는 0.736. **지역 내 시간축만 봐도 지역별 ρ 중앙값 0.727**이라 단면 효과가 아니다.
  가용성은 pre 0.152 → during **0.031(−80 %)** → post 0.033(2025 부분표본). **P7의 "consequence not
  demonstrated"를 철회한다.** DMI-ASIP L3는 파일당 190 MB·original-files뿐이라 **16일 표본만** 받았고
  사전등록대로 H9 판정에 쓰지 않았다. MET Norway 차트는 **발행일수가 248/253/251/250일로 불변** —
  고정 일정 산출물이 전파 지표가 못 된다는 P7의 예고를 실증했고, 역시 H9 근거로 쓰지 않았다.
- **P8 step 2 (계획 대 실측, 램프업)**: ESA acquisition-segment KML 8종(172 MB) 파싱. 램프업 시점을
  아카이브에서 도출 — **S1C routine 2025-04**(브리프와 일치), **S1D 2026-04 첫 자료로 6개월뿐이라 미확정**.
  A+C 정규 창(2025-04…2026-03)에서 **유럽·러시아 77.4 % vs 북미·베링 121.1 %**로 적자 존속,
  **계획 커버리지도 EUR 86.4 % vs NAM 122.3 %**(Barents 계획 56 %). → 사전등록 조건 (a)·(b) 모두 충족이므로
  **"위성 수가 아니라 배분" 진술 유지**. 단 **범위를 Barents–Kara–Laptev 하위 구획으로 좁힌다** —
  같은 구획의 **Vilkitsky는 계획 146 %·실측 156 %**, Long Strait 112.7 %로 오히려 증가했다.
  3위성 창(2026 Apr–Aug)에서는 EUR 107 %로 절대 적자가 사라지나 융빙기 5개월뿐이라 대표성이 없다.
- **P8 step 3 (겨울 chokepoint 실증)**: 20 pair(40 scene, 9.2 GB)를 Stage 4 R1 파라미터로 처리.
  **해협에서 겨울·결빙기 C-band 추적은 작동한다** — 20 pair 전부 유효벡터 ≥30, 평균 성공률 **0.510**
  (winter 0.484–0.779, freeze-up 0.377–0.419). P4에서 OSI SAF가 62.5 km로 Vilkitsky를 통째로 마스크했던 것과
  대조적이다: **해협 위험이 관측 불가능한 게 아니라 저해상 산출물이 해상하지 못했던 것.**
  **P5의 공백을 메웠다 — 결빙기 성공률 첫 실측 0.394로, 낙관 대입 0.47은 약 19 % 과대**(P5에 갱신 주석 추가).
  수렴 사건 19건 검출(전부 winter, Sannikov 13·Vilkitsky 6) — 그러나 **magnitude가 전부 <3 km**
  (median 0.28, max 1.39)라 **사전등록한 ≥3 km 실증은 실패**했고, 0에서 외삽하지 않았다(rule of three 상한
  0.15/window만 제시). 미관측 비율은 등급 무관 진술로만: **H_episode 0.196 → 0.084이므로 80 % → 92 %**.
  **부이 검증은 불가능**했다 — 19건 전부 100 km 내 IABP 부이 없음(±12 h로 완화해도 동일).
- **P8 step 4 (BATCH_SUMMARY 갱신)**: 세 공백이 닫힌 결과로 논문 진술 3·4·6을 개정.
  **(6) "산출물 영향 미검정" → "전파 확인"(ρ=0.711)**, **(4) "배분 문제" 유지하되 Barents–Kara–Laptev로 범위 축소**
  (Vilkitsky는 계획·실측 모두 증가), **(3) "해협 위험 관측 불가" → "저해상 산출물이 해상하지 못했을 뿐,
  S1은 작동한다"**(성공률 0.510, 사건 19건). 살아남은 단서는 전부 유지했고 두 개를 새로 추가했다 —
  DTU는 S1 파생이라 독립 검증이 아니며, 검출 사건이 전부 <3 km라 ≥3 km 실증은 실패했다.
  **BATCH_SUMMARY는 53줄로 원래 40줄 상한을 초과** — "살아남은 단서를 전부 유지"하라는 지시를 우선했다.
  누적 다운로드 ≈14.3 GB(P8 상한 25 GB 내). **P9 이후는 시작하지 않았다.**

### ARC-P9
- **P9 step 1 (등급 재조정)**: 두 지표가 **baseline만 다르다**는 해석적 관계(`mag_S1/mag_buoy = √area/L`)를 확인.
  실측 비율 **0.248**(√area median 12.2 km vs 부이 L median 49.4 km) → P8 사건을 환산하면 median 0.28 → **1.13 km**.
  20개 window의 벡터장에 **가상 부이쌍 240,949개**(20–100 km)를 놓고 P1b의 rate 임계를 적용하니
  **0.50 %가 통과, 그 폐합량 median 5.88 km = ≥5 km class**(Vilkitsky winter 1.86 %). →
  **P8 step 3의 "≥3 km 실증 실패"를 철회한다** — 실패한 것은 물리가 아니라 S1쪽 사건 정의(면적을 baseline으로
  써 등급을 4배 축소)였다. 역방향으로 P1b 사건의 수렴률은 median 0.125/day vs S1 해협 0.020/day로
  **강도는 여전히 6–9배 약하고**, S1의 24–48 h window가 1–3 h 에피소드를 시간평균한다는 한계가 남는다.
  등급별 H 재산출: **1–3 km class는 during 0.029(97 % 미관측)**, ≥5 km는 0.121. 1–3 km 지속시간이 **2–4 h**라
  **12 h 요구선보다 3–6배 짧은 재방문**이 필요하다.
- **P9 steps 2–4 (robustness·산출물·QC)**: H9는 유효화소 임계 2/5/10 %에서 **ρ = 0.714 / 0.711 / 0.659**로
  **전부 사전등록 0.5를 넘는다**; 임계를 높이면 지역 내 시간축 ρ가 0.673 → **0.816**으로 오른다.
  **필수 단서를 모든 H9 진술에 병기**: DTU는 S1 입력 제품이라 **독립 검증이 아니라 같은 아카이브 파생량 간 관계**다.
  산출물: 25 km 셀 H 지도 6 PNG + GeoTIFF 18장(`data/products/`, 미커밋), 계획 대 실측 막대그래프,
  DTU 가용성 히트맵, 해협 예시 4장. QC contact sheet 19건(`decision` 공란) + baseline 환산 등급을 더한
  `qc_table_p9.csv` — 환산 후 **<1 km 10 · 1–3 km 8 · ≥5 km 1**.
- **P9 step 5 (paper skeleton)**: `stage5/P9/PAPER_OUTLINE.md` 77줄 — 제목, **초록 251 단어**, 12개 절과 각 절이
  쓰는 그림·표, **6개 주장 표**(근거 + 본문에 반드시 남길 단서), 그리고 **8개 한계**(부이→해협 외삽, 등급 baseline
  불일치, 공유 아카이브 의존, KML 계획 대 실측, S1D 램프업, H의 상한 성격, 셀 CI 과소, 작은 사건의 2–4 h 요구).
  목표 **RSE**, 대안 **CRST**. 제출 전 할 일도 명시(S2 API 키로 novelty 재실행, contact sheet 인간 판독,
  C3의 미검증 사건을 본문에 둘지 부록으로 옮길지 결정).
- **P10 (원고 초안)**: `paper/MANUSCRIPT.md` — 참고문헌 제외 **8,086 단어**(목표 7,000–8,500), 초록 251 단어,
  번호 절 구성·산문 내 불릿 없음(RSE 형식). 제목은 **working title**로 표기(최종본은 전체 검토 후 결정).
  지시대로 **19개 미검증 사건을 Appendix A로 이동**하고 본문에는 20/20 retrieval 결과와 가상 부이쌍 폐합
  (0.50 % 통과, median 5.88 km)만 남겼다. **두 기간·두 기제**를 §5.1로 명시 — 2022–24는 OSE(15/16 지역 10 pp 이내)로
  위성 수, 2025–26은 계획 문서(EUR 86.4 % vs NAM 122.3 %)로 배분. 그림 10장을 일관 스타일로 재생성
  (`paper/figures/`, EPSG:3413, H 0–1 컬러바, chokepoint 라벨). **NUMBERS_TRACE.md 127줄**로 모든 그림·표·
  주장 C1–C6의 수치를 CSV와 P-패키지에 매핑했고, 재생성 명령도 기록. 참고문헌은 **[V] 검증본 16건**만 싣고
  나머지는 **[CITATION NEEDED]** 5건으로 남겼다(사용자의 Semantic Scholar 패스용).

### ARC-P12 — 일관성·분량·투고물
- **plan ratio 전파(1)**: P11에서 S1A 2022–24 계획 아카이브를 추가해 재산출한 값이 Table 5에만 반영돼
  있었다. 본문 3곳(초록·§4.5·§7)을 **86.4 % → 87.1 %**, **122.3 % → 123.4 %**로 고치고, §4.5의
  **Barents 56 % → 56.8 %**, **Vilkitsky 146 % → 147.1 %**(취득 156 % → 156.1 %)도 맞췄다.
  덤으로 **Long Strait 113 % → 102.9 %** — `planned_with_gap.csv`와 어긋난 값이었다.
- **gap-year 단서 교체(2)**: "2022–24 계획은 회수하지 못했다"는 §4.5·§6.4의 단서를 삭제하고,
  **회수한 gap-year 계획은 S1A 단독이므로 절대량은 2위성 기간과 비교 불가, 섹터 간 비율만 비교 가능**이라는
  실제 제약으로 바꿨다. Table 5 각주가 이미 말하던 내용을 본문이 부정하고 있었다.
- **H 언어로 요구 재진술(5)**: **met = H ≥ 0.8**을 명시하고 실제 도달 수를 세었다 —
  **H_episode ≥ 0.8: 512 units 중 0, chokepoint 160 units 중 0**(최대 0.640 / 0.467);
  **H_state ≥ 0.8: 512 중 25**(Greenland/Fram 13 · Baffin 5 · Barents 4 · Lancaster 3),
  **chokepoint 0**(최대 0.793 Kara Gate). "4개 지역이 24 h 요구 충족"이 **O(24 h) ≥ 0.8**을 뜻함을 명기
  (main-season 512 중 38 units). O(12 h) 최대치도 정정: **0.278은 main season, 전체 688에서는 0.320**.
- **[중요] Table 3b 집계 불일치**: ≥3 km 행이 0.181/0.093/0.161인데 Table 3의 같은 양은 0.200/0.097/0.176.
  원인은 **Table 3b가 셀 가중 평균**이라 Sannikov(109셀)가 값을 끌어내린 것. Table 3와 동일한 2단계
  비가중 평균으로 재집계해 **0.200/0.097/0.176로 일치**시켰고 전 등급을 갱신(1–3 km는 0.029 → **0.030**).
- **[중요] §4.4 3위성 비교가 like-for-like가 아니었다**: melt 2026 3위성 0.511을 melt 계절 전체·16지역의
  2위성 평균 0.451과 비교하고 있었다. **동일 window·동일 9지역**으로 맞추면 1/2/3위성 = **0.373/0.441/0.511**
  (해협 2곳 0.293/0.353/0.429). 본문 교체.
- **그림 번호 정합**: 인용 순서가 1,2,3,7,8,4,5,6이었다. **7→4, 8→5, 4→6, 5→7, 6→8**로 재번호하고
  라벨·본문 참조·PNG 파일명·`p10_figs.py`·NUMBERS_TRACE를 모두 갱신. Fig. 5 캡션은 **divergence field +
  edge audit**(중심거리 18.9/76.7/46.0/32.4 km, 5 km 내 노드 0)로 다시 썼다.
- **분량(7)**: 초록 **250 단어**(≤250), §5.4 358 → **197**, §3.6 matcher 파라미터를
  **`paper/SUPPLEMENTARY.md` Supplementary Table S1**으로 이관, §4.7 Bering 설명 2문장.
  **본문 9,561 → 9,288 단어**(표·캡션·후미 제외), 헤딩 포함 9,480. 파일 전체는 11,487.
- **S2_API_KEY는 설정되어 있었다(9)** — P9~P11의 "키 없음" 기록은 이 환경에서 더 이상 사실이 아니다.
  - **9c 76건 재검증**: 63 clean · 10 flag · 3 미색인. flag 10건은 **전부 서지 쪽이 옳다**(6건은 S2가
    Copernicus discussion-paper/online-first 연도를 기록, Crossref `issued`로 확정; 2권 책과 Kaplan–Meier는
    S2 색인 결함; 1건은 저자 문자열 분할). **실제 결함 1건**: `karvonen2022baltic` 제목이 잘려 있었다 → 복원.
  - **9a novelty 21 쿼리**: **핵심 주장과 겹치는 논문 없음**. 최근접은 Geiger & Drinkwater(2001,
    샘플링 해상도 → drift/deformation), Kaminski(이미 인용), Sentinel-1 mission-status/task-planning 계열.
    관측계획을 취득 아카이브와 대조해 지역 배분 비대칭을 드러낸 연구는 색인에 없다.
  - **9b cluster 8**: "strict 기준으로는 verified 2"라던 공백을 닫았다 — **`geiger2001resolution`**과
    **`covington2022bridging`** 추가로 cluster 8이 3 → **5**, 서지 76 → **78**.
- **[중요] 인용 근거 감사(8)**: `fu2016besetting`은 문장을 **지지한다**(Northeast Passage besetting BBN 모델).
  **Wulf/Wuite 3건은 지지하지 않는다** — OpenAlex 초록으로 확인한 결과 셋 다 2021 불연속을 *지나가는*
  Sentinel-1 파생 산출물 기록이고, **누락 영상의 하류 영향을 문서화하지 않는다**. §1 문장을 그 사실만
  말하도록 다시 쓰고, 기제 주장은 새로 넣은 strict 2건이 지게 했다.
- **투고물(10)**: `paper/HIGHLIGHTS.md` — 5불릿(73·78·71·80·78자, 전부 ≤85) + graphical abstract 1문단 명세.
  `paper/build.md`에 submission items 표 추가.
