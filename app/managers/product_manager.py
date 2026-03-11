from app.daos.product_dao import ProductDAO
from app.utils.logger_util import HermesLogger

class ProductManager:
    def __init__(self):
        self.log = HermesLogger.get_logger("PRODUCT_MANAGER")
        self._dao = ProductDAO()
        self._last_results = {}
        self._offsets = {}
        self._page_size = 5

    def initialize_data(self):
        self._dao.load_data()

    def search(self, query: str):
        """Inicia búsqueda y devuelve los primeros resultados."""
        self._last_results = self._dao.find_all_by_query(query)
        self._offsets = {store: 0 for store in self._last_results}
        return self.get_next_page()

    def get_next_page(self):
        """Obtiene el siguiente bloque de la búsqueda actual."""
        page = {}
        for store, products in self._last_results.items():
            start = self._offsets[store]
            end = start + self._page_size
            page[store] = products[start:end]
            self._offsets[store] = end
        return page

    def has_more(self) -> bool:
        """Comprueba si queda algo por mostrar en algún supermercado."""
        return any(self._offsets[store] < len(self._last_results[store]) 
                   for store in self._last_results)