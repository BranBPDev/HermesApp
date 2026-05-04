import tkinter as tk
from app.gui.components.sections.search.search_bar import SearchBar
from app.gui.components.sections.shared.product_list import ProductList
from app.gui.components.sections.shared.feedback_toast import FeedbackToast
from app.gui.styles.styles import COLOR_BG_DARK
from app.managers.product_manager import ProductManager

class SearchSection(tk.Frame):
    def __init__(self, master, on_add, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.pm = ProductManager()
        self.on_add = on_add

        # 1. Barra de búsqueda (Componente extraído)
        self.search_bar = SearchBar(self, on_search=self.run_search)
        self.search_bar.pack(fill="x", padx=10, pady=5)
        
        # 2. Lista de productos (Reutilizable)
        self.list_view = ProductList(self, self._get_data, self._handle_add, "Busca algo para empezar...")
        self.list_view.pack(fill="both", expand=True)

        # 3. Toast para notificaciones (Componente extraído)
        self.toast = FeedbackToast(self)
        self.toast.pack(fill="x", side="bottom")

    def _get_data(self, height):
        # El alto ahora se calcula sobre la lista, no sobre toda la sección
        self.pm.page_size = max(1, int(height // 65))
        return self.pm.get_current_page_items()

    def run_search(self, query):
        self.pm.search(query)
        self.list_view.refresh()

    def _handle_add(self, prod):
        self.on_add(prod)
        # Usamos el método show del componente Toast
        self.toast.show(f"✓ Añadido: {prod['name'][:25]}...")