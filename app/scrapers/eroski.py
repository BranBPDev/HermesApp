from app.models.scraper_base import BaseScraper
from app.utils.configs_util import COMMON_HEADERS, EROSKI_API_SEARCH

class EroskiScraper(BaseScraper):
    def __init__(self):
        super().__init__("EROSKI", COMMON_HEADERS)

    def scrape(self):
        self.session.headers.update({'referer': 'https://compraonline.eroski.es/'})
        data = self.get_json(EROSKI_API_SEARCH)
        if not data or 'products' not in data: return []
        for p in data['products']:
            self.add_prod(p.get('name'), p.get('brandName'), p.get('price', {}).get('amount'), p.get('referencePrice', {}).get('amount'), p.get('quantity'), p.get('image'))
        return self.products

def scrape(): return EroskiScraper().scrape()