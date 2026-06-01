import tkinter as tk
from PIL import ImageTk
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_DIM, 
    COLOR_TEXT_INACTIVE, FONT_INPUT, CORNER_RADIUS, FONT_LABEL, FONT_PROD_PRICE
)
from app.gui.components.widgets.visual_elements import ShapeDrawer
from app.utils.image_util import ImageLoader

class ProductDetail(tk.Frame):
    def __init__(self, master, product, on_back, on_rate, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.product = product
        self.on_back = on_back
        self.on_rate = on_rate
        self.rating = product.get("user_rating", 0) 
        self._img_ref = None
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w / 2, h / 2

        # 1. Botón Volver
        self.canvas.create_text(50, 40, text="← Volver", fill=COLOR_PRIMARY, font=FONT_INPUT, tags="btn_back")
        self.canvas.tag_bind("btn_back", "<Button-1>", lambda e: self.on_back())

        # 2. Contenedor (Calculado dinámico)
        card_w, card_h = 600, 450
        y_card = cy - (card_h / 2)
        ShapeDrawer.rounded_rect(self.canvas, cx - card_w/2, y_card, card_w, card_h, CORNER_RADIUS, fill="#1a1a1a")

        # 3. Imagen
        img_x, img_y = cx - 200, y_card + 120
        img_url = self.product.get('image_url')
        if img_url:
            cached = ImageLoader.get_image(img_url, size=(150, 150))
            if cached:
                try:
                    self._img_ref = ImageTk.PhotoImage(cached)
                    self.canvas.create_image(img_x, img_y, image=self._img_ref, anchor="center")
                except: pass
            else:
                self.canvas.create_rectangle(img_x-75, img_y-75, img_x+75, img_y+75, fill="#222", outline="")
                self.canvas.create_text(img_x, img_y, text="Cargando...", fill=COLOR_TEXT_INACTIVE)
                ImageLoader.load_async(img_url, self._on_image_loaded, size=(150, 150))
        
        # 4. Textos (Sistema de espaciado)
        tx = cx - 50
        ty = y_card + 50
        
        # Nombre (truncado para no solapar)
        full_name = self.product.get("name", "Producto")
        name = (full_name[:35] + "...") if len(full_name) > 35 else full_name
        
        self.canvas.create_text(tx, ty, text=name, fill="white", font=("Roboto", 18, "bold"), anchor="w", width=300)
        self.canvas.create_text(tx, ty + 40, text=f"Tienda: {str(self.product.get('store_name', 'N/A')).upper()}", fill=COLOR_PRIMARY, font=FONT_LABEL, anchor="w")
        self.canvas.create_text(tx, ty + 80, text=f"{self.product.get('price', 0)} €", fill="white", font=FONT_PROD_PRICE, anchor="w")
        self.canvas.create_text(tx, ty + 115, text=f"P. Unitario: {self.product.get('price_norm', 0)} € / {self.product.get('unit_type', 'ud')}", fill=COLOR_TEXT_DIM, font=FONT_INPUT, anchor="w")
        self.canvas.create_text(tx, ty + 150, text=f"Última actualización: {self.product.get('last_update', 'N/A')}", fill=COLOR_TEXT_INACTIVE, font=("Roboto", 9), anchor="w")

        # 5. Sistema de Estrellas
        label_text = "Tu valoración:" if self.rating > 0 else "Valora este producto:"
        self.canvas.create_text(cx, y_card + card_h - 60, text=label_text, fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL)
        self._draw_stars(cx, y_card + card_h - 20)

    def _on_image_loaded(self, res):
        if self.winfo_exists(): self.after(0, self._apply_image, res)
            
    def _apply_image(self, res):
        if self.winfo_exists():
            try:
                self._img_ref = ImageTk.PhotoImage(res.get('pil'))
                self._draw()
            except: pass

    def _draw_stars(self, cx, cy):
        for i in range(5):
            x = cx - 100 + (i * 50)
            tag = f"star_{i}"
            color = "#FFD700" if i < self.rating else "#333333"
            self.canvas.create_text(x, cy, text="★", fill=color, font=("Roboto", 30), tags=tag)
            self.canvas.tag_bind(tag, "<Enter>", lambda e, s=i+1: self._highlight_stars(s))
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self._draw())
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, r=i+1: self._handle_rate(r))

    def _highlight_stars(self, count):
        for i in range(5):
            color = "#FFD700" if i < count else "#444444"
            self.canvas.itemconfig(f"star_{i}", fill=color)

    def _handle_rate(self, new_rating):
        self.rating = new_rating
        self.on_rate(self.product.get("id"), new_rating)
        self._draw()