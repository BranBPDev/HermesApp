import requests
from abc import ABC, abstractmethod

class BaseScraper(ABC):

    def __init__(self, name, headers):
        self.name = name
        self.products = []
        self._id_counter = 0

        self.session = requests.Session()
        self.session.headers.update(headers)

        adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
        self.session.mount("https://", adapter)

    @abstractmethod
    def scrape(self):
        pass

    def get_json(self, url, timeout=10):
        try:
            r = self.session.get(url, timeout=timeout)
            if r.status_code != 200:
                return None
            return r.json()
        except:
            return None

    def add_product(self, name, price, reference_price, quantity, unit_type, image_url):
        if name and price is not None:
            self.products.append({
                "id": self._id_counter,
                "nombre": name,
                "precio": float(price),
                "precio_referencia": float(reference_price) if reference_price else None,
                "cantidad": float(quantity) if quantity else None,
                "tipo_unidad": unit_type,
                "imagen": image_url
            })
            self._id_counter += 1