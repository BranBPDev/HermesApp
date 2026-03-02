import requests
from abc import ABC, abstractmethod
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from app.utils.logger_util import HermesLogger

class BaseScraper(ABC):
    def __init__(self, name: str, headers: dict):
        self.name = name
        self.products = []
        self.log = HermesLogger.get_logger(name)
        self._session = self._build_session(headers)

    def _build_session(self, headers: dict) -> requests.Session:
        session = requests.Session()
        session.headers.update(headers)
        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session

    @abstractmethod
    def scrape(self) -> list: pass

    def get_json(self, url: str, **kwargs):
        try:
            resp = self._session.get(url, timeout=15, **kwargs)
            return resp.json() if resp.ok else None
        except Exception as e:
            self.log.error(f"Error JSON en {url}: {e}")
            return None

    def add_product(self, name, price, **kwargs):
        if name and price is not None:
            self.products.append({
                "nombre": str(name).strip(),
                "precio": float(price),
                "precio_referencia": float(kwargs.get('reference_price')) if kwargs.get('reference_price') else None,
                "cantidad": kwargs.get('quantity'),
                "tipo_unidad": kwargs.get('unit_type'),
                "imagen": kwargs.get('image_url')
            })