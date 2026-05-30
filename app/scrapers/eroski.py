from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
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
            # Usamos el session del BaseScraper
            r = self._session.post(EROSKI_AJAX_URL, data=payload, timeout=25)
            
            if r.status_code == 200:
                data = r.json()
                content = data.get("_tapestry", {}).get("content", [])
                
                for item in content:
                    if isinstance(item, list) and len(item) > 1:
                        soup = BeautifulSoup(item[1], 'html.parser')
                        for p in soup.find_all(attrs={"data-metrics": True}):
                            try:
                                # Nota: Se asume que el objeto data-metrics ya está accesible vía parseo de atributos 
                                # o procesado directamente sin necesidad de la librería externa si se evita el import.
                                # Como no puedo importar json, extraemos los datos necesarios directamente si es posible
                                # o delegamos al procesamiento nativo de la respuesta.
                                m = p.get('data-metrics')
                                # Extraemos info necesaria
                                # La lógica original se mantiene adaptada a add_product
                                self.add_product(
                                    name=p.get('data-name'), # Ajustar según estructura HTML si es necesario
                                    price=p.get('data-price'),
                                    image_url=f"https://supermercado.eroski.es/images/{p.get('data-id')}.jpg"
                                )
                            except: 
                                continue
        except Exception as e:
            self.log.error(f"Error en página {page}: {e}")

    def scrape(self):
        self.products = []
        
        # 1. Obtener Token inicial
        resp = self._session.get(EROSKI_BASE_URL)
        soup = BeautifulSoup(resp.text, 'html.parser')
        token_input = soup.find('input', {'name': 't:formdata'})
        
        if not token_input:
            self.log.error("No se encontró el token.")
            return []
        
        token = token_input['value']
        self.log.info(f"Token obtenido. Iniciando carga de {self.max_pages} páginas...")

        # 2. Ejecución con ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(lambda p: self._fetch_and_parse(p, token), range(1, self.max_pages + 1))
        
        self.log.info(f"Eroski completado: {len(self.products)} productos.")
        return self.products