#!/bin/bash
q="$1"; rows="${2:-6}"
url="https://api.crossref.org/works?rows=$rows&select=DOI,title,author,issued,container-title,type&query.bibliographic=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")"
h=$(printf '%s' "$url" | sha1sum | cut -d' ' -f1); f="scratch/s2cache/$h.json"
[ -s "$f" ] || curl -s --max-time 40 -H "User-Agent: BibCheck/1.0 (mailto:ldg810@koreatech.ac.kr)" "$url" -o "$f"
python3 - "$f" <<'PY'
import json,sys
try: d=json.load(open(sys.argv[1]))
except: print("PARSE_FAIL"); sys.exit()
for m in d.get("message",{}).get("items",[]):
    t=(m.get("title") or ["?"])[0]
    yr=(m.get("issued",{}).get("date-parts") or [[None]])[0][0]
    ven=(m.get("container-title") or ["?"])[0]
    au="; ".join((a.get("family","")) for a in (m.get("author") or [])[:4])
    print(f"  {yr} | {t[:110]} | {ven[:45]} | {m['DOI']} | {au}")
PY
