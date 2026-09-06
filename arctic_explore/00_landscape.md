# 00_landscape — Stage 1 Step 0 (2026-09-04, OpenAlex 10 queries, from_publication_date 2023-01-01)

검증 방식: OpenAlex API 조회로 title/venue/DOI 확인 -> [V]. 아래는 §4.3에 없던 항목 위주.

## A. 검증된 선행 연구 [V]

| # | Work (year, venue) | DOI | Gist | Bucket |
|---|---|---|---|---|
| L1 | Model Ensemble With Dropout for Uncertainty Estimation in Sea Ice Segmentation Using Sentinel-1 SAR (2023, IEEE TGRS) | 10.1109/tgrs.2023.3331276 | S1 ice segmentation에 MC-dropout 앙상블로 화소별 불확실성 산출 | C, E |
| L2 | Inter-comparison and evaluation of Arctic sea ice type products (2023, The Cryosphere) | 10.5194/tc-17-279-2023 | OSI SAF 계열 ice type product 간 불일치 정량화; SAR 기준 부재 | B, E |
| L3 | AI4SeaIce: selecting loss functions for automated SAR sea ice concentration charting (2023, Sci Rep) | 10.1038/s41598-023-32467-x | AI4Arctic/ASIP 계열 SIC 자동화; chart를 label로 사용(순환성 잔존) | C |
| L4 | Incremental route planning based on daily risk assessment for Arctic navigation (2025, Ocean Engineering) | 10.1016/j.oceaneng.2025.120294 | 일 단위 risk 갱신형 incremental routing; 입력은 coarse ice field, 실현경로 검증 없음 | A |
| L5 | Arctic weather routing: review of ship performance models and ice routing algorithms (2023, Front Mar Sci) | 10.3389/fmars.2023.1190164 | routing 알고리즘·저항모델 리뷰; SAR-resolution 입력 부재를 공백으로 지적 | A |
| L6 | Object-oriented Bayesian network QRA of navigational accidents in ice-covered waters (2023, RESS) | 10.1016/j.ress.2023.109459 | besetting/충돌 BN 위험모형; 전문가 확률 기반, 관측 hazard layer 미결합 | J, F |
| L7 | An interpretable XGBoost-based approach for Arctic navigation risk assessment (2023, Risk Analysis) | 10.1111/risa.14175 | ML 위험 스코어 + SHAP; 입력은 재분석/PM, SAR 없음 | F, J |
| L8 | NISAR sea ice motion validation: preliminary results (2026, JPL Data) | 10.48577/jpl.zcd8gh | NISAR L-band 해빙 drift 초기 검증 — 공식 sea-ice 활용 착수 근거 | D |
| L9 | Sea ice detection using concurrent multispectral and SAR imagery (2024, RSE) | 10.1016/j.rse.2024.114073 | SAR+광학 동시관측 융합 ice/water; 융합 이득 정량화 선례 | D |
| L10 | Investigating coincident L- and S-band ASAR imagery over Arctic sea ice (2024, Geomatica) | 10.1016/j.geomat.2024.100034 | L/S 동시취득 비교; 위성 L+C 정식 비교는 미수행 | D |
| L11 | Incidence angle dependency and seasonal evolution of L and C-band backscatter over landfast ice (2024, Annals of Glaciology) | 10.1017/aog.2024.30 | L vs C 계절·입사각 의존성 실측 — L+C 분리도 연구의 물리 근거 | D, C |
| L12 | Estimation of sea ice drift and concentration during melt season using C-band dual-pol Sentinel-1 (2023, RSASE) | 10.1016/j.rsase.2023.101104 | 융빙기 C-band drift 성능 저하 보고 | C, D |
| L13 | Sea Ice Remote Sensing—Recent Developments in Methods and Climate Data Sets (2023, Surveys in Geophysics) | 10.1007/s10712-023-09781-0 | 종합 리뷰; navigability measurand 부재 확인 | all |
| L14 | Sea-Ice Classification and POLARIS-Based Risk-Informed Route Analysis, Barents (2026, Sustainability, MDPI) | 10.3390/su18147414 | SAR ice class -> POLARIS -> route; 실현경로/사고 검증 없음 — 최근접 선행, 반드시 차별화 | A |
| L15 | Navigation Risk Assessment of Arctic Shipping Routes Based on Bayesian Networks (2025, JMSE, MDPI) | 10.3390/jmse13122306 | 전문가 가중 BN; outcome validation 없음 | F |
| L16 | Navigability of LNG Carriers Along the NSR (2024, JMSE, MDPI) | 10.3390/jmse12122166 | PM 기반 navigability window; chokepoint/SAR 해상도 아님 | B |

## B. 공백 목록 (Stage 1 카드가 반드시 겨냥할 것)

1. **Measurand 공백**: ice *type* 분류는 포화(§4.3). hazard·navigability·reliability 자체를 측정량으로
   정의하고 안전 outcome에 연결한 연구가 없음 (L2, L3, L13).
2. **Routing 입력 해상도 공백**: routing 문헌(L4, L5, L14)은 coarse(PM/모델/chart) ice field 사용.
   40 m SAR hazard field가 최적경로·위험을 바꾸는지 정량화된 바 없음.
3. **Outcome validation 공백**: 위험지수·BN·ML(L6, L7, L15)은 전문가/재분석 기반이며 realised
   transit(CHNL), besetting/grounding 기록과 대조된 적이 거의 없음 -> §3.6 불가반증성 문제.
4. **L+C 공백**: NISAR sea-ice 활용은 drift validation 단계(L8). 위성 L+C 동시쌍 기반 융빙기
   ice/water·deformed vs level 분리도 비교는 미수행(L10, L11이 물리 근거만 제공).
5. **Uncertainty 공백**: L1이 화소 불확실성을 냈지만 이를 route risk bound로 전파한 연구 없음.
6. **Reliability 공백**: navigable window의 연간 변동성/최악연도/지속성(=신뢰도) 지표 부재(L16은 평균 창만).
7. **Coverage/센서 공백**: S1B gap(2022-2024)의 북극 감시 성능 영향은 문헌에 정량화된 바 없음.
8. **Charting 공백**: SAR-derived bathymetry·survey adequacy를 결빙 항로 이탈과 교차한 연구 없음.
9. **Melt-season 공백**: 융빙기 C-band 성능 저하는 알려졌으나(L12) 항해가능성 판단에의 영향 미평가.
10. **Port/coast 공백**: landfast timing + permafrost subsidence를 항만 운영 신뢰도로 통합한 사례 없음.

## C. 환경 상태 (Setup)
- GEE `alpha-earth-app` init OK (S1_GRD 접근 확인). **주의: noncommercial compute quota 초과 -> restricted mode.**
  메타데이터(P3)·소규모 reduceRegion 위주로 pilot 설계, 대형 export 금지.
- asf_search 13.0.1 설치 완료. `~/.netrc` 없음 -> EARTHDATA_LOGIN=false -> NISAR/ASF 토픽은 `PILOT=CATALOG`.
- geopandas/rasterio/sklearn/pandas/numpy 사용 가능.
