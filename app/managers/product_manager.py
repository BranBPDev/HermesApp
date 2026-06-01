from app.daos.product_dao import ProductDAO
from app.utils.logger_util import HermesLogger

class ProductManager:
    def __init__(self):
        self.dao = ProductDAO()
        self.log = HermesLogger.get_logger("PRODUCT_MANAGER")
        self.all_results = []
        self.current_page = 0
        self.page_size = 15 

    def search(self, query):
        self.log.info(f"Iniciando búsqueda con query: '{query}'")
        self.current_page = 0
        res = self.dao.search_by_tag(query)
        self.all_results = res if res else [] 
        self.log.info(f"Búsqueda finalizada. Encontrados: {len(self.all_results)} resultados.")
        return self.get_current_page_items()

    def load_featured(self):
        self.log.info("Cargando productos destacados.")
        self.current_page = 0
        res = self.dao.get_top_rated(20)
        self.all_results = res if res else []
        return self.get_current_page_items()

    def get_next_page(self):
        if self.has_more():
            self.current_page += 1
            self.log.debug(f"Cargando página {self.current_page}")
            return self.get_current_page_items()
        return []

    def get_current_page_items(self):
        if not self.all_results: return []
        start = self.current_page * self.page_size
        end = start + self.page_size
        return self.all_results[start:end]

    def has_more(self):
        return ((self.current_page + 1) * self.page_size) < len(self.all_results)