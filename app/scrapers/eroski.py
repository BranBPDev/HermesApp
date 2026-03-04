import asyncio
import httpx
import json
import re
import html
from app.models.scraper_base import BaseScraper
from app.utils.configs_util import EROSKI_HEADERS, EROSKI_CATEGORIES, EROSKI_LOAD_URL, EROSKI_REFERER

class EroskiScraper(BaseScraper):
    def __init__(self):
        super().__init__("EROSKI", EROSKI_HEADERS)
        self.re_metrics = re.compile(r"data-metrics='(\{.*?\})'")
        self.seen_ids = set()

    def _parse_content(self, content):
        """Extrae productos únicos del contenido HTML devuelto por la API."""
        if not content or len(content) < 200:
            return
        
        matches = self.re_metrics.findall(content)
        for m in matches:
            try:
                clean_json = html.unescape(m)
                data = json.loads(clean_json)
                item = data['ecommerce']['items'][0]
                
                uid = str(item['item_id'])
                
                if uid in self.seen_ids:
                    continue
                
                self.seen_ids.add(uid)
                self.add_product(
                    name=item['item_name'],
                    price=item['price'],
                    image_url=f"https://supermercado.eroski.es/images/{uid}.jpg",
                    quantity=item.get('item_variant'),
                    brand=item.get('item_brand', 'Eroski')
                )
            except (KeyError, IndexError, json.JSONDecodeError):
                continue

    async def _fetch_page(self, client, cat_url, page):
        """Petición individual por página."""
        try:
            payload = {
                "t:zoneid": "productListZone",
                "pageNumber": str(page)
            }
            r = await client.post(cat_url, data=payload, timeout=20.0)
            
            if r.status_code == 200:
                resp_data = r.json()
                content = resp_data.get('content', '')
                self._parse_content(content)
        except Exception:
            pass

    async def _async_run(self):
        """Motor asíncrono principal."""
        # Límites optimizados para la ráfaga
        limits = httpx.Limits(max_connections=100, max_keepalive_connections=50)
        
        async with httpx.AsyncClient(
            http2=True, 
            limits=limits, 
            headers=self._session.headers,
            follow_redirects=True
        ) as client:
            
            # Warm-up para cookies
            try:
                await client.get(EROSKI_REFERER, timeout=10.0)
            except Exception:
                pass

            tasks = []
            for cat in EROSKI_CATEGORIES:
                target_url = EROSKI_LOAD_URL.format(cat=cat)
                for page in range(1, 23):
                    tasks.append(self._fetch_page(client, target_url, page))

            await asyncio.gather(*tasks)

    def scrape(self):
        """Punto de entrada compatible con ScraperManager."""
        self.products = []
        self.seen_ids = set()
        
        try:
            # Creamos un loop nuevo para este hilo específico
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self._async_run())
            finally:
                loop.close()
        except Exception as e:
            self.log.error(f"Error crítico en motor Eroski: {e}")
            
        return self.products