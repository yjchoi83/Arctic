import json, re, pathlib, collections
d = json.load(open("/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/P12/novelty_raw.json"))
KEEP = re.compile(r"gap|outage|fail|missing|availab|revisit|observab|acquisition plan|tasking|"
                  r"coverage|sampling|Sentinel-1B|Sentinel-1C|adequa|requirement|detect", re.I)
for grp, rows in d.items():
    seen = {}
    for r in rows:
        k = (r["title"] or "").lower()
        if k not in seen: seen[k] = r
    print("="*110); print(grp, "-", len(rows), "hits,", len(seen), "unique")
    scored = []
    for r in seen.values():
        txt = (r["title"] or "") + " " + (r["abstract"] or "")
        hits = len(set(m.group(0).lower() for m in KEEP.finditer(txt)))
        scored.append((hits, r))
    for hits, r in sorted(scored, key=lambda x: -x[0])[:14]:
        print(f"  [{hits}] {r['year']} | {r['title']} | {r['venue']} | cites {r['cites']} | doi {r['doi']} | arXiv {r['arxiv']}")
        if hits >= 3 and r["abstract"]:
            print("       ", " ".join(r["abstract"].split())[:420])
