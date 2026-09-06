# Arctic Sea Routes × SAR × Safety — Wide-Lens Research-Topic Exploration (Claude Code Prompt v3, 2026-09)

Usage: save as `PROMPT.md` in a SEPARATE project folder (e.g. `.../Arctic/`), edit §0, then tell
Claude Code: "Read ./PROMPT.md and execute it end-to-end." Never run this in the AlphaEarth folder.

## 0. CONFIG (edit before running)

```yaml
GEE_PROJECT: "alpha-earth-app"      # Earth Engine project (Sentinel-1 GRD incl. EW mode is in GEE). Empty -> DESK_ONLY
EARTHDATA_LOGIN: false              # true if ~/.netrc holds NASA Earthdata credentials (asf_search downloads, NISAR)
REPORT_LANGUAGE: ko                 # Korean prose, English technical terms/titles. en cuts output tokens ~30%
AUTOPILOT: true                     # false -> pause once after the Stage 1 ranking
WORKDIR: ./arctic_explore
HARD_CONSTRAINTS:
  NO_KOMPSAT: true                  # KOMPSAT-5/6 are NOT available. Never build a topic on them.
  AIS_POLICY: validation_only       # AIS only as an optional validation source (free feeds: US MarineCadastre, Norway
                                    # BarentsWatch, Denmark/Greenland DMA, Global Fishing Watch research API). Every topic
                                    # must stand WITHOUT AIS; AIS-centric topics (dark vessels, SAR-AIS fusion) are KILLED.
  NO_METOCEAN: true                 # No marine-meteorological hazard research (SAR wind/wave retrieval, icing, polar lows)
                                    # and no numerical ocean/atmosphere/ice modelling. Reanalysis or forecast products may be
                                    # used ONLY as ancillary data layers, never as the research object.
  METHOD_POLICY: layer_integration  # Prefer transparent integration of SAR-derived layers with external data layers
                                    # (GIS overlay, indices, statistics). ML only where a SAR retrieval needs it.
  SCOPE: safety_and_transparency    # §5 ethics rule; no targeting, no naval/military asset identification or tracking
PRIORITY_ROUTES: [Northern Sea Route (Kara Gate, Vilkitsky, Sannikov/Dmitry Laptev, Long Strait, Chukchi approach),
                  Bering Strait corridor (Korea's gateway; IMO two-way routes), Northwest Passage (Canadian Arctic),
                  Transpolar Sea Route, Barents/Svalbard and Greenland approaches]
PRIORITY_PROBLEMS: [safe routing and decision support, route navigability and feasibility by ice class,
                    multi-layer route safety and reliability assessment, ice hazards (ridging, pressure, multiyear
                    inclusions, icebergs, freeze-up ice, rotten summer ice), L-band + C-band fusion (NISAR + Sentinel-1),
                    search-and-rescue enablement, oil-in-ice pollution, poorly charted waters and port/coastal
                    infrastructure stability, monitoring under the NSR data blackout]
TARGET: ">=6 GO topics after Stage 3; ultimate venues IEEE TGRS and RSE, plus The Cryosphere / Cold Regions Science
         and Technology / Ocean Engineering / Safety Science for ice-operations and risk science; MDPI excluded"
BUDGETS:
  stage1_landscape_queries: 10
  stage1_queries_per_subagent: 4
  stage1_pass_target: [12, 16]       # wider net than usual
  stage2_queries_per_topic: 6
  stage2_gee_checks_per_topic: 3
  stage2_pilot_runs_per_topic: 2     # each <=10 min, <=6 SAR scenes or <=10k samples, <=80-line script
  stage3_queries_per_topic: 4
  max_parallel_gee_pilots: 4
  stage2_wallclock_cap_hours: 2.5
```

## 1. MISSION

You are a polar remote-sensing research strategist and hands-on SAR/GIS engineer. Explore WIDELY, then
narrow: discover, screen, and validate research topics on the safety, reliability and feasibility of
Arctic sea routes built on spaceborne SAR (Sentinel-1 C-band as the workhorse; NISAR L-band as the
new opportunity) combined with EXTERNAL DATA LAYERS (ice charts, bathymetry and chart-adequacy layers,
port and SAR-asset locations, iceberg charts, traffic statistics, incident records, permafrost and
coastal data, Polar Code rules). Topics must (a) address a real safety problem — safe routing, route
feasibility and reliability, ice hazards, search and rescue, pollution, charting, infrastructure
stability — (b) be verifiable against independent reference data, and (c) be publishable in IEEE
TGRS / RSE / The Cryosphere / Cold Regions Science and Technology / Ocean Engineering / Safety Science
and peers (§10). No marine-meteorological hazard research and no numerical modelling
(HARD_CONSTRAINTS). Three stages, each stricter; deliver >=6 GO topics with proposals and target
journals. The saturated spaces (§4.3) are entry points only; every candidate must state what it adds.

## 2. OPERATING RULES (speed and token discipline)

1. No engineering ceremony: no git, tests, linters, type hints, docstrings, READMEs, CI, checksum/SHA
   verification, license audits (one line max), dependency pinning, retries beyond one, refactors.
   Pilot scripts: single file, <=80 lines, throwaway, in `scratch/`.
2. Print little: never dump >30 lines of any file or API response; use `jq`, `head`, field selects.
   No plots before Stage 3. Save results to files; chat summaries <=15 lines per stage. Never re-read
   files you wrote; never restate these instructions or narrate intentions.
3. Literature via compact APIs (`curl`+`jq`): OpenAlex
   `https://api.openalex.org/works?search=<q>&per-page=5&filter=from_publication_date:2023-01-01&select=title,publication_year,doi,primary_location,cited_by_count`;
   Semantic Scholar `https://api.semanticscholar.org/graph/v1/paper/search?query=<q>&limit=5&fields=title,year,venue,externalIds,citationCount`;
   arXiv API. WebSearch/WebFetch only for gray literature (ESA/NASA/ASF notices, ice services, CHNL
   statistics, Bellona / High North News, IMO circulars, hydrographic offices) or when APIs fail.
4. Fan out with subagents (Task/Agent tool); each reads only the PROMPT.md sections it needs (§2-§3,
   §7, its stage in §8, its bucket in §5-§6; use line ranges), writes its own file, returns <=10 lines.
   Main agent merges, scores, decides. Never paste the whole prompt into a subagent prompt.
   Subagent-to-main communication is English.
5. No questions unless truly blocked. GEE init failure -> DESK_ONLY. EARTHDATA_LOGIN=false -> NISAR /
   ASF topics run catalog-only (asf_search metadata needs no login), mark `PILOT=CATALOG`.
6. Wall clock: beyond `stage2_wallclock_cap_hours`, finish pilots in Stage-1-score order and mark the
   rest `PILOT=PENDING`.

## 3. SCIENTIFIC RIGOR (non-negotiable)

1. Never fabricate references; verify via API/DOI/arXiv id in-session -> [V], else [U] (never argue
   from [U]).
2. Novelty = a specific unanswered question with a testable answer. "Sentinel-1 not yet applied to
   strait X" or "an index nobody has computed" is not novelty by itself; the index must be validated
   against realised outcomes or independent data. A prior paper kills a topic only if it answers the
   same RQ with comparable data and convincing validation.
3. Separate convenience from scientific value: only better accuracy or lead time, a new hazard,
   navigability or reliability measurand, a validated safety linkage, or new insight about
   sensors/products justifies TGRS/RSE/Cryosphere.
4. Pilots: spatial AND temporal blocking (hold out whole regions and seasons; never random
   pixel/scene splits); one mandatory baseline (operational ice chart, passive-microwave product,
   classical threshold/texture method, or for indices: an equal-weight / chart-only index); report
   n, class balance, metric, fold spread; name confounders (incidence angle, wind roughening of open
   water, wet snow in melt season, EW noise-floor scalloping, chart-vs-scene time offset,
   frequency-dependent penetration, layer resolution mismatch).
5. Reference independence: ice charts are SAR-interpreted -> validating only against charts is
   circular; require at least one non-SAR or in-situ reference (buoys, ship observations, ALS/EM
   thickness, altimetry, optical, incident records, gauges, soundings). For routing, feasibility and
   reliability claims, "realised" evidence counts: detected convoy channels, CHNL transit counts,
   besetting and grounding records, port operating logs.
6. Multi-layer indices: state every layer's source, resolution, date and independence; test
   sensitivity to weights (equal vs expert vs data-driven) and to layer omission; never report a
   composite without its sensitivity range. Expert-weighted indices without outcome validation are
   killed as unfalsifiable.
7. Real-world verifiability: every survivor names (i) the safety problem, (ii) the operator or
   decision it informs (ice service, ship master/routing service, port authority, SAR coordination
   centre, hydrographic office, insurer, IMO/Polar Code), (iii) the independent data that could prove
   it wrong.
8. Kills with reasons are a deliverable; never soften kills to reach the quota (Stage 1.5 exists).
9. Reviewer-2 prediction for every survivor.
10. Ethics (§5 scope rule): safety and transparency only; aggregate traffic and hazards, never
    individual naval or military vessels or facilities, no sanction attribution to individual ships,
    no targeting or evasion assistance. One ethics/provenance line per card in buckets G and J.

## 4. BACKGROUND FACTS (pre-verified 2026-09; extend, do not re-research)

### 4.1 Sensors and access
- Sentinel-1: 1B failed Dec 2021 (mission ended Aug 2022) -> single-satellite gap 2022-2024; 1C
  launched Dec 2024, 1D launched 4 Nov 2025, 1D replaces 1A after overlap. Two-satellite
  constellation restored: Arctic revisit <1 day. 1C/1D carry an AIS payload (irrelevant under
  AIS_POLICY except as optional validation). Data free via Copernicus Data Space and ASF
  (`asf_search`). EW mode (HH/HV, ~40 m GRDM) is the polar workhorse; IW over coasts and ports. GEE
  `COPERNICUS/S1_GRD` holds EW and IW GRD with metadata (mode, polarisation, orbit) usable for
  coverage audits without imagery.
- NISAR (NASA-ISRO, launched Jul 2025): calibrated L-band PROVISIONAL products publicly released
  20 Jul 2026 (acquisitions from 17 Jun 2026; first-year backlog to follow; full record expected by
  end 2026) via ASF/Earthdata. L-band, 12-day repeat, wide swath, dual-pol (quad-pol over selected
  areas). Verify the sea-ice acquisition plan and actual Arctic coverage. First public data are
  MELT-SEASON data (Jun-Sep 2026) — the season ships sail and C-band discrimination is weakest;
  freeze-up 2026-27 data will follow.
- NOT available: KOMPSAT-5/6 (HARD_CONSTRAINT). Restricted/commercial, future-work only: RCM,
  ALOS-2/4, SAOCOM (verify open-access windows), TerraSAR-X, ICEYE, Capella, Umbra (small open set).
- Complementary observation layers: AMSR2 sea-ice concentration (JAXA/Bremen), OSI SAF ice
  type/edge/drift, CryoSat-2 / SMOS thickness, ICESat-2 ATL07/ATL10 (freeboard, leads, ridges) and
  ATL03 photon bathymetry in clear shallow water, Sentinel-3 SLSTR (thin ice), MODIS/VIIRS,
  Sentinel-2/Landsat (summer optical, melt ponds, shorelines). Reanalysis (ERA5) only as an ancillary
  layer for stratification, never as a research object (NO_METOCEAN).

### 4.2 External data layers and validation data (verify access once each)
- Ice information: US NIC, Canadian Ice Service (SIGRID-3), AARI (Russia; verify continuity),
  Norwegian Met (Svalbard), DMI (Greenland; iceberg charts); AI4Arctic/ASIP v2 (S1 + AMSR2 + charts;
  Greenland waters only); OSI SAF and NSIDC climatologies.
- Charting and seabed: GEBCO bathymetry; ENC/chart adequacy and survey-coverage layers (CHS, NOAA,
  Norwegian Hydrographic Service; IHO C-55 survey status); IHO crowd-sourced bathymetry (CSB);
  ICESat-2 ATL03 shallow-water bathymetry points.
- Infrastructure and response assets: ports, places of refuge, icebreaker bases, SAR stations and
  helicopter ranges (Arctic Council EPPR/SAR Agreement documents, national SAR plans), airstrips;
  Arctic Coastal Dynamics erosion database; permafrost maps (ESA CCI Permafrost); tide/river gauges.
- Rules and thresholds: IMO Polar Code and POLARIS (MSC.1/Circ.1519: Risk Index Outcome by Polar
  Class), Canadian AIRSS ice numerals, IMO two-way routes and precautionary areas in the Bering
  Strait (2018; verify).
- Traffic and incidents WITHOUT AIS: CHNL (Nord University) annual NSR transit statistics; Bellona
  report (Dec 2025): 100 sanctioned vessels on the NSR in the past year vs 13 in 2024, 38 sanctioned
  tankers many without ice class; Russia's NSR administration stopped publishing traffic data ->
  information vacuum. Incident records: besetting news (tanker Lynx beset awaiting icebreaker, Dec
  2025), Rosatom convoy announcements, Hudson Strait besetting inventory (33 transits 2005-2014),
  Canadian Arctic groundings attributed to poor charting (Clipper Adventurer 2010, Akademik Ioffe
  2018), IMO GISIS casualty module, Allianz Safety & Shipping Review, TSB Canada reports.
- In situ / independent: IABP drifting buoys, MOSAiC 2019-20 (ridges, thickness, buoys, melt ponds),
  ASSIST/ASPeCt ship-based observations (Icewatch), KOPRI Araon Chukchi Sea cruises (verify access;
  Korea-specific), AWI airborne EM thickness, CryoSat-2/ICESat-2 freeboard.
- Optical validation of SAR detections: Sentinel-2 10 m (ships >~50 m, convoy channels, icebergs,
  melt ponds) in summer; VHR via Google Earth for ports and coasts.

### 4.3 Known work (verified 2026-09) -> taken unless the stated gap is addressed
- Sea-ice TYPE segmentation with deep learning / foundation models: SATURATED (IceFMBench
  arXiv:2503.22516 v2 Feb 2026; SAR-IceFM SSRN 2026; pan-Arctic winter dual-pol classification, Dai
  et al., RSE 2026; few-shot ESICM EGU 2026; weakly supervised SOD from charts; AutoICE lineage).
  Gap: hazard-, navigability- and reliability-specific measurands tied to safety outcomes;
  melt-season and freeze-up discrimination; L+C.
- SAR+AIS dark-vessel detection and ship-iceberg discrimination: many papers. KILLED by AIS_POLICY
  unless AIS-free.
- Ice routing optimisation (A*/Dijkstra with POLARIS or ice numerals on passive-microwave or model
  ice fields; Baltic and Arctic case studies): established. Gap: SAR-resolution hazard inputs,
  validation against REALISED routes (detected channels) and incidents, reliability of routes across
  years, lead-time value of sub-daily SAR.
- Multi-criteria Arctic route risk assessments (AHP/fuzzy/expert-weighted indices; Bayesian
  besetting model for NSR convoys, RESS 2022; Hudson Strait pressured-ice besetting inventory 2016;
  Antarctic navigation risk framework, MDPI JMSE 2025): many, mostly expert-weighted and rarely
  validated against outcomes. Gap: SAR-derived hazard layers at 40 m, outcome validation (incidents,
  realised transits), reliability/stability metrics across seasons and years, sensitivity analysis.
- Navigability windows from passive microwave / CMIP6 (many; Korean NRF preprint May 2026 on NSR
  windows with ecological overlap). Gap: chokepoint-scale observational navigability at SAR
  resolution, ice-class-specific windows, interannual reliability, reconciliation with realised
  transits.
- SAR sea-ice deformation methods (Itkin, The Cryosphere 2025; MOSAiC studies), landfast-ice InSAR
  deformation, S1(+MISR) roughness for community ice trails (Annals of Glaciology 2020). Gap:
  convergence/pressure nowcasts linked to besetting; port-scale landfast timing and stability.
- SAR-derived bathymetry from wave kinematics and chart-adequacy studies: methods exist mostly outside
  the Arctic routes context. Gap: poorly charted approaches where ice forces deviations from surveyed
  tracks.

### 4.4 Input-stream events (hypotheses; verify)
S1B gap 2022-2024 reduced polar coverage regionally (quantify from S1_GRD metadata); 1C/1D
restoration; NISAR first data mid-2026 (melt season first); possible reduction of ESA acquisitions
over Russian Arctic waters after 2022 (verify with scene counts); AARI chart availability changes.

## 5. EXPLORATION ANGLES (10 buckets; every bucket yields candidates; >=40 total)

Scope rule for all buckets: safety and transparency only. Out of scope, never propose: targeting or
weapon-employment support, identification or tracking of naval/military vessels or facilities,
individual-vessel sanction attribution, aiding evasion of monitoring, marine-meteorological hazard
retrieval or any numerical modelling (NO_METOCEAN). Aggregate statistics, public data, named civilian
operator or beneficiary.

A. Safe routing and decision support: SAR-resolution hazard fields -> POLARIS/ice-numeral risk
   surfaces; risk-aware and uncertainty-aware path planning (algorithmic, no physical model); dynamic
   rerouting and the lead-time value of sub-daily SAR; escort/convoy planning and channel reuse;
   corridor design (Bering two-way routes) and places of refuge; community on-ice travel safety.
B. Navigability and route feasibility: chokepoint-scale navigable windows by Polar Class from the
   2014-2026 Sentinel-1 archive vs passive microwave; opening/closing date variability and trends;
   NSR vs NWP vs Transpolar comparison; obstacles (multiyear inclusions, landfast ice, icebergs);
   feasibility for non-ice-class ships (Busan-Europe scenario); effective navigability including
   chart adequacy, refuge/SAR access and iceberg exposure from external layers; reconciliation of
   observed windows with realised transits (CHNL) and with published projection claims.
C. Ice hazards as measurands: ridging/deformation intensity, convergence/pressure nowcasts from
   drift pairs, multiyear inclusions, lead/polynya persistence, landfast onset/breakup and stability
   at ports and coastal routes, iceberg detection and drift near routes, thin/young ice at freeze-up,
   rotten ice and melt-pond fraction in summer.
D. L-band + C-band fusion and multi-frequency/multi-sensor synergy (NISAR + Sentinel-1 first):
   melt-season ice/water and ice-type discrimination where C-band fails (wet snow); deformed/MYI vs
   level FYI separability (volume scattering, roughness sensitivity); icebergs inside sea ice
   (glacial-ice L-band brightness); drift tracking in melt season with L-band feature stability;
   thin ice vs wind-roughened water at freeze-up; snow-on-ice decoupling; L-band InSAR coherence for
   landfast ice, grounded ridges (stamukhi) and permafrost coasts; polarimetric and cross-frequency
   features; coincidence/coverage catalog of L+C pairs; sensor-agnostic hazard retrieval; also
   SAR+ICESat-2/CryoSat-2 (ridges, thickness), SAR+SLSTR (thin ice), SAR+Sentinel-2 (melt ponds),
   SAR+passive microwave (fidelity).
E. Sensor and coverage science: S1B-gap natural experiment on Arctic monitoring (coverage, chart
   revision frequency, drift-product gaps, hazard-detection latency); 1C/1D restoration; NISAR
   first-season assessment; EW noise floor and incidence-angle effects on hazard retrieval; coverage
   audit of Russian Arctic waters 2019-2026; latency from acquisition to usable hazard product;
   product stability (do hazard layers agree year to year where nothing changed?).
F. Multi-layer safety and reliability assessment (GIS integration, no physical model): composite
   route-segment safety indices from SAR hazard-frequency layers (2016-2026) + external layers (chart
   adequacy / survey coverage, distance to refuge, icebreaker and SAR assets, iceberg exposure,
   landfast timing, traffic exposure proxies, permafrost and coastal stability at ports); route
   RELIABILITY defined as interannual stability of navigable windows and hazard exposure
   (coefficient of variation, worst-year analysis, persistence); layer-intersection analyses (ice
   forcing ships off surveyed tracks into unsurveyed water; hazard ice near poorly served SAR zones);
   weight-sensitivity and layer-omission analysis; validation against incident catalogs and realised
   transits; data-driven weights (logistic/Bayesian on incidents) vs expert weights; port and
   approach reliability indices for NSR ports.
G. Traffic and activity WITHOUT AIS (safety framing): icebreaker/convoy channel detection as a
   traffic proxy during the data blackout; SAR ship detection validated by Sentinel-2 optical; port
   and anchorage activity proxies; exposure of corridors to hazard ice (aggregate only).
H. Environmental safety: oil-in-ice and oil-among-ice detection, look-alike catalogs (grease ice,
   wind shadow, low-wind slicks), discharge monitoring along corridors; validation via documented
   incidents and experiments.
I. Charting, infrastructure and coastal stability: SAR-derived bathymetry for poorly charted
   approaches (wave kinematics as a retrieval, not met-ocean research; validated with ICESat-2 photon
   bathymetry, CSB, ENC soundings); shoal and uncharted-hazard flags; permafrost thaw subsidence and
   coastal retreat at ports, airstrips and SAR stations (Sabetta, Dikson, Tiksi, Pevek, Anadyr, Nome)
   with S1 InSAR and shorelines; landfast ice as coastal protection; river-ice breakup for river-sea
   logistics (Ob, Yenisei, Lena). Bridge to the AlphaEarth track where annual land embeddings help.
J. Safety outcomes and risk integration: besetting/grounding incident catalog vs SAR hazard fields;
   POLARIS from SAR ice types vs from charts; SAR-and-rescue response-gap mapping (hazard x exposure
   x asset distance); Polar Code and insurance relevance; uncertainty communication to ice services.

Diversity constraint for the final GO set: >=4 buckets and >=2 routes.

## 6. SEEDS (screen like any other candidate; tiers = pre-screen against §4.3)

Tier 1 (timely; no journal treatment found):
- S1 SAR-resolution POLARIS and risk-aware routing: do 40 m hazard fields change optimal routes and
  risk vs chart-based routing? Validate against realised convoy channels detected in SAR (AIS-free)
  and besetting records; quantify lead-time value of sub-daily S1 (buckets A, G, J).
- S2 Chokepoint navigability climatology by Polar Class from Sentinel-1 2014-2026 (Vilkitsky,
  Sannikov, Long Strait, Bering) vs AMSR2/OSI SAF; how many navigable days coarse products over- or
  under-state; ice-class-specific windows; interannual reliability; Busan-Europe non-ice-class
  scenario (buckets B, F).
- S3 Convergence/pressure nowcast for besetting risk from S1 EW drift pairs; validate deformation
  with IABP/MOSAiC; link to an incident catalog (news, Rosatom, CHNL, Hudson Strait) (buckets C, J).
- S4 NISAR L-band first season: coincident L+C pairs over Arctic ice (Jun-Sep 2026); melt-season
  ice/water and deformed/MYI separability with L vs C vs L+C; plan freeze-up 2026-27; CATALOG-only
  without Earthdata login (bucket D).
- S5 Multi-layer route safety and reliability index: per-segment composite of SAR hazard frequency
  (2016-2026) + chart adequacy + distance to refuge/icebreaker/SAR assets + iceberg exposure +
  landfast timing + traffic exposure proxy; reliability = interannual variability of the index and of
  navigable windows; equal vs expert vs incident-fitted weights; layer-omission sensitivity;
  validation against grounding/besetting records and CHNL transits (buckets F, J).
- S6 S1B-gap natural experiment for Arctic monitoring (mirror of the AlphaEarth TB02 design):
  per-region scene counts 2019-2026; effect on drift-product gaps, chart revision frequency, hazard
  latency; recovery after 1C/1D (bucket E).
Tier 2 (open; reference-dependent):
- S7 Chart adequacy x ice forcing: where do ice conditions (SAR hazard layers) push ships off
  surveyed tracks into unsurveyed or poorly surveyed water? Layer intersection with survey-coverage
  polygons and detected channels; validate with grounding records (Canadian Arctic, Chukchi) (F, I).
- S8 Landfast ice onset/breakup timing and stability at NSR ports 2015-2026 from S1
  backscatter/coherence; port operating-window reliability; validate with charts + optical + port
  records (buckets C, F).
- S9 Icebreaker/convoy channel detection in S1 as an AIS-free traffic proxy during the data blackout;
  channel persistence vs ice regime; validate with Sentinel-2 and announced convoys (bucket G).
- S10 Iceberg detection and drift near Barents-Kara routes with S1 (+ L-band brightness where NISAR
  exists); iceberg-vs-ship confusion handled WITHOUT AIS (optical, persistence, ice context) (C, D).
- S11 Melt-pond fraction and rotten-ice hazard in summer from S1 (+ Sentinel-2, + L-band); relevance
  to late-season navigability (buckets C, D).
- S12 SAR-derived bathymetry and uncharted-shoal flags for poorly charted approaches (Canadian
  Arctic, Chukchi); validate with ICESat-2 ATL03 bathymetry, CSB and ENC soundings (bucket I).
- S13 Port and airstrip permafrost subsidence + coastal retreat (Sabetta, Tiksi, Pevek, Nome) with S1
  InSAR and shoreline change; AlphaEarth embeddings as land-change prior; port stability index
  combining subsidence, erosion and landfast timing; validate with Arctic Coastal Dynamics rates and
  optical (buckets I, F).
- S14 SAR-and-rescue response-gap mapping: hazard-frequency layers x traffic exposure (CHNL, channel
  proxies) x asset reach (icebreaker bases, SAR stations, helicopter ranges); worst-season analysis;
  validate reach assumptions against documented rescue operations (buckets J, F).
Tier 3 (conditional):
- S15 Oil-in-ice detection and look-alike catalog for corridors; keep only if >=10 verifiable events
  exist (bucket H).
- S16 Multiyear-ice inclusion mapping for the Transpolar route with S1 + ICESat-2 + CryoSat-2; keep
  only if it adds hazard/thickness linkage beyond type segmentation (buckets B, C).
- S17 Uncertainty-aware routing: propagating SAR retrieval uncertainty (incidence angle, season) into
  route-risk bounds; keep only if S1 or S2 passes (bucket A).

Korea-specific advantages (no KOMPSAT): Bering/Chukchi as primary test region (Korea's gateway; US
free AIS for validation only; KOPRI Araon observations if accessible); Busan-Europe NSR scenario for
non-ice-class container ships; ROK stakeholders (KOPRI, Ministry of Oceans and Fisheries, Coast
Guard, shipbuilders' route-design interest).

## 7. SCORING AND KILL RULES

Score 0-3: N novelty | R real-world safety relevance (named operator) | F feasibility (data access,
Sentinel-1 in GEE + downloadable layers + laptop, <=3 months) | A SAR/layer-integration scientific
advantage (convenience only -> <=1) | V verifiability (independent, non-chart or in-situ or
realised-outcome reference; falsifiable) | J journal fit.
Total max 18. Hard kills: F=0 or V=0; A<=1 and N<=1; RQ answered convincingly (§4.3); violates
HARD_CONSTRAINTS (KOMPSAT-dependent, AIS-centric, met-ocean or numerical modelling, out-of-scope
ethics); composite index without outcome validation and sensitivity analysis. IDs `T<bucket><nn>`;
keep seed labels in titles.

## 8. STAGES

### Stage 1 — Landscape + wide shallow screen (no code)
Step 0 (main agent, <= `stage1_landscape_queries`): search "Sentinel-1 sea ice navigation safety",
"Northern Sea Route SAR", "Arctic ice routing POLARIS", "Arctic navigability Sentinel-1 chokepoint",
"Arctic shipping risk index multi-criteria validation", "NISAR sea ice", "L-band C-band sea ice
fusion", "landfast ice breakup SAR port", "Arctic shipping besetting grounding", "SAR bathymetry
Arctic chart adequacy" (2023-2026). Write `00_landscape.md` (<=70 lines): verified works [V] beyond
§4.3, gist, bucket, gap list.
Step 1 (10 subagents, buckets A-J): each reads `00_landscape.md` and §4-§7, produces 4-6 candidate
cards, <= `stage1_queries_per_subagent` lookups total, no code, memory citations tagged [U]. Writes
`stage1/bucket_<X>.md`; returns <=10 lines.
Card row:
`ID | Title (<=12 words) | Route/Region | RQ (1 sentence) | Why SAR / which layers (1 sentence) | Reference data (named; independence noted) | Closest prior work (title, year, [V]/[U]) | N R F A V J Total | PASS/KILL + reason (<=15 words)`
Main agent -> `01_stage1_screen.md` (sorted; kill list at bottom); pass `stage1_pass_target` topics
with >=5 buckets represented. If AUTOPILOT=false, pause.

### Stage 2 — Feasibility and smoke tests (one subagent per pass)
Per topic: <= `stage2_queries_per_topic` lookups, <= `stage2_gee_checks_per_topic` data checks,
<= `stage2_pilot_runs_per_topic` pilot runs (<=80-line script, <=10 min, <=6 SAR scenes or <=10k
samples). Templates:
- P1 Drift/deformation: two S1 EW scenes 1-3 days apart -> pattern-matching drift (open-source
  `sea_ice_drift`, or GEE displacement proxies) -> divergence; compare with IABP buoy pairs.
- P2 Time series: S1 backscatter (coherence where SLC access exists) over a port/strait polygon
  2016-2026 -> onset/breakup dates, open-water fraction; vs charts, AMSR2 and optical.
- P3 Coverage audit: S1_GRD scene counts per region-year-mode from GEE metadata (no imagery).
- P4 Navigability day-count and reliability: per-scene open-water/ice fraction at a chokepoint for
  3+ seasons vs AMSR2/OSI SAF; navigable days by threshold and Polar Class rule; interannual CV.
- P5 Linear-feature detection: convoy channels / leads in S1 over dated events; precision/recall via
  Sentinel-2 inspection.
- P6 NISAR catalog and coincidence: `asf_search` for NISAR and S1 frames since 2026-06-17 over an
  ROI; count L+C pairs within 6 h; one pair analysed if downloads possible.
- P7 Multi-layer index pilot: for one route sector (e.g. Bering-Chukchi or eastern NSR), build a
  segment table (20-50 km segments) with SAR hazard frequency from P4/P2 + downloaded layers (GEBCO
  depth and survey-coverage polygons, port/refuge/SAR asset points with distances, iceberg chart
  polygons, CHNL segment counts); compute equal-weight and rank-based indices; perturb weights (100
  draws) and drop layers one at a time; check association with incident locations (rank correlation
  or logistic fit with leave-one-segment-out).
- P8 Bathymetry feasibility: one S1 IW subset (GEE getDownloadURL <32 MB or ASF) -> FFT wavelength
  map -> depth from linear dispersion; vs ENC soundings or ICESat-2 ATL03 points (retrieval only).
- P9 Routing sensitivity: A* on a POLARIS surface built from (a) chart ice types and (b) S1-derived
  ice types for one chokepoint/day; compare route length and risk; compare with a detected channel.
- P10 Coastal/InSAR: S1 IW amplitude change (+ optional coherence) at a port; shoreline change from
  S2; combine with landfast timing into a port stability table.
DESK_ONLY: skip pilots, `PILOT=PENDING`, conservative F. Revise scores; PASS/KILL; top-3 risks;
Reviewer-2; ethics line for G/J. Write `stage2/<ID>.md` (<=40 lines); main agent ->
`02_stage2_feasibility.md`. Target 6-9 passes; Stage 1.5 if <6.

### Stage 3 — Go/No-Go proposals (one subagent per pass)
`stage3/<ID>.md` (<=60 lines): title; one-sentence contribution; 2-3 RQs with falsifiable
hypotheses; safety problem, operator and use; data (sensors, layers with source/resolution/date,
references with independence argument, sampling); method with mandatory baselines, ablations and
weight/layer sensitivity where indices are involved; evaluation protocol (spatial + temporal
blocking; realised-outcome or incident-linked metrics where relevant); expected figures; pilot
evidence and effect size; threats and mitigations (incidence angle, melt season, chart circularity,
sparse incidents, layer resolution mismatch, frequency-dependent penetration); compute plan and
12-week timeline; journals primary/secondary/stretch with fit and the preempted Reviewer-2
objection; verdict GO / CONDITIONAL-GO / NO-GO.
Main agent -> `03_stage3_proposals.md`, `04_final_ranking.md` (ranked GO list >=6, diversity check,
first project, two pivots per topic, kill log, and a "programme map" grouping GO topics into 2-4
coherent paper clusters, e.g. routing+navigability+reliability index, L+C fusion, hazards+incidents,
charting+infrastructure stability). If <6 GO, promote CONDITIONAL-GO with conditions stated; report
the shortfall.

## 9. OUTPUT FILES (under WORKDIR)
`PROMPT.md` | `00_landscape.md` | `stage1/bucket_*.md` | `01_stage1_screen.md` | `stage2/<ID>.md` |
`02_stage2_feasibility.md` | `stage3/<ID>.md` | `03_stage3_proposals.md` | `04_final_ranking.md` |
`scratch/` (pilot scripts, small layer extracts, segment tables). User-facing files follow
REPORT_LANGUAGE; sensor/dataset/method names and titles stay English. Plain markdown tables; no emoji.

## 10. JOURNAL GUIDE (SCIE; MDPI excluded)
- SAR retrieval / fusion / detection methods (L+C, deformation, bathymetry) -> IEEE TGRS; smaller ->
  IEEE JSTARS, IEEE GRSL.
- Validated geophysical measurement or product assessment -> Remote Sensing of Environment; ice
  science -> The Cryosphere, Journal/Annals of Glaciology, JGR Oceans.
- Ice operations, hazards, navigability, reliability -> Cold Regions Science and Technology; ship-ice,
  routing, route risk -> Ocean Engineering, Applied Ocean Research, Journal of Marine Science and
  Technology; routing algorithms -> IEEE Transactions on Intelligent Transportation Systems,
  Transportation Research Part E/D.
- Multi-layer risk and reliability indices -> Reliability Engineering & System Safety, Safety
  Science, Risk Analysis, International Journal of Disaster Risk Reduction, Ocean & Coastal
  Management; GIS methods -> International Journal of Geographical Information Science, Transactions
  in GIS, Applied Geography. Navigation -> Journal of Navigation.
- Feasibility framing -> Climatic Change, Environmental Research Letters; stretch Nature Climate
  Change / Nature Communications.
- Pollution -> Marine Pollution Bulletin. Governance, data blackout, policy -> Marine Policy (SSCI),
  Polar Geography (check indexing).
- Charting/infrastructure/permafrost -> RSE, TGRS (InSAR), Permafrost and Periglacial Processes,
  Marine Geodesy.
- Excluded: Remote Sensing, JMSE, Sustainability and all other MDPI titles. Do not look up impact
  factors; verify SCIE indexing only if unsure (1 query).

## 11. SETUP AND SNIPPETS (adapt; <=80 lines per script)
Setup (<=5 min): `pip show earthengine-api asf_search scikit-learn pandas geopandas rasterio numpy`
(install only missing); `ee.Initialize(project=GEE_PROJECT)`; check `~/.netrc` for Earthdata; proceed.
```python
import ee; ee.Initialize(project=GEE_PROJECT)
S1 = ee.ImageCollection("COPERNICUS/S1_GRD")
roi = ee.Geometry.Rectangle([lon0, lat0, lon1, lat1])           # e.g. Vilkitsky Strait
ew = (S1.filterBounds(roi).filter(ee.Filter.eq("instrumentMode", "EW"))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "HH")))
# P3 coverage audit (metadata only)
counts = {y: ew.filterDate(f"{y}-01-01", f"{y+1}-01-01").size().getInfo() for y in range(2016, 2027)}
# P2/P4 per-scene open-water fraction with a simple HH threshold (baseline; refine per incidence angle)
def ow_frac(img):
    ow = img.select("HH").lt(-18)                                 # crude open-water threshold, dB
    return ee.Feature(None, {"t": img.date().format(), "ow": ow.reduceRegion(ee.Reducer.mean(), roi, 200).get("HH")})
ts = ew.filterDate("2023-06-01", "2023-11-30").map(ow_frac).getInfo()["features"]   # keep <= ~1k
```
```python
import asf_search as asf   # P6: catalog queries need no login
nisar = asf.search(platform=[asf.PLATFORM.NISAR], start="2026-06-17", intersectsWith=WKT_ROI, maxResults=500)
s1 = asf.search(platform=[asf.PLATFORM.SENTINEL1], start="2026-06-17", intersectsWith=WKT_ROI, maxResults=2000)
# pair NISAR and S1 acquisitions within 6 h for L+C coincidence counting
```
```python
# P7 multi-layer index skeleton (segments as GeoDataFrame; layers pre-extracted to columns)
import numpy as np, pandas as pd
cols = ["hazard_freq", "chart_inadequacy", "dist_refuge_km", "dist_sar_km", "iceberg_exposure", "traffic_proxy"]
Z = (seg[cols] - seg[cols].mean()) / seg[cols].std()
idx_equal = Z.mean(axis=1)
W = np.random.dirichlet(np.ones(len(cols)), 100)                 # weight perturbation
idx_draws = Z.values @ W.T                                        # segments x draws -> report rank stability
```
No checksum/license/version verification beyond this.

## 12. EXECUTION PROTOCOL
1. Setup -> Stage 1 (Step 0, Step 1) -> [pause if AUTOPILOT=false] -> Stage 2 -> [Stage 1.5 if
   needed] -> Stage 3 -> final summary (<=25 lines: GO list with contribution and journal, programme
   map, diversity, first project, file paths).
2. Resume from the first incomplete stage if WORKDIR has stage files; never redo completed work.
3. Failures: API 429 -> wait 20 s once, then skip/[U]; GEE timeout -> halve region or scenes once,
   then `PILOT=PENDING`; never loop.
Begin now with Setup and Stage 1 Step 0. Do not ask for confirmation.
