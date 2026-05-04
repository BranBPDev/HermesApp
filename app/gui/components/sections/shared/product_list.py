import tkinter as tk
import threading
import requests
from io import BytesIO
from PIL import Image, ImageTk
from app.gui.components.shared.visual_elements import ShapeDrawer
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_TEXT_MAIN, COLOR_TEXT_INACTIVE, 
    COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_PRIMARY_ACTIVE, FONT_LABEL, FONT_INPUT
)
from app.config.scrapers_config import EROSKI_HEADERS

class ProductList(tk.Frame):
    def __init__(self, master, get_items_func, on_action, empty_text="No hay productos", **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.get_items_func = get_items_func
        self.on_action = on_action
        self.empty_text = empty_text
        self.img_cache = {}
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.refresh())

    def refresh(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w <= 1: return

        products = self.get_items_func(h) # Pasamos el alto para calcular items_per_page
        
        if not products:
            self.canvas.create_text(w/2, h/2, text=self.empty_text, 
                                   fill=COLOR_TEXT_INACTIVE, font=FONT_INPUT, anchor="center")
            return

        self._draw_table(products, w, h)

    def _draw_table(self, products, w, h):
        header_y, start_y, row_h = 20, 60, 65
        col_img, col_prod, col_super, col_price = 60, w*0.25, w*0.45, w*0.58
        col_unit, col_punit, col_acc = w*0.70, w*0.83, w-50

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

            name = (p['name'][:25] + "..") if len(p['name']) > 25 else p['name']
            self.canvas.create_text(col_prod, y, text=name, fill="white", font=FONT_INPUT, anchor="center")
            self.canvas.create_text(col_super, y, text=str(p['store_name']).upper(), fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")
            self.canvas.create_text(col_price, y, text=f"{p['price']}€", fill=COLOR_TEXT_MAIN, font=FONT_INPUT, anchor="center")
            self.canvas.create_text(col_unit, y, text=p['unit_type'], fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")
            self.canvas.create_text(col_punit, y, text=f"{p['price_norm']}€/{p['unit_type']}", fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")

            # Botón de Acción Reutilizable
            btn_tag = f"btn_{i}"
            rect_id = ShapeDrawer.rounded_rect(self.canvas, col_acc-15, y-15, 30, 30, 5, fill=COLOR_PRIMARY, tags=btn_tag)
            self.canvas.create_text(col_acc, y, text="+", fill="white", font=FONT_INPUT, tags=btn_tag, anchor="center")
            
            self.canvas.tag_bind(btn_tag, "<ButtonRelease-1>", lambda e, prod=p: self.on_action(prod))

    def _draw_product_img(self, url, x, y):
        if not url or url in self.img_cache:
            if url in self.img_cache: self.canvas.create_image(x, y, image=self.img_cache[url], anchor="nw")
            else: self.canvas.create_rectangle(x, y, x+40, y+40, fill="#333333", outline="")
            return
        temp_id = self.canvas.create_rectangle(x, y, x+40, y+40, fill="#222222", outline="")
        threading.Thread(target=self._download_img, args=(url, x, y, temp_id), daemon=True).start()

    def _download_img(self, url, x, y, temp_id):
        try:
            resp = requests.get(url, headers=EROSKI_HEADERS, timeout=5)
            img = Image.open(BytesIO(resp.content)).resize((40, 40), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.img_cache[url] = photo
            self.after(0, lambda: (self.canvas.delete(temp_id), self.canvas.create_image(x, y, image=photo, anchor="nw")))
        except: pass