"""P12 item 9c: re-verify all 76 references.bib entries against Semantic Scholar (DOI first, title fallback)."""
import json, re, difflib, pathlib, sys
import s2

BIB = pathlib.Path("/d/yj_projects/workspace_yj/Arctic/arctic_explore/paper/references.bib")
raw = BIB.read_text()
entries = []
for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", raw, re.S):
    kind, key, body = m.group(1), m.group(2).strip(), m.group(3)
    f = dict(re.findall(r"(\w+)\s*=\s*\{(.*?)\}(?=,\s*\n|\s*\n\s*\w+\s*=|\s*$)", body, re.S))
    f = {k: " ".join(v.split()) for k, v in f.items()}
    entries.append({"kind": kind, "key": key, **f})
print(f"parsed {len(entries)} entries", file=sys.stderr)


def norm(s):
    s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
    return " ".join(s.split())


def surnames(a):
    out = []
    for part in re.split(r"\s+and\s+|;", a or ""):
        part = part.strip().strip(".")
        if not part or "et al" in part.lower() or part.startswith("("):
            continue
        toks = [t for t in re.split(r"[ ,]+", part) if t]
        cand = [t for t in toks if len(t) > 2 and not t.isupper()]
        if cand:
            out.append(norm(cand[-1] if len(toks[-1]) > 2 else cand[0]))
    return [x for x in out if x]


rows = []
for e in entries:
    doi = (e.get("doi") or "").split(" ")[0].strip()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    rec, how = None, None
    if doi and "/" in doi:
        r = s2.get(f"/paper/DOI:{doi}", fields="title,year,venue,authors,externalIds")
        if "_error" not in r and r.get("title"):
            rec, how = r, "doi"
    if rec is None and e.get("eprint"):
        r = s2.get(f"/paper/arXiv:{e['eprint']}", fields="title,year,venue,authors,externalIds")
        if "_error" not in r and r.get("title"):
            rec, how = r, "arxiv"
    if rec is None:
        r = s2.search(e.get("title", ""), limit=5, fields="title,year,venue,authors,externalIds")
        best, bs = None, 0.0
        for c in (r.get("data") or []):
            sc = difflib.SequenceMatcher(None, norm(e.get("title")), norm(c.get("title"))).ratio()
            if sc > bs:
                best, bs = c, sc
        if best and bs >= 0.72:
            rec, how = best, f"title({bs:.2f})"
    row = {"key": e["key"], "bib_title": e.get("title", ""), "bib_year": e.get("year", ""),
           "bib_authors": e.get("author", ""), "doi": doi, "found_via": how}
    if rec is None:
        row.update(status="NOT_FOUND", notes="no S2 record via DOI/arXiv/title")
    else:
        ts = difflib.SequenceMatcher(None, norm(e.get("title")), norm(rec.get("title"))).ratio()
        yb, yf = str(e.get("year", "")).strip(), str(rec.get("year") or "")
        bs_, fs = set(surnames(e.get("author"))), {norm((a.get("name") or "").split()[-1]) for a in (rec.get("authors") or [])}
        amiss = sorted(bs_ - fs)
        probs = []
        if ts < 0.90:
            probs.append(f"title {ts:.2f}: S2='{rec.get('title')}'")
        if yb and yf and yb != yf:
            probs.append(f"year bib={yb} S2={yf}")
        if bs_ and amiss and len(amiss) > max(0, len(bs_) // 3):
            probs.append("authors not matched: " + ",".join(amiss))
        rdoi = (rec.get("externalIds") or {}).get("DOI", "")
        if doi and rdoi and doi.lower() != rdoi.lower():
            probs.append(f"doi bib={doi} S2={rdoi}")
        row.update(status="MISMATCH" if probs else "OK", s2_title=rec.get("title"),
                   s2_year=yf, s2_venue=rec.get("venue"), notes="; ".join(probs))
    rows.append(row)
    print(f"{row['status']:10s} {row['key']:28s} via={how} {row.get('notes','')[:110]}", flush=True)

out = pathlib.Path("/d/yj_projects/workspace_yj/Arctic/arctic_explore/scratch/P12/ref_verify.json")
out.write_text(json.dumps(rows, indent=1))
n = {}
for r in rows:
    n[r["status"]] = n.get(r["status"], 0) + 1
print("\nSUMMARY", n)
