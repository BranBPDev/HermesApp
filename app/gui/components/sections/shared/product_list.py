import tkinter as tk
import threading
import requests
from io import BytesIO
from PIL import Image, ImageTk
from app.gui.components.shared.visual_elements import ShapeDrawer
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_TEXT_MAIN, COLOR_TEXT_INACTIVE, 
    COLOR_PRIMARY, FONT_LABEL, FONT_INPUT, COLOR_BADGE_BG
)
from app.config.scrapers_config import EROSKI_HEADERS
import logging

class ProductList(tk.Frame):
    def __init__(self, master, get_items_func, on_action=None, empty_text="No hay productos", show_action_btn=True, pm_ref=None, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.log = logging.getLogger("PRODUCT_LIST")
        self.get_items_func = get_items_func
        self.on_action = on_action
        self.empty_text = empty_text
        self.show_action_btn = show_action_btn
        self.pm = pm_ref  
        self.img_cache = {}
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.refresh())

    def refresh(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w <= 1: return

        # Paginación al fondo (ocupará unos 50px)
        products = self.get_items_func(h)
        
        if not products:
            self.canvas.create_text(w/2, h/2, text=self.empty_text, 
                                   fill=COLOR_TEXT_INACTIVE, font=FONT_INPUT, anchor="center")
            return

        self._draw_table(products, w, h)
        if self.pm:
            self._draw_pagination(w, h)

    def _draw_table(self, products, w, h):
        header_y, start_y, row_h = 20, 60, 65
        margin_right = 50 if self.show_action_btn else 25
        
        col_img, col_prod, col_super, col_price = 60, w*0.28, w*0.48, w*0.60
        col_unit, col_punit, col_acc = w*0.72, w*0.84, w - margin_right

        headers = [(col_prod, "PRODUCTO"), (col_super, "SUPER"), (col_price, "PRECIO"), 
                   (col_unit, "UNIDAD"), (col_punit, "P. UNIT")]
        
        for x, title in headers:
            self.canvas.create_text(x, header_y, text=title, fill=COLOR_PRIMARY, font=FONT_LABEL, anchor="center")
        
        self.canvas.create_line(30, header_y + 15, w-30, header_y + 15, fill="#333333")

        for i, p in enumerate(products):
            y = start_y + (i * row_h)
            # Solo dibujamos si no se sale del área (dejando espacio para paginación)
            if y + row_h/2 > h - 50: break

            bg_color = "#1a1a1a" if i % 2 == 0 else COLOR_BG_DARK
            ShapeDrawer.rounded_rect(self.canvas, 25, y-25, w-50, row_h-10, 8, fill=bg_color)
            
            img_url = p.get('image_url') or p.get('img_url')
            self._draw_product_img(img_url, 40, y-20)

            full_name = p.get('name', 'Producto sin nombre')
            name = (full_name[:25] + "..") if len(full_name) > 25 else full_name
            
            self.canvas.create_text(col_prod, y, text=name, fill="white", font=FONT_INPUT, anchor="center")
            self.canvas.create_text(col_super, y, text=str(p.get('store_name', 'N/A')).upper(), fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")
            self.canvas.create_text(col_price, y, text=f"{p.get('price', 0)}€", fill=COLOR_TEXT_MAIN, font=FONT_INPUT, anchor="center")
            self.canvas.create_text(col_unit, y, text=p.get('unit_type', 'ud'), fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")
            self.canvas.create_text(col_punit, y, text=f"{p.get('price_norm', 0)}€", fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")

            if self.show_action_btn and self.on_action:
                btn_tag = f"btn_{i}"
                ShapeDrawer.rounded_rect(self.canvas, col_acc-15, y-15, 30, 30, 5, fill=COLOR_PRIMARY, tags=btn_tag)
                self.canvas.create_text(col_acc, y, text="+", fill="white", font=FONT_INPUT, tags=btn_tag, anchor="center")
                self.canvas.tag_bind(btn_tag, "<ButtonRelease-1>", lambda e, prod=p: self.on_action(prod))

    def _draw_pagination(self, w, h):
        curr = self.pm.current_page + 1
        has_prev = self.pm.current_page > 0
        has_next = self.pm.has_more()
        
        y_pos = h - 30 # Pegado al fondo
        x_center = w / 2
        
        # Estilo visual atractivo: Botones circulares
        def draw_page_btn(x, text, active, delta=None):
            tag = f"page_btn_{text}"
            color = COLOR_PRIMARY if active else "#333333"
            text_color = "white" if active else COLOR_TEXT_INACTIVE
            
            ShapeDrawer.rounded_rect(self.canvas, x-15, y_pos-15, 30, 30, 15, fill=color, tags=tag)
            self.canvas.create_text(x, y_pos, text=text, fill=text_color, font=FONT_INPUT, tags=tag)
            
            if delta is not None and active:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e: self._change_page(delta))
                self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.config(cursor=""))

        # Dibujar elementos
        draw_page_btn(x_center - 50, "<", has_prev, -1)
        # El número de página actual resaltado
        ShapeDrawer.rounded_rect(self.canvas, x_center-20, y_pos-15, 40, 30, 8, fill=COLOR_BADGE_BG)
        self.canvas.create_text(x_center, y_pos, text=str(curr), fill=COLOR_PRIMARY, font=FONT_INPUT)
        draw_page_btn(x_center + 50, ">", has_next, 1)

    def _change_page(self, delta):
        self.pm.current_page += delta
        self.refresh()

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
        except Exception as e:
            self.log.debug(f"Error cargando imagen {url}: {e}")