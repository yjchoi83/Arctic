# D2 / 작업패키지 **C0 — 공유 ice/water 분류기** (사전등록 가능 desk spec, 2026-09-04)

**존재 이유**: Stage 2 공통위험 1. TJ02의 crude HH/HV 임계는 면적가중 rho_Spearman(chart RIO, SAR RIO) = **-0.12** —
공간 기술이 0~음수다. 따라서 TA01(면적 flip 0.599 = calibration 0.270 + spatial 0.329), TB01(PM-SAR
navigable day +23~+103 d, mean +57), TC01(deformation pattern-matching)은 **모두 C0을 전제조건으로 인용**한다.
C0 완료 전에는 어떤 headline 수치도 공표하지 않는다(TA01 §8, TB01 §9와 동일 서약).
차트는 SAR 해석물이므로(§3.5) **평가 진리값은 항상 비-chart 축**이고, chart는 baseline과 하한 게이트로만 쓴다.

## 1. 클래스와 측정량
| 클래스 | 운영적 정의(비-SAR 심판 가능 형태) | 비-SAR 심판자 |
|---|---|---|
| **OW** open water | 부빙 총밀도 < 1/10; 표면이 물 | S2 반사율·질감, IABP 부이 무빙 구간, 선박관측 total conc. |
| **level ice** (thin-young 흡수) | 총밀도 >= 1/10, 능선/균열 융기 없는 평탄면 | S2, ICESat-2 ATL07 freeboard 저분산 구간, 선박관측 ice type |
| **deformed ice** | 능선·해머크·압축역; freeboard 분산·능선밀도 상승 | ICESat-2 ATL10 lead/ridge 통계(극야 가용), 선박관측 ridging code |

- **thin-young은 별도 클래스로 두지 않고 level ice에 병합**한다. 이유: 10-30 cm 두께 경계를 판정할 수 있는 비-SAR
  참조가 사실상 없다(S2는 극야 부재, ICESat-2 freeboard는 트랙 표본). chart 라벨로만 학습·평가하면 그 클래스는
  정의상 순환적이다. 단 **POLARIS reduced 4-class(OW/thin-young/FYI/MYI-deformed)** 입력이 필요한 TA01·TB01에는
  chart-학습 head를 **부수 출력**으로 얹되, 검증 주장과 acceptance는 3-class 측정량에서만 한다.
- 산출 단위: 40 m GRDM -> **400 m 다중룩 격자의 class posterior**(TA01/TB01 공통), POLARIS용 2 km regime 집계.

## 2. 라벨 출처와 독립성 감사
| 출처 | 순환성 | 해상도 | 시간·계절 한계 | 라벨 가능 클래스 | 역할 |
|---|---|---|---|---|---|
| **AI4Arctic / ASIP** (513 train / 20 test, S1+AMSR2) | **순환(chart 유래)** | scene | Greenland 해역 중심, 도메인 시프트 | 3+4 class 전부 | **pre-training 전용**. fine-tune·평가·acceptance 계산에서 배제. 기관·해역·시즌을 평가 대상(NSR chokepoint)과 분리 |
| **NIC G10033 SIGRID-3 weekly** | 순환 | polygon(주 4-8개/일자) | ~2026-08, partial conc. 없음 | reduced 4-class | baseline + §6 하한 게이트 전용 |
| **DMI-ASIP** 0.5 km S1 SIC (2014-2024) | 순환(부분) + SAR | 0.5 km | pan-Arctic | OW/ice | 독립 3자 **retrieval arm**(진리값 아님) |
| **Sentinel-2** | 독립 | 10 m | **74-75N Nov-Jan 0 scenes**, Feb SZA 83도 사용불가 -> 융빙/어깨철 전용 | OW / level / (능선 그림자 한정) | 주 confusion matrix 축, 융빙기 |
| **IABP 부이** (4,335 `.dat`, 로그인 불요) | 독립 | 점 | 전계절, **pack-ice 편향**(연안·flaw lead 표본 부족) | ice 유무, 표류 | ice-presence 검증 + drift 정합 |
| **선박관측 ASSIST / IceWatch** | 독립(육안) | 시선 반경 ~1 km, 1시간 간격 | 항로 transit 축 편향(항해가능 구간만 관측 -> OW·thin 과표집) | total/partial conc., ice type, **ridging/topography** | deformed 클래스의 유일한 광역 육안 축 |
| **ICESat-2 ATL07/ATL10** | 독립 | 트랙 ~11-20 m | dt<=3 h 코인시던스 파일럿 18 pairs -> 2025 EW 회복(32->202 scenes) 후 **실질 30-90/시즌** | level vs **deformed** | deformed 검증의 1차 축(극야 가용) |
| **VIIRS/MODIS TIR IST** | 독립 | 1 km | 야간 가용, 운량 제약 | OW/ice(열대비) | 겨울 보조 |

**라벨 예산이 얇은 곳**: (i) **deformed 클래스 전체** — ICESat-2 트랙 30-90/시즌 + 선박관측뿐, 화소 confusion matrix가
아니라 along-track 일치율로만 보고. (ii) **극야(Nov-Feb) OW** — S2 0 scenes이므로 IABP·ATL10·CHNL 통과일자에 의존.
(iii) **연안 flaw lead / fast-ice 경계** — 부이가 pack 편향이라 사실상 무라벨 -> 해당 구역은 acceptance에서 제외 선언.

## 3. Block cross-validation (무작위 화소·scene 분할 절대 금지, §3.4)
- **공간 블록 5개**: Vilkitsky / Sannikov / Long Strait / Bering-Chukchi / Canadian Arctic Archipelago(NWP).
  **Leave-one-strait-out 5 fold** — 각 fold에서 한 해협의 모든 scene·모든 시즌을 훈련에서 완전히 제거.
- **시간 블록**: 계절 3층 = **freeze-up(10-12월) / mid-winter(1-4월) / melt(6-9월)**, 그리고 연도 블록(홀수/짝수 시즌).
  **Leave-one-season-out**: 각 계절층을 통째로 홀드아웃하는 3 fold(TC01은 melt를 분석 범위에서 제외하므로 melt fold의
  실패는 TC01에 대해 비치명).
- **결합 fold(1차 acceptance 대상)**: 훈련에서 본 적 없는 **(해협 x 계절) 조합 5 x 3 = 15 cell** 중, 해협·계절이 동시에
  홀드아웃된 대각 5 cell을 **strict fold**로 지정. 보고는 항상 fold min/max 병기.
- **제3 축 = IPF 버전** 층화(002.84 시대 vs 003.71 시대 교차평가). **금지**: 동일 scene 타일 분할, 인접 orbit 중첩 타일 누수.

## 4. 훈련 전 필수 confounder 통제(파이프라인 고정, ablation on/off 의무)
1. **입사각 across-swath 정규화**: TE02 측정 HV gradient **-11.40 dB(IPF 002.84) -> -1.45 dB(IPF 003.71)**.
   cosine + IPF-버전별 경험 회귀. 미보정 시 hazard threshold **flip rate 25.89 %(near swath 44.2 %)**가 전 측정량에 전파.
2. **EW noise-floor scalloping**: 잔여 **9.72 dB p-p** -> 서브스와스 경계 마스킹 + 잔여 scalloping을 민감도 항목으로 보고.
3. **IPF 버전 층화**: 라벨·훈련·평가 표에 IPF 버전 열 필수. 버전 혼합 학습 arm과 층화 학습 arm을 별도 보고.
4. **습설(melt)**: 융빙기 HH/HV 붕괴 -> melt fold 별도 head·별도 보고, 겨울 성능과 합산 금지.
5. **풍성 거칠기 OW look-alike**: 바람장 bin별 water-recall 별도 보고 + HH-only vs HH+HV ablation.
6. **chart-scene 시간 오프셋**: NIC weekly vs S1 daily -> 동일 주 다중 scene 간 flip을 **시간 성분 상한**으로 계상.
7. 클래스 불균형: 파일럿 계절평균 ice fraction SAR **0.62-0.94**(PM SIC 0.16-0.56) -> **water가 소수 클래스**.
   **accuracy 보고 금지**, water-class recall/precision과 balanced accuracy를 1차 지표로.

## 5. 필수 baseline과 보고 지표(§3.4)
| Baseline | 내용 |
|---|---|
| B1 **classical threshold/texture** | crude HH/HV dB 임계(-15/-18/-21 민감도) + GLCM texture — 파일럿 재현, 실패 사례로 병기 |
| B2 **operational ice chart** | NIC G10033 reduced 4-class (SAR 유래 -> 종속 baseline 표기) |
| B3 **passive microwave** | OSI SAF 25 km SIC, Bremen AMSR2 6.25 km (스케일 대조) |
| B4 **DMI-ASIP** | 독립 3자 S1 retrieval |

보고 형식: 모든 표에 **n(화소/트랙/scene), 클래스 균형, fold min/max spread**. 1차 지표 = balanced accuracy,
water-class recall/precision, deformed along-track AUC. **fold 간 balanced accuracy spread > 0.15면 "단일 분류기"
주장 철회**(TB01 §7 승계). 표본 목표: 관측일 >= 900, S2 coincident(<=6 h, 무운) >= 25/해협, ATL 코인시던스 >= 30/해협-시즌.

## 6. Acceptance threshold
**(A) chart 게이트(사전등록)**: `rho`는 **면적가중 Spearman rank correlation(chart reduced-RIO, SAR reduced-RIO)`,
단위 = **2 km regime 셀**, chart-date별로 계산하고 held-out 해협(leave-one-strait-out 5 fold)의 chart-date에 대한
**중앙값 >= +0.4**, 추가로 **어떤 fold의 중앙값도 +0.25 미만이 아닐 것**[U, 제안값] — TA01 W5 게이트와 동일 기준.
- **증명하는 것**: 분류기가 운영 해석과 공간적으로 **역상관이 아님**(-0.12 -> +0.4). 즉 flip rate 59.9 %가
  "분류기 실패의 척도"가 아니라 해상도·해석 차이의 척도로 읽힐 수 있는 **최소 sanity floor**를 통과했다는 것.
- **증명하지 않는 것**: 정확도. 차트는 SAR 해석물이므로 rho 상승은 순환적 동의일 뿐이며, rho >= +0.4 자체는
  어떤 과학적 주장의 근거로도 인용되지 않는다(합격/불합격 스위치로만 사용).
**(B) 비-chart acceptance(과학적 검증축, 모두 held-out fold에서)** — 제안값은 전부 [U]:
| 축 | 기준 | 근거 |
|---|---|---|
| S2 (melt/어깨철) | balanced accuracy >= 0.85, **water recall >= 0.80**, n >= 25 scenes/해협 | water가 소수 클래스(ice frac 0.62-0.94) |
| IABP 부이 | 부이 위치 ice-presence 일치 >= 0.95; 표류 벡터와 분류 경계 정합 시 모순율 <= 0.05 | 점 표본·pack 편향이라 상한 기준 |
| 선박관측(ASSIST/IceWatch) | total concentration MAE <= 2/10, ice/water 이진 일치 >= 0.90 | 육안 오차·transit 편향 감안 |
| ICESat-2 ATL10 | deformed 클래스 along-track AUC >= 0.70, coincidences 30-90/시즌 | 화소 CM 불가, 방법 차이 명시 |
**(A)와 (B)를 모두 통과해야 C0 PASS**. (A)만 통과 시 -> chart-agreeing but unvalidated, 조건부 사용 금지.

## 7. C0 실패 시 소비 토픽의 fallback(신규 창작 없음, stage3 명시안 재사용)
- **TA01**: 해상도 주장 전면 철회 -> "reduced-RIO 입력으로서 S1 EW의 한계"를 다루는 **negative-result + 판정
  불확실성 논문**, Primary를 CRST -> **RESS**로 전환. flip rate 미공표 유지.
- **TB01**: 3-arm(자체 분류기 / DMI-ASIP / crude 임계) **일치 구간에서만** bias 주장, 불일치 구간은 bound로 보고.
  Δ_scale/Δ_total 95 % CI 하한 0.5 미충족 시 헤드라인 폐기 -> **"C-band 항해가능일 retrieval 오차 예산 + 신뢰도
  하한"**으로 CRST 재프레이밍. "by Polar Class"는 부수 산출물 강등 유지.
- **TC01**: 측정량이 amplitude가 아닌 변위장이라 의존도가 가장 낮음. C0 실패는 **pattern-matching 실패율을 layer로
  기록**하는 것으로 흡수하고, 그래도 붕괴 시 (a) 호송 지연/쇄빙선 지원 요청 해역-일을 outcome proxy로 대체,
  (b) TE01/TD05와 병합해 **outcome 검증 없는 deformation-observability 논문**으로 축소.

## 8. 공수와 의존 순서
| 주 | 작업 |
|---|---|
| W1 | 라벨 하베스트: AI4Arctic 수령, IABP 4,335 `.dat` 파싱, ASSIST/IceWatch 대조, S2/ATL07·10/VIIRS 코인시던스 목록 |
| W2 | 전처리 파이프라인 고정: 입사각 정규화, scalloping 마스킹, IPF 층화, 바람장 결합 |
| W3 | AI4Arctic pre-training + 3-class head 정의, fold 매트릭스(5 해협 x 3 계절) 동결·사전등록 |
| W4 | strict fold 학습·평가 + B1~B4 baseline 동시 산출 |
| W5 | ablation(입사각 on/off, HH-only, 임계 vs 학습기, IPF 층화) + fold spread |
| W6 | acceptance (A)+(B) 판정 및 PASS/FAIL 공표, 실패 시 §7 발동 |

- 총 **6주**(GPU 1장; TA01 ~20 GPU-h, TB01 24 GB GPU 3-5일 추정과 정합). **의존 순서**: C0 W1-2는 TA01 W1-2 / TB01 W1-2 / TC01 W4-5의 전처리 작업과 **공유·동시 수행**.
  C0 W6의 PASS 판정이 **TA01 W6(RIO 면 생성), TB01 W5-6(3-arm 일치 분석), TC01 W6-7(drift/deformation)의 개시 조건**이다.
  TC01 W1-3(사건 좌표화 게이트)은 C0과 독립적으로 병행 가능.
