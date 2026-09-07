# Bibliography verification — clusters 1-4

Verification method: every entry below was retrieved in-session from the Crossref REST API
(`https://api.crossref.org/works/<doi>` and `.../works?query.bibliographic=`), with title, year,
container-title and author list read off the API response. Raw responses are cached under
`scratch/s2cache/<sha1-of-url>.json`.

Semantic Scholar was **not usable**: `$S2_API_KEY` is unset, and the unauthenticated
`graph/v1/paper/search` endpoint returned HTTP 429 on every attempt including after 2s/4s/8s
exponential backoff. No entry here depends on Semantic Scholar.

MDPI usage in these four clusters: **2** items (`korosov2017combination` — Remote Sensing, already
accepted as central; `zakhvatkina2019satellite` — Geosciences, a named seed and the standard SAR
sea-ice classification review). 3 MDPI slots remain for the rest of the paper.

---

## Cluster 1 — Sentinel-1 mission, EW mode, Arctic acquisition

| bibkey | authors | year | title | venue | DOI/arXiv | verified? | relevance to this paper |
|---|---|---|---|---|---|---|---|
| `torres2012gmes` | Torres, Snoeij, Geudtner, Bibby, Davidson, Attema, Potin, Rommen, Floury, Brown, Navas Traver, Deghaye, Duesmann, Rosich, Miranda, Bruno, L'Abbate, Croci, Pietropaolo, Huchler, Rostan | 2012 | GMES Sentinel-1 mission | Remote Sensing of Environment | 10.1016/j.rse.2011.05.028 | yes (Crossref) | Primary mission reference: defines the EW/IW modes, swath geometry and duty-cycle limits that set the Arctic observability ceiling we quantify. |
| `torres2017evolution` | Torres, Lokas, Di Cosimo, Geudtner, Bibby | 2017 | Sentinel 1 evolution: Sentinel-1C and -1D models | Proc. IGARSS 2017 | 10.1109/igarss.2017.8128261 | yes (Crossref) | The only peer-reviewed description we could verify of the Sentinel-1C/-1D units, used to justify assumptions about post-2024 constellation capability. |
| `potin2019copernicus` | Potin, Rosich, Miranda, Grimont, Shurmer, O'Connell, Krassenburg, Gratadour | 2019 | Copernicus Sentinel-1 Constellation Mission Operations Status | Proc. IGARSS 2019 | 10.1109/igarss.2019.8898949 | yes (Crossref) | Documents the operational observation scenario and conflict-resolution priorities that govern where EW acquisitions actually fall over the Arctic. |
| `geudtner2021copernicus` | Geudtner, Tossaint, Davidson, Torres | 2021 | Copernicus Sentinel-1 Next Generation Mission | Proc. IGARSS 2021 | 10.1109/igarss47720.2021.9554226 | yes (Crossref) | Frames the forward-looking part of the discussion: what C-band continuity and revisit will look like after the current constellation. |

target 3-4, verified 4.

**Discarded seed:** the *ESA Sentinel-1B end-of-mission announcement*. Crossref returns no citable
record for it under any phrasing tried ("Sentinel-1B end of mission", "Sentinel-1B mission
termination power anomaly ESA announcement 2022", "Sentinel-1B anomaly end of mission Sentinel-1
constellation gap"). A formal citable record does not appear to exist; it should be cited as a
dated ESA web notice / grey literature, or the constellation-gap statement should instead lean on
`potin2019copernicus` plus the observed acquisition record. **No DOI is guessed for it.**

---

## Cluster 2 — SAR-based sea-ice monitoring and ice-service operations

| bibkey | authors | year | title | venue | DOI/arXiv | verified? | relevance to this paper |
|---|---|---|---|---|---|---|---|
| `dierking2013sea` | Dierking | 2013 | Sea Ice Monitoring by Synthetic Aperture Radar | Oceanography | 10.5670/oceanog.2013.33 | yes (Crossref) | Canonical statement of what C-band SAR can and cannot resolve on sea ice; anchors our interpretation of backscatter-limited observability. |
| `zakhvatkina2019satellite` | Zakhvatkina, Smirnov, Bychkova | 2019 | Satellite SAR Data-based Sea Ice Classification: An Overview | Geosciences (MDPI) | 10.3390/geosciences9040152 | yes (Crossref) | Review of the SAR sea-ice classification literature that our observability metrics are meant to feed. |
| `karvonen2022baltic` | Karvonen | 2022 | Baltic Sea Ice Concentration Estimation From C-Band Dual-Polarized SAR Imagery by Image Segmentation | IEEE TGRS | 10.1109/tgrs.2021.3097885 | yes (Crossref) | Representative automated ice-charting chain built directly on operational C-band SAR; shows the downstream product our coverage statistics constrain. |
| `cheng2020accuracy` | Cheng, Casati, Tivy, Zagon, Lemieux, Tremblay | 2020 | Accuracy and inter-analyst agreement of visually estimated sea ice concentrations in Canadian Ice Service ice charts using single-polarization RADARSAT-2 | The Cryosphere | 10.5194/tc-14-1289-2020 | yes (Crossref) | Quantifies the human-analyst error floor in a national ice service, the baseline any SAR-derived automated product is judged against. |
| `eriksson2025finnish` | Eriksson, Vainio, Tollman, Jokiniemi, Arola, Mäkynen, Karvonen, Kangas | 2025 | The Finnish Ice Service, its sea-ice monitoring of the Baltic Sea and operational concept | Frontiers in Marine Science | 10.3389/fmars.2025.1561461 | yes (Crossref) | Recent first-hand account of a national ice service's dependence on Sentinel-1 timeliness and coverage — the operational stake in our observability question. |
| `lohse2020mapping` | Lohse, Doulgeris, Dierking | 2020 | Mapping sea-ice types from Sentinel-1 considering the surface-type dependent effect of incidence angle | Annals of Glaciology | 10.1017/aog.2020.45 | yes (Crossref) | Shows incidence-angle dependence across the EW swath, a geometry effect that couples directly to which parts of a scene are usable. |

target 5-6, verified 6.

---

## Cluster 3 — Sea-ice drift retrieval from SAR

| bibkey | authors | year | title | venue | DOI/arXiv | verified? | relevance to this paper |
|---|---|---|---|---|---|---|---|
| `komarov2014sea` | Komarov, Barber | 2014 | Sea Ice Motion Tracking From Sequential Dual-Polarization RADARSAT-2 Images | IEEE TGRS | 10.1109/tgrs.2012.2236845 | yes (Crossref) | Reference cross-correlation drift retrieval; establishes the image-pair quality and separation requirements we test against real Sentinel-1 sampling. |
| `muckenhuber2017open` | Muckenhuber, Sandven | 2017 | Open-source sea ice drift algorithm for Sentinel-1 SAR imagery using a combination of feature tracking and pattern matching | The Cryosphere | 10.5194/tc-11-1835-2017 | yes (Crossref) | The hybrid feature-tracking/pattern-matching approach applied to exactly the Sentinel-1 EW data stream we assess. |
| `korosov2017combination` | Korosov, Rampal | 2017 | A Combination of Feature Tracking and Pattern Matching with Optimal Parametrization for Sea Ice Drift Retrieval from SAR Data | Remote Sensing (MDPI) | 10.3390/rs9030258 | yes (Crossref; pre-verified, reused) | Parameterization study underlying the drift retrieval whose achievable coverage this paper bounds. |
| `howell2022generating` | Howell, Brady, Komarov | 2022 | Generating large-scale sea ice motion from Sentinel-1 and the RADARSAT Constellation Mission using the Environment and Climate Change Canada automated sea ice tracking system | The Cryosphere | 10.5194/tc-16-1125-2022 | yes (Crossref) | Demonstrates basin-scale operational drift from Sentinel-1 plus RCM — the production system whose input availability is our subject. |
| `lehtiranta2015comparing` | Lehtiranta, Siiriä, Karvonen | 2015 | Comparing C- and L-band SAR images for sea ice motion estimation | The Cryosphere | 10.5194/tc-9-357-2015 | yes (Crossref) | Frequency-dependence of drift retrieval success, relevant to how far C-band-only conclusions generalise. |
| `demchev2017sea` | Demchev, Volkov, Kazakov, Alcantarilla, Sandven, Khmeleva | 2017 | Sea Ice Drift Tracking From Sequential SAR Images Using Accelerated-KAZE Features | IEEE TGRS | 10.1109/tgrs.2017.2703084 | yes (Crossref) | Feature-detector-based alternative whose performance also degrades with increasing pair separation — the variable our revisit statistics control. |

target 5-6, verified 6.

---

## Cluster 4 — Sea-ice deformation and buoy-based statistics

| bibkey | authors | year | title | venue | DOI/arXiv | verified? | relevance to this paper |
|---|---|---|---|---|---|---|---|
| `marsan2004scale` | Marsan, Stern, Lindsay, Weiss | 2004 | Scale Dependence and Localization of the Deformation of Arctic Sea Ice | Physical Review Letters | 10.1103/physrevlett.93.178501 | yes (Crossref) | Establishes the spatial scaling law for deformation, which is why sampling scale (and hence SAR revisit) determines the measured deformation rate. |
| `hutchings2008small` | Hutchings, Hibler | 2008 | Small-scale sea ice deformation in the Beaufort Sea seasonal ice zone | JGR Oceans | 10.1029/2006jc003971 | yes (Crossref) | Buoy-array deformation statistics at the scales our SAR pairs would need to resolve. |
| `rampal2008scaling` | Rampal, Weiss, Marsan, Lindsay, Stern | 2008 | Scaling properties of sea ice deformation from buoy dispersion analysis | JGR Oceans | 10.1029/2007jc004143 | yes (Crossref) | Joint space-time scaling from buoy dispersion; supplies the temporal-scaling exponent used to interpret irregular revisit intervals. |
| `stern2009spatial` | Stern, Lindsay | 2009 | Spatial scaling of Arctic sea ice deformation | JGR Oceans | 10.1029/2009jc005380 | yes (Crossref) | RGPS-based spatial scaling companion to Marsan et al.; directly relates observation footprint to recovered deformation magnitude. |
| `hutchings2011spatial` | Hutchings, Roberts, Geiger, Richter-Menge | 2011 | Spatial and temporal characterization of sea-ice deformation | Annals of Glaciology | 10.3189/172756411795931769 | yes (Crossref) | Buoy-array design guidance for separating spatial from temporal deformation scaling; underpins our buoy-comparison design. (Note: a corrigendum exists, J. Glaciology, 10.1017/jog.2018.11.) |
| `oikkonen2017small` | Oikkonen, Haapala, Lensu, Karvonen, Itkin | 2017 | Small-scale sea ice deformation during N-ICE2015: From compact pack ice to marginal ice zone | JGR Oceans | 10.1002/2016jc012387 | yes (Crossref) | Sub-kilometre deformation from a dense buoy array, defining the regime that current SAR sampling under-resolves. |
| `itkin2025novel` | Itkin | 2025 | Novel methods to study sea ice deformation, linear kinematic features and coherent dynamic clusters from imaging remote sensing data | The Cryosphere | 10.5194/tc-19-1135-2025 | yes (Crossref) | Current state of the art for extracting deformation and LKFs from imaging remote sensing; the analysis our observability limits apply to. |
| `bouillon2015producing` | Bouillon, Rampal | 2015 | On producing sea ice deformation data sets from SAR-derived sea ice motion | The Cryosphere | 10.5194/tc-9-663-2015 | yes (Crossref) | The explicit bridge from SAR drift fields to deformation products, including how pair timing and triangulation propagate into deformation error. |

target 5-6, verified 8 (6 named seeds all verified, plus `stern2009spatial` and
`bouillon2015producing`, both of which carry load in the argument rather than padding it).

---

## Verified DOIs

10.1016/j.rse.2011.05.028
10.1109/igarss.2017.8128261
10.1109/igarss.2019.8898949
10.1109/igarss47720.2021.9554226
10.5670/oceanog.2013.33
10.3390/geosciences9040152
10.1109/tgrs.2021.3097885
10.5194/tc-14-1289-2020
10.3389/fmars.2025.1561461
10.1017/aog.2020.45
10.1109/tgrs.2012.2236845
10.5194/tc-11-1835-2017
10.3390/rs9030258
10.5194/tc-16-1125-2022
10.5194/tc-9-357-2015
10.1109/tgrs.2017.2703084
10.1103/physrevlett.93.178501
10.1029/2006jc003971
10.1029/2007jc004143
10.1029/2009jc005380
10.3189/172756411795931769
10.1002/2016jc012387
10.5194/tc-19-1135-2025
10.5194/tc-9-663-2015
