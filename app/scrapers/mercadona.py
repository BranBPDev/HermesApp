import requests
from app.models.scraper_base import BaseScraper
from app.config.scrapers_config import COMMON_HEADERS, MERCADONA_API_INDEX, MERCADONA_API_CAT
from concurrent.futures import ThreadPoolExecutor

class MercadonaScraper(BaseScraper):
    def __init__(self):
        super().__init__("MERCADONA", COMMON_HEADERS)

    def scrape(self):
        index = self.get_json(MERCADONA_API_INDEX)
        if not index:
            return []

        # Extraemos IDs de categorías de primer nivel
        cat_ids = [c["id"] for res in index.get("results", []) for c in res.get("categories", [])]
        
        def fetch_cat(cat_id):
            url = MERCADONA_API_CAT.format(cat_id=cat_id)
            return self.get_json(url)

        with ThreadPoolExecutor(max_workers=5) as exe:
            responses = list(exe.map(fetch_cat, cat_ids))

        for data in filter(None, responses):
            # Mercadona organiza por: Categoría -> Subcategorías -> Productos
            for subcategory in data.get("categories", []):
                for p in subcategory.get("products", []):
                    i = p.get("price_instructions", {})
                    
                    self.add_product(
                        name=p.get("display_name"), 
                        price=i.get("unit_price"), 
                        image_url=p.get("thumbnail"), 
                        quantity=i.get("unit_size"),
                        # NUEVO: Usamos los datos calculados por la API
                        reference_price=i.get("reference_price"),
                        unit_type=i.get("reference_format")
                    )
        
        self.log.info(f"Mercadona finalizado: {len(self.products)} productos")
        return self.products