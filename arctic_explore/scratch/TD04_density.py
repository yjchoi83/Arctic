import json, urllib.request, numpy as np, h5py, os
B = (95.0, 76.0, 120.0, 80.0)
u = ("https://cmr.earthdata.nasa.gov/search/granules.json?short_name=ATL10&version=007"
     f"&temporal=2023-11-01T00:00:00Z,2023-11-03T00:00:00Z&bounding_box={B[0]},{B[1]},{B[2]},{B[3]}&page_size=3")
e = json.load(urllib.request.urlopen(u, timeout=120))['feed']['entry']
f = "/tmp/TD04_atl10.h5"
if not os.path.exists(f):
    urllib.request.urlretrieve(e[0]['links'][0]['href'], f)
print("granule:", e[0]['title'], round(os.path.getsize(f)/1e6, 1), "MB (anonymous download OK)")
with h5py.File(f, 'r') as h:
    beams = [k for k in h.keys() if k.startswith('gt')]
    print("beams:", beams)
    tot = 0
    for b in beams:
        try:
            g = h[b]['freeboard_segment']
            lat, lon = g['latitude'][:], g['longitude'][:]
            fb = g['beam_fb_height'][:] if 'beam_fb_height' in g else g['beam_fb_height'][:]
        except Exception as ex:
            print(b, 'skip', ex); continue
        m = (lon > B[0]) & (lon < B[2]) & (lat > B[1]) & (lat < B[3])
        n = int(m.sum()); tot += n
        if n:
            v = fb[m]; v = v[np.isfinite(v) & (np.abs(v) < 10)]
            print(f"{b}: segs_in_ROI={n:6d} fb_mean={v.mean():.3f}m p90={np.percentile(v,90):.3f}m p99={np.percentile(v,99):.3f}m")
    print("TOTAL freeboard segments in ROI (one granule):", tot)
