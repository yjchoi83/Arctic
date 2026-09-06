import asf_search as asf, json, datetime as dt
from shapely.geometry import shape
try:
    ds=[d for d in dir(asf.DATASET) if 'NISAR' in d.upper()]
    print("datasets:",ds)
except Exception as e: print(e)
r=asf.search(dataset='NISAR', maxResults=2000)
print("total NISAR",len(r))
from collections import Counter
c=Counter((p.properties.get('processingLevel'),p.properties.get('beamModeType')) for p in r)
print(c.most_common(8))
