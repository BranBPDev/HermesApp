import tkinter as tk
import threading
import requests
from io import BytesIO
from PIL import Image, ImageTk

from app.gui.components.visual_elements import CButton, CInput, ShapeDrawer
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_TEXT_MAIN, COLOR_TEXT_INACTIVE, 
    COLOR_PRIMARY, FONT_LABEL, FONT_INPUT
)
from app.managers.product_manager import ProductManager

class Search(tk.Frame):
    def __init__(self, master, on_add, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.on_add = on_add
        self.pm = ProductManager()
        self.img_cache = {}
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.inp = CInput(self.canvas, "BUSCAR PRODUCTO", "Escribe el nombre del producto...")
        self.btn = CButton(self.canvas, "BUSCAR", self.execute_search)
        
        self.canvas.bind("<Configure>", lambda e: self._draw())
        self.master.winfo_toplevel().bind("<Return>", lambda e: self.execute_search())

    def execute_search(self):
        query = self.inp.get()
        if query:
            self.pm.search(query)
            self._draw()

    def _draw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        # Evita renderizar si la ventana aún no se ha dibujado (w <= 1)
        if w <= 1: return 
        
        # 1. Buscador (Input + Botón)
        self.inp.draw(30, 40, w=w-200)
        self.btn.draw(w-150, 40, w=120)

        query = self.inp.get()
        products = self.pm.get_current_page_items()
        
        # 2. Lógica de resultados
        if query and not products:
            self._draw_no_results(w, h)
            return
        
        if products:
            self._draw_table(products, w)
            self._draw_pagination(w, h)

    def _draw_no_results(self, w, h):
        msg = f"No se encontraron resultados para: '{self.inp.get()}'"
        self.canvas.create_text(w/2, h/2, text=msg, fill=COLOR_TEXT_INACTIVE, font=FONT_INPUT)

    def _draw_table(self, products, w):
        # Configuración de columnas (Posición X, Título)
        cols = [
            (35, "IMG"),
            (100, "PRODUCTO"),
            (w * 0.45, "SUPER"),
            (w * 0.58, "PRECIO"),
            (w * 0.68, "UNIDAD"),
            (w * 0.78, "P. UNIT"),
            (w * 0.90, "ACC")
        ]

        # Cabecera
        header_y = 110
        for x, title in cols:
            self.canvas.create_text(x, header_y, text=title, fill=COLOR_PRIMARY, font=FONT_LABEL, anchor="w")
        
        self.canvas.create_line(30, header_y + 15, w-30, header_y + 15, fill="#333333")

        # Lista de productos
        start_y = 150
        row_h = 60

        for i, p in enumerate(products):
            y = start_y + (i * row_h)
            
            # Fondo de fila alterno
            bg_color = "#1a1a1a" if i % 2 == 0 else COLOR_BG_DARK
            ShapeDrawer.rounded_rect(self.canvas, 25, y-20, w-50, row_h-10, 8, fill=bg_color)

            # 1. Imagen (Carga asíncrona)
            self._draw_product_img(p.get('image_url'), 35, y-15)

            # 2. Nombre abreviado
            name = p['name'][:35] + "..." if len(p['name']) > 35 else p['name']
            self.canvas.create_text(100, y, text=name, fill="white", font=FONT_INPUT, anchor="w")

            # 3. Logo Super (Texto por ahora)
            store = p.get('store_name', '??').upper()
            self.canvas.create_text(w * 0.45, y, text=store, fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="w")

            # 4. Precio
            self.canvas.create_text(w * 0.58, y, text=f"{p['price']}€", fill=COLOR_TEXT_MAIN, font=FONT_INPUT, anchor="w")

            # 5. Sistema unitario
            self.canvas.create_text(w * 0.68, y, text=p['unit_type'], fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="w")

            # 6. Precio unitario
            self.canvas.create_text(w * 0.78, y, text=f"{p['price_norm']}€/{p['unit_type']}", fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="w")

            # 7. Botón añadir (+ centrado al final)
            btn_tag = f"add_{p.get('id', i)}_{i}"
            ShapeDrawer.rounded_rect(self.canvas, w-60, y-15, 30, 30, 5, fill=COLOR_PRIMARY, tags=btn_tag)
            self.canvas.create_text(w-45, y, text="+", fill="white", font=FONT_INPUT, tags=btn_tag)
            self.canvas.tag_bind(btn_tag, "<Button-1>", lambda e, prod=p: self.on_add(prod))

    def _draw_pagination(self, w, h):
        footer_y = h - 30
        page_text = f"Página {self.pm.current_page + 1}"
        
        self.canvas.create_text(w/2, footer_y, text=page_text, fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL)
        
        if self.pm.current_page > 0:
            prev_tag = "prev_page"
            self.canvas.create_text(w/2 - 60, footer_y, text="< Ant", fill=COLOR_PRIMARY, font=FONT_LABEL, tags=prev_tag)
            self.canvas.tag_bind(prev_tag, "<Button-1>", lambda e: self._change_page(-1))

        if self.pm.has_more():
            next_tag = "next_page"
            self.canvas.create_text(w/2 + 60, footer_y, text="Sig >", fill=COLOR_PRIMARY, font=FONT_LABEL, tags=next_tag)
            self.canvas.tag_bind(next_tag, "<Button-1>", lambda e: self._change_page(1))

    def _change_page(self, delta):
        if delta > 0: 
            self.pm.get_next_page()
        else: 
            self.pm.current_page = max(0, self.pm.current_page - 1)
        self._draw()

    def _draw_product_img(self, url, x, y):
        if not url or not str(url).startswith("http"):
            self.canvas.create_rectangle(x, y, x+40, y+40, fill="#333333", outline="")
            return

        if url in self.img_cache:
            self.canvas.create_image(x, y, image=self.img_cache[url], anchor="nw")
            return

        temp_id = self.canvas.create_rectangle(x, y, x+40, y+40, fill="#222222", outline="")
        threading.Thread(target=self._download_and_prepare_img, args=(url, x, y, temp_id), daemon=True).start()

    def _download_and_prepare_img(self, url, x, y, temp_id):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            img_data = Image.open(BytesIO(response.content))
            img_data = img_data.resize((40, 40), Image.Resampling.LANCZOS)
            
            self.after(0, lambda: self._render_downloaded_image(url, img_data, x, y, temp_id))
        except Exception:
            pass

    def _render_downloaded_image(self, url, pil_img, x, y, temp_id):
        photo = ImageTk.PhotoImage(pil_img)
        self.img_cache[url] = photo
        self.canvas.delete(temp_id)
        self.canvas.create_image(x, y, image=photo, anchor="nw")