# ARC-P7 — consequence in Sentinel-1-dependent products
사전등록 `stage5/PLAN.md §F`. **판정: consequence NOT demonstrated.** 논문 범위를 observability로 좁힌다.

## 1. H9는 검정되지 못했다 — 실패가 아니라 **자료 접근 불가**
사전등록된 H9(제품 가용성 대 H_state의 Spearman ρ ≥ 0.5)를 계산하려면 아래 둘 중 하나가 필요하다.

| 산출물 | 상태 | 증거 |
|---|---|---|
| DMI-ASIP L3 일별 SIC | 존재하나 **다운로드 불가** | `SEAICE_ARC_PHY_AUTO_L3_MYNRT_011_023`, dataset `cmems_obs-si_arc_phy_{my,nrt}_l3_P1D`; `copernicusmarine` subset 시 **username 프롬프트**, 저장된 자격증명 없음 |
| DTU Sentinel-1 drift | 존재하나 **다운로드 불가** | NRT `cmems_sat-si_glo_drift_nrt_north_d`(011_006), MY `cmems_obs-si_glo_phy-drift-north_my_l4_P1D-m`(011_020); 동일 |
| OSI SAF **SAR** drift(대체 후보) | **존재하지 않음** | OSI-407 중단, `drift_mr`은 파일명 `avhrr-ch4` → AVHRR 기반; `drift_sar` 404 |
| MET Norway ice-chart quicklook | 접근 가능하나 **부적합** | `cryo.met.no/archive/ice-service/icecharts/quicklooks/...` 200, 1997–2026. **PNG 래스터**이며 차트는 고정 일정으로 발행되어 "S1 결측 → 산출물 결측"의 정량 지표가 되지 못한다 |

**계정은 만들지 않았다**(PLAN §G). 따라서 H9는 **기각도 채택도 아닌 미검정**이며, 그 사실을 그대로 적는다.
"제품이 영향을 받지 않았다"는 결론으로 읽어서는 안 된다 — 검사 자체를 하지 못했다.

## 2. 대신 말할 수 있는 것 (직접 증거는 아님)
- DTU S1 drift와 DMI-ASIP는 **정의상 Sentinel-1 입력에 의존**한다. P3이 보인 취득 붕괴
  (chokepoint H_state 0.504 → 0.363, H_episode 0.200 → 0.097)가 이 산출물들에 **전파되지 않았을 물리적 경로는 없다**.
  그러나 이것은 **추론이지 측정이 아니며**, 본 논문은 그 차이를 흐리지 않는다.
- P4에서 관측된 것 하나는 산출물 수준의 직접 증거에 가깝다: Sannikov에서 **단일 취득은 24 h 내에 있어도
  drift 쌍이 24 h 내에 존재하지 않아** QC 대상 사건이 0건이었다. drift 산출물은 쌍이 없으면 생성되지 않는다.

## 3. H9를 실제로 검정하려면
(1) Copernicus Marine 계정 1개(무료) — 사용자가 발급하면 `copernicusmarine login` 후 §1의 dataset id로 즉시 실행 가능.
(2) region×season×year 가용일수를 P3의 `P3_region_season_year.csv`와 join → Spearman.
이 두 단계는 자격증명만 있으면 **추가 다운로드 1 GB 미만**으로 끝난다.
