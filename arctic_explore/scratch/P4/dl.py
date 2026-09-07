import os,urllib.request,concurrent.futures as cf,datetime as dt
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
OUT="scratch/P4/osisaf"; os.makedirs(OUT,exist_ok=True)
BASE="https://thredds.met.no/thredds/fileServer/osisaf/met.no/ice/drift_lr/merged"
CAT="https://thredds.met.no/thredds/catalog/osisaf/met.no/ice/drift_lr/merged"
import re
tasks=[]
for y in range(2016,2026):
    for m in range(1,13):
        if m in (4,5): continue
        try:
            x=urllib.request.urlopen(f"{CAT}/{y}/{m:02d}/catalog.xml",timeout=45).read().decode()
        except Exception: continue
        for f in sorted(set(re.findall(r'ice_drift_nh_polstere-625_multi-oi_[0-9\-]+\.nc',x))):
            p=f"{OUT}/{f}"
            if not os.path.exists(p): tasks.append((f"{BASE}/{y}/{m:02d}/{f}",p))
print("to download",len(tasks),flush=True)
def get(a):
    u,p=a
    try:
        urllib.request.urlretrieve(u,p); return 1
    except Exception: return 0
ok=0
with cf.ThreadPoolExecutor(8) as ex:
    for i,r in enumerate(ex.map(get,tasks)):
        ok+=r
        if i%300==0: print(i,ok,flush=True)
print("done",ok,"/",len(tasks),flush=True)
