"""ARC-P13-5: parse references.bib and enrich each DOI-bearing entry from Crossref
(full author names, volume, pages, container title). Cached to crossref_meta.json."""
import json, re, pathlib, time, urllib.request, urllib.error

HERE = pathlib.Path("/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/P13")
BIB = pathlib.Path("/d/yj_projects/workspace_yj/Arctic/arctic_explore/paper/references.bib")
CACHE = HERE / "crossref_meta.json"
UA = "arctic-p13/1.0 (mailto:ldg810@koreatech.ac.kr)"


def parse_bib():
    raw = BIB.read_text()
    out = []
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", raw, re.S):
        kind, key, body = m.group(1), m.group(2).strip(), m.group(3)
        f = dict(re.findall(r"(\w+)\s*=\s*\{(.*?)\}(?=,\s*\n|\s*\n\s*\w+\s*=|\s*$)", body, re.S))
        f = {k: " ".join(v.split()) for k, v in f.items()}
        out.append({"kind": kind, "key": key, **f})
    return out


def clean_doi(d):
    d = (d or "").split(" ")[0].strip()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", d)


def fetch(entries):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    for e in entries:
        doi = clean_doi(e.get("doi"))
        if not doi or "/" not in doi or doi.startswith("10.48550") or doi in cache:
            continue
        try:
            req = urllib.request.Request(f"https://api.crossref.org/works/{doi}", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                m = json.load(r)["message"]
            cache[doi] = {
                "authors": [{"family": a.get("family", ""), "given": a.get("given", "")}
                            for a in m.get("author", [])],
                "container": (m.get("container-title") or [""])[0],
                "volume": m.get("volume") or "", "issue": m.get("issue") or "",
                "page": m.get("page") or "", "article": m.get("article-number") or "",
                "publisher": m.get("publisher") or "", "type": m.get("type") or "",
                "issued": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                "title": (m.get("title") or [""])[0],
            }
            print("ok  ", doi, flush=True)
        except Exception as ex:  # noqa: BLE001
            print("FAIL", doi, repr(ex)[:90], flush=True)
            cache[doi] = {"_error": repr(ex)[:200]}
        time.sleep(0.6)
    CACHE.write_text(json.dumps(cache, indent=1))
    return cache


if __name__ == "__main__":
    es = parse_bib()
    print(len(es), "bib entries")
    c = fetch(es)
    ok = sum(1 for v in c.values() if "_error" not in v)
    print(f"crossref metadata: {ok} ok, {len(c)-ok} failed, of {len(c)} DOIs")
