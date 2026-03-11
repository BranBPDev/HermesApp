import unicodedata
from typing import Dict, List
from app.utils.json_util import read_json
from app.utils.paths_util import PRODUCT_PATHS, SCRAPERS_DIR
from app.utils.dates_util import get_current_date_str
from app.utils.logger_util import HermesLogger

class ProductDAO:
    def __init__(self):
        self.log = HermesLogger.get_logger("PRODUCT_DAO")
        self._cache: Dict[str, List[dict]] = {}

    def load_data(self):
        today = get_current_date_str()
        for store, prefix in PRODUCT_PATHS.items():
            path = SCRAPERS_DIR / f"{prefix.name}_{today}.json"
            if path.exists():
                try:
                    self._cache[store] = read_json(path)
                    self.log.info(f"Cargados {len(self._cache[store])} productos de {store}")
                except Exception as e:
                    self.log.error(f"Error en {store}: {e}")
                    self._cache[store] = []
            else:
                self._cache[store] = []

    def _normalize(self, text: str) -> str:
        if not text: return ""
        return "".join(
            c for c in unicodedata.normalize('NFD', str(text).lower())
            if unicodedata.category(c) != 'Mn'
        )

    def find_all_by_query(self, query: str) -> Dict[str, List[dict]]:
        """Busca y devuelve todos los match ordenados por precio."""
        terms = self._normalize(query).split()
        results = {}

        for store, products in self._cache.items():
            matched = [
                p for p in products
                if all(t in self._normalize(p.get('nombre', '')) for t in terms)
            ]
            results[store] = sorted(matched, key=lambda x: x.get('precio', 999.0))
        
        return results