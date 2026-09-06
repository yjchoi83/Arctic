import asf_search as asf, os
os.makedirs("scratch/R2_data",exist_ok=True)
sess=asf.ASFSession()
nid="NISAR_L2_PR_GCOV_029_049_A_037_4005_DHDH_A_20260828T141700_20260828T141732_P05023_N_F_J_001"
r=asf.search(platform=[asf.PLATFORM.NISAR],start="2026-08-28",end="2026-08-29",
             processingLevel=["GCOV"],maxResults=2000)
sel=[p for p in r if p.properties.get("fileID","").startswith(nid)]
print("nisar match",len(sel))
if sel: sel[0].download(path="scratch/R2_data",session=sess,fileType=asf.FileDownloadType.DEFAULT_FILE)
s=asf.granule_search(["S1D_EW_GRDM_1SDH_20260828T174021_20260828T174121_004329_007FC1_62A1"])
s=[p for p in s if p.properties.get('processingLevel')=='GRD_MD']
print("s1 match",len(s))
if s: s[0].download(path="scratch/R2_data",session=sess)
print("R2 DONE")
