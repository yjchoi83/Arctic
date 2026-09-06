import json, urllib.request, datetime as dt
import asf_search as asf

# ROI: Vilkitsky Strait + eastern Kara/western Laptev approaches
BBOX = (95.0, 76.0, 120.0, 80.0)
WKT = "POLYGON((95 76,120 76,120 80,95 80,95 76))"
T0, T1 = "2023-10-01T00:00:00Z", "2023-11-30T23:59:59Z"

url = ("https://cmr.earthdata.nasa.gov/search/granules.json?short_name=ATL10&version=007"
       f"&temporal={T0},{T1}&bounding_box={BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}&page_size=500")
g = json.load(urllib.request.urlopen(url, timeout=120))['feed']['entry']
def P(s): return dt.datetime.fromisoformat(s.replace('Z','+00:00'))
i2 = sorted([(P(e['time_start']), P(e['time_end']), e['title']) for e in g])
print("ATL10 granules intersecting ROI:", len(i2))

r = asf.search(platform=[asf.PLATFORM.SENTINEL1], beamMode=['EW'], processingLevel=['GRD_MD'],
               start=T0, end=T1, intersectsWith=WKT, maxResults=2000)
s1 = sorted([P(p.properties['startTime']) for p in r])
print("S1 EW GRDM scenes over ROI:", len(s1))

for h in (1, 3, 6, 12):
    w = dt.timedelta(hours=h)
    pairs = sum(1 for a, b, _ in i2 for t in s1 if a - w <= t <= b + w)
    tracks = len({tt for a, b, tt in i2 if any(a - w <= t <= b + w for t in s1)})
    print(f"dt<={h:2d}h: pairs={pairs:5d}  distinct ATL10 granules matched={tracks:3d}")
