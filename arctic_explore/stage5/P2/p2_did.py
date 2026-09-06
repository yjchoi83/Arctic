import pandas as pd, numpy as np, json, os
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
rng=np.random.default_rng(0)
t=pd.read_csv("scratch/P2/P2_tables.csv"); t=t[t.season!="shoulder"]
R=pd.read_csv("scratch/P2/retention.csv",index_col=0)
t["class"]=t.region.map(R["class"])
def period(y): return "pre" if 2019<=y<=2021 else ("during" if 2022<=y<=2024 else ("post" if y>=2025 else None))
t["period"]=t.year.map(period); t=t[t.period.notna()]
# region-year cell = window-weighted mean of the three seasons
def cell(g,col): return np.average(g[col],weights=g.window_h)
cells=t.groupby(["region","class","period","year"]).apply(
    lambda g: pd.Series({"O24":cell(g,"O24"),"O12":cell(g,"O12"),"n_acq":g.n_acq.sum()}),
    include_groups=False).reset_index()
cells.to_csv("scratch/P2/P2_cells.csv",index=False)
def grpmean(d,cl,per,col):
    s=d[(d["class"]==cl)&(d.period==per)][col]
    return float(s.mean()) if len(s) else np.nan
def did(d,col,g1="lost",g0="intermediate"):
    return ((grpmean(d,g1,"during",col)-grpmean(d,g1,"pre",col))
           -(grpmean(d,g0,"during",col)-grpmean(d,g0,"pre",col)))
def recov(d,col,cl="lost"):
    return grpmean(d,cl,"post",col)-grpmean(d,cl,"pre",col)
regs=cells.region.unique()
out={}
for col in ("O24","O12"):
    pt_did=did(cells,col); pt_rec=did(cells,col)  # placeholder
    pt_rec=recov(cells,col)
    bd=[];br=[]
    for _ in range(1000):
        pick=rng.choice(regs,len(regs),replace=True)
        d=pd.concat([cells[cells.region==r] for r in pick],ignore_index=True)
        v=did(d,col); w=recov(d,col)
        if np.isfinite(v): bd.append(v)
        if np.isfinite(w): br.append(w)
    out[col]=dict(
        lost_pre=grpmean(cells,"lost","pre",col),lost_during=grpmean(cells,"lost","during",col),
        lost_post=grpmean(cells,"lost","post",col),
        int_pre=grpmean(cells,"intermediate","pre",col),int_during=grpmean(cells,"intermediate","during",col),
        int_post=grpmean(cells,"intermediate","post",col),
        did=pt_did,did_ci=[float(np.percentile(bd,2.5)),float(np.percentile(bd,97.5))],
        recovery=pt_rec,rec_ci=[float(np.percentile(br,2.5)),float(np.percentile(br,97.5))],
        n_boot_did=len(bd))
for c,v in out.items():
    print(f"=== {c} ===")
    print("  lost      pre %.3f during %.3f post %.3f  (drop %.1f pp)"%(v['lost_pre'],v['lost_during'],v['lost_post'],100*(v['lost_during']-v['lost_pre'])))
    print("  intermed  pre %.3f during %.3f post %.3f  (drop %.1f pp)"%(v['int_pre'],v['int_during'],v['int_post'],100*(v['int_during']-v['int_pre'])))
    print("  DiD %.1f pp  CI [%.1f, %.1f]  (n_boot %d)"%(100*v['did'],100*v['did_ci'][0],100*v['did_ci'][1],v['n_boot_did']))
    print("  H2 recovery(lost post-pre) %.1f pp  CI [%.1f, %.1f]"%(100*v['recovery'],100*v['rec_ci'][0],100*v['rec_ci'][1]))
json.dump(out,open("scratch/P2/did.json","w"),indent=1,default=float)
