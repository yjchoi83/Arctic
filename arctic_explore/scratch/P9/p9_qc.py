import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import matplotlib.image as mpimg, glob, os, pandas as pd, numpy as np
os.chdir("/d/yj_projects/workspace_yj/Arctic/arctic_explore")
Q=pd.read_csv("results/P8/qc_table.csv")
files=sorted(glob.glob("results/P8/quicklooks/E*.png"))
print("event PNGs",len(files))
n=len(files); ncol=3; nrow=int(np.ceil(n/ncol))
fig,axes=plt.subplots(nrow,ncol,figsize=(15,3.1*nrow))
for ax,f in zip(axes.ravel(),files):
    ax.imshow(mpimg.imread(f)); ax.set_xticks([]); ax.set_yticks([])
    ev=os.path.basename(f).split("_")[0]
    r=Q[Q.event==ev]
    t=f"{ev} {r.region.iloc[0]} {r.date.iloc[0]}  {r.area_km2.iloc[0]:.0f} km2  mag {r.magnitude_km.iloc[0]:.2f} km" if len(r) else ev
    ax.set_title(t,fontsize=6)
for ax in axes.ravel()[n:]: ax.axis("off")
fig.suptitle("ARC-P8/P9 strait convergence events — contact sheet for human adjudication (decision column blank)",fontsize=10)
fig.savefig("results/P9/contact_sheet_events.png",dpi=95,bbox_inches="tight"); plt.close(fig)
print("contact sheet written")
# per-event QC table carried forward with the P9 rescaled magnitude
Q["mag_buoy_baseline_km"]=(Q.magnitude_km/ (np.sqrt(Q.area_km2)/49.4)).round(2)
Q["mag_class_rescaled"]=np.where(Q.mag_buoy_baseline_km>=5,">=5km",
                          np.where(Q.mag_buoy_baseline_km>=3,">=3km",
                          np.where(Q.mag_buoy_baseline_km>=1,"1-3km","<1km")))
Q.to_csv("results/P9/qc_table_p9.csv",index=False)
print(Q.mag_class_rescaled.value_counts().to_dict())
