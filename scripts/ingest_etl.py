import pandas as pd, re
from datetime import date

raw = pd.read_csv("data/inventory_raw.csv")

name_col = next((c for c in raw.columns if re.search("name|title|model", c, re.I)), raw.columns[0])
raw["model_colorway"] = raw[name_col].str.strip()

allowed = {str(x) for x in [6,6.5,7,7.5,8,8.5,9,11,11.5,12,13,14,15]}
model_numbers = {str(i) for i in range(3, 16)}

def extract_size(txt: str) -> str:
    txt = str(txt)
    m_kw = re.search(r'(?:size|sz)\s*([0-9]{1,2}(?:\.5)?)(?:\s*(men|mens|m|women|w|youth|y))?', txt, re.I)
    if m_kw:
        num, tag = m_kw.group(1), (m_kw.group(2) or "").upper()
    else:
        pairs = re.findall(r'([0-9]{1,2}(?:\.5)?)(?:\s*(men|mens|m|women|w|youth|y))?', txt, re.I)
        candidates = []
        for num, tag in pairs:
            tag = tag.upper()
            if num in model_numbers: continue
            if num not in allowed: continue
            # skip if part of a 4-digit year
            span = re.search(num, txt).span()
            around = txt[max(0, span[0]-2):span[1]+2]
            if re.match(r'(19|20)[0-9]{2}', around): continue
            candidates.append((num, tag))
        if not candidates:
            return "UNKNOWN"
        num, tag = max(candidates, key=lambda x: float(x[0]))
    if num not in allowed:
        return "UNKNOWN"
    if re.match(r'WOMEN|W$', tag): return f"{num}W"
    if re.match(r'YOUTH|Y$', tag):  return f"{num}Y"
    return num  # men / default

size_col = next((c for c in raw.columns if re.search("size", c, re.I)), name_col)
raw["size"] = raw[size_col].apply(extract_size)

raw["processed_date"] = date.today().isoformat()
raw.to_csv("data/work_inventory_stage1.csv", index=False)
raw.to_csv("data/inventory_clean.csv", index=False)
print("ETL complete – size column follows approved list")
