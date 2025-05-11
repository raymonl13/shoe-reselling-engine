import requests, urllib.parse, time
from typing import Optional, Tuple

BASE = "https://www.kicksonfire.com/wp-json/search/all?query="
UA   = {"User-Agent": "Mozilla/5.0"}

def get_kof_data(query: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    url = BASE + urllib.parse.quote(query)
    r = requests.get(url, headers=UA, timeout=10)
    if r.status_code != 200:
        return None, None, None
    try:
        item = r.json().get("items", [])[0]
    except Exception:
        return None, None, None
    code      = item.get("styleId") or item.get("sku")
    title     = item.get("title")
    colorway  = item.get("colorway")
    time.sleep(1.0)
    return code, title, colorway
