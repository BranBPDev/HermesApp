import time
from concurrent.futures import ThreadPoolExecutor
from app.models.scraper_base import BaseScraper
from app.utils.configs_util import (
    GADIS_HEADERS,
    GADIS_API_CATEGORIES,
    GADIS_API_SEARCH
)

class GadisScraper(BaseScraper):

    def __init__(self):
        super().__init__("GADIS", GADIS_HEADERS)
        self.rows_per_page = 100 # Subimos a 100 para ir más rápido
        self._session_ready = False

    def _initialize_session(self):
        if self._session_ready:
            return True
        
        print("[DEBUG-GADIS] Forzando handshake con Gadisline...")
        try:
            # Paso 1: Limpiar y resetear headers para la home
            self.session.cookies.clear()
            
            # Paso 2: Visitar la home simulando un navegador real
            response = self.session.get(
                "https://www.gadisline.com/", 
                timeout=20,
                allow_redirects=True
            )
            
            # Paso 3: Verificar si tenemos la cookie crítica 'next-site'
            cookie_names = [c.name for c in self.session.cookies]
            if 'next-site' in cookie_names or 'OptanonConsent' in cookie_names:
                print(f"[DEBUG-GADIS] Sesion establecida (Cookies: {len(cookie_names)})")
                self._session_ready = True
                return True
            else:
                print("[DEBUG-GADIS] Advertencia: No se recibieron cookies de sesion.")
                # Intentamos seguir de todos modos
                return True
        except Exception as e:
            print(f"[DEBUG-GADIS] Error critico de handshake: {e}")
            return False

    def get_categories(self):
        if not self._initialize_session():
            return []
            
        print("[DEBUG-GADIS] Solicitando arbol de productos...")
        try:
            # Gadis a veces requiere este header extra para la API de categorias
            headers = self.session.headers.copy()
            headers["Accept"] = "application/json, text/plain, */*"
            
            r = self.session.get(GADIS_API_CATEGORIES, headers=headers, timeout=15)
            
            if r.status_code == 200:
                data = r.json()
                # Sacamos todas las categorías del campo 'elements'
                ids = [str(c["id"]) for c in data.get("elements", []) if "id" in c]
                
                # Si no hay en elements, quizás están en una estructura anidada
                if not ids:
                    print("[DEBUG-GADIS] Estructura inusual, intentando parseo profundo...")
                    # Este es un fallback por si cambian el JSON
                    for item in data.get("elements", []):
                        if "children" in item:
                            for child in item["children"]:
                                ids.append(str(child["id"]))

                print(f"[DEBUG-GADIS] Total categorias detectadas: {len(ids)}")
                return list(set(ids)) # Evitar duplicados
            else:
                print(f"[DEBUG-GADIS] Error API: {r.status_code}")
        except Exception as e:
            print(f"[DEBUG-GADIS] Excepcion obteniendo categorias: {e}")
        return []

    def fetch_category(self, category_id):
        page = 1
        collected = []
        
        # Payload base que usa la web
        payload = {
            "minimum_should_match": 1,
            "category_ids": [int(category_id)]
        }

        while True:
            params = {
                "page_number": page,
                "rows_per_page": self.rows_per_page,
                "keep_request": "false",
                "order_field": "relevance",
                "sort_type": "asc"
            }

            try:
                r = self.session.post(
                    GADIS_API_SEARCH,
                    params=params,
                    json=payload,
                    timeout=20
                )

                if r.status_code != 200:
                    break

                data = r.json()
                elements = data.get("elements", [])

                if not elements:
                    break

                collected.extend(elements)
                
                # Si recibimos menos de los pedidos, fin de categoría
                if len(elements) < self.rows_per_page:
                    break
                
                page += 1
                if page > 10: break # Seguridad: no más de 10 páginas por categoría (500-1000 productos)
                
            except:
                break

        return collected

    def scrape(self):
        category_ids = self.get_categories()
        if not category_ids:
            # Si falla la API de categorías, usamos IDs "hardcoded" de las principales como plan B
            print("[DEBUG-GADIS] Fallo API categorias. Usando IDs de emergencia...")
            category_ids = [22601, 22608, 22701, 22718, 22801] # Alimentación, Lácteos, Frescos...

        # Limitamos workers a 3 para Gadis. Es lento pero seguro contra bans.
        with ThreadPoolExecutor(max_workers=3) as executor:
            for products in executor.map(self.fetch_category, category_ids):
                if not products: continue
                
                for p in products:
                    try:
                        # Extraer nombre ES
                        name = None
                        descriptions = p.get("commercial_description", [])
                        for d in descriptions:
                            if d.get("language") == "ES":
                                name = d.get("value")
                                break
                        
                        if not name and descriptions:
                            name = descriptions[0].get("value")
                        
                        if not name: continue

                        self.add_product(
                            name=name,
                            price=p.get("price"),
                            reference_price=p.get("price_kilo_litre"),
                            quantity=p.get("weight"), # Cambiado scale por weight para probar
                            unit_type=None,
                            image_url=p.get("image", {}).get("image")
                        )
                    except:
                        continue

        print(f"[DEBUG-GADIS] Scraping finalizado: {len(self.products)} productos.")
        return self.products

def scrape():
    return GadisScraper().scrape()