import pandas as pd, io, urllib.request
U="https://www.tsb.gc.ca/sites/default/files/stats/MARSISdb_MDOTW_VW_OCCURRENCE_PUBLIC.csv"
raw=urllib.request.urlopen(U,timeout=180).read()
for enc in ("utf-8","latin-1"):
    try: df=pd.read_csv(io.BytesIO(raw),encoding=enc,low_memory=False); break
    except Exception: pass
print("rows",len(df)); print([c for c in df.columns][:40])
