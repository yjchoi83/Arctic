<!-- ARC-P10 manuscript draft. Working title; final title to be decided after full draft review. -->

# Hazard-timescale observability of Arctic shipping chokepoints: two periods, two mechanisms in the Sentinel-1 record

**Target journal: Remote Sensing of Environment. Fallback: Cold Regions Science and Technology.**

## Abstract

Synthetic aperture radar underpins Arctic navigation support, yet observing capability is normally reported as scene counts or revisit intervals, neither of which says whether a hazard is actually caught. We define a hazard-timescale observability metric, H, as the probability that a randomly occurring convergence event overlaps at least one acquisition, given the length-biased distribution of acquisition gaps and an independently measured distribution of hazard durations. Hazard durations come from 82,439 convergence events derived from 2016–2025 International Arctic Buoy Programme pairs; acquisition gaps come from Sentinel-1 metadata for 1,771 cells of 25 km across sixteen Arctic regions, 2016–2026. At Northern Sea Route chokepoints, H for episode-scale hazards was 0.200 before the loss of Sentinel-1B and fell to 0.097 in 2022–2024. The 12 h episode requirement implied by the buoy record was met in none of 688 region-season-year cells, and no chokepoint ever reached the 24 h state requirement, so the requirement was already unmet before the constellation gap. A remove-one-platform experiment reproduces the observed 2022–2024 collapse to within 10 percentage points in fifteen of sixteen regions, so that period is explained by satellite count. The incomplete recovery is not: annual scene volume returned to 88.5 % with three platforms, yet European Space Agency acquisition plans allocate 86.4 % of pre-loss coverage to the European–Russian sector against 122.3 % to North America, and the deficit survives control for Sentinel-1C ramp-up. Availability of the Copernicus DTU Sentinel-1 drift product tracks H across region-years, with a Spearman correlation of 0.711. Twenty Sentinel-1 pairs show that chokepoint convergence is retrievable in winter and freeze-up.

**Keywords:** Sentinel-1; sea-ice drift; Arctic shipping; observing system experiment; Northern Sea Route; observability

## 1. Introduction

The Northern Sea Route and the approaches to it are navigated on the basis of information that is, in the great majority of cases, derived from spaceborne synthetic aperture radar (SAR). Ice charts, drift products and route-level risk indices all take SAR as their primary input, and the Sentinel-1 constellation has been the dominant free source of that input since 2014. It follows that the capability of the Sentinel-1 constellation over the Arctic is not merely a technical property of a satellite system but a determinant of what ship masters, ice services and routing providers are able to know.

That capability is almost always reported in one of two currencies. The first is a count: how many scenes were acquired over a region in a season or a year. The second is an interval: the median or the ninetieth-percentile time between successive acquisitions. Both are natural and both are easy to compute from metadata alone, and both share a defect that becomes decisive once the question is operational rather than descriptive. Neither tells us whether the phenomenon of interest was caught. A region can be observed frequently in the aggregate and still miss every hazard, if the hazards are short relative to the gaps between acquisitions; conversely a region observed rarely can catch a large fraction of hazards if those hazards persist for days. The quantity that matters to a decision maker is the probability that a hazard, occurring at an arbitrary moment, is seen at least once while it exists. That quantity depends jointly on the acquisition pattern and on the duration distribution of the hazard, and it cannot be recovered from either alone.

This paper constructs that quantity, which we call H, and applies it to the Arctic marine domain over the period 2016–2026. The construction has three requirements. It needs an acquisition record at a spatial resolution comparable to the features being navigated, which for a strait 20–50 km wide means cells substantially smaller than a SAR scene. It needs a distribution of hazard durations that is measured rather than assumed, and measured independently of SAR so that the metric does not become circular. And it needs an explicit statement of what "caught" means, because a single acquisition inside a hazard window is sufficient to see the hazard but insufficient to retrieve ice motion, which requires a pair.

The period covered contains a natural discontinuity. Sentinel-1B failed in December 2021 and the constellation operated with a single Arctic-capable platform through 2022–2024 before Sentinel-1C entered routine operations in April 2025 and Sentinel-1D began contributing in April 2026. This sequence has been treated informally as a natural experiment on observing capability. We show that it is a natural experiment only in part, and that treating it as one uniformly leads to a mistaken diagnosis. The collapse of 2022–2024 is explained almost entirely by the reduction in platform count, in the sense that a counterfactual constructed by deleting one platform from the 2019–2021 record reproduces the observed 2022–2024 values closely. The incomplete recovery of 2025–2026 is not explained by platform count, because the constellation is now larger than it was before the loss. It is explained instead by where the acquisitions are planned, and we demonstrate this using the acquisition-segment plans published by the European Space Agency rather than inferring it from the acquired record alone. Two periods, two mechanisms.

A third result cuts across both. Because the requirement implied by the measured hazard durations was never met at the chokepoints even in the pre-loss period, the constellation gap did not create the observability deficit at the locations that matter most for navigation; it widened one that already existed. We show that adding platforms does not close it either, because the marginal gain per platform falls from 0.13 to 0.05 between the second and third satellite while the chokepoint requirement remains a factor of two away.

The paper is organised as follows. Section 2 describes the data. Section 3 derives H and the ancillary methods: the buoy-based event definitions, the reconciliation between the buoy and SAR magnitude scales, the observing system experiment, and the parsing of acquisition plans. Section 4 presents six results, one per subsection, each with its figure or table and the caveat that qualifies it. Section 5 discusses what a constellation can and cannot fix. Section 6 states the limitations in full, and Section 7 concludes.

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

Consider a cell, a season and a year, and let the qualifying acquisitions in that window occur at times t₁ < t₂ < … < tₙ, defining gaps gᵢ = tᵢ₊₁ − tᵢ. Let a hazard occur with duration D, and assume that its onset time is uniformly distributed over the season. Under that assumption the onset falls inside gap i with probability proportional to gᵢ rather than uniformly across gaps, because long gaps present more opportunity for an onset to land in them; this is the standard length-biasing of interval sampling and it is the reason the metric cannot be built from a mean revisit interval. Given an onset inside a gap of length g, the hazard overlaps at least one acquisition with probability min(1, D/g), since the hazard is seen unless it both begins and ends strictly inside the gap.

Combining these gives the probability that a randomly occurring hazard of duration D is caught,

  H(D) = Σᵢ gᵢ · min(1, D/gᵢ) / Σᵢ gᵢ = Σᵢ min(gᵢ, D) / Σᵢ gᵢ,

where the second equality follows from g·min(1, D/g) = min(g, D) and is what makes the metric cheap to evaluate. Averaging over the empirical duration distribution yields

  H = E_D [ Σᵢ min(gᵢ, D) ] / Σᵢ gᵢ.

We evaluate this exactly by sorting the gaps, forming their cumulative sum and using a binary search over the duration sample, which agrees with a direct evaluation of the defining expression to within 10⁻¹². Figure 1 illustrates the construction: panel (a) shows an acquisition sequence with a hazard of duration D, and panel (b) shows H as a function of D for single fixed gaps and for the length-biased mixture, making clear that the mixture is dominated by the longest gaps at small D.

Two distinct hazard quantities are used. H_episode uses the duration of a convergence episode, the interval over which the closure rate exceeds a threshold. H_state uses the persistence of the resulting hazard state, the time until the geometry relaxes back towards its pre-event configuration. The two answer different operational questions, the first being whether the event itself is witnessed and the second whether a ship approaching afterwards can still be warned.

Four assumptions are made explicit because each has a direction of failure. First, hazard occurrence and acquisition planning are assumed independent; the Sentinel-1 background mission follows a fixed plan, so this is largely defensible, but any seasonal replanning correlated with ice conditions would bias H upward. Second, the duration distributions are transferred from the buoy network to the chokepoints, which is extrapolation and is treated as a limitation in Section 6. Third, a single acquisition inside the hazard window is counted as an observation, whereas drift retrieval requires a pair, so H is an upper bound on the probability of an actionable retrieval; Section 5 multiplies H by a measured retrieval success rate to obtain an effective value. Fourth, gaps are truncated at season boundaries and no credit is given before the first or after the last acquisition of a season.

Cell-level values are aggregated to region, season and year by unweighted averaging over cells, and uncertainty is expressed by a block bootstrap over cells with 1,000 draws. We report those intervals but do not interpret them as sampling uncertainty, because cells within a region share satellite orbits and are therefore far from independent; the intervals are consequently much narrower than the true uncertainty.

### 3.2 Buoy convergence events

Hazard timescales were measured from buoy pairs rather than from SAR, so that the duration distribution entering H is independent of the acquisition record whose adequacy is being judged. All buoy pairs separated by 20–100 km with overlapping records were formed, giving 9,884 pairs, and the separation time series s(t) computed for each contiguous run of at least eight three-hourly epochs within the separation band. The convergence rate is r(t) = [s(t+Δ) − s(t)]/Δ. A single threshold was fixed once, before any event was counted, as the ninetieth percentile of the magnitude of all negative rates pooled across every pair and epoch, giving 2.954 km d⁻¹ at three-hourly sampling and 4.706 km d⁻¹ at one-hourly sampling. An event is a maximal run of consecutive intervals with r below the negative of that threshold, lasting at least two intervals. Event magnitude is the total separation decrease, and event duration is the run length.

Two properties of this definition matter downstream. It is left-censored at twice the sampling interval, so at three-hourly sampling 55.9 % of events have the minimum possible duration of six hours and the median duration is a detection floor rather than a central tendency. Re-running on the one-hourly subset moves the median from 6 h to 2 h and places 85.8 % of events below the six-hour floor of the coarser sampling, confirming that the coarse median is an artefact. Magnitude filtering stabilises it: for events of at least 3 km the median duration is 9 h at one-hourly sampling against 12 h at three-hourly, and for at least 5 km it is 12 h against 18 h. All durations entering H are therefore taken from the one-hourly subset and stratified by magnitude class and season, as summarised in Table 2.

Hazard-state persistence was defined as the time from event end until the separation recovers to 90 % of its pre-event value, with runs that end before recovery treated as right-censored and handled by a Kaplan–Meier estimator. This measurand is undefined for events whose magnitude is less than a tenth of the pre-event separation, because such events never drop below the recovery threshold; that describes 84.6 % of all events, so persistence statistics are reported only for the remaining 15.4 %.

**Table 2.** Hazard timescales by magnitude class, from the one-hourly buoy subset (episode) and the three-hourly archive with relative magnitude of at least 10 % (persistence). Median hours.

| Class | Episode, winter | Episode, melt | Episode, freeze-up | Persistence, winter | Persistence, melt | Persistence, freeze-up |
|---|---|---|---|---|---|---|
| 1–3 km | 2 | 4 | 4 | — | — | — |
| ≥ 3 km | 12 | 8 | 9 | 24 | — | — |
| ≥ 5 km | 14 | 11 | 15 | 33 | 9 | 30 |
| all, relmag ≥ 10 % | — | — | — | 27 | 12 | 39 |

### 3.3 Reconciling the buoy and SAR magnitude scales

Convergence measured from a SAR drift field and convergence measured between two buoys are not the same number even when they describe the same deformation, because they use different baselines. A SAR event defined as a connected region of divergence below a threshold has a natural length scale equal to the square root of its area, whereas a buoy pair has the baseline of its separation. For a given strain the two magnitudes are therefore related by the ratio of those baselines, and in our data the median square root of event area is 12.2 km against a median buoy separation of 49.4 km, a factor of 0.248. Comparing the two directly without correction understates SAR magnitudes fourfold.

To place both on a common footing, virtual buoy pairs were constructed on the SAR drift fields. Node pairs separated by 20–100 km, the same band used for the real buoys, were sampled from each field, and the change in their separation over the acquisition interval was computed from the retrieved displacements. This yields, for each SAR window, a distribution of closures directly comparable with the buoy event magnitudes, and it permits the buoy rate threshold to be applied to SAR-derived pairs so that the two samples are selected in the same way as well as measured in the same way.

### 3.4 Observing system experiment

The counterfactual removes platforms rather than scenes. For each cell, season and year the acquisition series was rebuilt from the subset of passes belonging to a nominated combination of platforms, and H recomputed on the resulting gaps. Because 2022–2024 was a single-platform period, the pre-registered comparison is between the Sentinel-1A-only counterfactual constructed from 2019–2021 and the observed 2022–2024 values, region by region. Using the best-matching platform per region would be a post hoc selection and is reported only as a sensitivity. Design curves were formed by evaluating every platform combination available in each period, giving one-, two- and three-platform values.

### 3.5 Acquisition plan parsing

Planned segments were extracted from the Keyhole Markup Language archives by parsing each placemark for satellite identifier, datatake identifier, mode, observation start time and footprint ring. Because successive mission-plan files overlap in validity, segments were deduplicated on the triple of satellite, datatake identifier and observation start time. Footprint rings were projected to EPSG:3413 and a segment was credited to a region when it covered at least half the region box, the same rule applied to acquired scenes so that planned and acquired counts are commensurable. The ramp-up of new platforms was determined from the archive itself, by taking the first month in which a platform's monthly scene count reached 80 % of the median of its last six months.
