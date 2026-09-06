import asf_search as asf, collections, re
from datetime import datetime
# marine-only ROIs (offshore, no land)
ROIS = {
 "Chukchi_marine": "POLYGON((-172 70,-160 70,-160 74,-172 74,-172 70))",
 "Laptev_marine": "POLYGON((110 74,140 74,140 79,110 79,110 74))",
 "Barents_marine": "POLYGON((30 76,50 76,50 80,30 80,30 76))",
}
def pol_of(fid):
    m = re.search(r"_(SHSV|DHDH|SH|DH|QQ|NASV|SV|HH|DV)_", fid or "")
    return m.group(1) if m else "?"
for name, wkt in ROIS.items():
    n = asf.search(platform=[asf.PLATFORM.NISAR], start="2026-06-17", end="2026-09-30",
                   processingLevel=["GCOV"], intersectsWith=wkt, maxResults=2000)
    s1 = asf.search(platform=[asf.PLATFORM.SENTINEL1], start="2026-06-17", end="2026-09-30",
                    beamMode=["EW"], processingLevel=["GRD_MD"], intersectsWith=wkt, maxResults=4000)
    print("===", name, "NISAR_GCOV=", len(n), "S1_EW_GRDMD=", len(s1))
    print("  pol:", dict(collections.Counter(pol_of(g.properties.get("fileID")) for g in n)))
    def t(g): return datetime.strptime(g.properties["startTime"][:19], "%Y-%m-%dT%H:%M:%S")
    nt = sorted(t(g) for g in n); st = sorted(t(g) for g in s1)
    for h in (3, 6, 12, 24):
        c = sum(1 for a in nt if any(abs((a-b).total_seconds()) <= h*3600 for b in st))
        print(f"  NISAR frames with S1 EW within {h}h: {c}/{len(nt)}")
    if nt: print("  NISAR date span:", nt[0].date(), "->", nt[-1].date(), " uniq days:", len(set(x.date() for x in nt)))
