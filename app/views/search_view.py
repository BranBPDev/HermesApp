import tkinter as tk
import customtkinter as ctk

# Importaciones de Estilos
from app.views.styles import (
    COLOR_BG_DARK, COLOR_BG_SIDE, COLOR_PRIMARY, COLOR_TEXT_MAIN,
    FONT_LABEL, FONT_REGULAR, FONT_SM, STYLE_INPUT, STYLE_BUTTON_PRIMARY
)
from app.daos.product_dao import ProductDAO
from app.utils.image_util import ImageLoader
from app.utils.paths_util import get_store_logo_path
from app.utils.logger_util import HermesLogger

class SearchView(ctk.CTkFrame):
    def __init__(self, master, on_add_to_cart):
        super().__init__(master, fg_color=COLOR_BG_DARK)
        self.log = HermesLogger.get_logger("SEARCH_VIEW")
        self.dao = ProductDAO()
        self.on_add_to_cart = on_add_to_cart
        
        # Estado dinámico
        self.all_products = []
        self.current_page = 0
        self.items_per_page = 0
        self.row_height = 60 
        self.canvas_items = []
        self._resize_timer = None
        self.tk_refs = {}

        self._init_widgets()
        self.bind("<Configure>", self._handle_resize_event)
        self._show_results_ui(False)

    def _init_widgets(self):
        # --- TOOLBAR ---
        self.toolbar = ctk.CTkFrame(self, fg_color=COLOR_BG_SIDE, corner_radius=8, height=70)
        self.toolbar.pack(fill="x", pady=(0, 25), padx=20) 
        self.toolbar.pack_propagate(False)
        
        self.search_entry = ctk.CTkEntry(self.toolbar, placeholder_text="Buscar producto...", **STYLE_INPUT)
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(15, 10), pady=10)
        self.search_entry.bind("<Return>", lambda e: self._perform_search())
        
        self.search_btn = ctk.CTkButton(self.toolbar, text="BUSCAR", width=120, **STYLE_BUTTON_PRIMARY, 
                                        command=self._perform_search)
        self.search_btn.pack(side="right", padx=(0, 15), pady=10)

        # --- EMPTY STATE ---
        self.empty_lbl = ctk.CTkLabel(self, text="Introduce un término para comparar precios.\nEjemplo: 'leche', 'aceite'...",
                                     font=FONT_REGULAR, text_color="#666666")
        self.empty_lbl.pack(expand=True)

        # --- FOOTER ---
        self.footer = ctk.CTkFrame(self, fg_color=COLOR_BG_SIDE, height=60, corner_radius=8)

        self.prev_btn = ctk.CTkButton(self.footer, text="<", width=50, fg_color="#222222", 
                                      hover_color=COLOR_PRIMARY, command=self._prev_page)
        self.prev_btn.pack(side="left", padx=20, pady=12)

        self.page_lbl = ctk.CTkLabel(self.footer, text="", font=FONT_LABEL, text_color=COLOR_TEXT_MAIN)
        self.page_lbl.pack(side="left", expand=True)

        self.next_btn = ctk.CTkButton(self.footer, text=">", width=50, fg_color="#222222", 
                                      hover_color=COLOR_PRIMARY, command=self._next_page)
        self.next_btn.pack(side="right", padx=20, pady=12)

        # --- CANVAS ---
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0, borderwidth=0)

    def _show_results_ui(self, show):
        if show:
            self.empty_lbl.pack_forget()
            # Footer pegado abajo
            self.footer.pack(side="bottom", fill="x", pady=(0, 15), padx=20)
            # Canvas pegado al footer con un pequeño margen inferior (pady=(0,10))
            self.canvas.pack(side="bottom", expand=True, fill="both", padx=20, pady=(0, 10))
        else:
            self.canvas.pack_forget()
            self.footer.pack_forget()
            self.empty_lbl.pack(expand=True)

    def _perform_search(self):
        query = self.search_entry.get().strip()
        if not query: return
        results = self.dao.search_by_tag(query)
        self.all_products = results if results else []
        self.current_page = 0
        if self.all_products:
            self._show_results_ui(True)
            self._on_layout_ready()
        else:
            self._show_results_ui(False)
            self.empty_lbl.configure(text=f"No se encontraron resultados para '{query}'")

    def _handle_resize_event(self, event):
        if self._resize_timer:
            self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(150, self._on_layout_ready)

    def _on_layout_ready(self):
        if not self.all_products: return
        self.update_idletasks()
        h, w = self.canvas.winfo_height(), self.canvas.winfo_width()
        if h < 50 or w < 50: return
        self.items_per_page = max(1, h // self.row_height)
        self._create_virtual_rows(w)
        self._render_page()

    def _create_virtual_rows(self, width):
        self.canvas.delete("all")
        self.canvas_items = []
        self.tk_refs.clear() 

        # Centro horizontal simple
        center_x = width / 2

        for i in range(self.items_per_page):
            y = i * self.row_height
            mid_y = y + (self.row_height / 2)
            
            # 1. Fondo (Centrado horizontal)
            rect_w = width - 10
            rect = self.canvas.create_rectangle(center_x - rect_w/2, y+2, center_x + rect_w/2, y+self.row_height-2, 
                                                fill=COLOR_BG_SIDE, outline="#1a1a1a")
            
            # 2. Imagen (Borde minimalista cuadrado para evitar errores de redondeo manual)
            img_bg = self.canvas.create_rectangle(15, y+8, 55, y+52, outline="#333333", width=1)
            img_p = self.canvas.create_image(35, mid_y, image=None)
            
            # 3. Nombre (Tamaño 9, truncado a 20)
            name = self.canvas.create_text(70, mid_y - 10, text="", anchor="w", 
                                          fill=COLOR_TEXT_MAIN, font=(FONT_REGULAR[0], 9))
            
            # 4. Logo Supermercado (Mini logo restaurado)
            logo_s = self.canvas.create_image(70, mid_y + 12, image=None, anchor="w")
            
            # 5. Precios (Tamaño 9)
            p_unit = self.canvas.create_text(width * 0.60, mid_y, text="", 
                                            fill="#888888", font=(FONT_SM[0], 9))
            
            price = self.canvas.create_text(width - 110, mid_y, text="", 
                                           fill=COLOR_PRIMARY, font=("Roboto", 12, "bold"), anchor="e")
            
            # 6. Botón Añadir (Mismo estilo que buscar, rectángulo simple)
            btn_tag = f"btn_add_{i}"
            bx1, by1, bx2, by2 = width-60, mid_y-15, width-30, mid_y+15
            
            self.canvas.create_rectangle(bx1, by1, bx2, by2, fill="#252525", 
                                         outline=COLOR_PRIMARY, width=1, tags=(btn_tag, "shape"))
            self.canvas.create_text(width-45, mid_y, text="+", fill="white", 
                                    font=(FONT_LABEL[0], 11, "bold"), tags=(btn_tag, "text"))

            self.canvas.tag_bind(btn_tag, "<Button-1>", lambda e, idx=i: self._on_row_click(idx))
            self.canvas.tag_bind(btn_tag, "<Enter>", lambda e, t=btn_tag: self._on_btn_hover(t, True))
            self.canvas.tag_bind(btn_tag, "<Leave>", lambda e, t=btn_tag: self._on_btn_hover(t, False))

            self.canvas_items.append({
                "rect": rect, "img_p": img_p, "name": name, 
                "logo_s": logo_s, "p_unit": p_unit, "price": price, "btn": btn_tag
            })

    def _on_btn_hover(self, tag, is_hover):
        color = COLOR_PRIMARY if is_hover else "#252525"
        items = self.canvas.find_withtag(tag)
        for item in items:
            if self.canvas.type(item) == "rectangle":
                self.canvas.itemconfig(item, fill=color)

    def _render_page(self):
        start = self.current_page * self.items_per_page
        data = self.all_products[start : start + self.items_per_page]
        total = max(1, (len(self.all_products) + self.items_per_page - 1) // self.items_per_page)

        for i in range(self.items_per_page):
            row = self.canvas_items[i]
            if i < len(data):
                p = data[i]
                raw_name = p['name']
                display_name = (raw_name[:17] + "...") if len(raw_name) > 20 else raw_name
                
                self.canvas.itemconfig(row["name"], text=display_name)
                self.canvas.itemconfig(row["p_unit"], text=f"{p['price_norm']:.2f}€/{p['unit_type']}")
                self.canvas.itemconfig(row["price"], text=f"{p['price']:.2f} €")
                
                self._async_load_img(p.get('image_url'), row["img_p"], (35, 35))
                
                logo_path = get_store_logo_path(p['store_name'])
                if logo_path:
                    self._async_load_img(logo_path, row["logo_s"], (35, 12))

                self.canvas.itemconfigure(row["rect"], state="normal")
                self.canvas.itemconfigure(row["btn"], state="normal")
            else:
                self.canvas.itemconfigure(row["rect"], state="hidden")
                self.canvas.itemconfigure(row["btn"], state="hidden")

        self.page_lbl.configure(text=f"Página {self.current_page + 1} de {total}")

    def _async_load_img(self, source, canvas_id, size):
        if not source: return
        def callback(imgs):
            self.tk_refs[canvas_id] = imgs["pil"]
            self.canvas.after(0, lambda: self.canvas.itemconfig(canvas_id, image=imgs["pil"]))
        ImageLoader.load_async(source, callback, size=size)

    def _on_row_click(self, index):
        real_idx = (self.current_page * self.items_per_page) + index
        if real_idx < len(self.all_products):
            self.on_add_to_cart(self.all_products[real_idx])

    def _next_page(self):
        if (self.current_page + 1) * self.items_per_page < len(self.all_products):
            self.current_page += 1
            self._render_page()

    def _prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._render_page()