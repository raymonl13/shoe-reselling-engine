import requests, urllib.parse, time
from typing import Optional
BASE = "https://www.kicksonfire.com/wp-json/search/all?query="
def get_kof_code(q: str) -> Optional[str]:
    url = BASE + urllib.parse.quote(q)
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return None
    items = r.json().get("items", [])
    if not items:
        return None
    code = items[0].get("styleId") or items[0].get("sku")
    time.sleep(1.0)
    return code
