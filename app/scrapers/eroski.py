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
        self.log_counter = 0
        self.log_lock = threading.Lock()

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
                                
                                # LOGS DE DEPURACIÓN
                                with self.log_lock:
                                    if self.log_counter < 10:
                                        self.log.info(f"DEBUG EROSKI [{self.log_counter}] - Input: Name='{name}', Price={price}")
                                        self.log_counter += 1
                                
                                # Pasamos los datos crudos, el Manager se encargará de refactorizar
                                self.add_product(
                                    name=name,
                                    price=price,
                                    quantity=1.0, 
                                    unit_type="ud",
                                    image_url=f"https://supermercado.eroski.es/images/{product_data.get('item_id')}.jpg"
                                )
                            except Exception:
                                continue
        except Exception as e:
            self.log.error(f"Error en página {page}: {e}")

    def scrape(self):
        self.products = []
        
        resp = self._session.get(EROSKI_BASE_URL)
        soup = BeautifulSoup(resp.text, 'html.parser')
        token_input = soup.find('input', {'name': 't:formdata'})
        
        if not token_input:
            self.log.error("No se encontró el token.")
            return []
        
        token = token_input['value']
        self.log.info(f"Token obtenido. Iniciando carga de {self.max_pages} páginas...")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(lambda p: self._fetch_and_parse(p, token), range(1, self.max_pages + 1))
        
        self.log.info(f"Eroski completado: {len(self.products)} productos.")
        return self.products