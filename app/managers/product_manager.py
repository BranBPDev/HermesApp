from app.daos.product_dao import ProductDAO

class ProductManager:
    def __init__(self):
        self.dao = ProductDAO()
        self.all_results = []
        self.current_page = 0
        self.page_size = 10

    def sync_with_cloud(self, store_name, products):
        """
        Mantiene la compatibilidad con el ScraperManager.
        Envía los datos recolectados directamente al DAO.
        """
        self.dao.upsert_batch(store_name, products)

    def search(self, query):
        """
        Busca en la nube y prepara la lista global ordenada por precio.
        """
        self.current_page = 0
        self.all_results = self.dao.search_by_name(query)
        return self.get_next_page()

    def get_next_page(self):
        """
        Devuelve el siguiente bloque de 10 productos (mezclando tiendas).
        """
        start = self.current_page * self.page_size
        end = start + self.page_size
        page_items = self.all_results[start:end]
        self.current_page += 1
        return page_items

    def has_more(self):
        """
        Verifica si quedan más productos en la lista global.
        """
        # Usamos el puntero de la página anterior para ver si hay más
        return (self.current_page * self.page_size) < len(self.all_results)