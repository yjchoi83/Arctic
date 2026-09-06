# 03_stage3_proposals — Stage 3 제안서 요약 (10건, 2026-09-04)

전문: `stage3/<ID>.md` (각 36-60줄). 아래는 주심 판정용 요약.
**문헌 조회 제약**: Stage 3 진행 중 OpenAlex 일일 할당량이 소진(429, retryAfter ~21 h)되어
신규 검증이 제한되었다. 각 제안서는 Stage 1-2에서 이미 [V] 처리된 근거만 사용하고, 재검증하지
못한 항목은 [U]로 표기했다. Crossref/WebSearch로 우회 검증에 성공한 2건(TB01, TD04)은 아래 표시.

## 판정표

| ID | 제목(축약) | 검증 verdict | Primary journal | 핵심 effect size | 구속 조건 (gate) |
|---|---|---|---|---|---|
| TD05 | Melt-season L vs C drift tracking failure rate | **GO** | IEEE TGRS | IABP 48 h 변위 melt 19.58 km (n=4,468) vs winter 11.08 km (n=7,662) = **1.77x**; melt기 pair 가용성은 오히려 우수(gap 23.8 vs 47.7 h) -> 실패 원인은 feature persistence로 특정 | 없음. Tier 1(C-only)이 단독 논문으로 성립, 무료 CDSE 계정만 필요. Tier 2(L+C)는 상승 여력 |
| TE01 | S1B gap as a natural experiment | **GO** | Cold Reg Sci Technol | freeze-up 12-72 h drift pair **110(2021) -> 23(2023, -79 %) -> 121(2025)**; Vilkitsky 2023 pair 0, 관측일 30.4 -> 13.0 -> 59.8 % | 없음. 메타데이터만 사용, 로그인 불필요, 파일럿에서 effect size·독립교차검증·반사실 확보 |
| TD01 | Melt-season L+C separability (NISAR x S1) | CONDITIONAL-GO | IEEE TGRS | NISAR GCOV 2291 frames / 64 days; **L+C <=6 h 563 pairs**; latency median 123 h; **78N 이북 granule 0** | **W1 말까지 무료 Earthdata Login 취득 + GCOV 1 frame 실제 다운로드.** 미달 시 RQ3(observability) 단독 short-form(GRSL)으로 강등 |
| TE02 | Artefact budget -> decision flip | CONDITIONAL-GO | IEEE TGRS | HV hazard threshold **flip rate 25.89 %** (near swath 44.2 %); 잔여 scalloping 9.72 dB p-p; inter-IPF drift +1.51 dB | **W1-2 가용성 gate**: quasi-static landfast polygon 유효면적 >=1,500 km2 및 asc/desc pair >=60. 무료 CDSE 계정(SAFE annotation XML) 필요 |
| TA01 | SAR-resolution POLARIS routing (+TJ02 흡수) | CONDITIONAL-GO | Cold Reg Sci Technol | route divergence mean 6.9 / max 10.8 km, chart route의 **19.9 %가 negative-RIO**; area flip **0.599** (calibration 0.270 + spatial 0.329) | **W5 gate**: 학습 분류기가 held-out 해협 AND held-out 시즌에서 area-weighted rho >= +0.4. 미달 시 해상도 주장 철회, negative-result 논문으로 RESS 전환 |
| TF02 | Ice forcing ships off surveyed tracks | CONDITIONAL-GO | Cold Reg Sci Technol | NWP corridor의 **28 %(11/40)만 직접측량 bathymetry**; NOAA NOS 129 polygons | 3중 gate: (a) TID-vs-NOS adequacy AUC >=0.75(<0.65면 NO-GO), (b) joint-exposure 최상위 stratum <=25 % 길이, (c) TSB n 확정 |
| TB01 | Chokepoint navigable-day + reliability | CONDITIONAL-GO | Remote Sens Environ | PM가 항해가능일을 **+23~+103 d/season (mean +57)** 과대평가, 5/5 시즌 부호 일치 | **W8 gate**: scale/retrieval 분해에서 Delta_scale/Delta_total의 bootstrap 95 % CI 하한 > 0.5. 미달 시 C-band 오차예산 논문(CRST)으로 재프레이밍 |
| TC01 | Convergence nowcast + besetting case-control | CONDITIONAL-GO | Cold Reg Sci Technol | 2021 East Siberian 38 usable drift pairs vs 2023 Vilkitsky 0; 성공기준 SIC-only 대비 **Delta AUC >= +0.05** | **W3 gate**: sigma<=50 km, <=24 h로 georeferencing된 besetting n>=20 (그중 사건 전 24-72 h pair 존재 n>=12), 사전등록 + 위치 지터 power simulation |
| TA03 | Hazard positional staleness | CONDITIONAL-GO | Cold Reg Sci Technol | 2023 Vilkitsky 96 h refresh -> hazard가 median **22.0 km** (p95 60.3) 이동, 해협폭 ~55 km | **W9 gate**: decision flip-rate 곡선이 Delta t에 대해 비평탄(24 h vs 96 h 간 >=20 pp, 5개 해협 중 4개에서 부호 일치). 실패 시 즉시 NO-GO, TE01 §3으로 흡수 |
| TD04 | ICESat-2 ridge stats as independent reference | CONDITIONAL-GO | The Cryosphere | n_folds **16** (4 ROI x 4 years); 대안 track arm 30-90 folds | **W9 H3 gate**: 평균 freeboard 통제 후 HV texture의 잔여 partial \|rho\| >= 0.25. 미달 시 측정량이 TC 2025와 동일해져 kill |

## Stage 3에서 드러난 중요 사실 3가지

1. **TD04의 위협 2개가 동시에 해소됨(신규 [V] 발견)**: **UMD-RDA gridded ICESat-2 sea ice deformation
   product** (Duncan & Farrell, PANGAEA 10.1594/PANGAEA.990265) — sail height, sail spacing, ridging
   intensity를 월 3.125/10/25 km로 2018-10~2025-02 제공하며 **로그인 불필요**. 이로써 (a) ATL10의
   HTTP 401 문제와 (b) "ATL10은 ridge product가 아니다"라는 반론이 함께 사라졌다. 대신 대상 시즌이
   2025-26에서 **Oct-Nov 2018-2021**(S1A+S1B 시기)로 이동했고, 이 이동분은 파일럿되지 않았다 —
   이것이 GO가 아닌 이유다.
2. **TB01은 부분적으로 선점되었다(신규 [V])**: Wulf et al., **RSE 2026** — DMI-ASIP, 2014-2024
   pan-Arctic 0.5 km Sentinel-1 SIC. S1 SIC > PMW가 MIZ·융빙기에서 나타난다는 *방향*은 이미 발표됨.
   따라서 TB01의 novelty는 "S1이 PM보다 낫다"가 아니라 **해협 규모 navigable-day/rate 측정량 +
   scale-vs-retrieval 귀속 분해**로 재진술되었고, DMI-ASIP은 경쟁자가 아니라 **제3의 독립 retrieval
   arm**으로 흡수되었다. 이것이 정직한 처리다.
3. **TF02는 자신의 파일럿 결과를 스스로 부정했다**: "알려진 좌초 4건이 전부 직접측량 코드 밖"이라는
   Stage 2 관찰은 72 % 기저율에 대해 0.72^4 = 0.27 — **유의하지 않다**. 제안서는 이를 명시하고
   headline을 coverage 수치(28 %)로 교체했으며, case-agreement 주장은 joint stratum이 q<=0.25로
   좁혀질 때만 유효하다고 사전등록했다. 이런 자기부정이 §3의 요구사항이다.

## 공통 설계 특징 (10건 전부 충족 확인)
- **Spatial + temporal blocking**: 전 제안서가 무작위 화소/장면 분할을 배제하고 지역·시즌 단위
  hold-out을 채택. fold 수를 병목으로 명시한 사례: TD04 16 folds, TD05 buoy trajectory 기반
  (fold당 8개 미만이면 유의성 주장 금지), TA03 5개 해협 leave-one-out.
- **Mandatory baseline**: TD05는 OSI SAF drift, TD01은 C-only, TA01/TB01은 chart 및 PM,
  TE02는 ESA IPF 기본 thermal-noise removal(+ 발표된 denoiser를 상한 참조 arm으로만 사용).
- **Reference independence (§3.5)**: IABP buoys(TC01/TA03/TD05), ICESat-2 RDA(TD04),
  UAF CSIRS·NOAA CO-OPS(TI03), NOAA NOS survey polygons(TF02), Sentinel-2(계절 제한 명시).
  chart 단독 검증은 어느 제안서에서도 채택되지 않았다.
- **Sensitivity**: 지수를 다루는 유일한 생존 토픽 TF02는 **자유 가중치가 0개**인 곱 형태
  E = 1{d>0} x C(x_dev)를 채택해 TF01을 죽인 §3.6 함정을 구조적으로 회피.
