from app.daos.product_dao import ProductDAO

class ProductManager:
    def __init__(self):
        self.dao = ProductDAO()
        self.all_results = []
        self.current_page = 0
        self.page_size = 10

    def search(self, query):
        self.current_page = 0
        res = self.dao.search_by_name(query)
        self.all_results = res if res else [] 
        return self.get_next_page()

    def get_next_page(self):
        if not self.all_results: return []
        start = self.current_page * self.page_size
        end = start + self.page_size
        page_items = self.all_results[start:end]
        self.current_page += 1
        return page_items

    def has_more(self):
        return (self.current_page * self.page_size) < len(self.all_results)