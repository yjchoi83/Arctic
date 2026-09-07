"""ARC-P13-5: render references.bib as an Elsevier Harvard author-year list and
resolve every in-text citation in MANUSCRIPT.md to a bib key.

No pandoc and no bibtexparser in this environment, so the bib is parsed and formatted here.
Author initials, volume, pagination and container titles come from Crossref where a DOI exists
(scratch/P13/crossref_meta.json); where it does not, the bibliography string is used verbatim
and nothing is invented.
"""
import json, re, pathlib, sys, unicodedata
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bib import parse_bib, clean_doi

HERE = pathlib.Path(__file__).parent
PAPER = pathlib.Path("/d/yj_projects/workspace_yj/Arctic/arctic_explore/paper")
META = json.loads((HERE / "crossref_meta.json").read_text())

INITIAL = re.compile(r"^(?:[A-Z]\.?-?)+\.?$")


def initials(given):
    """'Robert Anthony' -> 'R.A.'; 'S.-A.' -> 'S.-A.'; '' -> ''"""
    parts = [p for p in re.split(r"[\s.]+", given or "") if p]
    out = []
    for p in parts:
        if "-" in p:
            out.append("-".join(x[0].upper() + "." for x in p.split("-") if x))
        else:
            out.append(p[0].upper() + ".")
    return "".join(out)


def split_bib_name(tok):
    """Return (family, initials) from one bib author token, whichever order it is written in."""
    tok = tok.strip().rstrip(".,").strip()
    if not tok or tok.lower().startswith("et al"):
        return None
    words = tok.split()
    ini = [w for w in words if INITIAL.match(w)]
    rest = [w for w in words if not INITIAL.match(w)]
    if not rest:
        return None
    if not ini:
        # no initials given: 'Dierking', or 'Zhijie Wang' where the last word is the family name
        if len(rest) == 1:
            return (rest[0], "")
        return (rest[-1], "".join(w[0].upper() + "." for w in rest[:-1]))
    # initials before the surname -> 'D. R. Cox'; after -> 'Dabboor M.'
    if words.index(ini[0]) < words.index(rest[0]):
        return (" ".join(rest), "".join(i if i.endswith(".") else i + "." for i in ini))
    return (" ".join(rest), "".join(i if i.endswith(".") else i + "." for i in ini))


def authors_of(e):
    """[(family, initials)], plus a flag for a truncated list."""
    doi = clean_doi(e.get("doi"))
    m = META.get(doi, {})
    if m.get("authors"):
        return [(a["family"], initials(a["given"])) for a in m["authors"] if a["family"]], False
    raw = e.get("author", "")
    trunc = bool(re.search(r"et al", raw, re.I))
    raw = re.sub(r";?\s*et al\.?(\s*\(\d+ authors\))?", "", raw, flags=re.I)
    names = [split_bib_name(t) for t in re.split(r"\s+and\s+|;", raw)]
    return [n for n in names if n], trunc


def fmt_authors(lst, trunc):
    s = ", ".join(f"{f}, {i}" if i else f for f, i in lst)
    return s + (", et al." if trunc else "")


def sentence_case(s):
    """Elsevier Harvard uses sentence case for article titles; proper nouns and acronyms kept."""
    KEEP = {"Arctic", "Antarctic", "Sentinel", "Sentinel-1", "Sentinel-1A", "Sentinel-1B", "Sentinel-2",
            "Baltic", "SAR", "C-Band", "C-band", "L-band", "GMES", "Copernicus", "RADARSAT-2", "RADARSAT",
            "NSR", "POLARIS", "IMO", "Northern", "Sea", "Route", "Kaplan", "Meier", "European", "Russian",
            "Fram", "Svalbard", "Greenland", "Bering", "Chukchi", "Laptev", "Siberian", "Canadian",
            "AMSR-2", "AMSR2", "SMOS", "CryoSat-2", "MOSAiC", "GNSS-R", "TerraSAR-X", "ENVISAT",
            "Lagrangian", "Bayesian", "AutoICE", "Ice-FMBench", "GaoFen-3", "MSC.1/Circ.1519",
            "Extra", "Wide", "Interferometric", "Swath", "Vol.", "II", "Polar", "Code", "DTU", "EUMETSAT",
            "OSI", "SAF", "Danish", "Norwegian", "Alaska", "Finnish", "Hudson", "Beaufort", "Barents",
            "Kara", "NISAR", "InSAR", "Spearman", "Deep", "Learning"}
    words = s.split()
    out = []
    for k, w in enumerate(words):
        core = w.strip("()[],.:;\"'")
        if k == 0 or core in KEEP or (core.isupper() and len(core) > 1) or "-" in core and core.split("-")[0] in KEEP:
            out.append(w)
        elif core and core[0].isupper() and core.lower() not in KEEP:
            # leave acronym-like and hyphenated proper forms alone, otherwise lower-case
            out.append(w if any(c.isdigit() for c in core) or core.isupper() else w[0].lower() + w[1:])
        else:
            out.append(w)
    r = " ".join(out)
    return r


def render(e):
    doi = clean_doi(e.get("doi"))
    m = META.get(doi, {})
    lst, trunc = authors_of(e)
    a = fmt_authors(lst, trunc)
    yr = re.sub(r"\D.*$", "", e.get("year", "")) or e.get("year", "")
    # titles verbatim from the verified record: no heuristic sentence-casing, which mangled
    # acronyms and hyphenated compounds ("NOAA" -> "nOAA", "physics-Based"). Elsevier copy-edits case.
    title = e.get("title", "").rstrip(".")
    bits = [f"{a}, {yr}. {title}."]
    kind = e["kind"]
    if kind == "book":
        pub = re.sub(r"\s*\(book\)", "", e.get("publisher", ""))
        bits.append(f" {pub}.")
        if e.get("isbn"):
            bits.append(f" {e['isbn'].replace('ISBN ', 'ISBN ')}.")
    elif kind == "incollection":
        bits.append(f" In: {e.get('booktitle','')}. {e.get('publisher','')}, pp. {e.get('pages','').replace('--','–')}.")
    elif kind == "inproceedings":
        bits.append(f" In: {e.get('booktitle', m.get('container',''))}.")
        if m.get("page"):
            bits.append(f" pp. {m['page'].replace('-','–')}.")
    elif kind == "misc":
        hp = e.get("howpublished", "")
        hp = re.sub(r"\s*[—-]?\s*GREY LITERATURE.*$", "", hp).strip()
        if hp:
            bits.append(f" {hp}.")
        if e.get("eprint"):
            bits.append(f" arXiv:{e['eprint']}.")
    else:  # article
        cont = m.get("container") or e.get("journal", "")
        cont = cont.replace("&amp;", "&")
        seg = f" {cont}"
        if e.get("eprint") and "arXiv" in cont:
            seg = f" arXiv preprint arXiv:{e['eprint']}"
        else:
            if m.get("volume"):
                seg += f" {m['volume']}"
            if m.get("page"):
                seg += f", {m['page'].replace('-','–')}"
            elif m.get("article"):
                seg += f", {m['article']}"
        bits.append(seg + ".")
    if doi and "/" in doi:
        bits.append(f" https://doi.org/{doi}")
    elif e.get("url"):
        bits.append(f" {e['url']}")
    if e.get("howpublished", "").find("GREY LITERATURE") >= 0 or "no DOI" in e.get("howpublished", ""):
        bits.append("  [grey literature, no DOI]")
    return "".join(bits)


def sortkey(e):
    lst, _ = authors_of(e)
    fam = strip_accents(lst[0][0]).lower() if lst else ""
    m = re.search(r"(19|20)\d\d", e.get("year", ""))
    return (fam, m.group(0) if m else "0", e.get("title", "").lower())


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


# ---------------- in-text citation resolution ----------------
ALIAS = {"imo": "international maritime organization", "bellona": "bellona foundation"}


def index_entries(entries):
    idx = {}
    for e in entries:
        lst, _ = authors_of(e)
        if not lst:
            continue
        yr = (re.search(r"(19|20)\d\d", e.get("year", "")) or [None])
        yr = yr.group(0) if hasattr(yr, "group") else ""
        fam = strip_accents(lst[0][0]).lower().split()[-1]
        idx.setdefault((fam, yr), []).append(e["key"])
        if len(lst) >= 2:
            f2 = strip_accents(lst[1][0]).lower().split()[-1]
            idx.setdefault((fam, f2, yr), []).append(e["key"])
        full = strip_accents(lst[0][0]).lower()
        if full != fam:
            idx.setdefault((full, yr), []).append(e["key"])
    return idx


CIT_PROSE = re.compile(
    r"\b([A-Z][\w’'\-]+(?:\s+[A-Z][\w’'\-]+)?)"
    r"(?:\s+(?:et al\.|and\s+([A-Z][\w’'\-]+)))?\s*\((\d{4})[a-z]?\)")


def citations(text):
    """Yield (surname1, surname2_or_None, year, raw) for every author-year citation."""
    body = text.split("## References")[0]
    found = []
    for m in re.finditer(r"\(([^()]*?\b(?:19|20)\d\d[a-z]?[^()]*?)\)", body):
        inner = m.group(1)
        if not re.search(r"[A-Za-z]{3}", inner):
            continue
        for part in inner.split(";"):
            part = part.strip()
            mm = re.match(r"^(?:see also\s+|e\.g\.\s+)?([A-Z][\w’'\-]+(?:\s+[A-Z][\w’'\-]+)*?)"
                          r"(?:\s+et al\.|\s+and\s+([A-Z][\w’'\-]+))?,?\s+((?:19|20)\d\d)[a-z]?$", part)
            if mm:
                found.append((mm.group(1), mm.group(2), mm.group(3), part))
    for m in CIT_PROSE.finditer(body):
        found.append((m.group(1), m.group(2), m.group(3), m.group(0)))
    return found


if __name__ == "__main__":
    entries = parse_bib()
    idx = index_entries(entries)
    text = (PAPER / "MANUSCRIPT.md").read_text()
    cits = citations(text)
    used, unresolved, ambiguous = set(), [], []
    for s1, s2, yr, raw in cits:
        f1 = strip_accents(ALIAS.get(s1.lower(), s1)).lower().split()[-1]
        keys = None
        if s2:
            f2 = strip_accents(s2).lower().split()[-1]
            keys = idx.get((f1, f2, yr)) or idx.get((f1, yr))
        else:
            keys = idx.get((f1, yr)) or idx.get((strip_accents(ALIAS.get(s1.lower(), s1)).lower(), yr))
        if keys:
            used.update(keys)
            if len(set(keys)) > 1:
                ambiguous.append((raw, sorted(set(keys))))
        else:
            unresolved.append(raw)
    print(f"in-text citation instances found : {len(cits)}")
    print(f"distinct bib keys resolved       : {len(used)}")
    print(f"UNRESOLVED                       : {len(set(unresolved))}")
    seen=set()
    print(f"ambiguous (first author + year matches >1 entry): {len({a for a,_ in ambiguous})}")
    for raw,ks in ambiguous:
        if raw in seen: continue
        seen.add(raw); print("   ?", raw, "->", ks)
    for u in sorted(set(unresolved)):
        print("   !", u)
    unused = sorted({e["key"] for e in entries} - used)
    print(f"bib entries never cited in text  : {len(unused)}")
    for u in unused:
        print("   -", u)

    lines = [render(e) for e in sorted(entries, key=sortkey)]
    (HERE / "rendered_refs.txt").write_text("\n\n".join(lines) + "\n")
    print(f"\nrendered {len(lines)} references -> scratch/P13/rendered_refs.txt")
