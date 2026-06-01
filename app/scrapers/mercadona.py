from curl_cffi import requests
from app.models.scraper_base import BaseScraper
from app.config.scrapers_config import MERCADONA_HEADERS, MERCADONA_API_INDEX, MERCADONA_API_CAT
from concurrent.futures import ThreadPoolExecutor

class MercadonaScraper(BaseScraper):
    def __init__(self):
        super().__init__("MERCADONA", MERCADONA_HEADERS)
        self.session = requests.Session(impersonate="chrome120", headers=MERCADONA_HEADERS)

    def _warmup(self):
        """Realiza el calentamiento de sesión para evitar bloqueos"""
        try:
            self.session.get("https://tienda.mercadona.es/")
            self.session.get("https://tienda.mercadona.es/manifest.json")
            self.session.get("https://tienda.mercadona.es/locales/es.json")
        except Exception:
            pass

    def fetch_cat(self, cat_id):
        url = MERCADONA_API_CAT.format(cat_id=cat_id)
        try:
            resp = self.session.get(url)
            return resp.json() if resp.status_code == 200 else None
        except:
            return None

    def scrape(self):
        # 1. Calentamiento previo
        self._warmup()

        # 2. Obtener índice
        resp = self.session.get(MERCADONA_API_INDEX)
        if resp.status_code != 200:
            from app.utils.logger_util import HermesLogger
            HermesLogger.get_logger("MERCADONA").error(f"Error {resp.status_code} al acceder al índice de Mercadona")
            return []
            
        index = resp.json()
        cat_ids = [c["id"] for res in index.get("results", []) for c in res.get("categories", [])]
        
        # 3. Extracción concurrente
        with ThreadPoolExecutor(max_workers=5) as exe:
            responses = list(exe.map(self.fetch_cat, cat_ids))

        # 4. Procesamiento
        for data in filter(None, responses):
            for subcategory in data.get("categories", []):
                for p in subcategory.get("products", []):
                    i = p.get("price_instructions", {})
                    
                    self.add_product(
                        name=p.get("display_name"), 
                        price=i.get("unit_price"), 
                        image_url=p.get("thumbnail")
                    )
        
        return self.products