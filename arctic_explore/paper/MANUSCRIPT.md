<!-- ARC-P10 manuscript draft. Working title; final title to be decided after full draft review. -->

# Hazard-timescale observability of Arctic shipping chokepoints: two periods, two mechanisms in the Sentinel-1 record

**Target journal: Remote Sensing of Environment. Fallback: Cold Regions Science and Technology.**

## Abstract

Synthetic aperture radar underpins Arctic navigation support, yet observing capability is reported as scene counts or revisit intervals, neither of which says whether a hazard is caught. We define a hazard-timescale observability metric, H, as the probability that a randomly occurring convergence event overlaps at least one acquisition, given the length-biased distribution of acquisition gaps and an independently measured distribution of hazard durations. Hazard durations come from 82,439 convergence events derived from 2016–2025 International Arctic Buoy Programme pairs; acquisition gaps come from Sentinel-1 metadata for 1,771 cells of 25 km across sixteen Arctic regions, 2016–2026. At Northern Sea Route chokepoints, H for episode-scale hazards was 0.200 before the loss of Sentinel-1B and fell to 0.097 in 2022–2024. The 12 h episode requirement implied by the buoy record was met in none of 688 region-season-year units, and no chokepoint ever reached the 24 h state requirement, so the requirement was already unmet before the constellation gap. A remove-one-platform experiment reproduces the 2022–2024 collapse to within 10 percentage points in fifteen of sixteen regions, so that period is explained by satellite count. The incomplete recovery is not: annual scene volume returned to 88.5 % with three platforms, yet European Space Agency acquisition plans allocate 86.4 % of pre-loss coverage to the European–Russian sector against 122.3 % to North America, and the deficit survives control for Sentinel-1C ramp-up. Availability of the Copernicus DTU Sentinel-1 drift product tracks H across region-years, with a Spearman correlation of 0.711. Adding a second platform raises H by 0.10-0.14 depending on season, but the chokepoints remain far below requirement at every platform count observed. Twenty Sentinel-1 pairs show chokepoint convergence is retrievable in winter and freeze-up.

**Keywords:** Sentinel-1; sea-ice drift; Arctic shipping; observing system experiment; Northern Sea Route; observability

## 1. Introduction

The Northern Sea Route and its approaches are navigated on information that is, in the great majority of cases, derived from spaceborne synthetic aperture radar. Ice charts, drift products and route-level risk indices all take SAR as their primary input, and since 2014 the Copernicus Sentinel-1 constellation has been the dominant free and systematically acquired source of that input over the Arctic marine domain (Torres et al., 2012; Potin et al., 2019). Traffic on the route has grown through the same period and is projected to grow further as the ice season shortens (Eguíluz et al., 2016; Melia et al., 2016; Gunnarsson, 2021), so the question of what a ship master or an ice service can actually see has become an operational one rather than a technical curiosity. The hazard that concerns us here is convergence: the closing of ice around a vessel, which produces the pressured-ice conditions behind besetting events and which the Polar Code framework treats as a limiting operational condition (Kotovirta et al., 2009; Kubat et al., 2016; Fu et al., 2016; IMO, 2016; Lehtola et al., 2019).

Existing approaches to describing SAR capability fall into two families, and both are well developed. The first characterises what SAR can retrieve. Sea-ice type and concentration classification from C-band has matured from threshold and texture methods to operational segmentation and deep learning (Leigh et al., 2014; Zakhvatkina et al., 2019; Komarov and Buehner, 2019; Karvonen, 2022; Dai et al., 2026), with reviews establishing the scope of polarimetric applications (Dierking, 2013; Lyu et al., 2022; Shokr and Dabboor, 2023). Drift retrieval has a parallel lineage, from cross-correlation and feature tracking to combined schemes and learned optical flow (Komarov and Barber, 2014; Lehtiranta et al., 2015; Muckenhuber and Sandven, 2017; Korosov and Rampal, 2017; Demchev et al., 2017; Qiu and Li, 2022; Howell et al., 2022; Yang et al., 2024). Crucially for this paper, that literature has long recognised that retrieval succeeds only conditionally, and reliability measures for ice-motion retrieval are themselves a subject of study (Hollands et al., 2015), with melt-season decorrelation, incidence-angle dependence and the EW noise floor identified as the principal limits of C-band (Park et al., 2018; Lohse et al., 2020; Singha et al., 2021; Korosov et al., 2022).

The second family characterises the hazard rather than the sensor. Buoy arrays have been used for four decades to measure deformation and its scaling, establishing that convergence is intermittent, spatially localised and short-lived (Marsan et al., 2004; Hutchings and Hibler, 2008; Rampal et al., 2008; Stern and Lindsay, 2009; Hutchings et al., 2011; Bouillon and Rampal, 2015; Oikkonen et al., 2017; Itkin et al., 2025). Coarse-resolution drift products derived from passive microwave and scatterometer data provide continuous pan-Arctic fields but are explicitly limited near coasts and in narrow passages (Lavergne et al., 2010; Sumata et al., 2015; Lavergne et al., 2023), which is precisely where shipping chokepoints lie.

What is missing is a bridge between the two families. Capability is reported in units — scene counts, median or ninetieth-percentile revisit intervals — that make no reference to the timescale of the phenomenon being observed, while hazard timescales are measured in a literature that makes no reference to the acquisition pattern. A region can be observed frequently in aggregate and still miss every hazard if the hazards are short relative to the gaps between acquisitions; a region observed rarely can catch most hazards if they persist for days. The quantity a decision maker needs is the probability that a hazard occurring at an arbitrary moment is seen at least once while it exists, and that quantity is a joint property of the acquisition record and the duration distribution which neither literature computes. Observing-system design has developed exactly this style of reasoning for other domains, in numerical weather prediction and in quantitative network design for the cryosphere (Langland and Baker, 2004; Kaminski et al., 2015; Boukabara et al., 2016; Kaminski et al., 2018), but it has not been applied to the question of whether Arctic SAR coverage is adequate to the hazards it is used to manage.

A second gap concerns causal attribution. The failure of Sentinel-1B in December 2021 and the subsequent entry of Sentinel-1C and Sentinel-1D have been treated informally as a natural experiment on observing capability, and downstream consequences of missing imagery have begun to be documented (Wulf et al., 2024; Wuite et al., 2026; Wulf et al., 2026). But the loss period and the recovery period have not been separated, and they need not share a mechanism: a shortfall caused by having fewer satellites and a shortfall caused by where the remaining capacity is pointed have different remedies and are distinguishable only if the acquisition plans, not merely the acquired archive, are examined. A third gap is that the open Arctic SAR record depends on a single mission, so the propagation of an interruption into the products navigators use is both plausible and, as far as we are aware, unquantified.

This paper addresses all three. We define a hazard-timescale observability metric H as the probability that a randomly occurring convergence event overlaps at least one acquisition, given the length-biased distribution of acquisition gaps (Feller, 1971; Cox, 1962) and a hazard-duration distribution measured independently from buoy pairs, with right-censoring handled by standard survival estimators (Kaplan and Meier, 1958; Turnbull, 1976). We evaluate H for 1,771 cells of 25 km across sixteen Arctic regions from 2016 to 2026, using Sentinel-1 metadata alone. We then separate the two periods: a remove-one-platform observing-system experiment for 2022–2024, and a comparison of European Space Agency acquisition-segment plans against the acquired record for 2025–2026. We test propagation into an operational Sentinel-1-derived drift product, and we process twenty image pairs at three chokepoints to establish that the hazards in question are retrievable there at all. The result is a measurement framework in which the adequacy of an Arctic SAR constellation can be stated in the units that matter to a navigator, and four findings that follow from applying it.

## 2. Data

### 2.1 Sentinel-1 acquisition metadata

Acquisition times, platform identifiers, orbit pass direction, instrument mode and scene footprints were obtained from the Google Earth Engine mirror of the Copernicus Sentinel-1 ground-range-detected collection for 1 January 2016 to 5 September 2026, restricted to Extra Wide and Interferometric Wide modes and to all polarisations. No pixel data were read at this stage. An earlier audit of the same archive against the Alaska Satellite Facility catalogue found agreement of 93–102 % across six region-years, so we treat the mirror as representative of the mission archive for counting purposes.

Sixteen regions were defined as longitude-latitude boxes and are listed in Table 1. Four are Northern Sea Route chokepoints in the strict sense, namely Kara Gate, Vilkitsky Strait, the Sannikov and Dmitry Laptev straits taken together, and Long Strait. One is the Bering Strait and Chukchi approach. Six, denoted AK1 to AK6, are sectors of an Alaskan coastal corridor running from Bering Strait to Point Barrow; these derive from a forty-segment corridor constructed at an earlier stage of this work and are spatially overlapping with the Bering–Chukchi region, which is why the two sets are never treated as independent samples. The remaining five are larger marine regions used as candidate controls and as contrast cases: Barents and Svalbard, the Greenland Sea and Fram Strait, Baffin Bay, Lancaster Sound and Victoria Strait.

Each region was divided into cells of 25 km on the EPSG:3413 polar stereographic grid, giving 1,771 cells in total. A scene was credited to a cell when the intersection of the scene footprint with the cell exceeded half the cell area. Because ground-range-detected products are distributed as slices of a single pass, slices from the same platform and pass separated by less than fifteen minutes were merged into a single acquisition and their coverage fractions summed, capped at unity; without this step large regions can never reach the coverage threshold for any individual slice. All footprint geometry was computed in EPSG:3413 rather than in longitude and latitude, because Sentinel-1 footprints crossing the antimeridian degenerate into globe-spanning polygons under a naive longitude-latitude intersection, an error that produced a spurious co-location earlier in this work.

### 2.2 Buoy trajectories

Hazard durations were derived from the International Arctic Buoy Programme Level 1 position archive for 2016–2025, downloaded without authentication. Positions south of 70° N were discarded, duplicate timestamps removed, and fixes implying speeds above 120 km d⁻¹ relative to the preceding fix rejected as transmission errors, leaving 8,661,366 fixes from 1,271 buoys. Positions were interpolated onto a three-hourly grid, and separately onto a one-hourly grid for the subset of 1,111 buoys whose native fix interval had a median at or below one hour, with interpolation permitted only when bracketing fixes lay within the corresponding half-window.

### 2.3 Ancillary and product datasets

Low-resolution sea-ice drift from the EUMETSAT Ocean and Sea Ice Satellite Application Facility, product OSI-405, was used as a Sentinel-1-independent hazard record. The product provides 48 h displacement on a 62.5 km grid, distributed daily and accessible without authentication; 3,043 daily files covering 2016–2025 excluding April and May were retrieved.

Availability of a Sentinel-1-dependent operational product was assessed using the Copernicus Marine DTU sea-ice drift analysis, dataset `cmems_obs-si_glo_phy-drift-north_my_l4_P1D-m`, which spans 6 October 2014 to 1 November 2025 on a 0.1° grid. The Danish Meteorological Institute automated ice product `cmems_obs-si_arc_phy_my_l3_P1D` was inspected but is distributed only as original files of approximately 190 MB per day, so only a sixteen-day sample was retrieved and it is not used in any inferential statement. The Norwegian Meteorological Institute ice-chart quicklook archive was counted by issuance date for 2019, 2021, 2023 and 2025.

Planned coverage was reconstructed from the European Space Agency acquisition-segment archives published in the Copernicus SentiWiki document library, comprising Sentinel-1A for 2019, 2020, 2021 and 2025, Sentinel-1B for 2019, 2020 and 2021, and Sentinel-1C for 2025. Each archive contains Keyhole Markup Language files listing planned datatake segments with satellite identifier, mode, observation start and stop times, orbit numbers and a footprint ring.

Sentinel-1 pixel data were read only for the physical demonstration of Section 4.5, comprising forty Extra Wide ground-range-detected scenes forming twenty pairs, totalling 9.2 GB.

**Table 1.** Regions, cell counts and role. Cells are 25 km on EPSG:3413.

| Region | Cells | Role |
|---|---|---|
| Kara Gate | 24 | NSR chokepoint |
| Vilkitsky | 25 | NSR chokepoint |
| Sannikov / Dmitry Laptev | 109 | NSR chokepoint |
| Long Strait | 46 | NSR chokepoint |
| Bering–Chukchi | 162 | approach; overlaps AK1–AK6 |
| AK1–AK6 | 33, 39, 44, 47, 50, 40 | Alaskan corridor sectors |
| Barents / Svalbard | 374 | contrast |
| Greenland Sea / Fram | 240 | contrast |
| Baffin Bay | 296 | contrast |
| Lancaster Sound | 81 | contrast |
| Victoria Strait | 161 | contrast |
| **Total** | **1,771** | |

## 3. Methods

### 3.1 The observability metric H

Consider a cell, a season and a year, and let the qualifying acquisitions in that window occur at times t₁ < t₂ < … < tₙ, defining gaps gᵢ = tᵢ₊₁ − tᵢ. Let a hazard occur with duration D, and assume that its onset time is uniformly distributed over the season. Under that assumption the onset falls inside gap i with probability proportional to gᵢ rather than uniformly across gaps, because long gaps present more opportunity for an onset to land in them; this is the standard length-biasing of interval sampling (Cox, 1962; Feller, 1971) and it is the reason the metric cannot be built from a mean revisit interval. Given an onset inside a gap of length g, the hazard overlaps at least one acquisition with probability min(1, D/g), since the hazard is seen unless it both begins and ends strictly inside the gap.

Combining these gives the probability that a randomly occurring hazard of duration D is caught,

  H(D) = Σᵢ gᵢ · min(1, D/gᵢ) / Σᵢ gᵢ = Σᵢ min(gᵢ, D) / Σᵢ gᵢ,

where the second equality follows from g·min(1, D/g) = min(g, D) and is what makes the metric cheap to evaluate. Averaging over the empirical duration distribution yields

  H = E_D [ Σᵢ min(gᵢ, D) ] / Σᵢ gᵢ.

We evaluate this exactly by sorting the gaps, forming their cumulative sum and using a binary search over the duration sample, which agrees with a direct evaluation of the defining expression to within 10⁻¹². Figure 1 illustrates the construction: panel (a) shows an acquisition sequence with a hazard of duration D, and panel (b) shows H as a function of D for single fixed gaps and for the length-biased mixture, making clear that the mixture is dominated by the longest gaps at small D.

**Figure 1.** Construction of the observability metric H. (a) A sequence of acquisitions defines gaps g_i; a hazard of duration D is caught if it overlaps at least one acquisition. (b) H as a function of D for three single fixed gaps and for the length-biased mixture of the gaps in panel (a), showing that the mixture is controlled by the longest gaps at small D. `fig01_H_schematic.png`


Two distinct hazard quantities are used. H_episode uses the duration of a convergence episode, the interval over which the closure rate exceeds a threshold. H_state uses the persistence of the resulting hazard state, the time until the geometry relaxes back towards its pre-event configuration. The two answer different operational questions, the first being whether the event itself is witnessed and the second whether a ship approaching afterwards can still be warned.

Four assumptions are made explicit because each has a direction of failure. First, hazard occurrence and acquisition planning are assumed independent; the Sentinel-1 background mission follows a fixed plan, so this is largely defensible, but any seasonal replanning correlated with ice conditions would bias H upward. Second, the duration distributions are transferred from the buoy network to the chokepoints, which is extrapolation and is treated as a limitation in Section 6. Third, a single acquisition inside the hazard window is counted as an observation, whereas drift retrieval requires a pair, so H is an upper bound on the probability of an actionable retrieval; Section 5 multiplies H by a measured retrieval success rate to obtain an effective value. Fourth, gaps are truncated at season boundaries and no credit is given before the first or after the last acquisition of a season.

For comparison with conventional reporting we also compute a hazard-agnostic coverage measure, O(Δt), defined as the fraction of season time spanned by consecutive qualifying acquisitions separated by no more than Δt,

  O(Δt) = Σ_{i : gᵢ ≤ Δt} gᵢ / T_season,

evaluated at Δt of 6, 12, 24, 48, 72 and 168 h. O(Δt) requires no hazard-duration input and is therefore directly comparable with the revisit statistics normally published, whereas H requires the duration distribution and answers the operational question. We report both because the first shows that our conclusions do not depend on the buoy-derived durations, while the second is the quantity that a decision maker needs; where they diverge, the divergence is itself informative, since O(Δt) counts time and H counts hazards.

Cell-level values are aggregated to region, season and year by unweighted averaging over cells, and uncertainty is expressed by a block bootstrap over cells with 1,000 draws. We report those intervals but do not interpret them as sampling uncertainty, because cells within a region share satellite orbits and are therefore far from independent; the intervals are consequently much narrower than the true uncertainty.

### 3.2 Buoy convergence events

Hazard timescales were measured from buoy pairs rather than from SAR, so that the duration distribution entering H is independent of the acquisition record whose adequacy is being judged. All buoy pairs separated by 20–100 km with overlapping records were formed, giving 9,884 pairs, and the separation time series s(t) computed for each contiguous run of at least eight three-hourly epochs within the separation band. The convergence rate is r(t) = [s(t+Δ) − s(t)]/Δ. A single threshold was fixed once, before any event was counted, as the ninetieth percentile of the magnitude of all negative rates pooled across every pair and epoch, giving 2.954 km d⁻¹ at three-hourly sampling and 4.706 km d⁻¹ at one-hourly sampling. An event is a maximal run of consecutive intervals with r below the negative of that threshold, lasting at least two intervals. Event magnitude is the total separation decrease, and event duration is the run length.

Two properties of this definition matter downstream. It is left-censored at twice the sampling interval, so at three-hourly sampling 55.9 % of events have the minimum possible duration of six hours and the median duration is a detection floor rather than a central tendency. Re-running on the one-hourly subset moves the median from 6 h to 2 h and places 85.8 % of events below the six-hour floor of the coarser sampling, confirming that the coarse median is an artefact. Magnitude filtering stabilises it: pooled across seasons, events of at least 3 km have a median duration of 9 h at one-hourly sampling against 12 h at three-hourly, and events of at least 5 km 12 h against 18 h. The season-resolved medians for the one-hourly subset, which are the values that enter H and are listed in Table 2, are 12, 8 and 9 h for the ≥ 3 km class in winter, melt and freeze-up respectively; the pooled figure of 9 h and the winter figure of 12 h are therefore different statistics of the same distribution and not a discrepancy. All durations entering H are therefore taken from the one-hourly subset and stratified by magnitude class and season, as summarised in Table 2.

**Figure 2.** Hazard timescales measured from buoy pairs, independent of Sentinel-1. (a) Cumulative distribution of convergence episode duration by magnitude class, from the one-hourly buoy subset; the dashed line marks the 12 h episode requirement. (b) Cumulative distribution of hazard-state persistence for events whose magnitude is at least 10 % of the pre-event separation; the dashed line marks the 24 h state requirement. `fig02_hazard_timescales.png`


The requirement against which observability is judged follows from these distributions rather than from an assumed service level. For a revisit interval T, an event of duration D is bracketed with certainty when D ≥ T, so the interval that brackets a fraction q of events is the (1 − q) quantile of the duration distribution; we denote by T_exp80 the largest T for which the expected fraction bracketed, E_D[min(1, D/T)], is at least 0.8, which is the population analogue and the value we quote. Applied to the ≥ 3 km class this gives approximately 12 h for episodes and 24 h for the hazard state, and these are the figures used throughout as the episode and state requirements. Correspondingly, a region-season-year unit is said to **meet the requirement when H ≥ 0.8**, that is when at least four fifths of hazards of the stated class are caught; the same 0.8 is used as the design target in Section 4.4. Both the requirement interval and the 0.8 criterion are therefore properties of the measured hazard population and not of an operator's specification, a point returned to in Section 6.

Hazard-state persistence was defined as the time from event end until the separation recovers to 90 % of its pre-event value, with runs that end before recovery treated as right-censored and handled by a Kaplan–Meier estimator (Kaplan and Meier, 1958; Turnbull, 1976). This measurand is undefined for events whose magnitude is less than a tenth of the pre-event separation, because such events never drop below the recovery threshold; that describes 84.6 % of all events, so persistence statistics are reported only for the remaining 15.4 %.

**Table 2.** Hazard timescales. Episode durations are from the one-hourly buoy subset, stratified by magnitude class and season. Persistence is from the three-hourly archive restricted to events whose magnitude is at least 10 % of the pre-event separation, and is reported by class pooled over seasons and by season pooled over classes, because the class-by-season cells are not all populated. Median hours.

| Stratum | Winter | Melt | Freeze-up | Pooled |
|---|---|---|---|---|
| Episode, 1–3 km | 2 | 4 | 4 | — |
| Episode, ≥ 3 km | 12 | 8 | 9 | — |
| Episode, ≥ 5 km | 14 | 11 | 15 | — |
| Persistence, ≥ 1 km | — | — | — | 21 |
| Persistence, ≥ 3 km | — | — | — | 24 |
| Persistence, ≥ 5 km | — | — | — | 33 |
| Persistence, all classes | 27 | 12 | 39 | 21 |

### 3.3 Reconciling the buoy and SAR magnitude scales

Convergence measured from a SAR drift field and convergence measured between two buoys are not the same number even when they describe the same deformation, because they use different baselines. A SAR event defined as a connected region of divergence below a threshold has a natural length scale equal to the square root of its area, whereas a buoy pair has the baseline of its separation. For a given strain the two magnitudes are therefore related by the ratio of those baselines, and in our data the median square root of event area is 12.2 km against a median buoy separation of 49.4 km, a factor of 0.248. Comparing the two directly without correction understates SAR magnitudes fourfold.

To place both on a common footing, virtual buoy pairs were constructed on the SAR drift fields. Node pairs separated by 20–100 km, the same band used for the real buoys, were sampled from each field, and the change in their separation over the acquisition interval was computed from the retrieved displacements. This yields, for each SAR window, a distribution of closures directly comparable with the buoy event magnitudes, and it permits the buoy rate threshold to be applied to SAR-derived pairs so that the two samples are selected in the same way as well as measured in the same way.

### 3.4 Observing system experiment

The counterfactual removes platforms rather than scenes, in the manner of an observing-system experiment (Langland and Baker, 2004; Kaminski et al., 2015). For each cell, season and year the acquisition series was rebuilt from the subset of passes belonging to a nominated combination of platforms, and H recomputed on the resulting gaps. Because 2022–2024 was a single-platform period, the pre-registered comparison is between the Sentinel-1A-only counterfactual constructed from 2019–2021 and the observed 2022–2024 values, region by region. Using the best-matching platform per region would be a post hoc selection and is reported only as a sensitivity. Design curves were formed by evaluating every platform combination available in each period, giving one-, two- and three-platform values.

### 3.5 Acquisition plan parsing

Planned segments were extracted from the Keyhole Markup Language archives by parsing each placemark for satellite identifier, datatake identifier, mode, observation start time and footprint ring. Because successive mission-plan files overlap in validity, segments were deduplicated on the triple of satellite, datatake identifier and observation start time. Footprint rings were projected to EPSG:3413 and a segment was credited to a region when it covered at least half the region box, the same rule applied to acquired scenes so that planned and acquired counts are commensurable. The ramp-up of new platforms was determined from the archive itself, by taking the first month in which a platform's monthly scene count reached 80 % of the median of its last six months.

### 3.6 Sentinel-1 pair processing and virtual buoy pairs

Twenty Extra Wide ground-range-detected pairs were selected at Vilkitsky, Sannikov and Long Strait for freeze-up and winter of 2019–2021, requiring a separation of 12–72 h, a footprint overlap of at least half the smaller scene computed in EPSG:3413, and coverage of at least 30 % of the region box by each scene. Selection was balanced across the six region-season combinations by round-robin rather than by taking the globally best-overlapping pairs, which would have concentrated the sample at one strait.

Each scene was read from the HH band, converted to a relative decibel scale after dividing by the per-column median to suppress the across-track gradient, and reprojected from its ground-control points onto a common 200 m EPSG:3413 grid covering the region box with a 60 km margin. Ice motion was retrieved with a two-stage scheme following the design of Korosov and Rampal (2017), whose combination of feature tracking with pattern matching is the standard formulation for this problem (see also Muckenhuber and Sandven, 2017; Demchev et al., 2017): oriented FAST and rotated BRIEF features were detected on a four-times-decimated image pair, matched by Hamming distance with a ratio test, and filtered by median absolute deviation to give a coarse displacement field; that field then initialised a normalised cross-correlation search at nodes on a 5 km grid, with a template of 25 pixels and a search window of ±10 km about the coarse prediction. A node was accepted when the correlation peak reached 0.4, when the ratio of the peak to the next highest local maximum reached 1.2, and when the displacement lay within 80 % of the search radius. Parameters are those used earlier in this work for a Chukchi melt-versus-winter comparison and were not retuned per season or per strait. The scheme is a reimplementation of the published two-stage design and is **not claimed to be identical to the `sea_ice_drift` package**, which is not distributed through the Python Package Index.

The success rate is the number of accepted nodes divided by the number of nodes at which a match was attempted, a node being attempted when its template is fully within valid data in the first image, when its search window is at least 90 % valid in the second, and when the template standard deviation exceeds 0.3 dB. Accepted displacements were converted to velocities in kilometres per day, with the sign of the northing component inverted relative to the pixel row index, and divergence was formed by centred differences on the 5 km node grid.

Candidate convergence events were defined as connected components of the region where divergence falls below the tenth percentile of that pair's own divergence distribution, retaining components of at least 100 km². This definition is relative to each pair, so it identifies the most convergent tenth of each field rather than an absolute strain threshold, and its magnitude scale is set by the square root of component area, which is the origin of the baseline mismatch treated in Section 3.3. Every candidate event was subsequently subjected to the edge-artifact audit reported in Appendix A.

Virtual buoy pairs were formed on the same accepted-node fields. Node pairs were drawn at random and retained when their separation fell in the 20–100 km band used for the real buoys, giving 240,949 pairs across the twenty windows; the change in separation over the acquisition interval was computed from the retrieved displacements, and the implied rate compared with the thresholds derived from the buoy archive in Section 3.2. This construction measures the SAR fields on the buoy baseline and, when the buoy rate threshold is applied, selects them in the same way, which is what makes the two magnitude distributions comparable.

## 4. Results

### 4.1 The requirement was never met at the chokepoints

Taking the buoy record at face value, an episode-scale hazard of at least 3 km lasts a median of 8–12 h depending on season, 9 h pooled and the resulting hazard state persists for a median of 24 h, which implies revisit requirements of 12 h and 24 h respectively if a large majority of hazards is to be bracketed. Neither was met. Across 688 region-season-year units, of which 512 fall in the three main seasons, the hazard-agnostic coverage O(12 h) defined in Section 3.1 never reached 0.5, and its maximum over the whole record is 0.278. The 24 h criterion was reached in only four regions in any year, all of them large high-latitude boxes, and in none of the Northern Sea Route chokepoints in any year of the record.

The cell-level metric tells the same story in the currency of hazards rather than of time. Before the loss of Sentinel-1B, chokepoint H_episode for the 3 km class stood at 0.200 and H_state at 0.504 (Fig. 3). Four in five episode-scale convergence events at the chokepoints were therefore already going unseen in 2019–2021, a period with two satellites operating normally. This is the central negative result of the paper, and it is not a consequence of the constellation gap. *Caveat: the 12 h and 24 h requirements are derived from the buoy duration distribution rather than from an operator's stated need, so they express what would be needed to catch the measured hazards, not a service specification agreed with an ice service.*

**Figure 3.** H per 25 km cell on the EPSG:3413 grid, for the ≥ 3 km magnitude class, by season (rows) and period (columns). Northern Sea Route chokepoints are labelled. Colour runs from 0 to 1, where 1 means every hazard is caught. Two panels are provided, for H_state and for H_episode. `fig03_H_state3_maps.png`, `fig03_H_episode3_maps.png`


### 4.2 The 2022–2024 gap widened an existing deficit

Between 2022 and 2024 chokepoint H_episode fell from 0.200 to 0.097 and H_state from 0.504 to 0.363; across all sixteen regions H_episode fell from 0.267 to 0.151 and H_state from 0.562 to 0.441 (Fig. 3, Table 3). At the chokepoints this means that roughly nine in ten episode-scale hazards went unobserved during the gap, against four in five before it.

**Table 3.** Observability by period, for the ≥ 3 km magnitude class. Cell-level means, unweighted over cells; the three main seasons only.

| Group | Period | H_episode | H_state |
|---|---|---|---|
| All sixteen regions | pre 2019–21 | 0.267 | 0.562 |
| All sixteen regions | during 2022–24 | 0.151 | 0.441 |
| All sixteen regions | post 2025–26 | 0.245 | 0.532 |
| NSR chokepoints | pre 2019–21 | 0.200 | 0.504 |
| NSR chokepoints | during 2022–24 | 0.097 | 0.363 |
| NSR chokepoints | post 2025–26 | 0.176 | 0.467 |

**Table 3b.** Observability by magnitude class at the chokepoints, H_episode, cell-level means. Durations from the one-hourly buoy subset.

| Class | pre 2019–21 | during 2022–24 | post 2025–26 |
|---|---|---|---|
| ≥ 1 km | 0.081 | 0.042 | 0.073 |
| 1–3 km | 0.057 | 0.029 | 0.051 |
| ≥ 3 km | 0.181 | 0.093 | 0.161 |
| ≥ 5 km | 0.233 | 0.121 | 0.208 |


An attempt to express this as a difference-in-differences between treated and untreated regions fails at the first step, and the failure is itself informative. Defining treatment as a retention ratio below 0.5, where retention is the 2022–2024 scene count divided by the 2019–2021 count, nine of sixteen regions are treated and seven are intermediate, but **no region has a retention of 0.9 or above**. The lowest is Sannikov at 0.310 and the highest Bering–Chukchi at 0.846. The loss was an Arctic-wide simultaneous shock and there is no untreated control, so the pre-registered contrast cannot be constructed. A post hoc dose-response comparison between the lost and intermediate groups gives −25.7 percentage points on H_state with a bootstrap interval of −49.9 to +0.6, which includes zero, and the two groups differ systematically in latitude and in baseline observability, so parallel trends is not plausible. *Caveat: no causal estimate of the gap's effect is available from a between-region design; the counterfactual of Section 4.4 is the appropriate instrument instead.*

### 4.3 Chokepoint hazards are real and Sentinel-1 can retrieve them

The low-resolution drift product cannot be used to establish whether chokepoint convergence occurs. On the 62.5 km OSI-405 grid, Vilkitsky Strait yields **no valid retrieval at all** across 76,075 point-days in ten years, being classified as land or coast throughout; Sannikov, Long Strait and Kara Gate yield a divergence value on 0.1 %, 0.3 % and 0.0 % of point-days respectively, and most of those valid values are flagged as interpolated rather than measured. Only the Bering–Chukchi approach, at 6.8 %, supports a time series. There the fraction of convergence days with a Sentinel-1 acquisition within 24 h was 0.422 in 2022, 0.177 in 2023 and 0.892 in 2024, so the pre-registered expectation that this fraction would remain below 0.25 in every year of the gap is rejected.

Direct processing of Sentinel-1 pairs reverses the apparent picture. Twenty pairs at Vilkitsky, Sannikov and Long Strait in freeze-up and winter of 2019–2021, matched with a feature-tracking and normalised cross-correlation scheme, produced at least thirty valid vectors in **all twenty cases**, with a mean success rate of 0.510. Pooled over the ten freeze-up pairs the success rate is **0.392**, against 0.628 over the ten winter pairs; the per-strait means range from 0.377 to 0.419 in freeze-up and from 0.484 to 0.779 in winter. Where the coarse product sees nothing, Sentinel-1 itself yields thousands of drift vectors in the same straits. The hazards are not unobservable; the low-resolution product simply cannot resolve them.

Expressing those fields in the buoy-pair metric closes the loop. Sampling 240,949 virtual buoy pairs at 20–100 km separation on the twenty fields, and applying the buoy rate threshold so that the selection matches as well as the measurement, 0.50 % of pairs qualify and their median closure is 5.88 km, with a ninetieth percentile of 6.94 km and a maximum of 10.63 km (Fig. 7). Strait convergence of the magnitude the buoy record describes is therefore present in the SAR fields, concentrated at Vilkitsky in winter where 1.86 % of virtual pairs qualify. *Caveat: the nineteen individual events detected by the connected-component procedure are unvalidated, since no buoy lay within 100 km of any of them; they are reported in Appendix A and no inference rests on them.*

Four representative fields are shown in Fig. 8.

**Figure 8.** Four examples of strait convergence, two at Vilkitsky and two at Sannikov, showing before and after Extra Wide HH imagery with the divergence field overlaid. `fig08_strait_examples.png`


**Figure 7.** Strait drift fields expressed in the buoy-pair metric. Exceedance of window closure for 240,949 virtual buoy pairs at 20–100 km separation, unconditionally and after applying the buoy rate threshold; dashed and dotted lines mark 3 km and 5 km. `fig07_virtual_pairs.png`


### 4.4 The gap is explained by satellite count

Deleting Sentinel-1B from the 2019–2021 record and recomputing H_state reproduces the observed 2022–2024 values to within 10 percentage points in **fifteen of sixteen regions**, with most differences inside ±3 points: Fram +0.2, Barents +0.8, Vilkitsky −0.3, Long Strait −1.4 and Baffin −2.6 (Table 4). The single failure is Sannikov at +12.3 points, where the observed acquisition rate during the gap was lower than a single-platform constellation would predict. The collapse of 2022–2024 is thus almost entirely a platform-count phenomenon, and no appeal to changed tasking is needed to explain it.

**Table 4.** Observing system experiment. Sentinel-1A-only counterfactual built from 2019–2021 against observed 2022–2024 H_state, by region, in percentage points. Positive means the counterfactual exceeds the observation.

| Region | Difference (pp) | Region | Difference (pp) |
|---|---|---|---|
| Greenland Sea / Fram | +0.2 | Victoria Strait | +2.7 |
| Barents / Svalbard | +0.8 | AK6 | +2.8 |
| Vilkitsky | −0.3 | AK2 | +2.8 |
| Long Strait | −1.4 | AK1 | +2.9 |
| Baffin Bay | −2.6 | Bering–Chukchi | +2.9 |
| AK5 | +2.2 | Kara Gate | +5.6 |
| Lancaster Sound | +2.2 | **Sannikov** | **+12.3** |
| AK4 | +2.3 | | |
| AK3 | +2.4 | | |


The design curve shows why adding platforms does not resolve the chokepoint deficit (Fig. 4). Because platform availability differs by season, combinations are compared only within matched season windows, and a combination is admitted only when every platform in it actually acquired in that season; this removes 150 of 800 nominal combinations, including all apparent three-platform values outside melt 2026. Averaged over all regions, H_state rises from 0.525 with one platform to 0.662 with two in freeze-up, from 0.454 to 0.598 in winter, and from 0.351 to 0.451 in melt. At the chokepoints the corresponding pairs are 0.450 to 0.586, 0.388 to 0.527 and 0.287 to 0.386. The marginal gain of the second platform is therefore 0.10 to 0.14 depending on season, with a season-mean of 0.127 across all regions and 0.125 at the chokepoints. Only 15 of 650 admissible region-season-year-combination units reach 0.8, all of them in large high-latitude regions, and the chokepoint maximum over every admissible combination is 0.718.

**Figure 4.** Constellation design curve within matched season windows. Mean H_state against number of platforms, for all regions and for the Northern Sea Route chokepoints, with error bars showing the standard deviation across region-year combinations; a combination is admitted only when every platform in it acquired in that season. Filled markers are fully sampled; the hollow marker is the three-platform value, which exists only for melt 2026 (nine regions, two of them chokepoints) and is provisional. The dashed line marks the 0.8 requirement. `fig04_design_curve.png`


A three-platform value exists only for melt 2026, from nine regions of which two are chokepoints, and is plotted as a hollow provisional point in Fig. 4. In that single window it stands at 0.511 against 0.451 for two platforms across all regions, and 0.429 against 0.386 at the chokepoints. We deliberately draw no marginal-gain conclusion from it: one season, one year, and a platform still ramping up cannot support a statement about the third satellite's contribution. *Caveat: platform count is confounded with orbital plane in this design, and Sentinel-1D had six months of data with no established plateau at the time of analysis.*

### 4.5 The recovery shortfall is explained by allocation

By 2025–2026 the constellation is larger than before the loss, yet annual scene volume across the sixteen regions stands at 88.5 % of the 2019–2021 rate. The shortfall is not distributed evenly. Controlling for ramp-up by restricting to the window in which Sentinel-1A and Sentinel-1C were both in routine operation, from April 2025 to March 2026, the European–Russian sector sits at 77.4 % of its pre-loss rate while the North American and Bering sector sits at 121.1 %.

The acquisition plans show the same asymmetry before any acquisition takes place. Counting planned segments that cover at least half a region box, the European–Russian sector is planned at 86.4 % of its 2019–2021 rate against 122.3 % for North America, with Barents planned at 56 % (Fig. 5, Table 5). Because this appears in the plan rather than only in the outcome, the shortfall is an allocation decision and not a consequence of constellation size. Retrieving the Sentinel-1A plans for the gap years themselves shows that the reallocation did not begin in 2025: during 2022–2024, when a single platform had to be shared across the Arctic, the European–Russian sector was planned at 49.8 % of its pre-loss rate while the North American sector was planned at 62.0 %, so the sectoral asymmetry was already present when capacity was scarce and then widened once capacity was restored. The claim requires narrowing, however: within the same sector Vilkitsky is planned at 146 % and acquired at 156 %, and Long Strait at 113 %, so the deficit is specific to the Barents–Kara–Laptev sub-sector rather than to the European–Russian Arctic as a whole. *Caveat: acquisition-segment files describe planned datatakes and do not guarantee execution or downlink, and plans for 2022–2024 were not retrieved, so the comparison is pre versus post only.*

**Table 5.** Planned segments per year by sector, including the gap years, and acquired scenes. Planned counts are segments covering at least half a region box; acquired counts are passes meeting the same criterion. The ramp-up-controlled acquisition window is April 2025 to March 2026. Sentinel-1A plans were retrieved for 2019–2025 and Sentinel-1B plans for 2019–2021, so the gap-year column is single-platform by construction and its absolute level is not comparable with the two-platform pre-loss column; the sector *ratio* between the two columns is the quantity of interest.

| Sector | Planned 2019–21 /yr | Planned 2022–24 /yr | % of pre | Planned 2025 | % of pre | Acquired, ramp-up controlled |
|---|---|---|---|---|---|---|
| European–Russian | 7,162 | 3,570 | **49.8 %** | 6,240 | **87.1 %** | **77.4 %** |
| North American–Bering | 8,521 | 5,280 | **62.0 %** | 10,511 | **123.4 %** | **121.1 %** |
| of which Barents / Svalbard | 1,710 | 731 | 42.7 % | 971 | 56.8 % | 38.3 % |
| of which Sannikov | 570 | 209 | 36.7 % | 510 | 89.5 % | 63.5 % |
| of which Vilkitsky | 495 | 277 | 56.0 % | 728 | 147.1 % | 156.1 % |


**Figure 5.** European Space Agency planned acquisition segments against acquired scenes, per region, before and after the constellation gap, on a logarithmic axis. Regions are grouped by sector. `fig05_planned_vs_acquired.png`


### 4.6 The shortfall propagated into an operational product

Availability of the DTU Sentinel-1 drift product, defined as the fraction of days on which at least 5 % of a region's pixels carry a valid vector, correlates with H_state across region-years at a Spearman coefficient of **0.711** (p = 1.7 × 10⁻¹⁸, n = 112), and with H_episode at 0.736 (Fig. 6). The relationship is not merely a cross-sectional contrast between well- and poorly-observed regions: computing the correlation along the time axis within each region separately gives a median of 0.727 across the sixteen regions. Product availability fell from 0.152 before the loss to 0.031 during it, a decline of 80 %, and stood at 0.033 in the partial 2025 sample. Varying the validity threshold to 2 % and 10 % gives correlations of 0.714 and 0.659, so the result is robust to that choice (Table 6).

**Figure 6.** Availability of the DTU Sentinel-1 drift product per region-year, defined as the fraction of days with at least 5 % valid pixels. Cyan lines mark the loss of Sentinel-1B and the entry of Sentinel-1C into routine operations. `fig06_dtu_availability.png`


*Caveat, which must accompany every statement of this result: the DTU product is itself derived from Sentinel-1. The correlation therefore relates two quantities computed from the same archive and is not independent confirmation. No Sentinel-1-independent product was reachable for this test: the OSI SAF low-resolution drift product is derived from passive-microwave and scatterometer sensors, and no Sentinel-1-based OSI SAF drift product exists, and the Norwegian ice-chart archive is issued on a fixed weekday schedule, with 248, 253, 251 and 250 issuance days in 2019, 2021, 2023 and 2025 respectively, unchanged through the gap.*

**Table 6.** Sensitivity of the product-consequence result to the validity threshold. Region-years, n = 112.

| Valid-pixel threshold | ρ with H_state | p | ρ with H_episode | Within-region median ρ | Mean availability |
|---|---|---|---|---|---|
| ≥ 2 % | 0.714 | 9.6 × 10⁻¹⁹ | 0.741 | 0.673 | 0.104 |
| ≥ 5 % | 0.711 | 1.7 × 10⁻¹⁸ | 0.736 | 0.727 | 0.083 |
| ≥ 10 % | 0.659 | 2.8 × 10⁻¹⁵ | 0.683 | 0.816 | 0.062 |

### 4.7 Effective observability

Because H counts a hazard as observed when a single acquisition falls inside its window, whereas retrieving ice motion requires a pair, the operationally meaningful quantity is the product of H with the probability that a retrieval succeeds. Retrieval success was measured directly on image pairs: 0.628 pooled over ten winter pairs at the three straits and 0.392 pooled over ten freeze-up pairs, against 0.02 measured earlier for melt-season Chukchi pairs conditioned on ice presence. Table 7 combines these with the season-resolved chokepoint H_state values.

**Table 7.** Effective observability E = H_state × retrieval success at the Northern Sea Route chokepoints, ≥ 3 km class, by season and period. H_state is the season-resolved chokepoint mean; retrieval success is measured at the straits for winter and freeze-up and from Chukchi melt-season pairs conditioned on ice presence for melt.

| Season | H_state pre / during / post | Retrieval success | E, pre 2019–21 | E, during 2022–24 | E, post 2025–26 |
|---|---|---|---|---|---|
| Winter | 0.549 / 0.376 / 0.466 | 0.628 | **0.345** | **0.236** | **0.293** |
| Freeze-up | 0.574 / 0.437 / 0.607 | 0.392 | **0.225** | **0.171** | **0.238** |
| Melt | 0.390 / 0.276 / 0.398 | 0.020 | **0.008** | **0.006** | **0.008** |

The melt-season row is the important one. No acquisition schedule can lift E above about 0.01 in that season, because the limiting factor is the failure of classical C-band feature tracking on a melting surface rather than the observing cadence. In winter and freeze-up the effective values lie between 0.17 and 0.35, so even in the seasons where retrieval works, roughly seven in ten hazard states go unretrieved. Freeze-up is also the only season whose post-gap value exceeds its pre-gap value, which follows from the recovery of acquisition density at Vilkitsky and Long Strait noted in Section 4.5 rather than from any improvement in retrieval. *Caveat: the melt figure comes from a different region and a smaller sample than the winter and freeze-up figures, and all three are upper bounds in the sense of Section 6.6.*

One value in Section 4.3 deserves comment. The hazard-observed fraction at the Bering–Chukchi approach rises to 0.892 in 2024, higher than any pre-loss year, which is not a recovery of capability but a consequence of how the denominator is formed: convergence days are defined against each cell's own ten-year climatology, and 2024 yielded few qualifying days at a time when the Alaskan corridor was being planned and acquired above its pre-loss rate, so a small number of hazard days coincided with unusually dense sampling. The series should be read as three noisy annual estimates rather than as a trend.

## 5. Discussion

### 5.1 Two periods, two mechanisms

The most consequential result of this work is that the two halves of the Sentinel-1 discontinuity have different explanations, and that treating them as one phenomenon produces a wrong diagnosis. For 2022–2024 the observing system experiment is decisive: removing a platform from the pre-loss record reproduces what was observed, region by region, to within a few percentage points almost everywhere. Nothing beyond the loss of a satellite needs to be invoked. For 2025–2026 the same reasoning fails, because the constellation is larger than it was in 2019–2021 and yet the pre-loss acquisition rate has not been restored in the Barents–Kara–Laptev sub-sector. The acquisition plans resolve the ambiguity: the shortfall is present in the plan, before execution, and in the opposite direction to the North American sector, which is planned and acquired above its pre-loss level.

This distinction matters for what can be recommended. A capability gap caused by platform loss is remedied by launching platforms, and the recovery of the global aggregate to 88.5 % shows that this remedy has largely worked. A capability gap caused by allocation is not remedied by launching platforms at all; it is a question of mission planning priorities, and it will persist through any number of future launches unless the plan changes. Conflating the two would lead an agency to procure hardware in response to a scheduling decision.

### 5.2 What a constellation cannot fix

Three separate arguments converge on the conclusion that the chokepoint deficit is not a procurement problem. The first is the design curve. Adding a second platform buys 0.10 to 0.14 of H depending on season, which leaves the chokepoints at 0.386 to 0.586 against a requirement of 0.8; closing that distance would require roughly two further doublings of the acquisition rate, which no announced constellation provides. The third platform cannot yet be assessed, because an admissible three-platform window exists only for melt 2026, and we decline to extrapolate from it. The second is the magnitude structure of the hazard itself. Small convergence events are both more common and shorter: for the 1–3 km class the median episode duration is 2–4 h, and chokepoint H for that class during the gap is 0.029, meaning that 97 % of such events pass unobserved. Catching them would require a revisit of a few hours, which is three to six times more demanding than the 12 h figure quoted as the episode requirement, and that figure is itself the relaxed value appropriate to the ≥3 km class.

The third argument is that observation is not the only bottleneck. Multiplying H by the retrieval success rate measured on real image pairs gives an effective observability of roughly 0.18–0.28 in winter but only 0.006–0.009 in the melt season, because classical C-band feature tracking largely fails once the surface begins to melt. In that season no increase in acquisition frequency can raise the effective value above about 0.01, and the limiting factor is the retrieval algorithm and the radar band rather than the observing cadence. The freeze-up rate, previously unmeasured, is 0.392 pooled over the ten freeze-up pairs, so a working assumption of 0.47 carried over from winter was about 19 % optimistic. A recent benchmark of deep-learning optical flow on RADARSAT-2 reports sub-kilometre accuracy and might change this picture (Deep-learning optical flow benchmark, 2025), but it was evaluated only on March-to-May pack ice, so it cannot be assumed to transfer to melt or freeze-up conditions; the melt-season and incidence-angle limits of C-band are themselves well documented (Park et al., 2018; Lohse et al., 2020; Singha et al., 2021).

### 5.3 Implications for measurement practice

The metric proposed here is cheap. It requires only acquisition metadata and an externally measured duration distribution, and its closed form makes evaluation over thousands of cells trivial. We would argue that reporting observing capability without reference to the timescale of the phenomenon being observed is no longer defensible when the alternative costs so little. The length-biasing of gaps is not a technicality: using a mean revisit interval in place of the gap distribution systematically flatters the result, because it hides the long gaps in which most hazard onsets actually fall.

Two methodological cautions emerged that generalise beyond this application. Event duration statistics derived from interval-sampled trajectories are left-censored at twice the sampling interval, and a median that coincides with that floor should be read as a property of the sampling rather than of the physics; only magnitude-stratified durations proved stable across sampling rates. And magnitudes measured on different baselines are not comparable without correction, a factor of four in our case, which was large enough to invert a conclusion about whether events of a given class were present at all.

### 5.4 Dependence on a single open mission

Every quantitative statement in this paper concerns Sentinel-1, and that is not an arbitrary scope. For open, free and systematically acquired SAR over the Arctic marine domain there is at present no alternative of comparable coverage, which is why an interruption to one mission propagates as directly as Section 4.6 shows. Three other sources are sometimes offered as mitigation, and it is worth being precise about what each changes.

The RADARSAT Constellation Mission acquires C-band over the Canadian Arctic with a three-satellite revisit and would materially improve the North American sectors (Dabboor and Geldsetzer, 2014; Howell et al., 2022), but its catalogue is not openly distributed on the terms that Sentinel-1 is, and its coverage of the Russian Arctic chokepoints that dominate our deficit is not the mission's priority. NISAR adds L-band, whose advantages for ice mapping are established (Meyer et al., 2011; Singha et al., 2021) and which penetrates a melting surface far better than C-band and is therefore the one development that could plausibly attack the melt-season retrieval failure rather than the acquisition cadence; our earlier audit of its first season found dual-polarisation frames genuinely co-located with Sentinel-1 in only 92 unique pairs below 78° N, so the near-term contribution is to physics rather than to routine coverage. Commercial constellations offer short revisit at high resolution and can be tasked onto a specific strait, which suits incident response, but tasked acquisition is by construction not the systematic background coverage that a climatology of observability requires, and the cost model does not support continuous monitoring of every chokepoint.

None of the three removes the finding of Section 4.4, that the marginal value of an additional platform is 0.10 to 0.14 of H and the chokepoint requirement is a factor of two further away. What they change is the composition of the deficit rather than its size: L-band addresses the season in which retrieval fails, and additional C-band capacity addresses the seasons in which it works. We make no recommendation as to procurement; the point is only that the measurement framework of this paper is the one that would let such a comparison be made on the quantity that matters to a navigator.

## 6. Limitations

**6.1 Buoy-to-strait extrapolation.** The duration and persistence distributions that enter H are measured from International Arctic Buoy Programme pairs, and the buoy network is heavily biased towards the central Arctic, a limitation long recognised in deformation studies (Hutchings et al., 2011; Itkin et al., 2025): the central Arctic region supplied 55 % of all events, and the Laptev and East Siberian sector supplied 1,147 events in total, of which only 17 fall in winter, from eight pairs and fourteen buoys. Applying the pooled distribution to Vilkitsky, Sannikov and Long Strait is therefore extrapolation from where buoys drift to where ships transit. If strait convergence is systematically shorter than pack-ice convergence, which the confinement of a strait makes plausible, H as reported is too high and the deficit is worse than stated.

**6.2 Magnitude-class mismatch.** The SAR event metric and the buoy metric use different baselines, the square root of event area against the buoy separation, and differ by a factor of 0.248 in our data. Section 3.3 reconciles them with virtual buoy pairs, and after that correction the SAR fields do contain closures of the magnitude the buoy record describes. Two residuals remain. The two samples are selected differently, the buoy events being the extreme decile of a rate distribution and the virtual pairs an unconditional sample until the same threshold is applied; and the SAR windows of 24–48 h time-average the 2–12 h episodes of interest, so SAR-derived convergence rates are lower bounds on the instantaneous values. Comparisons of central tendency between the two are therefore not admissible without the threshold matching described in Section 3.3.

**6.3 Shared-archive dependence.** The product-consequence result of Section 4.6 relates the availability of the DTU drift product to H, but the DTU product is generated from Sentinel-1. The correlation is thus between two functions of one archive. The direction of causation is not in doubt, since acquisition precedes retrieval, but the result cannot be described as independent verification, and we do not claim that a Sentinel-1-independent dataset confirms the propagation. None was available: the OSI SAF drift products are passive-microwave and scatterometer based and no Sentinel-1-based OSI SAF drift product exists, and the Norwegian ice-chart archive is issued on a fixed weekday schedule whose issuance count was unchanged through the gap, so it cannot register a propagation signal even in principle.

**6.4 Planned segments versus acquired scenes.** The acquisition-segment archives describe planned datatakes. A planned segment may fail to execute, may not downlink, or may be superseded, and the archives give no means of distinguishing these outcomes. The plan-versus-acquisition comparison of Section 4.5 is therefore a comparison of intent with outcome, not an audit of execution. Plans for 2022–2024 were not retrieved, so the comparison is restricted to pre-loss against post-loss and cannot speak to how tasking behaved during the gap itself.

**6.5 Sentinel-1D ramp-up.** Sentinel-1D first appears in the archive in April 2026 with six months of data and no established plateau, so its routine-operations onset could not be determined by the criterion applied to Sentinel-1C, which reached routine operations in April 2025. The three-platform window consequently spans April to August 2026 only, comprising melt-season months, and does not represent a mature three-satellite constellation in freeze-up or winter. The three-platform point on the design curve should be read as provisional.

**6.6 H is an upper bound.** A single acquisition falling inside a hazard window is counted as an observation, but retrieving ice motion requires an image pair, and inspection of the strait record shows that the two conditions are far from equivalent: at Sannikov, convergence days with an acquisition within 24 h exist, whereas pairs separated by 24 h or less largely do not. The effective values obtained by multiplying H by measured retrieval success, of order 0.2 in winter and 0.01 in melt, are the operationally meaningful figures, and they are themselves upper bounds because the retrieval rates come from a small number of scenes in limited conditions.

**6.7 Cell bootstrap intervals are too narrow.** Uncertainty on region-level H is expressed by a block bootstrap over cells, but cells within a region are traversed by the same satellite orbits and their acquisition gaps are strongly dependent. The resulting intervals, which are often only one or two percentage points wide, describe the spread across cells and not the uncertainty in the regional value. They should not be read as confidence intervals, and no significance test in this paper relies on them.

**6.8 Small events require shorter revisit than the headline requirement.** The 12 h episode requirement is the value appropriate to convergence of at least 3 km. For the 1–3 km class the median episode duration is 2–4 h and chokepoint H falls to 0.029 during the gap. Any operational specification derived from this paper must therefore state its magnitude class explicitly, because the revisit implied by the requirement varies by a factor of three to six across the classes we can measure, and the smallest class we can measure is not the smallest class that exists.

**6.9 Additional constraints of scope.** Regions are approximated by longitude-latitude boxes rather than by strait polygons, and the coverage criterion of half a region box is sensitive to box size. The Alaskan corridor sectors overlap the Bering–Chukchi region, so the two are not independent in any aggregate. The novelty assessment underpinning the framing of this work was conducted with Crossref and arXiv only, because the Semantic Scholar interface returned rate-limit responses throughout, and it should be repeated with an authenticated search before submission.

## 7. Conclusions

Observing capability over the Arctic marine domain has been reported in units that cannot answer the question operators ask. We have proposed a metric, H, that can: the probability that a hazard occurring at an arbitrary moment is seen at least once, given the length-biased distribution of acquisition gaps and an independently measured distribution of hazard durations. Applied to sixteen Arctic regions and 1,771 cells of 25 km over 2016–2026, it yields four findings.

First, the requirement implied by the buoy-measured hazard timescales was never met at the Northern Sea Route chokepoints, in any year of the record including the two-satellite years before December 2021. Four in five episode-scale convergence events were already going unobserved at the chokepoints in 2019–2021.

Second, the 2022–2024 constellation gap widened that deficit to roughly nine in ten, and this period is explained by platform count alone: a single-platform counterfactual built from the pre-loss record reproduces the observed values within 10 percentage points in fifteen of sixteen regions.

Third, the incomplete recovery of 2025–2026 has a different cause. With three platforms the aggregate scene rate is 88.5 % of its pre-loss value, but the European Space Agency acquisition plans allocate 86.4 % of pre-loss coverage to the European–Russian sector against 122.3 % to North America, and the deficit survives control for Sentinel-1C ramp-up. The shortfall is an allocation decision, specific to the Barents–Kara–Laptev sub-sector, not a consequence of constellation size.

Fourth, the deficit reaches the products that navigators use. Availability of the Copernicus DTU Sentinel-1 drift analysis tracks H across region-years with a Spearman coefficient of 0.711, robust across validity thresholds, though the product is derived from the same archive and so this is not independent confirmation.

Adding satellites will not close the chokepoint gap. A second platform is worth 0.10 to 0.14 of H depending on season, which still leaves the chokepoints between 0.386 and 0.586 against a requirement of 0.8, and the contribution of a third cannot yet be assessed because only one melt-season window contains an admissible three-platform combination; the smallest and most frequent convergence events last two to four hours; and in the melt season the binding constraint is not observation at all but the failure of classical C-band retrieval, which no acquisition cadence can repair.

## Appendix A. Candidate strait convergence events

Twenty Sentinel-1 pairs at Vilkitsky, Sannikov and Long Strait in freeze-up and winter 2019–2021 were processed with the matcher described in Section 3.6, and connected regions of divergence below the tenth percentile of each pair's distribution, with area of at least 100 km², were extracted as candidate events. Nineteen were found, all in winter, thirteen at Sannikov and six at Vilkitsky, with a median area of 150 km² and a maximum of 700 km².

**Edge-artifact audit.** Because a convergence signal can be manufactured at the boundary of the two-scene overlap, where one image contributes no data and the matcher extrapolates, every event was tested against that boundary. For each event we computed the distance from its centroid to the boundary of the intersection of the two scene footprints, and the share of its constituent grid nodes lying within 5 km of that boundary, flagging an event as edge-suspect when that share exceeded one half. **None of the nineteen was flagged.** All nineteen centroids fall inside the overlap polygon, at distances from its boundary of 18.9 to 135.5 km, and no event has any node within 5 km of the boundary, so the share is zero in every case. The events are therefore not boundary artifacts. They are, however, strongly clustered by acquisition pair: the nineteen events come from only five pairs, and nine of them from a single Sannikov pair of 13 January 2019, so they cannot be treated as nineteen independent observations of strait convergence.

These events remain **not validated** against in-situ data. No International Arctic Buoy Programme buoy lay within 100 km of any of the nineteen, even after relaxing the temporal bracket to ±12 h, so no comparison was possible. They are presented as a contact sheet in Fig. A1 for human adjudication, with the decision column of the accompanying table left blank, and no result in the main text depends on them. Their magnitudes, expressed on the buoy baseline as described in Section 3.3, place ten below 1 km, eight between 1 and 3 km and one at or above 5 km. The main-text evidence that strait convergence of navigable magnitude exists in the SAR fields rests instead on the virtual buoy-pair analysis of Section 4.3, which does not depend on the connected-component event definition.

**Figure A1.** Contact sheet of the nineteen candidate strait convergence events, for human adjudication; the decision column of the accompanying table is left blank. `figA1_contact_sheet.png`


## References

All in-text citations resolve to keys in `paper/references.bib`, which holds **76 entries, every one verified
in-session** by retrieval of its DOI through Crossref, by OpenLibrary for the two books, by arXiv for the one
preprint, or by a live URL check for the three grey-literature items (the IMO POLARIS circular, the CHNL transit
statistics and the Bellona report), which carry no DOI and are marked as such. Nothing in the bibliography rests
on an unverified identifier, and no DOI was inferred or constructed.

Semantic Scholar could not be used: the environment variable holding the API key was unset, and the
unauthenticated `graph/v1/paper/search` endpoint returned HTTP 429 on every attempt including after exponential
backoff. Verification therefore ran on Crossref throughout. A search of Semantic Scholar with a working key
remains advisable before submission, since its index covers venues that Crossref bibliographic search ranks poorly.

Cluster composition, per-cluster targets and the section in which each cluster is cited are given in
`paper/LITERATURE_CLUSTERS.md` and `paper/LITERATURE_MAP.md`. Rendering instructions for the two journal styles
are in `paper/build.md`.

### Data availability

Sentinel-1 metadata via the Copernicus programme; International Arctic Buoy Programme Level 1 archive; EUMETSAT OSI SAF product OSI-405; Copernicus Marine datasets `cmems_obs-si_glo_phy-drift-north_my_l4_P1D-m` and `cmems_obs-si_arc_phy_my_l3_P1D`; European Space Agency acquisition-segment archives from the Copernicus SentiWiki document library; Norwegian Meteorological Institute ice-chart quicklook archive. Derived tables, figure-generating code, the full analysis pipeline and a per-number provenance trace are in the project repository at https://github.com/yjchoi83/Arctic (directories `arctic_explore/stage5`, `arctic_explore/paper` and `arctic_explore/results`). Gridded H products are held as GeoTIFF in `data/products` and are available on request.
