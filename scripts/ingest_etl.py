import pandas as pd, re
from datetime import date
raw = pd.read_csv("data/inventory_raw.csv")
raw["processed_date"] = date.today().isoformat()
raw.to_csv("data/work_inventory_stage1.csv", index=False)
raw.to_csv("data/inventory_clean.csv", index=False)
print("ETL complete → work_inventory_stage1.csv, inventory_clean.csv")
