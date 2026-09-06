import asf_search as asf, collections, sys
ROIS = {
 "Beaufort_Chukchi": "POLYGON((-170 68,-130 68,-130 76,-170 76,-170 68))",
 "Kara_Laptev": "POLYGON((60 72,130 72,130 80,60 80,60 72))",
 "Barents": "POLYGON((20 72,60 72,60 80,20 80,20 72))",
}
for name, wkt in ROIS.items():
    try:
        r = asf.search(platform=[asf.PLATFORM.NISAR], start="2026-06-17", end="2026-09-30",
                       intersectsWith=wkt, maxResults=500)
    except Exception as e:
        print(name, "ERR", type(e).__name__, str(e)[:200]); continue
    print("===", name, "n=", len(r))
    pt = collections.Counter(); pol = collections.Counter(); beam = collections.Counter()
    lats = []
    for g in r:
        p = g.properties
        pt[p.get("processingLevel")] += 1
        pol[str(p.get("polarization"))] += 1
        beam[str(p.get("beamModeType"))] += 1
        try:
            cs = g.geometry["coordinates"][0]
            lats += [c[1] for c in cs]
        except Exception: pass
    print(" ptype:", dict(pt)); print(" pol:", dict(pol)); print(" beam:", dict(beam))
    if lats: print(" lat range: %.1f .. %.1f" % (min(lats), max(lats)))
    for g in r[:2]:
        print("  ex:", g.properties.get("fileID"), g.properties.get("startTime"))
