import pandas as pd, re
from datetime import date

raw = pd.read_csv("data/inventory_raw.csv")

name_col = [c for c in raw.columns if re.search("name|title|model", c, re.I)]
name_col = name_col[0] if name_col else raw.columns[0]
raw["model_colorway"] = raw[name_col].astype(str).str.strip()

def extract_size(txt:str)->str:
    m=re.search(r'\b(1[0-5](?:\.[05])?|[3-9](?:\.[05])?)\s*(?:M|W|Y|men|women|youth)?\b',str(txt),re.I)
    return m.group(1) if m else "UNKNOWN"

size_src = [c for c in raw.columns if re.search("size", c, re.I)]
if size_src:
    raw["size"] = raw[size_src[0]].astype(str).apply(extract_size)
else:
    raw["size"] = raw[name_col].apply(extract_size)

raw["processed_date"] = date.today().isoformat()
raw.to_csv("data/work_inventory_stage1.csv", index=False)
raw.to_csv("data/inventory_clean.csv", index=False)
print("ETL complete → model_colorway and size columns added")
