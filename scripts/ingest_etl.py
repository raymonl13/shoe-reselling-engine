import pandas as pd, re
from datetime import date

raw = pd.read_csv("data/inventory_raw.csv")

name_col = next((c for c in raw.columns if re.search("name|title|model", c, re.I)), raw.columns[0])
raw["model_colorway"] = raw[name_col].str.strip()

allowed = {str(x) for x in [6,6.5,7,7.5,8,8.5,9,11,11.5,12,13,14,15]}

def extract_size(txt: str) -> str:
    txt = str(txt)
    pairs = re.findall(r'([0-9]{1,2}(?:\.5)?)(?:\s*(men|mens|m|women|w|youth|y))?', txt, re.I)
    candidates = []
    for num, tag in pairs:
        tag = tag.upper()
        # skip if part of a 4-digit year and no tag
        span = re.search(num, txt).span()
        around = txt[max(0, span[0]-2):span[1]+2]
        if not tag and re.match(r'(19|20)[0-9]{2}', around):
            continue
        if num in allowed:
            candidates.append((num, tag))
    if not candidates:
        return "UNKNOWN"
    tagged = [c for c in candidates if c[1]]
    num, tag = (tagged[0] if tagged else max(candidates, key=lambda x: float(x[0])))
    if re.match(r'WOMEN|W$', tag):  return f"{num}W"
    if re.match(r'YOUTH|Y$', tag):  return f"{num}Y"
    return num  # men / default

size_col = next((c for c in raw.columns if re.search("size", c, re.I)), name_col)
combo = raw[size_col].astype(str) + " " + raw[name_col].astype(str) if size_col else raw[name_col]
raw["size"] = combo.apply(extract_size)

raw["processed_date"] = date.today().isoformat()
raw.to_csv("data/work_inventory_stage1.csv", index=False)
raw.to_csv("data/inventory_clean.csv", index=False)
print("ETL complete – sizes follow approved list")
