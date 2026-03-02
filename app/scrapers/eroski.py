from app.models.scraper_base import BaseScraper
from app.utils.configs_util import EROSKI_HEADERS, EROSKI_COOKIES, EROSKI_BASE_CAT_URL
import re, json, time

class EroskiScraper(BaseScraper):
    def __init__(self):
        super().__init__("EROSKI", EROSKI_HEADERS)
        # Inyectamos cookies para evitar redirecciones y 404s
        self._session.cookies.update(EROSKI_COOKIES)

    def scrape(self):
        categories = [
            "2059988-aceite-vinagre-sal-harina-y-pan-rallado",
            "2060015-conservas-de-pescado",
            "2059807-leche-batidos-y-bebidas-vegetales",
            "2060029-legumbres-arroz-y-pasta",
            "2059818-yogures"
        ]
        
        try:
            self.log.info("Iniciando escaneo optimizado...")
            
            for cat in categories:
                for page in range(1, 11):
                    url = EROSKI_BASE_CAT_URL.format(cat=cat, page=page)
                    resp = self._session.get(url, timeout=15)
                    
                    if not resp.ok:
                        self.log.error(f"Error {resp.status_code} en {cat} p{page}")
                        break
                    
                    blocks = re.findall(r'data-metrics=["\'](\{.*?\})["\']', resp.text)
                    if not blocks: break

                    for b in blocks:
                        try:
                            clean_json = b.replace('&quot;', '"')
                            item_data = json.loads(clean_json)
                            items = item_data.get("ecommerce", {}).get("items", [{}])
                            if items and items[0]:
                                d = items[0]
                                self.add_product(
                                    name=f"{d.get('item_brand','')} {d.get('item_name','')}".strip(), 
                                    price=d.get("price")
                                )
                        except: continue
                    time.sleep(0.05)

            # Eliminar duplicados por nombre
            self.products = list({p['nombre']: p for p in self.products}.values())
            return self.products

        except Exception:
            self.log.exception("Error fatal en Eroski")
            return []