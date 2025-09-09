import os
import requests

RAWG_BASE = "https://api.rawg.io/api"
RAWG_KEY = os.getenv("RAWG_API_KEY", "")

def _get(url, params=None, timeout=20):
    params = params or {}
    if RAWG_KEY:
        params["key"] = RAWG_KEY
    r = requests.get(url, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()

def fetch_games_page(page: int = 1, page_size: int = 40, ordering: str = "-updated"):
    return _get(f"{RAWG_BASE}/games", params={"page": page, "page_size": page_size, "ordering": ordering})

def fetch_platforms_page(page: int = 1, page_size: int = 40):
    return _get(f"{RAWG_BASE}/platforms", params={"page": page, "page_size": page_size})
