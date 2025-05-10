import pandas as pd, re
from datetime import date

raw = pd.read_csv("data/inventory_raw.csv")

name_col = [c for c in raw.columns if re.search("name|title|model", c, re.I)]
name_col = name_col[0] if name_col else raw.columns[0]
raw["model_colorway"] = raw[name_col].astype(str).str.strip()

raw["processed_date"] = date.today().isoformat()
raw.to_csv("data/work_inventory_stage1.csv", index=False)
raw.to_csv("data/inventory_clean.csv", index=False)
print("ETL complete → inventory_clean.csv now includes model_colorway")
