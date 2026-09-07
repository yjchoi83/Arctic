# LITERATURE_MAP — cluster to papers to relevance to section

Every key resolves to an entry in `paper/references.bib`. Verification route is recorded in
`scratch/P11/clusters_*.md`; all responses are cached in `scratch/s2cache/`.

## Cluster 1 — Sentinel-1 mission, EW mode, Arctic acquisition
*Cited in: 1 Introduction; 2.1 Data; 5.4 Discussion*  ·  **5 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `dabboor2014rcm` | 2014 | Remote Sensing of Environment | Sea-ice classification with simulated RADARSAT Constellation compact polarimetry; the basis for our RCM discussion. |
| `geudtner2021copernicus` | 2021 | Proc. IGARSS 2021 | Frames the forward-looking part of the discussion: what C-band continuity and revisit will look like after the current constellation. |
| `potin2019copernicus` | 2019 | Proc. IGARSS 2019 | Documents the operational observation scenario and conflict-resolution priorities that govern where EW acquisitions actually fall over the Arctic. |
| `torres2012gmes` | 2012 | Remote Sensing of Environment | Primary mission reference: defines the EW/IW modes, swath geometry and duty-cycle limits that set the Arctic observability ceiling we quantify. |
| `torres2017evolution` | 2017 | Proc. IGARSS 2017 | The only peer-reviewed description we could verify of the Sentinel-1C/-1D units, used to justify assumptions about post-2024 constellation capability. |

## Cluster 2 — SAR-based sea-ice monitoring and ice-service operations
*Cited in: 1 Introduction; 2.1 Data; 5.3 Discussion*  ·  **12 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `cheng2020accuracy` | 2020 | The Cryosphere | Quantifies the human-analyst error floor in a national ice service, the baseline any SAR-derived automated product is judged against. |
| `dai2026panarctic` | 2026 | Remote Sensing of Environment | Pan-Arctic winter sea-ice classification from Sentinel-1 dual-pol; the downstream product class most exposed to acquisition gaps. |
| `dierking2013sea` | 2013 | Oceanography | Canonical statement of what C-band SAR can and cannot resolve on sea ice; anchors our interpretation of backscatter-limited observability. |
| `eriksson2025finnish` | 2025 | Frontiers in Marine Science | Recent first-hand account of a national ice service's dependence on Sentinel-1 timeliness and coverage — the operational stake in our observability qu |
| `evans2023iceberg` | 2023 | Remote Sensing of Environment | Unsupervised iceberg detection within sea ice from dual-pol SAR; adjacent hazard-detection task. |
| `karvonen2022baltic` | 2022 | IEEE TGRS | Representative automated ice-charting chain built directly on operational C-band SAR; shows the downstream product our coverage statistics constrain. |
| `komarov2019detection` | 2019 | IEEE Transactions on Geoscience and Remote S | FYI/MYI discrimination from dual-pol SAR; ice-type context for hazard interpretation. |
| `leigh2014automated` | 2014 | IEEE Transactions on Geoscience and Remote S | Automated dual-pol ice-water classification; the operational baseline our success rate presumes. |
| `lohse2020mapping` | 2020 | Annals of Glaciology | Shows incidence-angle dependence across the EW swath, a geometry effect that couples directly to which parts of a scene are usable. |
| `lyu2022metaanalysis` | 2022 | IEEE Journal of Selected Topics in Applied E | Meta-analysis of spaceborne polarimetric SAR sea-ice monitoring; scope of what SAR is used for operationally. |
| `shokr2023polarimetric` | 2023 | IEEE Journal of Selected Topics in Applied E | Review of polarimetric SAR sea-ice applications; situates the HH/HV EW products we count. |
| `zakhvatkina2019satellite` | 2019 | Geosciences (MDPI) | Review of the SAR sea-ice classification literature that our observability metrics are meant to feed. |

## Cluster 3 — Sea-ice drift retrieval from SAR
*Cited in: 1 Introduction; 3.6 Methods; 4.3 Results*  ·  **9 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `demchev2017sea` | 2017 | IEEE TGRS | Feature-detector-based alternative whose performance also degrades with increasing pair separation — the variable our revisit statistics control. |
| `hollands2015reliability` | 2015 | IEEE Journal of Selected Topics in Applied E | Reliability measures for SAR ice-motion retrieval; the precedent for treating retrieval success as a reported quantity, which our success rate operati |
| `howell2022generating` | 2022 | The Cryosphere | Demonstrates basin-scale operational drift from Sentinel-1 plus RCM — the production system whose input availability is our subject. |
| `komarov2014sea` | 2014 | IEEE TGRS | Reference cross-correlation drift retrieval; establishes the image-pair quality and separation requirements we test against real Sentinel-1 sampling. |
| `korosov2017combination` | 2017 | Remote Sensing (MDPI) | Parameterization study underlying the drift retrieval whose achievable coverage this paper bounds. |
| `lehtiranta2015comparing` | 2015 | The Cryosphere | Frequency-dependence of drift retrieval success, relevant to how far C-band-only conclusions generalise. |
| `muckenhuber2017open` | 2017 | The Cryosphere | The hybrid feature-tracking/pattern-matching approach applied to exactly the Sentinel-1 EW data stream we assess. |
| `qiu2022retrieval` | 2022 | IEEE Transactions on Geoscience and Remote S | Sequential-SAR drift retrieval from the central Arctic to Fram Strait; regional counterpart to our strait fields. |
| `yang2024drift` | 2024 | IEEE Journal of Selected Topics in Applied E | Feature-tracking drift extraction improvements; directly comparable matcher family to ours. |

## Cluster 4 — Sea-ice deformation and buoy-based statistics
*Cited in: 1 Introduction; 3.2 Methods; 6.1 Limitations*  ·  **8 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `bouillon2015producing` | 2015 | The Cryosphere | The explicit bridge from SAR drift fields to deformation products, including how pair timing and triangulation propagate into deformation error. |
| `hutchings2008small` | 2008 | JGR Oceans | Buoy-array deformation statistics at the scales our SAR pairs would need to resolve. |
| `hutchings2011spatial` | 2011 | Annals of Glaciology | Buoy-array design guidance for separating spatial from temporal deformation scaling; underpins our buoy-comparison design. (Note: a corrigendum exists |
| `itkin2025novel` | 2025 | The Cryosphere | Current state of the art for extracting deformation and LKFs from imaging remote sensing; the analysis our observability limits apply to. |
| `marsan2004scale` | 2004 | Physical Review Letters | Establishes the spatial scaling law for deformation, which is why sampling scale (and hence SAR revisit) determines the measured deformation rate. |
| `oikkonen2017small` | 2017 | JGR Oceans | Sub-kilometre deformation from a dense buoy array, defining the regime that current SAR sampling under-resolves. |
| `rampal2008scaling` | 2008 | JGR Oceans | Joint space-time scaling from buoy dispersion; supplies the temporal-scaling exponent used to interpret irregular revisit intervals. |
| `stern2009spatial` | 2009 | JGR Oceans | RGPS-based spatial scaling companion to Marsan et al.; directly relates observation footprint to recovered deformation magnitude. |

## Cluster 5 — Navigation hazards, pressured ice, besetting, Polar Code
*Cited in: 1 Introduction; 3.2 Methods (requirement); 5.1 Discussion*  ·  **7 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `aksenov2017navigability` | 2017 | Marine Policy | Projects where and when Arctic routes open, defining the geography over which SAR observability matters. |
| `fu2016besetting` | 2016 | Reliability Engineering & System Safety | Quantitative besetting-probability model; shows which ice-state variables a besetting forecast needs observed. |
| `imo2016polaris` | 2016 | IMO circular — GREY LITERATURE, no DOI | The operational risk-index framework that turns an ice chart into a permitted speed/entry decision; the regulatory hook for SAR-derived ice informatio |
| `kotovirta2009route` | 2009 | Cold Regions Science and Technology | Classic ship-transit-in-ice routing system; establishes the ice-information-to-route-cost chain this paper's observability metric feeds. |
| `kubat2016compression` | 2016 | Arctic Technology Conference (OTC), proceedi | The Kubat *et al.* 2016 ice-pressure seed: maps compressive-ice (besetting) risk across Canadian Arctic/sub-Arctic shipping zones including Hudson Str |
| `lehtola2019routes` | 2019 | Cold Regions Science and Technology | Route-safety model whose input is a gridded ice field — directly consumes the products a Sentinel-1 gap degrades. |
| `lensu2019bigdata` | 2019 | Marine Policy | Frames ice-navigation decision support as a data-availability problem, matching the observability framing. |

## Cluster 6 — Observing-system experiments and network design
*Cited in: 1 Introduction; 3.4 Methods; 4.4 Results*  ·  **5 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `boukabara2016gaps` | 2016 | Monthly Weather Review | An explicit OSE on a *satellite coverage gap* — the closest meteorological analogue to the Sentinel-1B loss experiment. |
| `howell2022motion` | 2022 | The Cryosphere | Multi-constellation SAR revisit in practice: quantifies how combining S1 and RCM changes pan-Arctic drift-retrieval coverage. |
| `kaminski2015network` | 2015 | The Cryosphere | Quantitative network design applied to Arctic sea ice: the methodological precedent for scoring an observing network rather than a single sensor. |
| `kaminski2018mission` | 2018 | The Cryosphere | Mission-benefit analysis linking observation availability to forecast skill — the value-of-observation argument this paper makes for SAR. |
| `langland2004impact` | 2004 | Tellus A: Dynamic Meteorology and Oceanograp | The classical NWP adjoint observation-impact reference; the OSE/FSO lineage the sea-ice observability metric borrows from. |

## Cluster 7 — Passive-microwave drift products and coastal limits
*Cited in: 2.3 Data; 4.3 Results*  ·  **4 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `lavergne2010drift` | 2010 | Journal of Geophysical Research: Oceans | The continuous maximum cross-correlation method behind the operational passive-microwave drift products, and its stated resolution floor. |
| `lavergne2023osisaf` | 2023 | Earth System Science Data | The current PM drift CDR; its 62.5 km grid and coastal masking are the baseline SAR observability is measured against. |
| `sumata2014inter` | 2014 | Journal of Geophysical Research: Oceans | Product-to-product spread of Arctic drift estimates, largest near coasts and in the marginal ice zone. |
| `sumata2015uncertainty` | 2015 | Journal of Geophysical Research: Oceans | Uses high-resolution SAR as the reference to bound low-resolution PM drift error — exactly the SAR-vs-PM comparison this paper extends. |

## Cluster 8 — Observation gaps propagating into products
*Cited in: 1 Introduction; 4.6 Results; 6.3 Limitations*  ·  **5 verified** (2 strict gap-quantification + 3 product records)

| key | year | venue | relevance |
|---|---|---|---|
| `geiger2001resolution` | 2001 | Solid Mechanics and Its Applications (Springer) | **[P12] strict gap-quantification.** Quantifies how temporal and spatial sampling resolution propagates into derived sea-ice drift and deformation — the mechanism this paper measures with H. Cited in §1 as the established form of the claim. |
| `covington2022bridging` | 2022 | J. Adv. Modeling Earth Systems | **[P12] strict gap-quantification.** Quantifies gaps in a Lagrangian ice-floe observation record caused by atmospheric obscuration and recovers the missing floe dynamics; the closest existing treatment of observation gaps as a measurable deficit. Cited in §1. |
| `wuite2026velocity` | 2026 | Remote Sensing of Environment | Decade-long Sentinel-1 polar ice-velocity record built from repeat-pass SAR, spanning the Sentinel-1B failure; stands in for the requested InSAR acqui |
| `wulf2024panarctic` | 2024 | The Cryosphere | The pan-Arctic SIC seed: a SAR+PM product whose SAR component is limited by where Sentinel-1 actually acquires. |
| `wulf2026decade` | 2026 | Remote Sensing of Environment | The DMI-ASIP decade paper: a ten-year Sentinel-1 SIC record spanning the Sentinel-1B loss, i.e. the downstream product this study's gaps propagate int |

## Cluster 9 — Length-biased sampling and censored durations
*Cited in: 3.1 Methods (length-biasing); 3.2 Methods (censoring)*  ·  **5 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `cox1962renewal` | 1962 | Methuen / Chapman & Hall (book) | Renewal-theoretic backbone for treating Sentinel-1 revisit gaps as inter-arrival times with a spread-out equilibrium distribution. |
| `feller1971introduction` | 1971 (2nd ed.) | Wiley (book) | Canonical source for the inspection/waiting-time paradox: sampling a renewal process at a random epoch length-biases the observed interval. |
| `kaplan1958nonparametric` | 1958 | Journal of the American Statistical Associat | Standard estimator for the revisit-gap survival function when gaps are right-censored by the ends of the observation window. |
| `turnbull1976empirical` | 1976 | Journal of the Royal Statistical Society Ser | Handles interval-censoring and truncation together, which is the actual observation regime for gaps bounded only by acquisition timestamps. |
| `vardi1989multiplicative` | 1989 | Biometrika | Directly treats nonparametric estimation under length-biased renewal sampling — the bias correction needed when gaps are observed through a sampling w |

## Cluster 10 — Arctic shipping traffic and policy
*Cited in: 1 Introduction; 5.1 Discussion*  ·  **5 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `aksenov2017future` | 2017 | Marine Policy | Projects the seasonal navigability window, setting the melt-season period over which C-band observability limits bite hardest. |
| `bellona2025nsr` | 2025 | GREY LITERATURE — no DOI | Recent NSR traffic composition, including unflagged/AIS-dark vessels — the case for SAR-based rather than AIS-based monitoring. |
| `eguiluz2016quantitative` | 2016 | Scientific Reports | AIS-derived quantification of pan-Arctic vessel activity; the traffic-density baseline against which observability gaps are weighted. |
| `gunnarsson2021recent` | 2021 | Marine Policy | Establishes where and when NSR traffic actually concentrates, motivating the choke-point regions in which SAR observability matters. |
| `melia2016seaice` | 2016 | Geophysical Research Letters | Route-level projections showing which corridors open, and when — the spatial prior for where monitoring demand will grow. |

## Cluster 11 — Melt-season, noise-floor and incidence-angle limits of C-band
*Cited in: 3.6 Methods; 4.7 Results; 5.2 Discussion*  ·  **6 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `bhattacharjee2024estimation` | 2024 | Remote Sensing Applications: Society and Env | Melt-season degradation of C-band drift retrieval — the seasonal failure mode this paper quantifies. |
| `korosov2022thermal` | 2022 | IEEE Transactions on Geoscience and Remote S | Updated denoising covering both IW and EW; supersedes the per-mode noise vectors and sets the current achievable noise floor. |
| `lee2020sentinel` | 2020 | Remote Sensing of Environment | Alternative scene-adaptive EW denoising in the target venue; shows how much residual banding survives correction. |
| `meyer2011landfast` | 2011 | Remote Sensing of Environment | L-band InSAR landfast-ice mapping; precedent for L-band advantages we discuss for NISAR. |
| `park2018efficient` | 2018 | IEEE Transactions on Geoscience and Remote S | The standard HV noise-floor correction; defines the residual noise level that bounds usable contrast in EW. |
| `singha2021robustness` | 2021 | IEEE Transactions on Geoscience and Remote S | Robustness of SAR ice-type classification across incidence angles and seasons; the confounder our preprocessing removes. |

## Cluster 12 — Deep-learning sea-ice classification and drift
*Cited in: 5.2 Discussion; 6.6 Limitations*  ·  **7 verified**

| key | year | venue | relevance |
|---|---|---|---|
| `chen2024mmseaice` | 2024 | The Cryosphere | The winning AutoICE entry; the concrete state of the art for SIC/SoD/floe-size retrieval from Sentinel-1. |
| `huang2024deeplearning` | 2024 | Remote Sensing of Environment | Deep-learning ice-type classification in the Beaufort Sea; contemporary retrieval performance. |
| `muckenhuber2016opensource` | 2016 | The Cryosphere | The open feature-tracking baseline that DL drift methods are measured against, and the drift retrieval used operationally on S1. |
| `martin2025opticalflow` | 2025 | arXiv preprint (2510.26653) | Martin & Gallego: benchmark of 48 deep-learning optical-flow models on RADARSAT-2 ScanSAR ice imagery against GNSS buoys; best models reach 300-400 m endpoint error. Cited in §5.2 as the development that could change the melt-season retrieval picture. |
| `stokholm2024autoice` | 2024 | The Cryosphere | The reference community benchmark for automated sea-ice mapping; defines the accuracy ceiling current DL methods reach. |
| `taleghan2025icefmbench` | 2025 | Proceedings of the 1st ACM SIGSPATIAL Intern | Foundation-model transferability to SAR sea-ice segmentation; shows generic RS foundation models degrade on polar EW data. |
| `zhao2023deeplearning` | 2023 | IEEE Journal of Selected Topics in Applied E | Deep-learning sea-ice classification from Sentinel-1 and AMSR-2; context for retrieval methods beyond feature tracking. |
