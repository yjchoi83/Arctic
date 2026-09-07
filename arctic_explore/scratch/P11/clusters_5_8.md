# Bibliography verification — clusters 5–8

Verification axis: **Crossref REST API** (`api.crossref.org/works/<doi>` and `?query.bibliographic=`), all responses cached under `scratch/s2cache/`.
Semantic Scholar was queried **unauthenticated** (`$S2_API_KEY` confirmed unset) and returned HTTP 429 on essentially every attempt even with 2/4/8 s exponential backoff; one query eventually returned after two 429s but with irrelevant hits. **S2 was effectively unusable**; every entry below was verified through Crossref.

"verified?" = title + year + venue + authors retrieved from a live API response in this session, with a DOI.

---

## Cluster 5 — Navigation hazards, pressured ice, besetting, Polar Code

| bibkey | authors | year | title | venue | DOI/arXiv | verified? | one-line relevance |
|---|---|---|---|---|---|---|---|
| kubat2016compression | Kubat I.; Watson D.; Sayed M. | 2016 | Ice Compression Risks to Shipping Over Canadian Arctic and Sub-Arctic Zones | Arctic Technology Conference (OTC), proceedings-article | 10.4043/27348-ms | yes | The Kubat *et al.* 2016 ice-pressure seed: maps compressive-ice (besetting) risk across Canadian Arctic/sub-Arctic shipping zones including Hudson Strait. |
| imo2016polaris | International Maritime Organization | 2016 | Guidance on Methodologies for Assessing Operational Capabilities and Limitations in Ice (POLARIS), MSC.1/Circ.1519 | IMO circular — **GREY LITERATURE, no DOI** | none; entry point verified HTTP 200: https://www.imo.org/en/OurWork/Safety/Pages/Polar-Code.aspx | grey | The operational risk-index framework that turns an ice chart into a permitted speed/entry decision; the regulatory hook for SAR-derived ice information. |
| kotovirta2009route | Kotovirta V.; Jalonen R.; Axell L.; Riska K.; Berglund R. | 2009 | A system for route optimization in ice-covered waters | Cold Regions Science and Technology | 10.1016/j.coldregions.2008.07.003 | yes | Classic ship-transit-in-ice routing system; establishes the ice-information-to-route-cost chain this paper's observability metric feeds. |
| lensu2019bigdata | Lensu M.; Goerlandt F. | 2019 | Big maritime data for the Baltic Sea with a focus on the winter navigation system | Marine Policy | 10.1016/j.marpol.2019.02.038 | yes | Frames ice-navigation decision support as a data-availability problem, matching the observability framing. |
| aksenov2017navigability | Aksenov Y.; Popova E. E.; Yool A.; Nurser A. J. G.; Williams T. D.; Bertino L.; Bergh J. | 2017 | On the future navigability of Arctic sea routes: High-resolution projections of the Arctic Ocean and sea ice | Marine Policy | 10.1016/j.marpol.2015.12.027 | yes | Projects where and when Arctic routes open, defining the geography over which SAR observability matters. |
| fu2016besetting | Fu S.; Zhang D.; Montewka J.; Yan X.; Zio E. | 2016 | Towards a probabilistic model for predicting ship besetting in ice in Arctic waters | Reliability Engineering & System Safety | 10.1016/j.ress.2016.06.010 | yes | Quantitative besetting-probability model; shows which ice-state variables a besetting forecast needs observed. |
| lehtola2019routes | Lehtola V.; Montewka J.; Goerlandt F.; Guinness R.; Lensu M. | 2019 | Finding safe and efficient shipping routes in ice-covered waters: A framework and a model | Cold Regions Science and Technology | 10.1016/j.coldregions.2019.102795 | yes | Route-safety model whose input is a gridded ice field — directly consumes the products a Sentinel-1 gap degrades. |

**target 5–6, verified 6** (plus 1 clearly marked grey-literature IMO circular with no DOI, as instructed). No seed discarded; the Kubat 2016 seed resolved to an OTC/Arctic Technology Conference paper rather than a journal article, and covers Canadian Arctic and sub-Arctic zones rather than Hudson Strait alone.

---

## Cluster 6 — Observing-system experiments, observing-network design, constellation revisit statistics

| bibkey | authors | year | title | venue | DOI/arXiv | verified? | one-line relevance |
|---|---|---|---|---|---|---|---|
| kaminski2015network | Kaminski T.; Kauker F.; Eicken H.; Karcher M. | 2015 | Exploring the utility of quantitative network design in evaluating Arctic sea ice thickness sampling strategies | The Cryosphere | 10.5194/tc-9-1721-2015 | yes | Quantitative network design applied to Arctic sea ice: the methodological precedent for scoring an observing network rather than a single sensor. |
| kaminski2018mission | Kaminski T.; Kauker F.; Toudal Pedersen L.; Voßbeck M.; et al. | 2018 | Arctic Mission Benefit Analysis: impact of sea ice thickness, freeboard, and snow depth products on sea ice forecast performance | The Cryosphere | 10.5194/tc-12-2569-2018 | yes | Mission-benefit analysis linking observation availability to forecast skill — the value-of-observation argument this paper makes for SAR. |
| langland2004impact | Langland R. H.; Baker N. L. | 2004 | Estimation of observation impact using the NRL atmospheric variational data assimilation adjoint system | Tellus A: Dynamic Meteorology and Oceanography | 10.3402/tellusa.v56i3.14413 | yes | The classical NWP adjoint observation-impact reference; the OSE/FSO lineage the sea-ice observability metric borrows from. |
| boukabara2016gaps | Boukabara S.-A.; Garrett K.; Kumar V. K. | 2016 | Potential Gaps in the Satellite Observing System Coverage: Assessment of Impact on NOAA's Numerical Weather Prediction Overall Skills | Monthly Weather Review | 10.1175/mwr-d-16-0013.1 | yes | An explicit OSE on a *satellite coverage gap* — the closest meteorological analogue to the Sentinel-1B loss experiment. |
| howell2022motion | Howell S. E. L.; Brady M.; Komarov A. S. | 2022 | Generating large-scale sea ice motion from Sentinel-1 and the RADARSAT Constellation Mission using the Environment and Climate Change Canada automated sea ice tracking system | The Cryosphere | 10.5194/tc-16-1125-2022 | yes | Multi-constellation SAR revisit in practice: quantifies how combining S1 and RCM changes pan-Arctic drift-retrieval coverage. |

**target 4–5, verified 5.** No dedicated "SAR constellation revisit statistics" journal paper of adequate venue quality was found via Crossref; the aerospace-engineering constellation-design hits (genetic-algorithm revisit optimisation, IJASS/IJAE) were judged off-topic and discarded rather than padded in. Howell *et al.* 2022 supplies the revisit-statistics role from the sea-ice side.

---

## Cluster 7 — Passive-microwave drift products and their coastal limits

| bibkey | authors | year | title | venue | DOI/arXiv | verified? | one-line relevance |
|---|---|---|---|---|---|---|---|
| lavergne2010drift | Lavergne T.; Eastwood S.; Teffah Z.; Schyberg H.; Breivik L.-A. | 2010 | Sea ice motion from low-resolution satellite sensors: An alternative method and its validation in the Arctic | Journal of Geophysical Research: Oceans | 10.1029/2009JC005958 | yes | The continuous maximum cross-correlation method behind the operational passive-microwave drift products, and its stated resolution floor. |
| lavergne2023osisaf | Lavergne T.; Down E. | 2023 | A climate data record of year-round global sea-ice drift from the EUMETSAT Ocean and Sea Ice Satellite Application Facility (OSI SAF) | Earth System Science Data | 10.5194/essd-15-5807-2023 | yes (pre-verified, reused) | The current PM drift CDR; its 62.5 km grid and coastal masking are the baseline SAR observability is measured against. |
| sumata2014inter | Sumata H.; Lavergne T.; Girard-Ardhuin F.; Kimura N.; Tschudi M. A.; Kauker F.; Karcher M.; Gerdes R. | 2014 | An intercomparison of Arctic ice drift products to deduce uncertainty estimates | Journal of Geophysical Research: Oceans | 10.1002/2013JC009724 | yes | Product-to-product spread of Arctic drift estimates, largest near coasts and in the marginal ice zone. |
| sumata2015uncertainty | Sumata H.; Kwok R.; Gerdes R.; Kauker F.; Karcher M. | 2015 | Uncertainty of Arctic summer ice drift assessed by high-resolution SAR data | Journal of Geophysical Research: Oceans | 10.1002/2015jc010810 | yes | Uses high-resolution SAR as the reference to bound low-resolution PM drift error — exactly the SAR-vs-PM comparison this paper extends. |

**target 3–4, verified 4.** No seed discarded.

---

## Cluster 8 — Observation gaps propagating into downstream products (incl. the Sentinel-1B loss)

| bibkey | authors | year | title | venue | DOI/arXiv | verified? | one-line relevance |
|---|---|---|---|---|---|---|---|
| wulf2024panarctic | Wulf T.; Buus-Hinkler J.; Singha S.; Shi H.; Kreiner M. B. | 2024 | Pan-Arctic sea ice concentration from SAR and passive microwave | The Cryosphere | 10.5194/tc-18-5277-2024 | yes | The pan-Arctic SIC seed: a SAR+PM product whose SAR component is limited by where Sentinel-1 actually acquires. |
| wulf2026decade | Wulf T.; Buus-Hinkler J.; Singha S.; Dasgupta N.; Athanasiadis A.; Kreiner M. B. | 2026 | A decade of sea ice concentration retrieved from Sentinel-1 | Remote Sensing of Environment | 10.1016/j.rse.2026.115252 | yes | The DMI-ASIP decade paper: a ten-year Sentinel-1 SIC record spanning the Sentinel-1B loss, i.e. the downstream product this study's gaps propagate into. |
| wuite2026velocity | Wuite J.; Nagler T.; Hetzenecker M.; Rott H. | 2026 | Ten years of polar ice velocity mapping using Copernicus Sentinel-1 | Remote Sensing of Environment | 10.1016/j.rse.2025.115092 | yes — **but see caveat** | Decade-long Sentinel-1 polar ice-velocity record built from repeat-pass SAR, spanning the Sentinel-1B failure; stands in for the requested InSAR acquisition-gap study. |

**target 3, verified 3 — with one caveat.** The first two seeds resolved exactly. The third seed, *"an InSAR study quantifying the impact of an acquisition gap"*, could **not** be located: Crossref title searches on `gap + InSAR`, `data gap + InSAR`, `acquisition gap + InSAR`, `Sentinel-1B` (40 title hits reviewed), and bibliographic searches on 6-day vs 12-day repeat, temporal decorrelation, and Sentinel-1B loss returned nothing that quantifies an acquisition-gap impact. `wuite2026velocity` is entered **as a deliberate substitution, not as the seed**: it is a repeat-pass-SAR downstream cryosphere product spanning the Sentinel-1B loss, so it is on-cluster, but it was not confirmed in-session to quantify a gap. If the paper is required to make a gap-quantification claim, drop this row and treat cluster 8 as **verified 2**.

---

## All verified DOIs

10.4043/27348-ms
10.1016/j.coldregions.2008.07.003
10.1016/j.marpol.2019.02.038
10.1016/j.marpol.2015.12.027
10.1016/j.ress.2016.06.010
10.1016/j.coldregions.2019.102795
10.5194/tc-9-1721-2015
10.5194/tc-12-2569-2018
10.3402/tellusa.v56i3.14413
10.1175/mwr-d-16-0013.1
10.5194/tc-16-1125-2022
10.1029/2009JC005958
10.5194/essd-15-5807-2023
10.1002/2013JC009724
10.1002/2015jc010810
10.5194/tc-18-5277-2024
10.1016/j.rse.2026.115252
10.1016/j.rse.2025.115092
