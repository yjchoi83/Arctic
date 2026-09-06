# Stage 4 — Novelty 재검증 A조 (TE01, TD05, TD01, TE02, TA01)

**API 가용성**: Semantic Scholar는 세션 내내 HTTP 429(무키 rate limit) — 초기 2건만 200(결과 0건), 이후 전 쿼리 실패,
재시도 2회·5–6 s sleep 무효. arXiv는 단일 phrase 쿼리만 응답하고 `AND` 복합 쿼리는 빈 응답(총 4/9 실패). 따라서
**Crossref가 주 검색축**이었고, dataset DOI는 DataCite로 보완. 모든 [V]는 세션 내 API 응답으로 확인.

### TE01
- RQ: Sentinel-1B 상실(2022–24)과 1C/1D 복구가 NSR chokepoint freeze-up의 usable drift-pair 가용성·hazard 관측가능성을 얼마나 붕괴/회복시켰는가.
- 쿼리: 4건 (Crossref 3, arXiv 1 `all:"Sentinel-1B" AND all:"sea ice"` → 0건). S2는 429로 사용 불가.
- 관련 hits:
  - `Arctic Sea ice leads detected using Sentinel-1B SAR image ... (2024, RSE) [V 10.1016/j.rse.2024.114193]` — S1B **데이터를 쓴** lead 연구이지 S1B **상실의 관측역량 영향**을 다루지 않음. 측정량이 다름.
  - `Community Challenge for Image-Derived Observation of Sea Ice Drift and Deformation (2026) [V 10.5194/egusphere-2026-4668]` — drift 알고리즘 벤치마크. 관측 **가용성**(pair 존재 여부)이 아니라 알고리즘 성능이 대상.
  - constellation 관련 hits는 전부 스케줄링·설계 논문(10.52202/078367-0002 등)으로 Arctic 관측역량 공백과 무관.
- VERDICT: **SURVIVES**. 2024–2026 구간에 "위성 상실을 자연실험으로 쓴 관측역량 정량화" 선행이 없음. 다만 §3.5대로 ASF/IABP 독립축을 반드시 유지할 것.

### TD05
- RQ: 융빙기 C-band drift retrieval success rate 하락을 IABP buoy 기준으로 정량화하고, 동일 시각 L-band가 그것을 회복시키는지 paired Δ로 판정.
- 쿼리: 4건 (Crossref 2, arXiv 1 성공 `all:"sea ice drift"`, S2 1 → 200이지만 0건 후 429).
- 관련 hits:
  - `Estimation of sea ice drift and concentration during melt season using C-band dual-polarimetric Sentinel-1 data (2023/2024, Remote Sensing Applications: Society and Environment) [V 10.1016/j.rsase.2023.101104]` — 융빙기 C-band drift라는 **동일 도메인**. 다만 abstract가 Crossref·S2·OpenAlex 어디에도 없어 "buoy 기준 success **rate**" 보고 여부를 확인 불가.
  - `Community Challenge for Image-Derived Observation of Sea Ice Drift and Deformation (2026) [V 10.5194/egusphere-2026-4668]` — buoy 네트워크 기반 **표준화된 drift 검증 절차와 데이터셋을 공개**. TD05의 "buoy로 drift를 검증한다"는 절차적 참신성은 이미 커뮤니티 자산이 됨.
  - `Towards Reliable Sea Ice Drift Estimation in the Arctic: Deep Learning Optical Flow on RADARSAT (2025) [V arXiv:2510.26653]` — matcher 개선 논문이며 계절별 실패율 측정이 목적이 아님.
  - `Wind-Informed Bayesian Classification of L-band SAR ... (2026) [V 10.5194/egusphere-2026-4775]` — L-band 융빙기 성능이지만 drift가 아니라 ice/water.
- VERDICT: **NARROWED**. 킬 근거 없음(§3.2: rsase 논문은 검증 강도를 확인할 수 없어 kill 요건 미충족, 그리고 [U] 내용으로 논증 금지). 단 프레이밍 두 곳을 바꿔야 함: (1) "융빙기 C-band 실패율 **최초** 정량화" 주장은 rsase 원문을 입수해 그 논문이 무엇을 보고했는지 명시한 뒤에만 가능 — 그 전까지는 "buoy 위치 기준 **success rate** 측정량"이라는 측정량 차별화로만 주장할 것. (2) 검증 프로토콜은 egusphere-2026-4668 챌린지 대비 위치를 밝히고, 가능하면 그 buoy truth를 재사용해 비교 가능성을 확보.

### TD01
- RQ: 융빙기 동일 40 m 격자에서 L+C가 C-only 대비 ice/water 및 deformed-vs-level 분리도를 개선하는가, 그 이득이 운용 가능한가(observability audit).
- 쿼리: 4건 (Crossref 3, arXiv 2 시도 중 `all:NISAR...` 복합 쿼리 실패). S2 429.
- 관련 hits:
  - `Wind-Informed Bayesian Classification of L-band SAR Imagery for Sea Ice and Open Water Separation (2026) [V 10.5194/egusphere-2026-4775]` — ALOS-2 dual-pol L-band, **융빙기 ice/water 분리** MCC>0.800, PMW 대비 우위. TD01 RQ1과 가장 가까움. 그러나 (a) L-only vs PMW 비교이지 **동일 격자 L+C vs C-only paired Δ**가 아니고, (b) 라벨 기준이 다르며, (c) deformed/level 문제를 다루지 않음 → §3.2 kill 요건(같은 RQ+비교 가능 데이터) 미충족.
  - `Incidence angle dependency and seasonal evolution of L and C-band SAR backscatter over landfast sea ice (2024, Annals of Glaciology) [V 10.1017/aog.2024.30]` — L·C 동시 특성화이나 landfast·backscatter 기술 연구이며 분리도(AUC/BA) 측정량이 아님.
  - `From snow wetting to pond formation: Stage-resolved L-band sea ice roughness ... (2026) [V 10.5194/egusphere-2026-2853]` — SMAP **수동** L-band. SAR가 아니므로 무관.
- VERDICT: **NARROWED**. RQ1(ice/water)의 "L-band가 융빙기에 유리하다"는 부분은 egusphere-2026-4775가 상당 부분 선점 → RQ1 단독으로는 발표 가치가 약해짐. 살아남는 핵심은 **동일 시각·동일 격자 paired L+C vs C-only Δ**, **RQ2 deformed-vs-level(ICESat-2 라벨)**, **RQ3 observability audit(latency 123 h, ~78 N 이북 granule 0)**. RQ1은 sanity-check tier로 강등하고 RQ2·RQ3를 논문 본체로 재배치할 것.

### TE02
- RQ: EW noise floor·입사각·IPF 버전 잔차 artefact가 운용 임계 결정을 얼마나 뒤집는가(flip rate), 그리고 그 flip이 기하·처리 기원임을 asc/desc 불변성으로 증명.
- 쿼리: 4건 (Crossref 4, arXiv 1 복합 쿼리 실패). S2 429.
- 관련 hits:
  - `Assessment of thermal noise impact on sea ice classification using Sentinel-1 images and U-Net (2024, IET Conf. Proc.) [V 10.1049/icp.2024.1598]` — noise → **분류 정확도** 영향 평가. TE02와 가장 가깝지만 측정량이 accuracy이지 **운용 임계 flip rate**가 아니고, IPF 버전 계단 bias와 asc/desc 불변성 대조가 없음. abstract 미제공(Crossref)이라 세부 확인 불가 → 킬 근거로 쓰지 않음.
  - `Incidence angle dependency ... L and C-band ... landfast sea ice (2024) [V 10.1017/aog.2024.30]` — landfast 불변 폴리곤이라는 TE02의 설계 전제(입사각 의존 분리)를 **뒷받침**하는 선행. 경쟁이 아니라 근거.
  - IPF 버전 drift를 다룬 2024–2026 논문은 Crossref 5건 중 0건.
- VERDICT: **SURVIVES**. 단, "noise floor가 분류에 영향을 준다"는 일반 명제는 이미 알려진 것으로 취급하고(icp.2024.1598 인용), 논문의 주장은 **오차예산의 의사결정 단위 환산(flip rate) + IPF 계단 bias + asc/desc 불변성 반증설계** 세 가지에만 걸 것.

### TA01
- RQ: chart 해상도 대신 SAR 해상도 RIO 면에서 경로를 재평가하면 음-RIO 구간이 남는가, flip의 spatial 성분이 기관 간 chart 불일치(human-noise floor)를 넘는가, posterior 전파 밴드가 판정구간을 얼마나 덮는가.
- 쿼리: 4건 (Crossref 3, arXiv 1 `all:POLARIS...` 실패). S2 429.
- 관련 hits:
  - `Sea-Ice Classification and POLARIS-Based Risk-Informed Route Analysis ... Bering Strait Using Sentinel-1 SAR and SVM (2026, Sustainability) [V 10.3390/su18147414]` — **S1 SAR → WMO/POLARIS 재분류 → RIO cost surface → least-cost path**를 Bering Strait에 이미 수행. 그러나 (a) 월 1씬 단위, (b) 정식 RIV 표가 아닌 **proxy weights**, (c) **chart 해상도 대조군이 없음** → 해상도 효과를 분리하지 않음, (d) flip rate의 calibration/spatial 분해 없음, (e) 분류기 posterior 전파 없음, (f) 검증은 MASIE 마스크 교차참조뿐. 같은 RQ가 아니고 설득력 있는 검증도 아니므로 §3.2 kill 미충족.
  - `Incremental route planning based on daily risk assessment for Arctic navigation (2025, Ocean Engineering) [V 10.1016/j.oceaneng.2025.120294]` — 라우팅 알고리즘 논문. 위험면의 **해상도·분류오차** 자체를 측정량으로 삼지 않음.
  - `POLARIS Risk Index Outcome estimates from sea ice models (2025) [V 10.2139/ssrn.5731495]` — 모델 기반 RIO. SAR 해상도 논점과 직교.
  - 보너스 [V]: `Inter- and intra-analyst ice edge assessment (2023) [V 10.6084/m9.figshare.22312648]` — RQ2의 **human-noise floor**를 뒷받침할 공개 데이터. 인용·활용 권장.
- VERDICT: **NARROWED**. "SAR 해상도로 POLARIS 라우팅을 처음 한다"는 프레이밍은 su18147414로 소진됨 → 기여 문장을 **"해상도 효과(resolution effect)와 분류기 오차(classifier error)를 분리하고, flip이 human-noise floor를 넘는지 판정한다"**로 재작성하고, su18147414를 "SAR-POLARIS 라우팅은 이미 가능하나 해상도 효과가 검정되지 않았다"는 motivation으로 명시 인용할 것.

## [U] 재검증
- **stage3/TA01.md:22 AI4Arctic/ASIP** → **[V]**. DataCite 확인: `Ready-To-Train AI4Arctic Sea Ice Challenge Dataset` (DTU, 2023) **10.11583/DTU.21316608.v3**, 원자료 `Raw AI4Arctic Sea Ice Challenge Dataset` **10.11583/DTU.21284967.v3**. 정식 명칭은 ASIP가 아니라 AI4Arctic Sea Ice Challenge Dataset이므로 stage3 표기를 수정할 것.
- **stage3/TD05.md:39 10.1016/j.rsase.2023.101104** → **메타데이터 [V] / 내용 [U]**. Crossref·S2·OpenAlex 3축에서 제목·연도·저널 일치 확인(`Estimation of sea ice drift and concentration during melt season using C-band dual-polarimetric Sentinel-1 data`, RSASE, S2 연도 2023 / Crossref 발행 2024). 그러나 세 API 모두 abstract를 제공하지 않고 closed access → **"융빙기 C-band drift 실패율을 in-situ로 검증해 보고했는지"는 여전히 확인 불가**. 따라서 이 논문을 근거로도 반박으로도 쓸 수 없으며, TD05는 원문 입수 전까지 "최초 정량화" 주장을 보류해야 함.
