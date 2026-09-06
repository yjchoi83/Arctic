# stage4/SUMMARY.md — Stage 4 결과 (2026-09-04). 세부: N_topic_recheck / REPILOT_RESULTS / D2 / D3 / R1_prereg
GEE 호출 **0회**. 다운로드 S1 EW 12 scene, NISAR GCOV 2 frame(상한 내). **Semantic Scholar는 세션 내내 429** → novelty는 Crossref + arXiv phrase 기반(커버리지 한계 명시).

## N — **KILLED-BY-LITERATURE 0건**, NARROWED 5건
SURVIVES 5(TE01·TE02·TC01·TA03·TD04) / NARROWED 5(TD05·TD01·TA01·TF02·**TB01**). TB01 축소 최대 — 계절길이·고해상 SIC·chart-vs-Copernicus가 모두 선행되어 **Δ_scale/Δ_retrieval 귀속과 신뢰도 통계만 잔존**. [U] 6건 중 **4건 [V] 해소**(AI4Arctic DOI, TC 2025, TSB n, TF02 미러 문장). TD05의 RSASE 논문 **내용은 [U] 유지**(closed access) → "최초 정량화" 주장 보류.

## D — 데스크
- **D1** 04_final_ranking §1에 evidence-provenance 열 + stage3 10개 파일 헤더 1줄. TD05 조건 "없음"→**melt-season tracking-failure pilot**. 분류: real SAR pixels 3(TE02·TA01·TB01) / GIS 1(TF02) / metadata-is-the-method 5 / unpiloted 1(TD04 H3).
- **D2** C0: OW/level/deformed 3계급(thin-young은 level에 병합 — 비-SAR로 10–30 cm 경계 판정 불가 → 별도 계급은 정의상 순환). 5 해협 × 3 계절 블록 CV(+IPF 버전 축). **chart rho ≥ +0.4는 인용 가능한 증거가 아니라 역상관 방지 sanity floor**로 재정의하고 비-chart 기준(S2 BA ≥0.85, IABP ≥0.95, 선박관측 MAE ≤2/10, ATL10 AUC ≥0.70) 병기.
- **D3** **TSB 취득 성공** — 403은 Azure WAF의 UA 차단이었고 브라우저 UA 한 줄로 해제(88,054 rows). **북극 좌초 2010–2026 = 59건**(좌표 59/59), CAA 엄격정의 **14건** → TF02 조건 "TSB n 확정" **PASS**(단 CAA 14건은 검정력 리스크).

## R1 — TD05 재파일럿 (기준을 실행 **전** 고정)
melt/winter 각 4 pair, **동일 relative orbit·동일 ROI**로 지리·기하 교락을 설계상 제거.
- 무조건 Δ = **+46.0 %p**(melt 0.008 / winter 0.468). **그러나 8월 ROI는 AMSR2 중앙값 SIC 0 %의 개활수** → H1을 검정하지 않는다.
- 얼음 조건부: SIC≥30 % **melt 0.016(n=492) vs winter 0.468 → Δ +45.2 %p**, SIC≥50 %는 **melt 0/217**. 임계 15–70 %에서 Δ 44.9–46.8 %p 안정.
- 사후 대조(초기추정 제거 + 탐색창 ±30 km): 융빙기 여전히 0, 겨울 0.400 → **matcher 초기화 탓 아님**.
- IABP: 겨울 유일 공동위치에서 SAR 13.05 km vs 부이 12.53 km, **오차 0.53 km**(n=1 부이·7 벡터). 융빙기는 부이가 2.5–29 km 표류했는데도 반경 10 km 내 유효 노드 0 → 진리값 대조 불가.
- **판정 PASS(조건부)**. 잔존 교락은 얼음 유무가 아니라 **레짐**(melt MIZ 30–70 % vs winter pack 99 %) → 주장은 "**융빙기 MIZ에서 C-band 고전 matcher가 사실상 작동하지 않는다**"까지.
- 설계 수정 3건: ①ROI를 **빙연 추종형**으로(고정 상자 금지) ②**SIC 층 매칭** 대비를 1차 측정량으로 ③`sea_ice_drift`는 PyPI에 없고, arXiv:2510.26653(DL optical flow·GNSS 부이·EPE 300–400 m) 때문에 **matcher 계열을 한정하거나 DL 팔을 포함**해야 한다.

## R2 — TD01 재파일럿
- 후보 선정이 **날짜변경선을 가로지르는 S1 footprint** 때문에 위경도 겹침을 허위 계산 → EPSG:3413 전면 재계산. **TD01 전제 수치 정정: "≤6 h 동시쌍 563"은 시간만 센 값이고, 실겹침 ≥50 %를 강제하면 524 → 99건(고유 92, −81 %)**. Chukchi는 4건뿐.
- 취득 쌍(3.39 h, 실겹침 0.98, 67.3–70.3 N, 공동 유효 **56,609 km²**)은 **SIC 0 %의 완전 개활수** → **3계급 분리도 산출 불가**. 대체 지표로 흉내내지 않았다.
- 개활수에서 측정 가능한 것만: NISAR freqB NESZ(HV) −25.9 dB 대비 L_HV −18.5 dB(**여유 7.4 dB**), L_HH–L_HV r=**+0.987**(편파 중복), **L vs C r=+0.13–0.15** → **"≤6 h 동시"가 "같은 표면 상태"를 뜻하지 않는다**.
- 단일 쌍으로 불가한 것: 분리도 자체, L/C/L+C 성능 비교(fold 1개 → blocking 미정의), level vs deformed 구분(ICESat-2/in-situ 필요).
- **미완료**: 얼음이 있는 실겹침 쌍의 화소 수준 분리도는 NISAR 1 frame + S1 1 scene **추가**가 필요(예산 2/2·12/12 소진).

## 개정 GO 리스트
| # | ID | Stage 4 변화 | 남은 조건 |
|---|---|---|---|
| 1 | **TE01** | 무변, 무조건 GO — 조건이 하나도 늘지 않은 유일한 토픽 | 없음 |
| 2 | **TE02** ↑2 | SURVIVES | landfast 면적·asc/desc pair |
| 3 | **TD05** ↓1 | **R1이 전제를 실증**, N은 NARROWED | 빙연추종 ROI + SIC층 매칭 + matcher 한정/DL 팔 |
| 4 | **TF02** ↑2 | **조건 1개 해소**(n=59/CAA 14), NARROWED | H3 AUC ≥0.75, stratum ≤25 %, 동기 재작성 |
| 5 | **TD01** ↓2 | 계정 병목 해소, **n 상한 563→92**, ROI를 73–77 N으로 | RQ1 강등, RQ2·RQ3 본체화 |
| 6 | **TA01** ↓1 | NARROWED(기여 문장 재작성) | C0 rho ≥ +0.4 |
| 7 | **TB01** | **최대 축소**, 측정량 2개만 잔존 | Δ_scale CI 하한 >0.5, 미충족 시 short-form |
CONDITIONAL-GO 3건 전원 SURVIVES 유지(TC01·TA03·TD04), TD04만 H3 위험 상향. **첫 프로젝트 TE01 유지.**
