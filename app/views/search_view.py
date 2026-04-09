import customtkinter as ctk
from app.components.scrollable_list import ScrollableList
from app.components.pagination_footer import PaginationFooter
from app.components.product_row import ProductRow
from app.managers.product_manager import ProductManager
from app.views.styles import COLOR_PRIMARY

class SearchView(ctk.CTkFrame):
    def __init__(self, master, on_add_to_cart):
        super().__init__(master, fg_color="transparent")
        self.prod_manager = ProductManager()
        self.on_add_to_cart = on_add_to_cart
        
        self._init_widgets()

    def _init_widgets(self):
        # Toolbar (Buscador + Filtros)
        self.toolbar = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=8, height=64)
        self.toolbar.pack(fill="x", pady=(0, 20))
        self.toolbar.pack_propagate(False)
        
        self.search_entry = ctk.CTkEntry(self.toolbar, placeholder_text="Buscar por tag (ej: leche, huevos...)", 
                                         height=40, fg_color="#242424", border_width=1, border_color="#333333")
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(15, 10), pady=12)
        self.search_entry.bind("<Return>", lambda e: self._perform_search())
        
        self.sort_filter = ctk.CTkOptionMenu(self.toolbar, values=["Precio (Menor)", "Precio (Mayor)", "Nombre"], 
                                             height=40, fg_color="#242424", button_color=COLOR_PRIMARY, width=160)
        self.sort_filter.pack(side="left", padx=(0, 10), pady=12)

        ctk.CTkButton(self.toolbar, text="BUSCAR", height=40, fg_color=COLOR_PRIMARY, font=("Roboto", 13, "bold"),
                      command=self._perform_search, width=110).pack(side="right", padx=(0, 15), pady=12)

        # Estado vacío
        self.empty_label = ctk.CTkLabel(self, text="Introduce un término para comparar precios.", 
                                        font=("Roboto", 13), text_color="#666666")
        self.empty_label.pack(expand=True)

        # Componentes de lista (ocultos inicialmente)
        self.table_header = self._create_table_header()
        self.results_list = ScrollableList(self)
        self.pagination = PaginationFooter(self, self._load_next_page)

    def _create_table_header(self):
        header = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=8)
        lbl_style = {"font": ("Roboto", 10, "bold"), "text_color": "#777777"}
        sep_style = {"text": "┊", "text_color": "#333333", "font": ("Roboto", 16)}
        
        ctk.CTkLabel(header, text="PRODUCTO", anchor="center", **lbl_style).pack(side="left", padx=(80, 0), expand=True, fill="x")
        ctk.CTkLabel(header, **sep_style).pack(side="left")
        ctk.CTkLabel(header, text="SUPERMERCADO", width=120, anchor="center", **lbl_style).pack(side="left", padx=10)
        ctk.CTkLabel(header, **sep_style).pack(side="left")
        ctk.CTkLabel(header, text="PRECIO UNITARIO", width=100, anchor="center", **lbl_style).pack(side="left", padx=5)
        ctk.CTkLabel(header, **sep_style).pack(side="left")
        ctk.CTkLabel(header, text="PRECIO TOTAL", width=100, anchor="center", **lbl_style).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="", width=60).pack(side="left", padx=(5, 15))
        return header

    def _perform_search(self):
        query = self.search_entry.get().strip()
        if not query: return
        mapping = {"Precio (Menor)": "p.price_norm ASC", "Precio (Mayor)": "p.price_norm DESC", "Nombre": "p.name ASC"}
        sort_sql = mapping.get(self.sort_filter.get(), "p.price_norm ASC")
        self.results_list.clear()
        products = self.prod_manager.search(query, order_by=sort_sql)
        self._render_results(products)

    def _render_results(self, products):
        if not products:
            self.table_header.pack_forget()
            self.results_list.pack_forget()
            self.pagination.show(False)
            self.empty_label.pack(expand=True)
            return
        self.empty_label.pack_forget()
        self.table_header.pack(fill="x", pady=(5, 2))
        self.results_list.pack(expand=True, fill="both")
        self.results_list.render_items(products, ProductRow, self.on_add_to_cart)
        self.pagination.show(self.prod_manager.has_more())

    def _load_next_page(self):
        products = self.prod_manager.get_next_page()
        if products:
            self.results_list.render_items(products, ProductRow, self.on_add_to_cart)
        self.pagination.show(self.prod_manager.has_more())