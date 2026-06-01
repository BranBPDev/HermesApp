import json
import threading
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from app.models.scraper_base import BaseScraper
from app.config.scrapers_config import EROSKI_HEADERS, EROSKI_BASE_URL, EROSKI_AJAX_URL

class EroskiScraper(BaseScraper):
    def __init__(self):
        super().__init__("EROSKI", EROSKI_HEADERS)
        self.max_pages = 50
        self.max_workers = 10

    def _fetch_and_parse(self, page, token):
        payload = {"t:zoneid": "productListZone", "t:formdata": token, "pageNumber": str(page)}
        
        try:
            r = self._session.post(EROSKI_AJAX_URL, data=payload, timeout=25)
            
            if r.status_code == 200:
                data = r.json()
                content = data.get("_tapestry", {}).get("content", [])
                
                for item in content:
                    if isinstance(item, list) and len(item) > 1:
                        soup = BeautifulSoup(item[1], 'html.parser')
                        for p in soup.find_all(attrs={"data-metrics": True}):
                            try:
                                m = json.loads(p.get('data-metrics'))
                                product_data = m.get("ecommerce", {}).get("items", [{}])[0]
                                
                                if not product_data:
                                    continue
                                
                                name = product_data.get("item_name")
                                price = product_data.get("price")
                                
                                # Pasamos los datos mínimos necesarios
                                self.add_product(
                                    name=name,
                                    price=price,
                                    image_url=f"https://supermercado.eroski.es/images/{product_data.get('item_id')}.jpg"
                                )
                            except Exception:
                                continue
        except Exception as e:
            from app.utils.logger_util import HermesLogger
            HermesLogger.get_logger("EROSKI").error(f"Error en página {page}: {e}")

    def scrape(self):
        self.products = []
        
        resp = self._session.get(EROSKI_BASE_URL)
        soup = BeautifulSoup(resp.text, 'html.parser')
        token_input = soup.find('input', {'name': 't:formdata'})
        
        if not token_input:
            return []
        
        token = token_input['value']

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(lambda p: self._fetch_and_parse(p, token), range(1, self.max_pages + 1))
        
        return self.products