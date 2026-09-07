#!/bin/bash
# crossref DOI lookup -> compact line
doi="$1"
h=$(printf '%s' "https://api.crossref.org/works/$doi" | sha1sum | cut -d' ' -f1)
f="scratch/s2cache/$h.json"
if [ ! -s "$f" ]; then
  curl -s --max-time 30 -H "User-Agent: BibCheck/1.0 (mailto:ldg810@koreatech.ac.kr)" "https://api.crossref.org/works/$doi" -o "$f"
fi
python3 - "$f" "$doi" <<'PY'
import json,sys
try:
    d=json.load(open(sys.argv[1]))
except Exception as e:
    print("PARSE_FAIL",sys.argv[2]); sys.exit()
if d.get("status")!="ok":
    print("NOTFOUND",sys.argv[2]); sys.exit()
m=d["message"]
t=(m.get("title") or ["?"])[0]
au=m.get("author") or []
auth="; ".join((a.get("family","")+" "+a.get("given","")).strip() for a in au[:12])
yr=(m.get("issued",{}).get("date-parts") or [[None]])[0][0]
ven=(m.get("container-title") or ["?"])[0]
print(f"OK|{sys.argv[2]}|{yr}|{t}|{ven}|{auth}|{m.get('type')}")
PY
