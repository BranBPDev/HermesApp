import tkinter as tk
from PIL import ImageTk
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_DIM, 
    COLOR_TEXT_INACTIVE, FONT_TITLE, FONT_PROD_PRICE, FONT_INPUT, CORNER_RADIUS, FONT_LABEL
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
        cx = w / 2

        # 1. Botón Volver
        self.canvas.create_text(50, 40, text="← Volver", fill=COLOR_PRIMARY, font=FONT_INPUT, tags="btn_back")
        self.canvas.tag_bind("btn_back", "<Button-1>", lambda e: self.on_back())

        # 2. Contenedor Principal (Tarjeta)
        card_w, card_h = 600, 400
        ShapeDrawer.rounded_rect(self.canvas, cx - card_w/2, 80, card_w, card_h, CORNER_RADIUS, fill="#1a1a1a")

        # 3. Imagen del producto
        img_url = self.product.get('image_url')
        if img_url:
            cached = ImageLoader.get_image(img_url, size=(150, 150))
            if cached:
                try:
                    self._img_ref = ImageTk.PhotoImage(cached)
                    self.canvas.create_image(cx - 200, 200, image=self._img_ref, anchor="center")
                except Exception:
                    pass
            else:
                self.canvas.create_rectangle(cx - 275, 125, cx - 125, 275, fill="#222", outline="")
                self.canvas.create_text(cx - 200, 200, text="Cargando...", fill=COLOR_TEXT_INACTIVE)
                ImageLoader.load_async(img_url, self._on_image_loaded, size=(150, 150))
        
        # 4. Textos de Información
        name = self.product.get("name", "Producto")
        store = self.product.get("store_name", "Desconocida").upper()
        price = f"{self.product.get('price', 0)} €"
        price_norm = f"{self.product.get('price_norm', 0)} € / {self.product.get('unit_type', 'ud')}"
        last_update = self.product.get("last_update", "N/A")

        # Info Layout
        tx = cx - 50
        self.canvas.create_text(tx, 130, text=name, fill="white", font=("Roboto", 20, "bold"), anchor="w", width=300)
        self.canvas.create_text(tx, 170, text=f"Tienda: {store}", fill=COLOR_PRIMARY, font=FONT_LABEL, anchor="w")
        self.canvas.create_text(tx, 210, text=price, fill="white", font=FONT_PROD_PRICE, anchor="w")
        self.canvas.create_text(tx, 245, text=f"Precio unitario: {price_norm}", fill=COLOR_TEXT_DIM, font=FONT_INPUT, anchor="w")
        self.canvas.create_text(tx, 275, text=f"Última actualización: {last_update}", fill=COLOR_TEXT_INACTIVE, font=("Roboto", 9), anchor="w")

        # 5. Sistema de Estrellas
        label_text = "Tu valoración:" if self.rating > 0 else "Valora este producto:"
        self.canvas.create_text(cx, 380, text=label_text, fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL)
        self._draw_stars(cx, 420)

    def _on_image_loaded(self, res):
        if self.winfo_exists():
            self.after(0, self._apply_image, res)
            
    def _apply_image(self, res):
        if self.winfo_exists():
            try:
                self._img_ref = ImageTk.PhotoImage(res.get('pil'))
                self._draw()
            except Exception:
                pass

    def _draw_stars(self, cx, cy):
        self.stars = []
        for i in range(5):
            x = cx - 100 + (i * 50)
            tag = f"star_{i}"
            color = "#FFD700" if i < self.rating else "#333333"
            self.canvas.create_text(x, cy, text="★", fill=color, font=("Roboto", 30), tags=tag)
            
            # Hover y Click
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