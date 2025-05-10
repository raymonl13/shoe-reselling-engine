import os,time,pandas as pd
from kof_lookup import get_kof_code
INV="data/inventory_clean.csv";REF="data/style_codes_reference.csv"
inv=pd.read_csv(INV)
ref=pd.read_csv(REF) if os.path.exists(REF) else pd.DataFrame(columns=["model_colorway","style_code","source"])
batch=[m for m in inv["model_colorway"].unique() if m not in ref["model_colorway"]][:40]
new=[]
for m in batch:
    code=get_kof_code(m) or "CODE_NA"
    new.append({"model_colorway":m,"style_code":code,"source":"KOF" if code!="CODE_NA" else "NONE"})
    time.sleep(1.2)
ref=pd.concat([ref,pd.DataFrame(new)]).drop_duplicates("model_colorway")
ref.to_csv(REF,index=False)
inv=inv.merge(ref[["model_colorway","style_code","source"]],on="model_colorway",how="left")
inv["style_code"].fillna("CODE_NA",inplace=True)
inv.to_csv(INV,index=False)
inv[inv["style_code"]=="CODE_NA"][["model_colorway","size"]].to_csv("data/missing_codes.csv",index=False)
print("Done → data/missing_codes.csv")
