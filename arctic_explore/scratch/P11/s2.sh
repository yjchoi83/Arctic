#!/bin/bash
# semantic scholar search, unauth, cached
q="$1"
url="https://api.semanticscholar.org/graph/v1/paper/search?query=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")&limit=8&fields=title,year,venue,externalIds,authors"
h=$(printf '%s' "$url" | sha1sum | cut -d' ' -f1)
f="scratch/s2cache/$h.json"
if [ ! -s "$f" ]; then
  for d in 0 2 4 8; do
    [ $d -gt 0 ] && sleep $d
    code=$(curl -s --max-time 40 -w '%{http_code}' "$url" -o "$f.tmp")
    if [ "$code" = "200" ]; then mv "$f.tmp" "$f"; break; fi
    echo "HTTP $code for: $q" >&2
  done
  sleep 1
fi
[ -s "$f" ] || { echo "FAIL_S2|$q"; exit; }
python3 - "$f" "$q" <<'PY'
import json,sys
try: d=json.load(open(sys.argv[1]))
except: print("PARSE_FAIL"); sys.exit()
for p in d.get("data",[]):
    e=p.get("externalIds") or {}
    ids=e.get("DOI") or ("arXiv:"+e["ArXiv"] if e.get("ArXiv") else "-")
    au="; ".join(a["name"] for a in (p.get("authors") or [])[:5])
    print(f"  {p.get('year')} | {p.get('title')} | {p.get('venue')} | {ids} | {au}")
PY
