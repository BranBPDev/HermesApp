import time
from concurrent.futures import ThreadPoolExecutor
from app.models.scraper_base import BaseScraper
from app.utils.configs_util import (
    COMMON_HEADERS,
    MERCADONA_API_INDEX,
    MERCADONA_API_CAT
)

class MercadonaScraper(BaseScraper):

    def __init__(self):
        super().__init__("MERCADONA", COMMON_HEADERS)

    def get_json(self, url, timeout=10, retries=2):
        """Versión robusta de get_json con retry y tolerancia a códigos no 200"""
        for attempt in range(retries + 1):
            try:
                r = self.session.get(url, timeout=timeout)
                if r.status_code == 403:
                    return None
                # Aceptamos cualquier 2xx
                if 200 <= r.status_code < 300:
                    return r.json()
                # reintentos ante errores 5xx
                if 500 <= r.status_code < 600:
                    time.sleep(0.5)
                    continue
            except:
                time.sleep(0.5)
                continue
        return None

    def fetch_category(self, category_id):
        return self.get_json(MERCADONA_API_CAT.format(cat_id=category_id))

    def scrape(self):
        data = self.get_json(MERCADONA_API_INDEX)
        if not data:
            return []

        category_ids = [
            category["id"]
            for result in data.get("results", [])
            for category in result.get("categories", [])
        ]

        with ThreadPoolExecutor(max_workers=20) as executor:
            for response in executor.map(self.fetch_category, category_ids):
                if not response:
                    continue

                for category in response.get("categories", []):
                    for product in category.get("products", []):

                        price_data = product.get("price_instructions") or {}

                        self.add_product(
                            name=product.get("display_name"),
                            price=price_data.get("unit_price"),
                            reference_price=price_data.get("bulk_price"),
                            quantity=price_data.get("unit_size"),
                            unit_type=price_data.get("reference_format"),
                            image_url=product.get("thumbnail")
                        )
        return self.products

def scrape():
    return MercadonaScraper().scrape()