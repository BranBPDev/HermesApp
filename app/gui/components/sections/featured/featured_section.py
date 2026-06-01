import tkinter as tk
from app.gui.components.common.product_list import ProductList
from app.gui.components.common.feedback_toast import FeedbackToast
from app.gui.styles.styles import COLOR_BG_DARK, FONT_TITLE
from app.managers.product_manager import ProductManager

class FeaturedSection(tk.Frame):
    def __init__(self, master, on_add, on_select, page=0, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.pm = ProductManager()
        self.on_add = on_add
        self.on_select = on_select

        self.header = tk.Label(
            self, text="Productos Destacados", font=FONT_TITLE, 
            bg=COLOR_BG_DARK, fg="white", pady=10
        )
        self.header.pack(fill="x")

        self.toast = FeedbackToast(self)
        self.toast.pack(fill="x", side="bottom")

        self.list_view = ProductList(
            self, 
            get_items_func=self._get_featured_data, 
            on_action=self._handle_add,
            on_select=self.on_select,
            show_action_btn=True,
            initial_page=page,
            empty_text="No hay productos destacados disponibles."
        )
        self.list_view.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.pm.load_featured()
        self.after(100, self.refresh)

    def get_current_page(self):
        return self.list_view.current_page

    def set_page(self, page):
        self.list_view.current_page = page
        self.refresh()

    def _get_featured_data(self, page, page_size):
        all_items = self.pm.all_results
        start = page * page_size
        end = start + page_size
        return all_items[start:end], len(all_items)

    def _handle_add(self, prod):
        if self.on_add:
            self.on_add(prod)
            self.toast.show(f"✓ Añadido: {prod.get('name', 'Producto')[:25]}...")

    def refresh(self):
        self.update_idletasks()
        self.list_view.refresh()