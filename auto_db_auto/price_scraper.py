
import os, re
from typing import Optional, Tuple
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": os.getenv("USER_AGENT", "Mozilla/5.0")}
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))

def fetch_best_price_pc(title: str) -> Optional[Tuple[float, str, str]]:
    """
    Heuristic DLCompare scraper. Returns: (price, shop, url) or None
    """
    try:
        q = (title or "").strip()
        if not q:
            return None
        url = f"https://www.dlcompare.fr/recherche?query={requests.utils.quote(q)}"
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        product = soup.select_one(".product-list .product-item a, .search-result a")
        if not product:
            return None
        product_url = product.get("href") or ""
        if product_url and not product_url.startswith("http"):
            product_url = "https://www.dlcompare.fr" + product_url

        r2 = requests.get(product_url, headers=HEADERS, timeout=TIMEOUT)
        r2.raise_for_status()
        soup2 = BeautifulSoup(r2.text, "lxml")

        price_el = soup2.select_one(".best-offer .price, .price .amount, .offer .price, [itemprop='price']")
        shop_el = soup2.select_one(".best-offer .merchant-name, .merchant .name, .offer .merchant, [itemprop='seller']")

        if not price_el:
            return None

        price_txt = re.sub(r"[^0-9.,]", "", price_el.get_text(strip=True)).replace(",", ".")
        price_val = float(price_txt)
        shop = (shop_el.get_text(strip=True) if shop_el else "N/A")
        return price_val, shop, product_url
    except Exception:
        return None
