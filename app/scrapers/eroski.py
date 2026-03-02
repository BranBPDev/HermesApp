from app.models.scraper_base import BaseScraper
from app.utils.configs_util import EROSKI_HEADERS, EROSKI_COOKIES
import re, json, time

class EroskiScraper(BaseScraper):
    def __init__(self):
        super().__init__("EROSKI", EROSKI_HEADERS)
        self._session.cookies.update(EROSKI_COOKIES)

    def scrape(self):
        # Usaremos las categorías con su nombre completo, que es lo que espera el loadpage
        categories = [
            "2059988-aceite-vinagre-sal-harina-y-pan-rallado",
            "2060015-conservas-de-pescado",
            "2059807-leche-batidos-y-bebidas-vegetales",
            "2060029-legumbres-arroz-y-pasta"
        ]
        
        try:
            for cat in categories:
                # El endpoint loadpage requiere el ID dentro de la ruta
                # Formato: .../loadpage/ID_CATEGORIA/PAGINA
                cat_id = cat.split('-')[0]
                for page in range(1, 11):
                    # Esta es la URL AJAX "pata negra" que usa su front-end
                    url = f"https://supermercado.eroski.es/es/supermarket.productlist:loadpage/{cat_id}/{page}"
                    
                    resp = self._session.get(url, timeout=15)
                    if not resp.ok or not resp.text: break
                    
                    # Buscamos el JSON de productos
                    blocks = re.findall(r'data-metrics=["\'](\{.*?\})["\']', resp.text)
                    if not blocks: break

                    for b in blocks:
                        try:
                            item = json.loads(b.replace('&quot;', '"'))
                            d = item.get("ecommerce", {}).get("items", [{}])[0]
                            if d.get('item_name'):
                                self.add_product(
                                    name=f"{d.get('item_brand','')} {d.get('item_name','')}".strip(),
                                    price=d.get("price")
                                )
                        except: continue
                    time.sleep(0.1)

            self.products = list({p['nombre']: p for p in self.products}.values())
            return self.products
        except Exception as e:
            self.log.error(f"Error: {e}")
            return []