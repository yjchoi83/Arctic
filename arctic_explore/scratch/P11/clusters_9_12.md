# Bibliography verification — clusters 9-12

Verification axes actually used this session:
- **Crossref** `https://api.crossref.org/works/<doi>` and `/works?query.bibliographic=` — primary, worked reliably.
- **OpenLibrary** `https://openlibrary.org/search.json?q=` — books only (cluster 9).
- **arXiv API / web** — only to establish that Ice-FMBench exists; its record was then confirmed on Crossref.
- **Semantic Scholar (unauthenticated): UNUSABLE.** `$S2_API_KEY` is unset; every `graph/v1/paper/search` call returned HTTP 429 after the full 2s/4s/8s backoff. No item below rests on S2.
- All raw responses cached under `scratch/s2cache/<sha1-of-url>.json`.

---

## Cluster 9 — Length-biased sampling and censored durations

| bibkey | authors | year | title | venue | DOI/arXiv/ISBN | verified? (API) | relevance |
|---|---|---|---|---|---|---|---|
| feller1971introduction | W. Feller | 1971 (2nd ed.) | An Introduction to Probability Theory and Its Applications, Vol. II | Wiley (book) | ISBN 0471257095 / 9780471257097 | YES — OpenLibrary search.json | Canonical source for the inspection/waiting-time paradox: sampling a renewal process at a random epoch length-biases the observed interval. |
| cox1962renewal | D. R. Cox | 1962 | Renewal Theory | Methuen / Chapman & Hall (book) | ISBN 041220570X / 9780412205705 | YES — OpenLibrary search.json | Renewal-theoretic backbone for treating Sentinel-1 revisit gaps as inter-arrival times with a spread-out equilibrium distribution. |
| kaplan1958nonparametric | E. L. Kaplan; P. Meier | 1958 | Nonparametric Estimation from Incomplete Observations | Journal of the American Statistical Association | 10.1080/01621459.1958.10501452 | YES — Crossref | Standard estimator for the revisit-gap survival function when gaps are right-censored by the ends of the observation window. |
| vardi1989multiplicative | Y. Vardi | 1989 | Multiplicative censoring, renewal processes, deconvolution and decreasing density: Nonparametric estimation | Biometrika | 10.1093/biomet/76.4.751 | YES — Crossref | Directly treats nonparametric estimation under length-biased renewal sampling — the bias correction needed when gaps are observed through a sampling window. |
| turnbull1976empirical | B. W. Turnbull | 1976 | The Empirical Distribution Function with Arbitrarily Grouped, Censored and Truncated Data | Journal of the Royal Statistical Society Series B | 10.1111/j.2517-6161.1976.tb01597.x | YES — Crossref | Handles interval-censoring and truncation together, which is the actual observation regime for gaps bounded only by acquisition timestamps. |

**target 2-3, verified 5.** No seeds discarded. Both books carry ISBN/publisher only (no DOI exists); the ISBNs were read out of an OpenLibrary API response. Note on Feller: the OpenLibrary record for Vol. II lists first publication 1966; ISBN 0471257095 is the 1971 second edition cited here.

---

## Cluster 10 — Arctic shipping traffic and policy

| bibkey | authors | year | title | venue | DOI/arXiv/URL | verified? (API) | relevance |
|---|---|---|---|---|---|---|---|
| gunnarsson2021recent | B. Gunnarsson | 2021 | Recent ship traffic and developing shipping trends on the Northern Sea Route—Policy implications for future arctic shipping | Marine Policy | 10.1016/j.marpol.2020.104369 | YES — Crossref | Establishes where and when NSR traffic actually concentrates, motivating the choke-point regions in which SAR observability matters. |
| eguiluz2016quantitative | V. M. Eguíluz; J. Fernández-Gracia; X. Irigoien; C. M. Duarte | 2016 | A quantitative assessment of Arctic shipping in 2010–2014 | Scientific Reports | 10.1038/srep30682 | YES — Crossref | AIS-derived quantification of pan-Arctic vessel activity; the traffic-density baseline against which observability gaps are weighted. |
| aksenov2017future | Y. Aksenov; E. E. Popova; A. Yool; A. J. G. Nurser; T. D. Williams; L. Bertino; J. Bergh | 2017 | On the future navigability of Arctic sea routes: High-resolution projections of the Arctic Ocean and sea ice | Marine Policy | 10.1016/j.marpol.2015.12.027 | YES — Crossref | Projects the seasonal navigability window, setting the melt-season period over which C-band observability limits bite hardest. |
| melia2016seaice | N. Melia; K. Haines; E. Hawkins | 2016 | Sea ice decline and 21st century trans-Arctic shipping routes | Geophysical Research Letters | 10.1002/2016GL069315 | YES — Crossref | Route-level projections showing which corridors open, and when — the spatial prior for where monitoring demand will grow. |
| chnl_nsr_transits | CHNL Information Office (Northern Sea Route Information Office) / Arctic Logistics Information Office | 2011–2024 (rolling) | NSR transit statistics | **GREY LITERATURE — no DOI** | https://arctic-lio.com/category/nsr-transit-statistics/ | YES — page retrieved live (WebFetch); organisation and 2011–2024 coverage confirmed on the page. **No DOI exists; none invented.** | Per-voyage transit counts used as the traffic denominator for revisit-adequacy statistics. Page notes the site is no longer actively updated. |
| bellona2025nsr | Bellona Foundation | 2025 | The Northern Sea Route: Russia's industrial and political expansion, its environmental costs, and Arctic shipping risks | **GREY LITERATURE — no DOI** | https://bellona.org/publication/the-northern-sea-route | YES — page retrieved live (WebFetch); title, subtitle, publisher and 2025 date read off the publication page. **No DOI exists; none invented.** | Recent NSR traffic composition, including unflagged/AIS-dark vessels — the case for SAR-based rather than AIS-based monitoring. |

**target 3-4, verified 6** (4 seeds + 2 additions). No seeds discarded. The two grey-literature items are recorded by URL and are explicitly marked; they carry no identifier of any kind.

---

## Cluster 11 — Melt-season, noise-floor and incidence-angle limits of C-band SAR

| bibkey | authors | year | title | venue | DOI | verified? (API) | relevance |
|---|---|---|---|---|---|---|---|
| lohse2020mapping | J. Lohse; A. P. Doulgeris; W. Dierking | 2020 | Mapping sea-ice types from Sentinel-1 considering the surface-type dependent effect of incidence angle | Annals of Glaciology | 10.1017/aog.2020.45 | YES — Crossref | Quantifies the surface-type-dependent incidence-angle slope that makes backscatter non-stationary across an EW swath. |
| park2018efficient | J.-W. Park; A. A. Korosov; M. Babiker; S. Sandven; J.-S. Won | 2018 | Efficient Thermal Noise Removal for Sentinel-1 TOPSAR Cross-Polarization Channel | IEEE Transactions on Geoscience and Remote Sensing | 10.1109/TGRS.2017.2765248 | YES — Crossref | The standard HV noise-floor correction; defines the residual noise level that bounds usable contrast in EW. |
| bhattacharjee2024estimation | S. Bhattacharjee; R. D. Garg | 2024 | Estimation of sea ice drift and concentration during melt season using C-band dual-polarimetric Sentinel-1 data | Remote Sensing Applications: Society and Environment | 10.1016/j.rsase.2023.101104 | YES — Crossref, **metadata only (reused from earlier session; full text was never retrieved)** | Melt-season degradation of C-band drift retrieval — the seasonal failure mode this paper quantifies. |
| korosov2022thermal | A. Korosov; D. Demchev; N. Miranda; N. Franceschi; J.-W. Park | 2022 | Thermal Denoising of Cross-Polarized Sentinel-1 Data in Interferometric and Extra Wide Swath Modes | IEEE Transactions on Geoscience and Remote Sensing | 10.1109/TGRS.2021.3131036 | YES — Crossref | Updated denoising covering both IW and EW; supersedes the per-mode noise vectors and sets the current achievable noise floor. |
| lee2020sentinel | P. Q. Lee; L. Xu; D. A. Clausi | 2020 | Sentinel-1 additive noise removal from cross-polarization extra-wide TOPSAR with dynamic least-squares | Remote Sensing of Environment | 10.1016/j.rse.2020.111982 | YES — Crossref | Alternative scene-adaptive EW denoising in the target venue; shows how much residual banding survives correction. |

**target 3, verified 5.** No seeds discarded. The 2023/2024 RSASE item is reused as metadata-only, exactly as flagged.

---

## Cluster 12 — Deep-learning sea-ice classification and drift (context)

| bibkey | authors | year | title | venue | DOI/arXiv | verified? (API) | relevance |
|---|---|---|---|---|---|---|---|
| ai4arctic2022dataset | AI4Arctic / DTU (Buus-Hinkler et al.) | 2022 | AI4Arctic Sea Ice Challenge Dataset | DTU Data (dataset) | 10.11583/DTU.21316608.v3 | YES — **reused, verified in an earlier session** | The benchmark SAR/ice-chart corpus underpinning AutoICE and every downstream model. |
| stokholm2024autoice | A. Stokholm; J. Buus-Hinkler; T. Wulf; A. Korosov; R. Saldo; L. T. Pedersen; et al. (36 authors) | 2024 | The AutoICE Challenge | The Cryosphere | 10.5194/tc-18-3471-2024 | YES — Crossref | The reference community benchmark for automated sea-ice mapping; defines the accuracy ceiling current DL methods reach. |
| chen2024mmseaice | X. Chen; M. Patel; F. J. Pena Cantu; J. Park; J. Noa Turnes; L. Xu; K. A. Scott; D. A. Clausi | 2024 | MMSeaIce: a collection of techniques for improving sea ice mapping with a multi-task model | The Cryosphere | 10.5194/tc-18-1621-2024 | YES — Crossref | The winning AutoICE entry; the concrete state of the art for SIC/SoD/floe-size retrieval from Sentinel-1. |
| taleghan2025icefmbench | S. Alkaee Taleghan; M. Karimzadeh; A. P. Barrett; W. N. Meier; F. Banaei-Kashani | **2025** | Ice-FMBench: A Foundation Model Benchmark for Sea Ice Type Segmentation | Proceedings of the 1st ACM SIGSPATIAL International Workshop on Polar Data Science | 10.1145/3764922.3771202 (arXiv:2503.22516) | YES — Crossref (existence first established via web/arXiv, then confirmed on Crossref) | Foundation-model transferability to SAR sea-ice segmentation; shows generic RS foundation models degrade on polar EW data. |
| opticalflow2025benchmark | (see earlier session record) | 2025 | optical-flow benchmark | arXiv preprint | arXiv:2510.26653 | YES — **reused, verified in an earlier session** | Optical-flow baselines relevant to dense sea-ice drift estimation. |
| muckenhuber2016opensource | S. Muckenhuber; A. A. Korosov; S. Sandven | 2016 | Open-source feature-tracking algorithm for sea ice drift retrieval from Sentinel-1 SAR imagery | The Cryosphere | 10.5194/tc-10-913-2016 | YES — Crossref | The open feature-tracking baseline that DL drift methods are measured against, and the drift retrieval used operationally on S1. |

**target 3, verified 6.** **Seed correction:** the seed named "IceFMBench 2026". The work exists but is **Ice-FMBench, 2025** (arXiv March 2025; ACM SIGSPATIAL Polar Data Science workshop proceedings, 2025). Year corrected; nothing discarded.

MDPI count across these four clusters: **0**.

---

## Verified identifiers (one per line)

ISBN 9780471257097
ISBN 9780412205705
10.1080/01621459.1958.10501452
10.1093/biomet/76.4.751
10.1111/j.2517-6161.1976.tb01597.x
10.1016/j.marpol.2020.104369
10.1038/srep30682
10.1016/j.marpol.2015.12.027
10.1002/2016GL069315
https://arctic-lio.com/category/nsr-transit-statistics/
https://bellona.org/publication/the-northern-sea-route
10.1017/aog.2020.45
10.1109/TGRS.2017.2765248
10.1016/j.rsase.2023.101104
10.1109/TGRS.2021.3131036
10.1016/j.rse.2020.111982
10.11583/DTU.21316608.v3
10.5194/tc-18-3471-2024
10.5194/tc-18-1621-2024
10.1145/3764922.3771202
arXiv:2503.22516
arXiv:2510.26653
10.5194/tc-10-913-2016
