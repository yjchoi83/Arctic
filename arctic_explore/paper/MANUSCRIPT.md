<!-- ARC-P10 manuscript draft. Working title; final title to be decided after full draft review. -->

# Hazard-timescale observability of Arctic shipping chokepoints: two periods, two mechanisms in the Sentinel-1 record

**Target journal: Remote Sensing of Environment. Fallback: Cold Regions Science and Technology.**

## Abstract

Synthetic aperture radar underpins Arctic navigation support, yet observing capability is reported as scene counts or revisit intervals, neither of which says whether a hazard is caught. We define a hazard-timescale observability metric, H, as the probability that a randomly occurring convergence event overlaps at least one acquisition, given the length-biased distribution of acquisition gaps and an independently measured distribution of hazard durations. Hazard durations come from 82,439 convergence events derived from 2016–2025 International Arctic Buoy Programme pairs; acquisition gaps come from Sentinel-1 metadata for 1,771 cells of 25 km across sixteen Arctic regions, 2016–2026. At Northern Sea Route chokepoints, H for episode-scale hazards was 0.200 before the loss of Sentinel-1B and fell to 0.097 in 2022–2024. The 12 h episode requirement implied by the buoy record was met in none of 688 region-season-year cells, and no chokepoint ever reached the 24 h state requirement, so the requirement was already unmet before the constellation gap. A remove-one-platform experiment reproduces the 2022–2024 collapse to within 10 percentage points in fifteen of sixteen regions, so that period is explained by satellite count. The incomplete recovery is not: annual scene volume returned to 88.5 % with three platforms, yet European Space Agency acquisition plans allocate 86.4 % of pre-loss coverage to the European–Russian sector against 122.3 % to North America, and the deficit survives control for Sentinel-1C ramp-up. Availability of the Copernicus DTU Sentinel-1 drift product tracks H across region-years, with a Spearman correlation of 0.711. Twenty Sentinel-1 pairs show chokepoint convergence is retrievable in winter and freeze-up.

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

The counterfactual removes platforms rather than scenes. For each cell, season and year the acquisition series was rebuilt from the subset of passes belonging to a nominated combination of platforms, and H recomputed on the resulting gaps. Because 2022–2024 was a single-platform period, the pre-registered comparison is between the Sentinel-1A-only counterfactual constructed from 2019–2021 and the observed 2022–2024 values, region by region. Using the best-matching platform per region would be a post hoc selection and is reported only as a sensitivity. Design curves were formed by evaluating every platform combination available in each period, giving one-, two- and three-platform values.

### 3.5 Acquisition plan parsing

Planned segments were extracted from the Keyhole Markup Language archives by parsing each placemark for satellite identifier, datatake identifier, mode, observation start time and footprint ring. Because successive mission-plan files overlap in validity, segments were deduplicated on the triple of satellite, datatake identifier and observation start time. Footprint rings were projected to EPSG:3413 and a segment was credited to a region when it covered at least half the region box, the same rule applied to acquired scenes so that planned and acquired counts are commensurable. The ramp-up of new platforms was determined from the archive itself, by taking the first month in which a platform's monthly scene count reached 80 % of the median of its last six months.

## 4. Results

### 4.1 The requirement was never met at the chokepoints

Taking the buoy record at face value, an episode-scale hazard of at least 3 km lasts a median of 8–12 h depending on season and the resulting hazard state persists for a median of 24 h, which implies revisit requirements of 12 h and 24 h respectively if a large majority of hazards is to be bracketed. Neither was met. Across 688 region-season-year cells, of which 512 fall in the three main seasons, the fraction of season time covered by an acquisition pair separated by 12 h or less never reached 0.5, and its maximum over the whole record is 0.278. The 24 h criterion was reached in only four regions in any year, all of them large high-latitude boxes, and in none of the Northern Sea Route chokepoints in any year of the record.

The cell-level metric tells the same story in the currency of hazards rather than of time. Before the loss of Sentinel-1B, chokepoint H_episode for the 3 km class stood at 0.200 and H_state at 0.504 (Fig. 3). Four in five episode-scale convergence events at the chokepoints were therefore already going unseen in 2019–2021, a period with two satellites operating normally. This is the central negative result of the paper, and it is not a consequence of the constellation gap. *Caveat: the 12 h and 24 h requirements are derived from the buoy duration distribution rather than from an operator's stated need, so they express what would be needed to catch the measured hazards, not a service specification agreed with an ice service.*

### 4.2 The 2022–2024 gap widened an existing deficit

Between 2022 and 2024 chokepoint H_episode fell from 0.200 to 0.097 and H_state from 0.504 to 0.363; across all sixteen regions H_episode fell from 0.267 to 0.151 and H_state from 0.562 to 0.441 (Fig. 3, Table 3). At the chokepoints this means that roughly nine in ten episode-scale hazards went unobserved during the gap, against four in five before it.

An attempt to express this as a difference-in-differences between treated and untreated regions fails at the first step, and the failure is itself informative. Defining treatment as a retention ratio below 0.5, where retention is the 2022–2024 scene count divided by the 2019–2021 count, nine of sixteen regions are treated and seven are intermediate, but **no region has a retention of 0.9 or above**. The lowest is Sannikov at 0.310 and the highest Bering–Chukchi at 0.846. The loss was an Arctic-wide simultaneous shock and there is no untreated control, so the pre-registered contrast cannot be constructed. A post hoc dose-response comparison between the lost and intermediate groups gives −25.7 percentage points on H_state with a bootstrap interval of −49.9 to +0.6, which includes zero, and the two groups differ systematically in latitude and in baseline observability, so parallel trends is not plausible. *Caveat: no causal estimate of the gap's effect is available from a between-region design; the counterfactual of Section 4.4 is the appropriate instrument instead.*

### 4.3 Chokepoint hazards are real and Sentinel-1 can retrieve them

The low-resolution drift product cannot be used to establish whether chokepoint convergence occurs. On the 62.5 km OSI-405 grid, Vilkitsky Strait yields **no valid retrieval at all** across 76,075 point-days in ten years, being classified as land or coast throughout; Sannikov, Long Strait and Kara Gate yield a divergence value on 0.1 %, 0.3 % and 0.0 % of point-days respectively, and most of those valid values are flagged as interpolated rather than measured. Only the Bering–Chukchi approach, at 6.8 %, supports a time series. There the fraction of convergence days with a Sentinel-1 acquisition within 24 h was 0.422 in 2022, 0.177 in 2023 and 0.892 in 2024, so the pre-registered expectation that this fraction would remain below 0.25 in every year of the gap is rejected.

Direct processing of Sentinel-1 pairs reverses the apparent picture. Twenty pairs at Vilkitsky, Sannikov and Long Strait in freeze-up and winter of 2019–2021, matched with a feature-tracking and normalised cross-correlation scheme, produced at least thirty valid vectors in **all twenty cases**, with a mean success rate of 0.510, ranging from 0.377 to 0.419 in freeze-up and 0.484 to 0.779 in winter. Where the coarse product sees nothing, Sentinel-1 itself yields thousands of drift vectors in the same straits. The hazards are not unobservable; the low-resolution product simply cannot resolve them.

Expressing those fields in the buoy-pair metric closes the loop. Sampling 240,949 virtual buoy pairs at 20–100 km separation on the twenty fields, and applying the buoy rate threshold so that the selection matches as well as the measurement, 0.50 % of pairs qualify and their median closure is 5.88 km, with a ninetieth percentile of 6.94 km and a maximum of 10.63 km (Fig. 7). Strait convergence of the magnitude the buoy record describes is therefore present in the SAR fields, concentrated at Vilkitsky in winter where 1.86 % of virtual pairs qualify. *Caveat: the nineteen individual events detected by the connected-component procedure are unvalidated, since no buoy lay within 100 km of any of them; they are reported in Appendix A and no inference rests on them.*

### 4.4 The gap is explained by satellite count

Deleting Sentinel-1B from the 2019–2021 record and recomputing H_state reproduces the observed 2022–2024 values to within 10 percentage points in **fifteen of sixteen regions**, with most differences inside ±3 points: Fram +0.2, Barents +0.8, Vilkitsky −0.3, Long Strait −1.4 and Baffin −2.6 (Table 4). The single failure is Sannikov at +12.3 points, where the observed acquisition rate during the gap was lower than a single-platform constellation would predict. The collapse of 2022–2024 is thus almost entirely a platform-count phenomenon, and no appeal to changed tasking is needed to explain it.

The design curve shows why adding platforms does not resolve the chokepoint deficit (Fig. 4). Averaged over all regions, H_state is 0.431 with one platform, 0.563 with two and 0.527 with three in the post-loss configuration; at the chokepoints the corresponding values are 0.372, 0.505 and 0.459. Only 16 of 800 region-season-year-combination values reach 0.8, all of them in large high-latitude regions, and the chokepoint maximum over every combination observed is 0.718. The marginal gain falls from 0.13 for the second platform to 0.05 for the third. *Caveat: platform count is confounded with orbital plane in this design, and Sentinel-1C and Sentinel-1D were still ramping up, so the three-platform values do not represent a mature three-satellite constellation.*

### 4.5 The recovery shortfall is explained by allocation

By 2025–2026 the constellation is larger than before the loss, yet annual scene volume across the sixteen regions stands at 88.5 % of the 2019–2021 rate. The shortfall is not distributed evenly. Controlling for ramp-up by restricting to the window in which Sentinel-1A and Sentinel-1C were both in routine operation, from April 2025 to March 2026, the European–Russian sector sits at 77.4 % of its pre-loss rate while the North American and Bering sector sits at 121.1 %.

The acquisition plans show the same asymmetry before any acquisition takes place. Counting planned segments that cover at least half a region box, the European–Russian sector is planned at 86.4 % of its 2019–2021 rate against 122.3 % for North America, with Barents planned at 56 % (Fig. 5, Table 5). Because this appears in the plan rather than only in the outcome, the shortfall is an allocation decision and not a consequence of constellation size. The claim requires narrowing, however: within the same sector Vilkitsky is planned at 146 % and acquired at 156 %, and Long Strait at 113 %, so the deficit is specific to the Barents–Kara–Laptev sub-sector rather than to the European–Russian Arctic as a whole. *Caveat: acquisition-segment files describe planned datatakes and do not guarantee execution or downlink, and plans for 2022–2024 were not retrieved, so the comparison is pre versus post only.*

### 4.6 The shortfall propagated into an operational product

Availability of the DTU Sentinel-1 drift product, defined as the fraction of days on which at least 5 % of a region's pixels carry a valid vector, correlates with H_state across region-years at a Spearman coefficient of **0.711** (p = 1.7 × 10⁻¹⁸, n = 112), and with H_episode at 0.736 (Fig. 6). The relationship is not merely a cross-sectional contrast between well- and poorly-observed regions: computing the correlation along the time axis within each region separately gives a median of 0.727 across the sixteen regions. Product availability fell from 0.152 before the loss to 0.031 during it, a decline of 80 %, and stood at 0.033 in the partial 2025 sample. Varying the validity threshold to 2 % and 10 % gives correlations of 0.714 and 0.659, so the result is robust to that choice (Table 6).

*Caveat, which must accompany every statement of this result: the DTU product is itself derived from Sentinel-1. The correlation therefore relates two quantities computed from the same archive and is not independent confirmation. No Sentinel-1-independent product was reachable for this test: the OSI SAF SAR-based drift product does not exist, having been discontinued, and the Norwegian ice-chart archive is issued on a fixed schedule, with 248, 253, 251 and 250 issuance days in 2019, 2021, 2023 and 2025 respectively, unchanged through the gap.*

**Table 6.** Sensitivity of the product-consequence result to the validity threshold. Region-years, n = 112.

| Valid-pixel threshold | ρ with H_state | p | ρ with H_episode | Within-region median ρ | Mean availability |
|---|---|---|---|---|---|
| ≥ 2 % | 0.714 | 9.6 × 10⁻¹⁹ | 0.741 | 0.673 | 0.104 |
| ≥ 5 % | 0.711 | 1.7 × 10⁻¹⁸ | 0.736 | 0.727 | 0.083 |
| ≥ 10 % | 0.659 | 2.8 × 10⁻¹⁵ | 0.683 | 0.816 | 0.062 |

## 5. Discussion

### 5.1 Two periods, two mechanisms

The most consequential result of this work is that the two halves of the Sentinel-1 discontinuity have different explanations, and that treating them as one phenomenon produces a wrong diagnosis. For 2022–2024 the observing system experiment is decisive: removing a platform from the pre-loss record reproduces what was observed, region by region, to within a few percentage points almost everywhere. Nothing beyond the loss of a satellite needs to be invoked. For 2025–2026 the same reasoning fails, because the constellation is larger than it was in 2019–2021 and yet the pre-loss acquisition rate has not been restored in the Barents–Kara–Laptev sub-sector. The acquisition plans resolve the ambiguity: the shortfall is present in the plan, before execution, and in the opposite direction to the North American sector, which is planned and acquired above its pre-loss level.

This distinction matters for what can be recommended. A capability gap caused by platform loss is remedied by launching platforms, and the recovery of the global aggregate to 88.5 % shows that this remedy has largely worked. A capability gap caused by allocation is not remedied by launching platforms at all; it is a question of mission planning priorities, and it will persist through any number of future launches unless the plan changes. Conflating the two would lead an agency to procure hardware in response to a scheduling decision.

### 5.2 What a constellation cannot fix

Three separate arguments converge on the conclusion that the chokepoint deficit is not a procurement problem. The first is the design curve, on which the marginal contribution of a platform falls from 0.13 to 0.05 between the second and the third while the chokepoint value remains at 0.459 against a requirement of 0.8. The second is the magnitude structure of the hazard itself. Small convergence events are both more common and shorter: for the 1–3 km class the median episode duration is 2–4 h, and chokepoint H for that class during the gap is 0.029, meaning that 97 % of such events pass unobserved. Catching them would require a revisit of a few hours, which is three to six times more demanding than the 12 h figure quoted as the episode requirement, and that figure is itself the relaxed value appropriate to the ≥3 km class.

The third argument is that observation is not the only bottleneck. Multiplying H by the retrieval success rate measured on real image pairs gives an effective observability of roughly 0.18–0.28 in winter but only 0.006–0.009 in the melt season, because classical C-band feature tracking largely fails once the surface begins to melt. In that season no increase in acquisition frequency can raise the effective value above about 0.01, and the limiting factor is the retrieval algorithm and the radar band rather than the observing cadence. The freeze-up rate, previously unmeasured, was found here to be 0.392, so a working assumption of 0.47 taken from winter was about 19 % optimistic. A recent benchmark of deep-learning optical flow on RADARSAT-2 reports sub-kilometre accuracy and might change this picture, but it was evaluated only on March-to-May pack ice [V, arXiv:2510.26653], so it cannot be assumed to transfer to melt or freeze-up conditions.

### 5.3 Implications for measurement practice

The metric proposed here is cheap. It requires only acquisition metadata and an externally measured duration distribution, and its closed form makes evaluation over thousands of cells trivial. We would argue that reporting observing capability without reference to the timescale of the phenomenon being observed is no longer defensible when the alternative costs so little. The length-biasing of gaps is not a technicality: using a mean revisit interval in place of the gap distribution systematically flatters the result, because it hides the long gaps in which most hazard onsets actually fall.

Two methodological cautions emerged that generalise beyond this application. Event duration statistics derived from interval-sampled trajectories are left-censored at twice the sampling interval, and a median that coincides with that floor should be read as a property of the sampling rather than of the physics; only magnitude-stratified durations proved stable across sampling rates. And magnitudes measured on different baselines are not comparable without correction, a factor of four in our case, which was large enough to invert a conclusion about whether events of a given class were present at all.

## 6. Limitations

**6.1 Buoy-to-strait extrapolation.** The duration and persistence distributions that enter H are measured from International Arctic Buoy Programme pairs, and the buoy network is heavily biased towards the central Arctic: the central Arctic region supplied 55 % of all events, and the Laptev and East Siberian sector supplied 1,147 events in total, of which only 17 fall in winter, from eight pairs and fourteen buoys. Applying the pooled distribution to Vilkitsky, Sannikov and Long Strait is therefore extrapolation from where buoys drift to where ships transit. If strait convergence is systematically shorter than pack-ice convergence, which the confinement of a strait makes plausible, H as reported is too high and the deficit is worse than stated.

**6.2 Magnitude-class mismatch.** The SAR event metric and the buoy metric use different baselines, the square root of event area against the buoy separation, and differ by a factor of 0.248 in our data. Section 3.3 reconciles them with virtual buoy pairs, and after that correction the SAR fields do contain closures of the magnitude the buoy record describes. Two residuals remain. The two samples are selected differently, the buoy events being the extreme decile of a rate distribution and the virtual pairs an unconditional sample until the same threshold is applied; and the SAR windows of 24–48 h time-average the 2–12 h episodes of interest, so SAR-derived convergence rates are lower bounds on the instantaneous values. Comparisons of central tendency between the two are therefore not admissible without the threshold matching described in Section 3.3.

**6.3 Shared-archive dependence.** The product-consequence result of Section 4.6 relates the availability of the DTU drift product to H, but the DTU product is generated from Sentinel-1. The correlation is thus between two functions of one archive. The direction of causation is not in doubt, since acquisition precedes retrieval, but the result cannot be described as independent verification, and we do not claim that a Sentinel-1-independent dataset confirms the propagation. None was available: the OSI SAF SAR drift product has been discontinued, and the Norwegian ice-chart archive is issued on a fixed weekly schedule whose issuance count was unchanged through the gap, so it cannot register a propagation signal even in principle.

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

Adding satellites will not close the chokepoint gap. The marginal gain per platform falls to 0.05 by the third satellite while the chokepoint value remains at 0.459 against a requirement of 0.8; the smallest and most frequent convergence events last two to four hours; and in the melt season the binding constraint is not observation at all but the failure of classical C-band retrieval, which no acquisition cadence can repair.

## Appendix A. Candidate strait convergence events

Twenty Sentinel-1 pairs at Vilkitsky, Sannikov and Long Strait in freeze-up and winter 2019–2021 were processed with the matcher described in Section 3.4 of the companion methods, and connected regions of divergence below the tenth percentile of each pair's distribution, with area of at least 100 km², were extracted as candidate events. Nineteen were found, all in winter, thirteen at Sannikov and six at Vilkitsky, with a median area of 150 km² and a maximum of 700 km².

These events are **not validated**. No International Arctic Buoy Programme buoy lay within 100 km of any of the nineteen, even after relaxing the temporal bracket to ±12 h, so no in-situ comparison was possible. They are presented as a contact sheet in Fig. A1 for human adjudication, with the decision column of the accompanying table left blank, and no result in the main text depends on them. Their magnitudes, expressed on the buoy baseline as described in Section 3.3, place ten below 1 km, eight between 1 and 3 km and one at or above 5 km. The main-text evidence that strait convergence of navigable magnitude exists in the SAR fields rests instead on the virtual buoy-pair analysis of Section 4.3, which does not depend on the connected-component event definition.

## Tables referenced in Section 4

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

**Table 5.** Planned segments and acquired scenes per year, by sector. Planned counts are segments covering at least half a region box; acquired counts are passes meeting the same criterion. Ramp-up-controlled window is April 2025 to March 2026.

| Sector | Planned 2019–21 /yr | Planned 2025 | Planned ratio | Acquired, ramp-up controlled |
|---|---|---|---|---|
| European–Russian | 7,162 | 6,188 | **86.4 %** | **77.4 %** |
| North American–Bering | 8,521 | 10,417 | **122.3 %** | **121.1 %** |
| of which Barents / Svalbard | 1,710 | 961 | 56.0 % | 38.3 % |
| of which Vilkitsky | 495 | 721 | 146.0 % | 156.1 % |

## Figure captions

**Figure 1.** Construction of the observability metric H. (a) A sequence of acquisitions defines gaps g_i; a hazard of duration D is caught if it overlaps at least one acquisition. (b) H as a function of D for three single fixed gaps and for the length-biased mixture of the gaps in panel (a), showing that the mixture is controlled by the longest gaps at small D. `fig01_H_schematic.png`

**Figure 2.** Hazard timescales measured from buoy pairs, independent of Sentinel-1. (a) Cumulative distribution of convergence episode duration by magnitude class, from the one-hourly buoy subset; the dashed line marks the 12 h episode requirement. (b) Cumulative distribution of hazard-state persistence for events whose magnitude is at least 10 % of the pre-event separation; the dashed line marks the 24 h state requirement. `fig02_hazard_timescales.png`

**Figure 3.** H per 25 km cell on the EPSG:3413 grid, for the ≥ 3 km magnitude class, by season (rows) and period (columns). Northern Sea Route chokepoints are labelled. Colour runs from 0 to 1, where 1 means every hazard is caught. Two panels are provided, for H_state and for H_episode. `fig03_H_state3_maps.png`, `fig03_H_episode3_maps.png`

**Figure 4.** Constellation design curve. Mean H_state against number of platforms, for all regions and for the Northern Sea Route chokepoints, with error bars showing the standard deviation across region-season-year combinations. The dashed line marks the 0.8 requirement, which the chokepoints do not reach at any platform count observed. `fig04_design_curve.png`

**Figure 5.** European Space Agency planned acquisition segments against acquired scenes, per region, before and after the constellation gap, on a logarithmic axis. Regions are grouped by sector. `fig05_planned_vs_acquired.png`

**Figure 6.** Availability of the DTU Sentinel-1 drift product per region-year, defined as the fraction of days with at least 5 % valid pixels. Cyan lines mark the loss of Sentinel-1B and the entry of Sentinel-1C into routine operations. `fig06_dtu_availability.png`

**Figure 7.** Strait drift fields expressed in the buoy-pair metric. Exceedance of window closure for 240,949 virtual buoy pairs at 20–100 km separation, unconditionally and after applying the buoy rate threshold; dashed and dotted lines mark 3 km and 5 km. `fig07_virtual_pairs.png`

**Figure 8.** Four examples of strait convergence, two at Vilkitsky and two at Sannikov, showing before and after Extra Wide HH imagery with the divergence field overlaid. `fig08_strait_examples.png`

**Figure A1.** Contact sheet of the nineteen candidate strait convergence events, for human adjudication; the decision column of the accompanying table is left blank. `figA1_contact_sheet.png`

## References

Verified in this work by retrieval of the digital object identifier or arXiv identifier during the literature phase; entries marked [V] were confirmed, and remaining citations required by the argument are marked [CITATION NEEDED] pending an authenticated Semantic Scholar pass.

Korosov, A.A., Rampal, P., 2017. A combining approach to sea-ice drift retrieval from Sentinel-1 SAR. Remote Sensing 9, 258. https://doi.org/10.3390/rs9030258 [V]

Lavergne, T., et al., 2023. A low-resolution sea-ice drift climate data record. Earth System Science Data 15, 5807. https://doi.org/10.5194/essd-15-5807-2023 [V]

Kortum, K., et al., 2025. Sea-ice freeboard from HV-intensity CDF matching. The Cryosphere 19, 4701. https://doi.org/10.5194/tc-19-4701-2025 [V]

Deep-learning optical flow benchmark on RADARSAT-2 ScanSAR sea-ice imagery, 2025. arXiv:2510.26653 [V]

Community challenge for image-derived observation of sea-ice drift and deformation, 2026. https://doi.org/10.5194/egusphere-2026-4668 [V]

Wind-informed Bayesian classification of L-band SAR imagery for sea ice and open water separation, 2026. https://doi.org/10.5194/egusphere-2026-4775 [V]

Sea-ice classification and POLARIS-based risk-informed route analysis in the Bering Strait using Sentinel-1 SAR and SVM, 2026. Sustainability 18, 7414. https://doi.org/10.3390/su18147414 [V]

Assessment of thermal noise impact on sea-ice classification using Sentinel-1 images and U-Net, 2024. IET Conference Proceedings. https://doi.org/10.1049/icp.2024.1598 [V]

Incidence angle dependency and seasonal evolution of L- and C-band SAR backscatter over landfast sea ice, 2024. Annals of Glaciology. https://doi.org/10.1017/aog.2024.30 [V]

Arctic sea-ice leads detected using Sentinel-1B SAR imagery, 2024. Remote Sensing of Environment 305, 114193. https://doi.org/10.1016/j.rse.2024.114193 [V]

High-resolution sea-ice concentration from Sentinel-1, 2024. The Cryosphere 18, 5277. https://doi.org/10.5194/tc-18-5277-2024 [V]

Integrating regional ice charts and Copernicus sea-ice products for navigation risk in Alaskan waters, 2025. arXiv:2512.11083 [V]

Estimation of sea-ice drift and concentration during melt season using C-band dual-polarimetric Sentinel-1 data, 2024. Remote Sensing Applications: Society and Environment. https://doi.org/10.1016/j.rsase.2023.101104 [V metadata only; full text not retrieved]

Bahr, F., Mahoney, A.R., Eicken, H., 2024. Landfast sea-ice breakup dates for 38 Alaskan communities. Environmental Research Letters 19. https://doi.org/10.1088/1748-9326/ad1c7b [V]

International Hydrographic Review, 2025. Satellite-derived bathymetry and shoal detection at Canadian Arctic grounding sites. https://doi.org/10.58440/ihr-31-2-a13 [V]

Inter- and intra-analyst ice-edge assessment, 2023. figshare. https://doi.org/10.6084/m9.figshare.22312648 [V]

[CITATION NEEDED] — Sentinel-1 mission and Extra Wide swath instrument description.
[CITATION NEEDED] — Polar Code and POLARIS risk-index methodology.
[CITATION NEEDED] — prior treatments of satellite constellation observing system experiments in the cryosphere.
[CITATION NEEDED] — Northern Sea Route traffic statistics for the study period.
[CITATION NEEDED] — length-biased sampling of renewal intervals, standard reference.

### Data availability

Sentinel-1 metadata via the Copernicus programme; International Arctic Buoy Programme Level 1 archive; EUMETSAT OSI SAF product OSI-405; Copernicus Marine datasets `cmems_obs-si_glo_phy-drift-north_my_l4_P1D-m` and `cmems_obs-si_arc_phy_my_l3_P1D`; European Space Agency acquisition-segment archives from the Copernicus SentiWiki document library; Norwegian Meteorological Institute ice-chart quicklook archive. Derived tables and figure-generating code accompany this manuscript; gridded H products are available as GeoTIFF on request.
