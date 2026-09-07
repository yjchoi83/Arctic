"""ARC-P13-5: build paper/MANUSCRIPT_RSE.md = MANUSCRIPT.md with the References section
replaced by the rendered Elsevier Harvard author-year list. MANUSCRIPT.md stays the source.
Regenerate with:  python3 scratch/P13/make_rse.py
"""
import pathlib, sys, subprocess, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bib import parse_bib
from render_refs import render, sortkey, citations, index_entries, strip_accents, ALIAS
import re

PAPER = pathlib.Path("/d/yj_projects/workspace_yj/Arctic/arctic_explore/paper")
src = (PAPER / "MANUSCRIPT.md").read_text()

entries = sorted(parse_bib(), key=sortkey)
idx = index_entries(parse_bib())
cits = citations(src)
unres = []
for s1, s2, yr, raw in cits:
    f1 = strip_accents(ALIAS.get(s1.lower(), s1)).lower().split()[-1]
    k = (idx.get((f1, strip_accents(s2).lower().split()[-1], yr)) if s2 else None) or idx.get((f1, yr)) \
        or idx.get((strip_accents(ALIAS.get(s1.lower(), s1)).lower(), yr))
    if not k:
        unres.append(raw)
assert not unres, f"UNRESOLVED CITATIONS: {sorted(set(unres))}"


# Back matter in P15 order: Data availability is its own top-level section before References,
# and References carries only the rendered list. The verification memo now lives in SUPPLEMENTARY.md.
head, _, tail = src.partition("## Data availability")
dataavail, _, refnote = tail.partition("## References")

listing = "\n\n".join(render(e) for e in entries)
built = datetime.date.today().isoformat()
out = f"""<!-- GENERATED FILE. Source of record is paper/MANUSCRIPT.md; this copy differs from it
     only in carrying a rendered reference list in place of the References pointer.
     Rebuild: python3 scratch/P13/make_rse.py   (built {built}) -->

{head.rstrip()}

## Data availability

{dataavail.strip()}

## References

{listing}
"""
(PAPER / "MANUSCRIPT_RSE.md").write_text(out)
print(f"wrote paper/MANUSCRIPT_RSE.md - {len(entries)} references, "
      f"{len(cits)} in-text citation instances, 0 unresolved")
