import asf_search as asf, json, os
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
os.makedirs("scratch/P8/s1",exist_ok=True)
sc=json.load(open("scratch/P8/scenes_sel.json"))
have={f.split(".")[0] for f in os.listdir("scratch/P8/s1")}
need=[s for s in sc if s not in have]
print("need",len(need),flush=True)
r=[p for p in asf.granule_search(need) if p.properties.get('processingLevel')=='GRD_MD']
print("found",len(r),flush=True)
asf.ASFSearchResults(r).download(path="scratch/P8/s1",session=asf.ASFSession(),processes=4)
print("DL DONE",flush=True)
