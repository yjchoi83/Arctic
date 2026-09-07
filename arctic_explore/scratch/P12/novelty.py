"""P12 item 9a/9b: Semantic Scholar novelty and cluster-8 searches."""
import json, pathlib, sys
import s2

QUERIES = {
 "A1_observability_metric": [
   "observability metric probability hazard observed satellite revisit",
   "hazard timescale matched satellite revisit interval adequacy",
   "length-biased sampling gap distribution satellite observation probability detection",
   "probability of detecting transient event given satellite revisit gaps",
   "observing system requirement sea ice deformation revisit timescale",
   "SAR coverage adequacy metric Arctic shipping route",
 ],
 "A2_s1b_gap": [
   "Sentinel-1B failure impact sea ice monitoring coverage",
   "Sentinel-1B loss consequences data availability Arctic",
   "Sentinel-1 constellation gap 2022 coverage reduction",
   "impact of satellite failure on operational sea ice products",
   "Sentinel-1C ramp up Arctic coverage recovery",
 ],
 "A3_plan_allocation": [
   "Sentinel-1 acquisition plan allocation Arctic priority",
   "mission planning acquisition segments Sentinel-1 observation scenario",
   "SAR tasking allocation regional bias satellite acquisition plan",
   "planned versus acquired SAR scenes archive analysis",
 ],
 "B_cluster8_gaps": [
   "quantifying observation gaps propagation sea ice product uncertainty",
   "missing SAR imagery effect on ice chart availability",
   "data gap quantification satellite time series sea ice product",
   "observation gap effect operational sea ice drift product availability",
   "temporal sampling gaps error sea ice drift retrieval",
   "coverage gaps impact on sea ice deformation product",
 ],
}

out = {}
for grp, qs in QUERIES.items():
    out[grp] = []
    for q in qs:
        r = s2.search(q, limit=20)
        data = r.get("data") or []
        print(f"[{grp}] {q!r} -> {len(data)} (total {r.get('total')}, err {r.get('_error','')})", flush=True)
        for d in data:
            out[grp].append({"q": q, "title": d.get("title"), "year": d.get("year"),
                             "venue": d.get("venue"), "cites": d.get("citationCount"),
                             "doi": (d.get("externalIds") or {}).get("DOI"),
                             "arxiv": (d.get("externalIds") or {}).get("ArXiv"),
                             "abstract": (d.get("abstract") or "")[:900]})
p = pathlib.Path("/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/P12/novelty_raw.json")
p.write_text(json.dumps(out, indent=1))
print("\nunique titles per group:")
for g, v in out.items():
    print(g, len({x["title"] for x in v}))
