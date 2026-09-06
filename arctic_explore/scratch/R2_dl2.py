import asf_search as asf, os, json
c=json.load(open("scratch/R2_pick2.json")); sess=asf.ASFSession()
r=asf.search(platform=[asf.PLATFORM.NISAR],start="2026-07-21",end="2026-07-22",processingLevel=["GCOV"],maxResults=3000)
sel=[p for p in r if p.properties.get("fileID")==c["nid"]]
print("nisar",len(sel))
if sel: sel[0].download(path="scratch/R2_data",session=sess,fileType=asf.FileDownloadType.DEFAULT_FILE)
s=[p for p in asf.granule_search([c["s1"]]) if p.properties.get('processingLevel')=='GRD_MD']
print("s1",len(s))
if s: s[0].download(path="scratch/R2_data",session=sess)
print("DONE2")
