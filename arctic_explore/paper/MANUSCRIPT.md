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
