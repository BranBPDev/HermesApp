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

        # Barra de búsqueda
        self.search_bar = SearchBar(self, on_search=self.run_search)
        self.search_bar.pack(fill="x", padx=10, pady=5)
        
        # Lista de productos: añadimos pm_ref para habilitar controles de paginación
        self.list_view = ProductList(
            self, 
            get_items_func=self._get_data, 
            on_action=self._handle_add, 
            show_action_btn=True,
            pm_ref=self.pm,
            empty_text="Busca algo para empezar..."
        )
        self.list_view.pack(fill="both", expand=True)

        self.toast = FeedbackToast(self)
        self.toast.pack(fill="x", side="bottom")

    def _get_data(self, height):
        # Cálculo dinámico de items por página según el alto disponible
        # Restamos un poco de espacio para los controles de paginación del fondo
        self.pm.page_size = max(1, int((height - 40) // 65))
        return self.pm.get_current_page_items()

    def run_search(self, query):
        self.pm.search(query)
        self.list_view.refresh()

    def _handle_add(self, prod):
        if self.on_add:
            self.on_add(prod)
            self.toast.show(f"✓ Añadido: {prod.get('name', 'Producto')[:25]}...")