import pandas as pd
def regions():
    R={"KaraGate":(57.0,60.5,70.0,71.0),"Vilkitsky":(100.0,106.0,77.3,78.4),
       "Sannikov_DmLaptev":(137.0,145.0,72.7,75.2),"LongStrait":(175.0,180.0,69.5,71.0),
       "BeringChukchi":(-172.0,-166.0,65.5,69.0),
       "Barents_Svalbard":(15.0,35.0,74.0,78.0),"GreenlandSea_Fram":(-10.0,5.0,76.0,80.0),
       "BaffinBay":(-65.0,-55.0,70.0,75.0),
       "LancasterSound":(-90.0,-80.0,73.5,75.0),"VictoriaStrait":(-105.0,-96.0,68.0,70.5)}
    d=pd.read_csv("scratch/TF01_segments.csv")
    grp=[(0,7),(7,14),(14,21),(21,28),(28,34),(34,40)]
    for k,(a,b) in enumerate(grp,1):
        s=d.iloc[a:b]
        R[f"AKcorr_{k}"]=(round(s.lon.min()-1.0,3),round(s.lon.max()+1.0,3),
                          round(s.lat.min()-0.5,3),round(s.lat.max()+0.5,3))
    return R
if __name__=="__main__":
    for k,v in regions().items(): print(k,v)
