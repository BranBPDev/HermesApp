from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests
from app.models.scraper_base import BaseScraper
from app.config.scrapers_config import GADIS_HEADERS, GADIS_CATEGORIES, GADIS_API_SEARCH
from app.utils.logger_util import HermesLogger

class GadisScraper(BaseScraper):
    def __init__(self):
        super().__init__("GADIS", GADIS_HEADERS)
        # Sobrescribimos la sesión del BaseScraper para usar curl_cffi con impersonate
        self._session = requests.Session(impersonate="chrome120")
        self._session.headers.update(GADIS_HEADERS)

    def _fetch_page(self, category_id: str, page: int):
        params = {
            "page_number": str(page),
            "rows_per_page": "100",
            "keep_request": "false",
            "order_field": "relevance",
            "sort_type": "asc"
        }
        payload = {
            "minimum_should_match": 1,
            "category_ids": [category_id]
        }

        try:
            response = self._session.post(GADIS_API_SEARCH, params=params, json=payload, timeout=20)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            HermesLogger.get_logger("GADIS").error(f"Error en GADIS (Cat: {category_id}, Pág: {page}): {e}")
            return None

    def _process_category(self, category_id: str):
        page = 1
        while True:
            data = self._fetch_page(category_id, page)
            
            # Validación de seguridad para evitar errores si la API falla o devuelve vacío
            if not data or not data.get('elements'):
                break
                
            products_list = data['elements']
            
            for p in products_list:
                # Extracción segura de datos
                descriptions = p.get('commercial_description') or []
                nombre = next((d['value'] for d in descriptions if d['language'] == 'ES'), "Sin nombre")
                
                # Extracción segura de imagen
                image_container = p.get('image') or {}
                image_url = image_container.get('image', '')

                # Mapeo a la estructura de la aplicación
                self.add_product(
                    name=nombre,
                    price=p.get('price', 0.0),
                    image_url=image_url
                )
            
            # Si recibimos menos de 100 productos, es la última página
            if len(products_list) < 100:
                break
            page += 1

    def scrape(self):
        self.products = []
        # Usamos ThreadPoolExecutor para procesar las categorías en paralelo
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self._process_category, GADIS_CATEGORIES)
            
        return self.products