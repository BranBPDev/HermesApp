import re
import json
import time
from app.models.scraper_base import BaseScraper

class EroskiScraper(BaseScraper):
    def __init__(self):
        # Usamos el User-Agent exacto de tu inspección
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Referer': 'https://supermercado.eroski.es/es/',
            'Connection': 'keep-alive'
        }
        super().__init__("EROSKI", headers)
        
        # Cookies iniciales según tu CURL para fijar la tienda y el idioma
        self._session.cookies.update({
            'supermarket.locale': 'es',
            'supermarket.direct_access': 'true',
            'supermarket.ali.shop': '157',  # Tienda Bilbondo/Coruña
            'supermarket.cookies': '1',
            'supermarket.data_protection': '1'
        })

    def scrape(self):
        # Estas son las subcategorías finales que vimos en tus enlaces
        # El formato es ID-SLUG
        categories = [
            "2060067-aceitunas-y-encurtidos",
            "2059988-aceite-vinagre-sal-harina-y-pan-rallado",
            "2060015-conservas-de-pescado",
            "2059807-leche-batidos-y-bebidas-vegetales"
        ]

        try:
            # Paso 1: "Calentar" la sesión visitando la página principal
            self._session.get("https://supermercado.eroski.es/es/", timeout=15)

            for cat in categories:
                # La URL de carga de página que usa el sistema de Tapestry de Eroski
                cat_id = cat.split('-')[0]
                url = f"https://supermercado.eroski.es/es/supermarket.productlist:loadpage/{cat_id}/1"
                
                # Actualizamos el referer dinámicamente para cada categoría
                self._session.headers.update({
                    'Referer': f'https://supermercado.eroski.es/es/supermercado/2059806-alimentacion/{cat}/',
                    'X-Requested-With': 'XMLHttpRequest'
                })

                resp = self._session.get(url, timeout=20)
                
                if not resp.ok:
                    self.log.warning(f"Categoría {cat} saltada (Status: {resp.status_code})")
                    continue

                # Buscamos el objeto JSON que contiene los datos del producto en el HTML devuelto
                # Eroski inyecta un JSON llamado data-metrics en cada div de producto
                product_blobs = re.findall(r'data-metrics=["\']({.*?})["\']', resp.text)
                
                if not product_blobs:
                    self.log.debug(f"No se encontraron bloques en {cat}")
                    continue

                for blob in product_blobs:
                    try:
                        # Limpiamos el escape de comillas de HTML
                        clean_blob = blob.replace('&quot;', '"')
                        data = json.loads(clean_blob)
                        
                        ecommerce = data.get("ecommerce", {})
                        items = ecommerce.get("items", [])
                        
                        if items:
                            prod = items[0]
                            self.add_product(
                                name=f"{prod.get('item_brand', '')} {prod.get('item_name', '')}".strip(),
                                price=prod.get("price")
                            )
                    except Exception:
                        continue
                
                self.log.info(f"Procesada categoría: {cat}")
                time.sleep(0.5) # Pausa para evitar rate-limit

            # Limpiar duplicados por nombre
            self.products = list({p['nombre']: p for p in self.products}.values())
            return self.products

        except Exception as e:
            self.log.error(f"Fallo crítico en Eroski: {str(e)}")
            return []