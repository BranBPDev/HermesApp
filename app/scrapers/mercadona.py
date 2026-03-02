from app.models.scraper_base import BaseScraper
from app.utils.configs_util import COMMON_HEADERS, MERCADONA_API_INDEX, MERCADONA_API_CAT
from concurrent.futures import ThreadPoolExecutor

class MercadonaScraper(BaseScraper):
    def __init__(self):
        super().__init__("MERCADONA", COMMON_HEADERS)

    def scrape(self):
        index = self.get_json(MERCADONA_API_INDEX)
        if not index: return []
        
        cat_ids = [c["id"] for res in index.get("results", []) for c in res.get("categories", [])]
        with ThreadPoolExecutor(max_workers=10) as exe:
            responses = list(exe.map(lambda i: self.get_json(MERCADONA_API_CAT.format(cat_id=i)), cat_ids))

        for data in filter(None, responses):
            for cat in data.get("categories", []):
                for p in cat.get("products", []):
                    i = p.get("price_instructions", {})
                    self.add_product(name=p.get("display_name"), price=i.get("unit_price"), 
                                     image_url=p.get("thumbnail"), quantity=i.get("unit_size"))
        return self.products