import pandas as pd, re
from datetime import date

raw = pd.read_csv("data/inventory_raw.csv")

name_col = next((c for c in raw.columns if re.search("name|title|model", c, re.I)), raw.columns[0])
raw["model_colorway"] = raw[name_col].str.strip()

model_numbers = {str(i) for i in range(3, 16)}

def extract_size(txt: str) -> str:
    s = str(txt)
    # explicit keyword first
    m = re.search(r'(?:size|sz)\s*([0-9]{1,2}(?:\.5)?)([mwly]?)', s, re.I)
    if m:
        num, tag = m.group(1), m.group(2).upper()
    else:
        # collect all 1–2 digit numbers with optional tag
        candidates = []
        for m in re.finditer(r'([0-9]{1,2}(?:\.5)?)([mwly]?)', s, re.I):
            num, tag = m.group(1), m.group(2).upper()
            # skip if part of a 4-digit year
            span = m.span(1)
            before = s[max(0, span[0]-2):span[0]]
            after  = s[span[1]:span[1]+2]
            if re.match(r'(19|20)', before+num+after):
                continue
            # skip Jordan model numbers
            if num in model_numbers:
                continue
            if float(num) >= 3:          # plausible shoe size
                candidates.append((num, tag))
        if not candidates:
            return "UNKNOWN"
        num, tag = max(candidates, key=lambda x: float(x[0]))
    if tag == 'W':
        return f"{num}W"
    if tag == 'Y':
        return f"{num}Y"
    return num

size_col = next((c for c in raw.columns if re.search("size", c, re.I)), name_col)
raw["size"] = raw[size_col].apply(extract_size)

raw["processed_date"] = date.today().isoformat()
raw.to_csv("data/work_inventory_stage1.csv", index=False)
raw.to_csv("data/inventory_clean.csv", index=False)
print("ETL complete – robust size extraction (model & year safe)")
