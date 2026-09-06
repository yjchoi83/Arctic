import asf_search as asf, os, json
os.makedirs("scratch/R1_data",exist_ok=True)
want={"melt":["2024-08-10T18:04:58","2024-08-12T17:48:32","2024-08-13T18:29:41","2024-08-24T17:48:32","2024-08-25T18:29:42"],
      "winter":["2024-02-12T18:04:59","2024-02-14T17:48:33","2024-02-15T18:29:42","2024-02-26T17:48:33","2024-02-27T18:29:42"]}
wkt="POLYGON((-172 69.5,-164 69.5,-164 72.5,-172 72.5,-172 69.5))"
sess=asf.ASFSession()
picked={}
for tag,(s,e) in {"melt":("2024-08-09","2024-08-26"),"winter":("2024-02-11","2024-02-28")}.items():
    r=asf.geo_search(platform=[asf.PLATFORM.SENTINEL1],processingLevel=['GRD_MD'],beamMode=['EW'],
                     intersectsWith=wkt,start=s,end=e)
    sel=[p for p in r if p.properties['startTime'][:19] in want[tag] and 'HH' in p.properties['polarization']]
    seen=set();uni=[]
    for p in sel:
        k=p.properties['startTime'][:19]
        if k in seen: continue
        seen.add(k);uni.append(p)
    picked[tag]=[{"t":p.properties['startTime'][:19],"n":p.properties['sceneName'],
                  "path":p.properties['pathNumber'],"size":p.properties.get('bytes')} for p in uni]
    print(tag,len(uni),[x['t'] for x in picked[tag]])
    asf.ASFSearchResults(uni).download(path="scratch/R1_data",session=sess,processes=3)
json.dump(picked,open("scratch/R1_picked.json","w"),indent=1)
print("DONE")
