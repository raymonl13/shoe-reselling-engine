import pandas as pd, re
from datetime import date

raw = pd.read_csv("data/inventory_raw.csv")

name_col = next((c for c in raw.columns if re.search("name|title|model", c, re.I)), raw.columns[0])
raw["model_colorway"] = raw[name_col].str.strip()

def extract_size(text):
    m = re.search(r'\b(1[0-5](?:\.5)?|[3-9](?:\.5)?|[0-2]?[0-9]Y|[0-9\.]+W)\b', str(text), re.I)
    return m.group(0).upper() if m else "UNKNOWN"

size_col = next((c for c in raw.columns if re.search("size", c, re.I)), name_col)
raw["size"] = raw[size_col].apply(extract_size)

raw["processed_date"] = date.today().isoformat()
raw.to_csv("data/work_inventory_stage1.csv", index=False)
raw.to_csv("data/inventory_clean.csv", index=False)
print("ETL complete → inventory_clean.csv updated")
