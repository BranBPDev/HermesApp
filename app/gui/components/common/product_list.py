import tkinter as tk
from PIL import ImageTk
from app.gui.components.widgets.visual_elements import ShapeDrawer
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_TEXT_MAIN, COLOR_TEXT_INACTIVE, 
    COLOR_PRIMARY, FONT_LABEL, FONT_INPUT, COLOR_BADGE_BG
)
from app.utils.image_util import ImageLoader 

class ProductList(tk.Frame):
    def __init__(self, master, get_items_func, on_action=None, on_select=None, empty_text="No hay productos", show_action_btn=True, pm_ref=None, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.get_items_func = get_items_func
        self.on_action = on_action
        self.on_select = on_select 
        self.empty_text = empty_text
        self.show_action_btn = show_action_btn
        self.pm = pm_ref  
        self._img_refs = [] 
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self._last_w = 0
        self._last_h = 0
        self._refresh_timer = None 
        self.canvas.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        if event.width != self._last_w or event.height != self._last_h:
            self._last_w = event.width
            self._last_h = event.height
            self.refresh()

    def refresh(self):
        if self._refresh_timer:
            self.after_cancel(self._refresh_timer)
        self._refresh_timer = self.after(15, self._do_refresh)

    def _do_refresh(self):
        self.canvas.delete("all")
        self._img_refs.clear() 
        w, h = self._last_w, self._last_h
        if w <= 1: 
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            if w <= 1: return

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
        
        col_img = 60
        col_prod = w * 0.25
        col_super = w * 0.40
        col_val = w * 0.52
        col_price = w * 0.62
        col_unit = w * 0.72
        col_punit = w * 0.84
        col_acc = w - margin_right

        headers = [
            (col_prod, "PRODUCTO"), (col_super, "SUPER"), (col_val, "VAL."), 
            (col_price, "PRECIO"), (col_unit, "UNIDAD"), (col_punit, "P. UNIT")
        ]
        
        for x, title in headers:
            self.canvas.create_text(x, header_y, text=title, fill=COLOR_PRIMARY, font=FONT_LABEL, anchor="center")
        
        self.canvas.create_line(30, header_y + 15, w-30, header_y + 15, fill="#333333")

        for i, p in enumerate(products):
            y = start_y + (i * row_h)
            if y + row_h/2 > h - 50: break

            bg_color = "#1a1a1a" if i % 2 == 0 else COLOR_BG_DARK
            row_tag = f"row_{i}"
            name_tag = f"name_{i}"
            
            # Dibujamos el fondo de la fila
            ShapeDrawer.rounded_rect(self.canvas, 25, y-25, w-50, row_h-10, 8, fill=bg_color, tags=row_tag)
            
            img_url = p.get('image_url') or p.get('img_url')
            self._handle_image(img_url, 40, y-20)

            full_name = p.get('name', 'Producto sin nombre')
            name = (full_name[:20] + "..") if len(full_name) > 20 else full_name
            
            rating = p.get('avg_rating')
            val_text = f"{float(rating):.1f}" if rating is not None else "-"
            
            # Dibujamos el nombre con el tag específico
            self.canvas.create_text(col_prod, y, text=name, fill="white", font=FONT_INPUT, anchor="center", tags=name_tag)
            
            # Efecto Hover solo en el nombre
            if self.on_select:
                self.canvas.tag_bind(name_tag, "<Enter>", lambda e, n=name_tag: [self.canvas.itemconfig(n, fill=COLOR_PRIMARY), self.canvas.config(cursor="hand2")])
                self.canvas.tag_bind(name_tag, "<Leave>", lambda e, n=name_tag: [self.canvas.itemconfig(n, fill="white"), self.canvas.config(cursor="")])
                self.canvas.tag_bind(name_tag, "<Button-1>", lambda e, prod=p: self.on_select(prod))

            # Resto de columnas (sin link)
            self.canvas.create_text(col_super, y, text=str(p.get('store_name', 'N/A')).upper(), fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center", tags=row_tag)
            self.canvas.create_text(col_val, y, text=val_text, fill="#FFD700", font=FONT_LABEL, anchor="center", tags=row_tag)
            self.canvas.create_text(col_price, y, text=f"{p.get('price', 0)}€", fill=COLOR_TEXT_MAIN, font=FONT_INPUT, anchor="center", tags=row_tag)
            self.canvas.create_text(col_unit, y, text=p.get('unit_type', 'ud'), fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center", tags=row_tag)
            self.canvas.create_text(col_punit, y, text=f"{p.get('price_norm', 0)}€", fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center", tags=row_tag)

            if self.show_action_btn and self.on_action:
                btn_tag = f"btn_{i}"
                ShapeDrawer.rounded_rect(self.canvas, col_acc-15, y-15, 30, 30, 5, fill=COLOR_PRIMARY, tags=btn_tag)
                self.canvas.create_text(col_acc, y, text="+", fill="white", font=FONT_INPUT, tags=btn_tag, anchor="center")
                self.canvas.tag_bind(btn_tag, "<ButtonRelease-1>", lambda e, prod=p: self.on_action(prod))

    def _handle_image(self, url, x, y):
        if not url:
            self.canvas.create_rectangle(x, y, x+40, y+40, fill="#333333", outline="")
            return

        cached = ImageLoader.get_image(url, size=(40, 40))
        if cached:
            try:
                img = ImageTk.PhotoImage(cached)
                self._img_refs.append(img)
                self.canvas.create_image(x, y, image=img, anchor="nw")
            except Exception:
                pass
        else:
            temp_id = self.canvas.create_rectangle(x, y, x+40, y+40, fill="#222222", outline="")
            
            def on_img_ready(res):
                if self.winfo_exists(): 
                    self.after(0, self._finalize_image, res['pil'], url, x, y, temp_id)
            
            ImageLoader.load_async(url, on_img_ready, size=(40, 40))

    def _finalize_image(self, pil_img, url, x, y, temp_id):
        if self.winfo_exists():
            try:
                if temp_id in self.canvas.find_all():
                    self.canvas.delete(temp_id)
            except Exception:
                pass
            
            try:
                photo = ImageTk.PhotoImage(pil_img)
                self._img_refs.append(photo)
                self.canvas.create_image(x, y, image=photo, anchor="nw")
            except Exception:
                pass

    def _draw_pagination(self, w, h):
        curr = self.pm.current_page + 1
        has_prev = self.pm.current_page > 0
        has_next = self.pm.has_more()
        y_pos = h - 30 
        x_center = w / 2
        
        def draw_page_btn(x, text, active, delta=None):
            tag = f"page_btn_{text}"
            color = COLOR_PRIMARY if active else "#333333"
            text_color = "white" if active else COLOR_TEXT_INACTIVE
            ShapeDrawer.rounded_rect(self.canvas, x-15, y_pos-15, 30, 30, 15, fill=color, tags=tag)
            self.canvas.create_text(x, y_pos, text=text, fill=text_color, font=FONT_INPUT, tags=tag)
            
            if delta is not None and active:
                self.canvas.tag_bind(tag, "<Button-1>", lambda e: self._change_page(delta))
            else:
                self.canvas.tag_unbind(tag, "<Button-1>")

        draw_page_btn(x_center - 50, "<", has_prev, -1)
        ShapeDrawer.rounded_rect(self.canvas, x_center-20, y_pos-15, 40, 30, 8, fill=COLOR_BADGE_BG)
        self.canvas.create_text(x_center, y_pos, text=str(curr), fill=COLOR_PRIMARY, font=FONT_INPUT)
        draw_page_btn(x_center + 50, ">", has_next, 1)

    def _change_page(self, delta):
        if delta == -1 and self.pm.current_page <= 0:
            return
        if delta == 1 and not self.pm.has_more():
            return
            
        self.pm.current_page += delta
        self.refresh()