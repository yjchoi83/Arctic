# ARC-P12 item 9c — re-verification of all 76 references against Semantic Scholar

Authenticated Semantic Scholar (`x-api-key`, ≤ 1 req/s, exponential backoff to 90 s, 7 attempts).
Resolution order per entry: DOI → arXiv id → title search with a 0.72 similarity floor.
Script `scratch/P12/verify_refs.py`; raw result `scratch/P12/ref_verify.json`; run log `scratch/P12/verify.log`.

**Result: 63 OK, 10 flagged, 3 not found. One real defect, now fixed. Nothing in the bibliography is wrong.**

## The one real defect — fixed

| key | defect | action |
|---|---|---|
| `karvonen2022baltic` | bib title truncated: "…by Image Segmentation", Crossref and S2 both give "…by Image Segmentation **and Convolutional Neural Networks**" | title completed in `references.bib` |

## Six flagged year differences — all resolve in favour of the bibliography

Semantic Scholar stores the Copernicus *discussion-paper* year for The Cryosphere titles and the online-first
year for two others. Crossref `issued` was re-queried for each and agrees with the bib in every case.

| key | bib | S2 | Crossref `issued` | verdict |
|---|---|---|---|---|
| `lehtiranta2015comparing` | 2015 | 2014 | 2015-02-17 | bib correct |
| `bouillon2015producing` | 2015 | 2014 | 2015-04-09 | bib correct |
| `muckenhuber2017open` | 2017 | 2016 | 2017-08-07 | bib correct |
| `kaminski2018mission` | 2018 | 2017 | 2018-08-13 | bib correct |
| `bhattacharjee2024estimation` | 2024 | 2023 | 2024-01 | bib correct |
| `korosov2022thermal` | 2022 | 2021 | 2022 | bib correct |

`kaminski2018mission` also flagged two unmatched surnames ("Toudal", "Vo Beck"); these are S2 author-string
splits of Toudal Pedersen and Vo Beck, both present in the S2 record. No defect.

## Three flagged records that Semantic Scholar indexes badly — bibliography correct

| key | flag | verdict |
|---|---|---|
| `cox1962renewal` | title search matched an unrelated 2025 chapter titled "Renewal theory" | Cox's 1962 monograph is not in the S2 index; verified in an earlier package by OpenLibrary. No change. |
| `feller1971introduction` | S2 gives 1968 | S2 holds an earlier edition; the bib cites Vol. II 2nd edition, 1971, which is the edition whose length-biasing treatment is used. No change. |
| `kaplan1958nonparametric` | S2 DOI `10.1007/978-1-4612-4380-9_25` | that is the Springer *Breakthroughs in Statistics* reprint; the bib carries the original JASA DOI `10.1080/01621459.1958.10501452`. Bib is the better identifier. No change. |

## Three not found in Semantic Scholar

| key | reason |
|---|---|
| `imo2016polaris` | IMO MSC.1/Circ. — grey literature, no DOI, not indexed. Already marked as such and live-URL checked. |
| `bellona2025nsr` | Bellona report — grey literature, no DOI, not indexed. Same. |
| `opticalflow2025benchmark` | **resolved during this package.** The run used the pre-fix bibliography. The stub is now `martin2025opticalflow`, resolved through S2 by `arXiv:2510.26653` to Martin, D. and Gallego, J., *Towards Reliable Sea Ice Drift Estimation in the Arctic: Deep Learning Optical Flow on RADARSAT-2*, DOI `10.48550/arXiv.2510.26653`. |
