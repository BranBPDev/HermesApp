import requests # Añade este import
from app.models.scraper_base import BaseScraper
from app.utils.configs_util import COMMON_HEADERS, MERCADONA_API_INDEX, MERCADONA_API_CAT
from concurrent.futures import ThreadPoolExecutor

class MercadonaScraper(BaseScraper):
    def __init__(self):
        super().__init__("MERCADONA", COMMON_HEADERS)
        # Forzamos una sesión nueva y simple para evitar conflictos con el parche
        self._session = requests.Session()
        self._session.headers.update(COMMON_HEADERS)

    def scrape(self):
        # 1. Obtener índice (categorías)
        try:
            resp = self._session.get(MERCADONA_API_INDEX, timeout=10)
            if not resp.ok:
                self.log.error(f"Error Mercadona Index: {resp.status_code}")
                return []
            index = resp.json()
        except Exception as e:
            self.log.error(f"Fallo conexión Mercadona: {e}")
            return []

        cat_ids = [c["id"] for res in index.get("results", []) for c in res.get("categories", [])]
        
        # 2. Función interna para el worker
        def fetch_cat(cat_id):
            url = MERCADONA_API_CAT.format(cat_id=cat_id)
            try:
                r = self._session.get(url, timeout=10)
                return r.json() if r.ok else None
            except:
                return None

        # 3. Descarga paralela
        with ThreadPoolExecutor(max_workers=5) as exe: # Bajamos a 5 por seguridad
            responses = list(exe.map(fetch_cat, cat_ids))

        # 4. Procesamiento
        for data in filter(None, responses):
            for cat in data.get("categories", []):
                for p in cat.get("products", []):
                    i = p.get("price_instructions", {})
                    self.add_product(
                        name=p.get("display_name"), 
                        price=i.get("unit_price"), 
                        image_url=p.get("thumbnail"), 
                        quantity=i.get("unit_size")
                    )
        
        self.log.info(f"Mercadona completado: {len(self.products)} productos")
        return self.products