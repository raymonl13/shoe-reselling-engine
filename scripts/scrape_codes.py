import os,time,pandas as pd,warnings,urllib3
from kof_lookup      import get_kof_data
from rapidapi_lookup import get_rapidapi_data
from stockx_lookup   import get_stockx_data

warnings.filterwarnings("ignore",category=urllib3.exceptions.NotOpenSSLWarning)

INV="data/inventory_clean.csv"; REF="data/style_codes_reference.csv"
key=["model_colorway","size"]

inv=pd.read_csv(INV)
inv["style_code"]=inv["style_code"].astype(str).str.strip().replace({"":pd.NA,"nan":pd.NA})
inv["style_code"]=inv["style_code"].fillna("CODE_NA")

try: ref=pd.read_csv(REF)
except FileNotFoundError: ref=pd.DataFrame(columns=["model_colorway","style_code","source"])

need=inv[inv["style_code"]=="CODE_NA"][key].drop_duplicates()

for mdl,sz in need.values:
    q=str(mdl)
    for fn,tag in ((get_kof_data,"KOF"),(get_rapidapi_data,"RAPIDAPI"),(get_stockx_data,"STOCKX")):
        try: code,name,cway=fn(q)
        except Exception: code=name=cway=None
        if code:
            idx=(inv["model_colorway"]==mdl)&(inv["size"]==sz)
            inv.loc[idx,["style_code","official_name","official_colorway","source"]]=[code,name,cway,tag]
            ref=pd.concat([ref,pd.DataFrame([{"model_colorway":mdl,"style_code":code,"source":tag}])])
            break
        time.sleep(1)

ref.drop_duplicates(["model_colorway","style_code"]).to_csv(REF,index=False)
inv.to_csv(INV,index=False)
inv[inv["style_code"]=="CODE_NA"][key].to_csv("data/missing_codes.csv",index=False)
print("rows",len(inv),"missing",(inv["style_code"]=="CODE_NA").sum())
