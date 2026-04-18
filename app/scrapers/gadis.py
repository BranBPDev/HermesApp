from concurrent.futures import ThreadPoolExecutor
from app.models.scraper_base import BaseScraper
from app.config.scrapers_config import GADIS_HEADERS, GADIS_CATEGORIES, GADIS_API_SEARCH

class GadisScraper(BaseScraper):
    def __init__(self):
        super().__init__("GADIS", GADIS_HEADERS)

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
            # self._session ya tiene los GADIS_HEADERS cargados desde el init
            response = self._session.post(GADIS_API_SEARCH, params=params, json=payload, timeout=20)
            return response.json() if response.ok else None
        except Exception as e:
            self.log.error(f"Error en GADIS (Cat: {category_id}, Pág: {page}): {e}")
            return None

    def _process_category(self, category_id: str):
        page = 1
        while True:
            data = self._fetch_page(category_id, page)
            # Cambiado de 'products' a 'elements' según el test exitoso
            if not data or not data.get('elements'):
                break
                
            products_list = data['elements']
            for p in products_list:
                # Extracción de nombre (ES)
                descriptions = p.get('commercial_description', [])
                nombre = next((d['value'] for d in descriptions if d['language'] == 'ES'), "Sin nombre")
                
                # Extracción de unidad de referencia (ES)
                suffixes = p.get('price_kilo_litre_suffix', [])
                unidad = next((s['value'] for s in suffixes if s['language'] == 'ES'), "ud")

                # URL de imagen
                image_url = p.get('image', {}).get('image', '')

                self.add_product(
                    name=nombre,
                    price=p.get('price', 0.0),
                    reference_price=p.get('price_kilo_litre', 0.0),
                    unit_type=unidad,
                    quantity=1.0, # Valor por defecto ya que Gadis lo incluye en el nombre
                    image_url=image_url
                )
            
            if len(products_list) < 100:
                break
            page += 1

    def scrape(self):
        self.log.info("Iniciando motor GADIS...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self._process_category, GADIS_CATEGORIES)
            
        self.log.info(f"Gadis completado: {len(self.products)} productos.")
        return self.products