import tkinter as tk
import threading
import requests
from io import BytesIO
from PIL import Image, ImageTk

from app.gui.components.visual_elements import CButton, CInput, ShapeDrawer
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_TEXT_MAIN, COLOR_TEXT_INACTIVE, 
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_PRIMARY_ACTIVE, FONT_LABEL, FONT_INPUT
)
from app.managers.product_manager import ProductManager
from app.config.scrapers_config import EROSKI_HEADERS

class Search(tk.Frame):
    def __init__(self, master, on_add, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.on_add = on_add
        self.pm = ProductManager()
        self.img_cache = {}
        self.feedback_msg = "" # Variable para el mensaje de éxito
        
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

    def show_feedback(self, product_name):
        """Muestra un mensaje temporal de producto añadido"""
        short_name = (product_name[:30] + "..") if len(product_name) > 30 else product_name
        self.feedback_msg = f"✓ Añadido: {short_name}"
        self._draw()
        # El mensaje desaparece a los 3 segundos
        self.after(3000, self.clear_feedback)

    def clear_feedback(self):
        self.feedback_msg = ""
        self._draw()

    def handle_add(self, product):
        """Gestiona la acción de añadir y dispara el feedback visual"""
        self.on_add(product)
        self.show_feedback(product.get('name', 'Producto'))

    def _draw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w <= 1 or h <= 1: return 

        self.inp.draw(30, 40, w=w-200)
        self.btn.draw(w-150, 40, w=120)

        header_y = 110
        footer_h = 60
        table_start_y = 150
        # Dejamos un margen extra de 25px para el mensaje de feedback
        available_height = h - table_start_y - footer_h - 25
        row_h = 65

        items_per_page = max(1, int(available_height // row_h))
        self.pm.page_size = items_per_page
        
        products = self.pm.get_current_page_items()
        
        if self.inp.get() and not products:
            self.canvas.create_text(w/2, h/2, text=f"No hay resultados para '{self.inp.get()}'", 
                                   fill=COLOR_TEXT_INACTIVE, font=FONT_INPUT, anchor="center")
            return
        
        if products:
            self._draw_table(products, w, header_y, table_start_y, row_h)
            self._draw_pagination(w, h, footer_h)

    def _draw_table(self, products, w, header_y, start_y, row_h):
        col_img = 60
        col_prod = w * 0.25
        col_super = w * 0.45
        col_price = w * 0.58
        col_unit = w * 0.70
        col_punit = w * 0.83
        col_acc = w - 50

        headers = [(col_prod, "PRODUCTO"), (col_super, "SUPER"), (col_price, "PRECIO"), 
                   (col_unit, "UNIDAD"), (col_punit, "P. UNIT")]
        
        for x, title in headers:
            self.canvas.create_text(x, header_y, text=title, fill=COLOR_PRIMARY, font=FONT_LABEL, anchor="center")
        
        self.canvas.create_line(30, header_y + 15, w-30, header_y + 15, fill="#333333")

        for i, p in enumerate(products):
            y = start_y + (i * row_h)
            bg_color = "#1a1a1a" if i % 2 == 0 else COLOR_BG_DARK
            ShapeDrawer.rounded_rect(self.canvas, 25, y-25, w-50, row_h-10, 8, fill=bg_color)

            self._draw_product_img(p.get('image_url'), col_img - 20, y-20)

            raw_name = p.get('name', '???')
            name = (raw_name[:25] + "..") if len(raw_name) > 25 else raw_name
            self.canvas.create_text(col_prod, y, text=name, fill="white", font=FONT_INPUT, anchor="center")

            store = str(p.get('store_name', '??')).upper()
            self.canvas.create_text(col_super, y, text=store, fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")

            self.canvas.create_text(col_price, y, text=f"{p['price']}€", fill=COLOR_TEXT_MAIN, font=FONT_INPUT, anchor="center")
            self.canvas.create_text(col_unit, y, text=p['unit_type'], fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")
            self.canvas.create_text(col_punit, y, text=f"{p['price_norm']}€/{p['unit_type']}", fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")

            btn_tag = f"add_{i}_{p.get('id')}"
            rect_id = ShapeDrawer.rounded_rect(self.canvas, col_acc-15, y-15, 30, 30, 5, fill=COLOR_PRIMARY, tags=btn_tag)
            self.canvas.create_text(col_acc, y, text="+", fill="white", font=FONT_INPUT, tags=btn_tag, anchor="center")
            
            self.canvas.tag_bind(btn_tag, "<Enter>", lambda e, rid=rect_id: self.canvas.itemconfig(rid, fill=COLOR_PRIMARY_HOVER))
            self.canvas.tag_bind(btn_tag, "<Leave>", lambda e, rid=rect_id: self.canvas.itemconfig(rid, fill=COLOR_PRIMARY))
            self.canvas.tag_bind(btn_tag, "<Button-1>", lambda e, rid=rect_id, tag=btn_tag: (
                self.canvas.itemconfig(rid, fill=COLOR_PRIMARY_ACTIVE),
                self.canvas.move(tag, 1, 1)
            ))
            self.canvas.tag_bind(btn_tag, "<ButtonRelease-1>", lambda e, rid=rect_id, tag=btn_tag, prod=p: (
                self.canvas.move(tag, -1, -1),
                self.canvas.itemconfig(rid, fill=COLOR_PRIMARY_HOVER),
                self.handle_add(prod) # Llamada a la nueva función de gestión
            ))

    def _draw_pagination(self, w, h, footer_h):
        footer_y = h - (footer_h / 2)
        
        # Área de feedback: justo encima de la línea del footer
        if self.feedback_msg:
            self.canvas.create_text(w/2, h - footer_h - 15, text=self.feedback_msg, 
                                   fill=COLOR_PRIMARY, font=FONT_LABEL, anchor="center")

        self.canvas.create_rectangle(0, h - footer_h, w, h, fill=COLOR_BG_DARK, outline="")
        self.canvas.create_line(30, h - footer_h, w - 30, h - footer_h, fill="#222222")

        page_text = f"Página {self.pm.current_page + 1}"
        self.canvas.create_text(w/2, footer_y, text=page_text, fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")
        
        if self.pm.current_page > 0:
            prev_tag = "prev_page"
            self.canvas.create_text(w/2 - 100, footer_y, text="< ANTERIOR", fill=COLOR_PRIMARY, font=FONT_LABEL, tags=prev_tag, anchor="center")
            self.canvas.tag_bind(prev_tag, "<Button-1>", lambda e: self._change_page(-1))

        if self.pm.has_more():
            next_tag = "next_page"
            self.canvas.create_text(w/2 + 100, footer_y, text="SIGUIENTE >", fill=COLOR_PRIMARY, font=FONT_LABEL, tags=next_tag, anchor="center")
            self.canvas.tag_bind(next_tag, "<Button-1>", lambda e: self._change_page(1))

    def _change_page(self, delta):
        if delta > 0: self.pm.current_page += 1
        else: self.pm.current_page = max(0, self.pm.current_page - 1)
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
            resp = requests.get(url, headers=EROSKI_HEADERS, timeout=5)
            resp.raise_for_status() 
            img = Image.open(BytesIO(resp.content)).resize((40, 40), Image.Resampling.LANCZOS)
            self.after(0, lambda: self._render_downloaded_image(url, img, x, y, temp_id))
        except:
            pass # Silenciamos errores de carga individual para limpiar la consola

    def _render_downloaded_image(self, url, pil_img, x, y, temp_id):
        photo = ImageTk.PhotoImage(pil_img)
        self.img_cache[url] = photo
        self.canvas.delete(temp_id)
        self.canvas.create_image(x, y, image=photo, anchor="nw")