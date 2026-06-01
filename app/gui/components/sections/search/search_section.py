import tkinter as tk
from app.gui.components.sections.search.search_bar import SearchBar
from app.gui.components.common.product_list import ProductList
from app.gui.components.common.feedback_toast import FeedbackToast
from app.gui.styles.styles import COLOR_BG_DARK
from app.managers.product_manager import ProductManager

class SearchSection(tk.Frame):
    def __init__(self, master, on_add, on_select, page=0, initial_query='', **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.pm = ProductManager()
        self.on_add = on_add
        self.on_select = on_select

        self.search_bar = SearchBar(self, on_search=self.run_search)
        self.search_bar.pack(fill="x", padx=10, pady=(10, 5))
        
        self.toast = FeedbackToast(self)
        self.toast.pack(fill="x", side="bottom")

        self.list_view = ProductList(
            self, 
            get_items_func=self._get_data, 
            on_action=self._handle_add,
            on_select=self.on_select,
            show_action_btn=True,
            initial_page=page,
            empty_text="Busca algo para empezar..."
        )
        self.list_view.pack(fill="both", expand=True, padx=10)
        
        if initial_query:
            self.search_bar.set_query(initial_query)
            self.run_search(initial_query)
            self.set_page(page)

    def get_query(self):
        return self.search_bar.get_query()

    def get_current_page(self):
        return self.list_view.current_page

    def set_page(self, page):
        self.list_view.current_page = page
        self.list_view.refresh()

    def _get_data(self, page, page_size):
        self.pm.page_size = page_size
        self.pm.current_page = page
        return self.pm.get_current_page_items(), len(self.pm.all_results)

    def run_search(self, query):
        self.pm.search(query)
        self.list_view.current_page = 0
        self.list_view.refresh()

    def _handle_add(self, prod):
        if self.on_add:
            self.on_add(prod)
            self.toast.show(f"✓ Añadido: {prod.get('name', 'Producto')[:25]}...")