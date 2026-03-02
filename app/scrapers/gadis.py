from app.models.scraper_base import BaseScraper
from app.utils.configs_util import GADIS_HEADERS, GADIS_API_CATEGORIES, GADIS_API_SEARCH
from concurrent.futures import ThreadPoolExecutor

class GadisScraper(BaseScraper):
    def __init__(self):
        super().__init__("GADIS", GADIS_HEADERS)
        self._session_ready = False

    def _initialize_session(self):
        if self._session_ready: return True
        try:
            # Visita inicial silenciosa para cookies
            self._session.get("https://www.gadisline.com/", timeout=15)
            self._session_ready = True
            return True
        except:
            return False

    def fetch_category(self, cat_id):
        payload = {"minimum_should_match": 1, "category_ids": [int(cat_id)]}
        params = {"page_number": 1, "rows_per_page": 100, "order_field": "relevance", "sort_type": "asc"}
        try:
            # Importante: Gadis usa POST para las búsquedas/categorías
            r = self._session.post(GADIS_API_SEARCH, params=params, json=payload, timeout=15)
            return r.json().get("elements", []) if r.status_code == 200 else []
        except:
            return []

    def scrape(self):
        if not self._initialize_session(): return []
        
        # Obtenemos categorías o usamos las principales si falla el listado
        cat_data = self.get_json(GADIS_API_CATEGORIES)
        cat_ids = [c["id"] for c in cat_data.get("elements", [])] if cat_data else [22601, 22608, 22701, 22801, 22901]

        # Gadis es sensible, usamos pocos workers para evitar bloqueos
        with ThreadPoolExecutor(max_workers=3) as executor:
            category_results = executor.map(self.fetch_category, cat_ids)
            
            for products in category_results:
                for p in products:
                    # Extraer el nombre en español de forma más segura
                    descriptions = p.get("commercial_description", [])
                    name = next((d.get("value") for d in descriptions if d.get("language") == "ES"), None)
                    if not name and descriptions: name = descriptions[0].get("value")
                    
                    if not name: continue

                    self.add_product(
                        name=name,
                        price=p.get("price"),
                        reference_price=p.get("price_kilo_litre"),
                        quantity=p.get("weight"),
                        unit_type=None,
                        image_url=p.get("image", {}).get("image")
                    )
        return self.products