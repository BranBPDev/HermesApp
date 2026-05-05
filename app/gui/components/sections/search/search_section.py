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

        # 1. Barra de búsqueda arriba
        self.search_bar = SearchBar(self, on_search=self.run_search)
        self.search_bar.pack(fill="x", padx=10, pady=(0, 5))
        
        # 2. Toast al fondo (fijo)
        self.toast = FeedbackToast(self)
        self.toast.pack(fill="x", side="bottom")

        # 3. Lista de productos llena el resto (el espacio entre search y paginacion interna)
        self.list_view = ProductList(
            self, 
            get_items_func=self._get_data, 
            on_action=self._handle_add, 
            show_action_btn=True,
            pm_ref=self.pm,
            empty_text="Busca algo para empezar..."
        )
        self.list_view.pack(fill="both", expand=True)

    def _get_data(self, height):
        # El alto ahora es el disponible real. 
        # Restamos 60px para el área de paginación visualmente atractiva al fondo
        self.pm.page_size = max(1, int((height - 60) // 65))
        return self.pm.get_current_page_items()

    def run_search(self, query):
        self.pm.search(query)
        self.list_view.refresh()

    def _handle_add(self, prod):
        if self.on_add:
            self.on_add(prod)
            self.toast.show(f"✓ Añadido: {prod.get('name', 'Producto')[:25]}...")