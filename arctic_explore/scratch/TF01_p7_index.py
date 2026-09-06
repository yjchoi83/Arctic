import json,io,urllib.parse,urllib.request,numpy as np,pandas as pd,rasterio
from rasterio.warp import transform as rtransform
from scipy.stats import spearmanr
df=pd.read_csv("scratch/TF01_segments.csv")
B="https://gis.ngdc.noaa.gov/arcgis/rest/services/"
def dep(p):
    g=urllib.parse.quote(json.dumps({"x":p[0],"y":p[1]}))
    u=(f"{B}DEM_mosaics/ETOPO1_bedrock/MapServer/identify?f=json&geometry={g}&geometryType=esriGeometryPoint&sr=4326"
       f"&layers=all&tolerance=2&mapExtent={p[0]-1},{p[1]-1},{p[0]+1},{p[1]+1}&imageDisplay=400,400,96&returnGeometry=false")
    try:
        r=json.loads(urllib.request.urlopen(u,timeout=45).read()).get("results",[])
        return float(str(list(r[0]["attributes"].values())[0]).split()[0])
    except Exception: return np.nan
df["depth"]=[dep((r.lon,r.lat)) for r in df.itertuples()]
# continuous mean SIC over the same 20 dates
MON={6:"jun",11:"nov"}; acc=[];
pts=list(zip(df.lon,df.lat))
for y in range(2016,2026):
    for m,dd in ((11,15),(6,25)):
        url=f"https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n6250/{y}/{MON[m]}/Arctic/asi-AMSR2-n6250-{y}{m:02d}{dd}-v5.4.tif"
        try: buf=urllib.request.urlopen(url,timeout=90).read()
        except Exception: continue
        with rasterio.open(io.BytesIO(buf)) as ds:
            xs,ys=rtransform("EPSG:4326",ds.crs,[p[0] for p in pts],[p[1] for p in pts])
            v=np.array([s[0] for s in ds.sample(zip(xs,ys))],dtype=float)
        v[v>100]=np.nan; acc.append(v)
S=np.vstack(acc); df["sic_mean"]=np.nanmean(S,0); df["sic_p90"]=np.nanpercentile(S,90,axis=0)
df["chart_inadequacy"]=(df.tid>=40).astype(float)
df["survey_staleness"]=2026-df.newest_survey
df["survey_sparsity"]=1/(1+df.n_survey)
df["shallowness"]=-df.depth.clip(upper=-1)*-1
df["shallowness"]=1/np.abs(df.depth).clip(lower=5)
cols=["sic_mean","sic_p90","chart_inadequacy","survey_staleness","dist_refuge_km","dist_sar_km","shallowness"]
Z=(df[cols]-df[cols].mean())/df[cols].std(ddof=0)
Z=Z.fillna(0.0)
base_eq=Z.mean(1).values
R=df[cols].rank(pct=True); base_rk=R.mean(1).values
print("n_seg",len(df),"layers",len(cols),"spearman(equal,rank)=%.3f"%spearmanr(base_eq,base_rk).statistic)
rng=np.random.default_rng(0); W=rng.dirichlet(np.ones(len(cols)),100)
D=Z.values@W.T
rho=np.array([spearmanr(D[:,j],base_eq).statistic for j in range(100)])
def dec(x): return pd.qcut(pd.Series(x).rank(method="first"),10,labels=False).values
b=dec(base_eq)
ch=np.array([(dec(D[:,j])!=b).sum() for j in range(100)])
top5=np.array([len(set(np.argsort(-D[:,j])[:5])&set(np.argsort(-base_eq)[:5])) for j in range(100)])
print("Dirichlet100: spearman median %.3f  p05 %.3f  min %.3f"%(np.median(rho),np.percentile(rho,5),rho.min()))
print("decile changes/40 segs: median %d  p95 %d  max %d"%(np.median(ch),np.percentile(ch,95),ch.max()))
print("top-5 overlap: median %d  min %d"%(np.median(top5),top5.min()))
print("--- layer omission (drop one, equal weight)")
for c in cols:
    o=Z.drop(columns=[c]).mean(1).values
    print("  drop %-18s rho=%.3f  decile_changes=%d  top5_overlap=%d"%(c,spearmanr(o,base_eq).statistic,(dec(o)!=b).sum(),len(set(np.argsort(-o)[:5])&set(np.argsort(-base_eq)[:5]))))
df.to_csv("scratch/TF01_segments.csv",index=False)
print("depth ok:",df.depth.notna().sum(),"/",len(df),"sic range %.1f-%.1f"%(df.sic_mean.min(),df.sic_mean.max()))
