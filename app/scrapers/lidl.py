from app.models.scraper_base import BaseScraper
from app.utils.configs_util import COMMON_HEADERS, LIDL_API_SEARCH

class LidlScraper(BaseScraper):
    def __init__(self):
        super().__init__("LIDL", COMMON_HEADERS)

    def scrape(self):
        self.session.headers.update({'accept': 'application/json', 'x-requested-with': 'XMLHttpRequest'})
        self.session.get("https://www.lidl.es/", timeout=5)
        data = self.get_json(LIDL_API_SEARCH)
        if not data or 'searchResults' not in data: return []
        for p in data['searchResults']:
            pr = p.get('price', {})
            kf = p.get('gridKeyfacts', [""])
            self.add_prod(p.get('fullTitle'), p.get('brand'), pr.get('currentPrice'), pr.get('basePrice', {}).get('price'), kf[0] if kf else "", p.get('mainImage', {}).get('src'))
        return self.products

def scrape(): return LidlScraper().scrape()