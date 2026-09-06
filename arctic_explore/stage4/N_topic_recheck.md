# stage4/N_topic_recheck.md — 10개 토픽 novelty 재검증 통합 (2026-09-04)

세부 근거: `stage4/N_recheck_A.md` (TE01·TD05·TD01·TE02·TA01), `stage4/N_recheck_B.md`
(TF02·TB01·TC01·TA03·TD04). 본 파일은 통합 판정·[U] 처분·검색축 한계를 기록한다.

## 0. 검색축 가용성 — 정직한 한계 보고
- **Semantic Scholar: 세션 전체 HTTP 429**(무키 rate limit). 두 subagent와 main agent가 각각
  재시도했으나 유효 결과 0건. 요구된 검색축 중 하나가 **실질적으로 작동하지 않았다.**
- **arXiv**: `+`가 OR로 파싱되어 subagent의 복합 쿼리가 대량 실패했다. main agent가 `all:"..."`
  **인용 phrase 쿼리로 재실행**해 아래 §3의 결과를 추가 확보했다.
- **OpenAlex**: 429 "Insufficient budget"(UTC 자정 초기화).
- **Crossref**: 정상. 사실상 주 검색축.
→ 따라서 본 재검증의 커버리지는 **Crossref + 부분 arXiv**이며, S2 색인 고유 항목은 누락 가능하다.
  이 한계 자체를 원고의 novelty 서술에 남기지 말고, 투고 전 S2 API 키로 재실행할 것.

## 1. 통합 판정표
| ID | 판정 | 핵심 근거 (모두 [V]) |
|---|---|---|
| TE01 | **SURVIVES** | 위성 상실을 관측역량 자연실험으로 쓴 2024–26 선행 없음 |
| TE02 | **SURVIVES** | 최근접 10.1049/icp.2024.1598은 측정량이 accuracy이지 flip rate 아님 |
| TC01 | **SURVIVES** | 2024–26 besetting case-control 관측연구 없음(전부 시뮬레이션). 10.5194/egusphere-2026-4668 인용 필요 |
| TA03 | **SURVIVES** | Stage 3이 못 돌린 검색을 재실행. 최근접 10.5194/egusphere-2025-6379는 모델 rheology 예측성 실험으로 RQ 상이 |
| TD04 | **SURVIVES (위험 상향)** | "TC 2025" = Kortum et al. 10.5194/tc-19-4701-2025 [V] 확인 — chart·ridge 평가 없음 → 측정량 구별 성립. 단 HV–freeboard 연결이 H3 게이트를 더 어렵게 만듦 |
| TD05 | **NARROWED** | 10.5194/egusphere-2026-4668이 buoy 검증 절차를 커뮤니티 자산화; arXiv:2510.26653이 C-band drift를 GNSS 부이로 벤치마크 |
| TD01 | **NARROWED** | 10.5194/egusphere-2026-4775 (ALOS-2 L-band 융빙기 ice/water, MCC>0.80)가 RQ1 상당 부분 선점 → RQ1은 sanity-check로 강등 |
| TA01 | **NARROWED** | 10.3390/su18147414가 S1→POLARIS RIO least-cost routing을 Bering에서 이미 수행 → 기여를 "해상도 효과 vs 분류기 오차 분리"로 재작성 |
| TF02 | **NARROWED** | 10.58440/ihr-31-2-a13 (IHR 2025)가 S2 SDB로 캐나다 북극 좌초지 7곳을 사전 탐지 가능함을 보임 → "미측량 = 관측불가" 동기 폐기, 전향적 우선순위화로 재조준 |
| TB01 | **NARROWED (최다)** | 10.1038/s43247-024-01477-6·10.12716/1001.18.03.02(계절길이), 10.5194/tc-18-5277-2024(고해상 SIC), arXiv:2512.11083(chart vs Copernicus 불일치) → **Δ_scale/Δ_retrieval 귀속과 신뢰도 통계만 남음** |

**KILLED-BY-LITERATURE: 0건.** 어느 토픽도 §3.2의 kill 요건(동일 RQ + 비교 가능 데이터 +
설득력 있는 검증)을 충족하는 선행을 만나지 않았다. 대신 **10건 중 5건이 NARROWED**이며,
축소 폭이 가장 큰 것은 TB01이다.

## 2. [U] 참고문헌 처분
| 위치 | Stage 3 상태 | Stage 4 결과 |
|---|---|---|
| TA01:22 AI4Arctic/ASIP | [U] | **[V]** — `Ready-To-Train AI4Arctic Sea Ice Challenge Dataset` 10.11583/DTU.21316608.v3, raw 10.11583/DTU.21284967.v3 (DTU 2023). 표기를 "ASIP"에서 **AI4Arctic Sea Ice Challenge Dataset**으로 정정할 것 |
| TD05:39 10.1016/j.rsase.2023.101104 | [U] | **메타데이터 [V] / 내용 [U]** — closed access, 3개 API 모두 abstract 미제공. "융빙기 실패율 최초 정량화" 주장은 원문 입수 전까지 **보류** |
| TD04:57 "TC 2025" | [U] | **[V]** 10.5194/tc-19-4701-2025 (Kortum et al., The Cryosphere 2025) |
| TD04:57 2018–21 ROI chart 연속성 | [U] | **[U] 유지** — 재검증하지 않음 |
| TA03:40 "선행 부재" 재확인 | [U] | **근거 보강, 그러나 Crossref 단독** → 완전한 [V]로 승격하지 않음. S2 재실행 필요 |
| TF02 TSB 좌초 전수 n | [U] | **[V] 해소** — D3가 MARSIS_OCC(88,054 rows)를 취득. §D3 참조 |
| TF02 "CSV 미러 부재" | [U] | 무의미해짐(정본 URL이 UA 헤더로 열림). 해당 문장 삭제 대상 |

## 3. main agent가 추가한 arXiv phrase 검색 (subagent 복합쿼리 실패분 보완)
`all:"sea ice drift"`, `all:"sea ice" AND all:"Sentinel-1"`, `all:"marginal ice zone"` (2025–2026):
- **arXiv:2510.26653** — RADARSAT-2 ScanSAR에서 **딥러닝 optical-flow 48개 모델을 GNSS 부이로
  벤치마크**, EPE 300–400 m. → **TD05의 최대 위협**: "C-band가 융빙기에 실패한다"는 주장을
  고전 feature-tracking/MCC 계열로 한정하거나 DL 팔을 포함하지 않으면 "matcher 탓"으로 환원된다.
- **arXiv:2512.11083** — Alaska ice chart vs Copernicus SIC 2010–2025 비교, MIZ·연안에서 Copernicus가
  SIC를 과소평가. → **TB01**과 방향이 겹친다. 측정량(navigable-day, Δ 귀속)으로만 차별화 가능.
- **arXiv:2603.13573 / 2603.03503 / 2604.03094 / 2509.25437 / 2507.20507 / 2608.11883** —
  weak-label SAR 세분화, 200 m 해상도 pan-Arctic SIC + 불확실성, ViT 베이스라인, MIZ 라벨 정합.
  → **D2의 C0 work package가 반드시 참조·비교해야 할 최신 베이스라인군**. C0를 "새 분류기"가 아니라
  "**비-chart 검증축을 갖춘 분류기**"로 포지셔닝해야 하는 이유가 여기서 강화된다.
