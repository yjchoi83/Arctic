import asf_search as asf, json, collections, datetime as dt
wkt="POLYGON((-172 69.5,-164 69.5,-164 72.5,-172 72.5,-172 69.5))"
res={}
for tag,(s,e) in {"melt":("2023-07-01","2023-08-31"),"winter":("2024-02-01","2024-03-31"),
                  "melt2":("2024-07-01","2024-08-31"),"winter2":("2023-02-01","2023-03-31")}.items():
    r=asf.geo_search(platform=[asf.PLATFORM.SENTINEL1],processingLevel=['GRD_MD'],beamMode=['EW'],
                     intersectsWith=wkt,start=s,end=e)
    g=collections.defaultdict(list)
    for p in r:
        pr=p.properties
        g[(pr['pathNumber'],pr['polarization'])].append((pr['startTime'][:19],pr['sceneName'],pr['frameNumber']))
    res[tag]={f"{k[0]}_{k[1]}":sorted(v) for k,v in g.items()}
    print(tag,"scenes",len(r),"tracks",len(g))
    for k,v in sorted(g.items(),key=lambda x:-len(x[1]))[:4]:
        print("  ",k,len(v),v[0][0],v[-1][0])
json.dump(res,open("scratch/R1_search.json","w"),indent=0)
