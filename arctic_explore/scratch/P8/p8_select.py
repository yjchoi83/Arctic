import json, collections, asf_search as asf
P=json.load(open("scratch/P8/pairs_all.json"))
P.sort(key=lambda o:(-o['ovl'],o['dt_h']))
cells=[(r,s) for r in ["Vilkitsky","Sannikov_DmLaptev","LongStrait"] for s in ["freeze-up","winter"]]
buckets={c:[o for o in P if (o['region'],o['season'])==c] for c in cells}
sel=[];scenes=set();peryr=collections.Counter();per=collections.Counter()
# round-robin so every chokepoint x season is represented
for rnd in range(4):
    for c in cells:
        for o in buckets[c]:
            if o in sel: continue
            if per[c]>=4: break
            if peryr[(o['region'],o['season'],o['year'])]>=2: continue
            new=scenes|{o['a'],o['b']}
            if len(new)>44: continue
            sel.append(o); scenes=new; per[c]+=1; peryr[(o['region'],o['season'],o['year'])]+=1
            break
    if len(sel)>=20: break
print("selected pairs",len(sel),"unique scenes",len(scenes))
for c in cells: print("  ",c,per[c])
json.dump(sel,open("scratch/P8/pairs_sel.json","w"),indent=1)
json.dump(sorted(scenes),open("scratch/P8/scenes_sel.json","w"),indent=1)
r=[p for p in asf.granule_search(sorted(scenes)) if p.properties.get('processingLevel')=='GRD_MD']
print("scenes found",len(r),"total %.1f GB"%(sum(p.properties.get('bytes') or 0 for p in r)/1e9))
