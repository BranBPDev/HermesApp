import tkinter as tk
from PIL import ImageTk
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_DIM, 
    COLOR_TEXT_INACTIVE, FONT_INPUT, CORNER_RADIUS, FONT_LABEL, FONT_PROD_PRICE,
    COLOR_PRIMARY_HOVER, COLOR_PRIMARY_ACTIVE
)
from app.gui.components.widgets.visual_elements import ShapeDrawer, CBadge
from app.utils.image_util import ImageLoader
from app.managers.cart_manager import CartManager
from app.managers.auth_manager import AuthManager

class ProductDetail(tk.Frame):
    def __init__(self, master, product, on_back, on_rate, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.product = product
        self.on_back = on_back
        self.on_rate = on_rate
        self.cm = CartManager()
        self.auth = AuthManager()
        
        # Sistema de estados: SELECTING, CONFIRMING, VIEWING
        self.saved_rating = product.get("user_rating", 0)
        self.current_step = "VIEWING" if self.saved_rating > 0 else "SELECTING"
        self.display_rating = self.saved_rating if self.saved_rating > 0 else 0
        self.cart_feedback = ""
            
        self._img_ref = None
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw())

    def _is_in_cart(self):
        user_id = self.auth.current_user_id
        if not user_id: return False
        items = self.cm.get_items(user_id)
        # Comparación basada en el ID del producto
        p_id = str(self.product.get('id') or self.product.get('product_id'))
        return any(str(item.get('product_id')) == p_id for item in items)

    def _toggle_cart(self):
        user_id = self.auth.current_user_id
        if not user_id: return
        p_id = self.product.get('id') or self.product.get('product_id')
        
        if self._is_in_cart():
            self.cm.remove_from_cart(user_id, p_id)
            self.cart_feedback = "Eliminado del carrito"
        else:
            self.cm.add_to_cart(user_id, p_id, 1)
            self.cart_feedback = "Añadido al carrito"
        
        self._draw()
        self.after(2000, self._clear_feedback)

    def _clear_feedback(self):
        self.cart_feedback = ""
        self._draw()

    def _draw(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w / 2, h / 2

        card_w, card_h = 600, 430
        x_card = cx - card_w / 2
        y_card = cy - (card_h / 2)
        ShapeDrawer.rounded_rect(self.canvas, x_card, y_card, card_w, card_h, CORNER_RADIUS, fill="#1a1a1a")

        back_x, back_y = x_card + 25, y_card + 25
        self.canvas.create_text(back_x, back_y, text="← Volver", fill=COLOR_PRIMARY, font=FONT_INPUT, tags="btn_back", anchor="nw")
        self.canvas.tag_bind("btn_back", "<Enter>", lambda e: [self.canvas.itemconfig("btn_back", fill=COLOR_PRIMARY_HOVER), self.canvas.config(cursor="hand2")])
        self.canvas.tag_bind("btn_back", "<Leave>", lambda e: [self.canvas.itemconfig("btn_back", fill=COLOR_PRIMARY), self.canvas.config(cursor="")])
        self.canvas.tag_bind("btn_back", "<Button-1>", lambda e: self.on_back())

        img_x, img_y = cx, y_card + 95
        
        # Texto informativo a la izquierda de la imagen
        if self.cart_feedback:
            self.canvas.create_text(img_x - 120, img_y, text=self.cart_feedback, fill=COLOR_PRIMARY, font=FONT_LABEL, anchor="e")

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
                ImageLoader.load_async(img_url, self._on_image_loaded, size=(150, 150))

        # Botón carrito: sobre la imagen, borde inferior derecho
        in_cart = self._is_in_cart()
        btn_txt = "−" if in_cart else "+"
        btn_x, btn_y = img_x + 75 - 20, img_y + 75 - 20
        ShapeDrawer.rounded_rect(self.canvas, btn_x-15, btn_y-15, 30, 30, 8, fill=COLOR_PRIMARY, tags="btn_cart_bg")
        self.canvas.create_text(btn_x, btn_y, text=btn_txt, fill="white", font=("Roboto", 20, "bold"), tags="btn_cart")
        self.canvas.tag_bind("btn_cart", "<Enter>", lambda e: [self.canvas.itemconfig("btn_cart_bg", fill=COLOR_PRIMARY_HOVER), self.canvas.config(cursor="hand2")])
        self.canvas.tag_bind("btn_cart", "<Leave>", lambda e: [self.canvas.itemconfig("btn_cart_bg", fill=COLOR_PRIMARY), self.canvas.config(cursor="")])
        self.canvas.tag_bind("btn_cart", "<Button-1>", lambda e: [self.canvas.itemconfig("btn_cart_bg", fill=COLOR_PRIMARY_ACTIVE), self._toggle_cart()])

        # Badge del Supermercado
        store_name = str(self.product.get('store_name', 'N/A')).upper()
        badge = CBadge(self.canvas, store_name, color=COLOR_PRIMARY)
        badge.draw(img_x + 95, img_y, w=100, h=24)

        full_name = self.product.get("name", "Producto")
        self.canvas.create_text(cx, y_card + 205, text=full_name, fill="white", font=("Roboto", 18, "bold"), anchor="center", justify="center", width=540)

        price_x1, price_x2 = cx - 120, cx + 120
        y_prices = y_card + 255
        self.canvas.create_text(price_x1, y_prices, text=f"{self.product.get('price', 0)} €", fill="white", font=FONT_PROD_PRICE, anchor="center")
        self.canvas.create_text(price_x2, y_prices, text=f"{self.product.get('price_norm', 0)} € / {self.product.get('unit_type', 'ud')}", fill=COLOR_TEXT_DIM, font=FONT_INPUT, anchor="center")
        
        # Línea discontinua centrada entre los precios
        line_w = 100
        start_line = cx - (line_w / 2)
        for i in range(0, int(line_w), 10):
            self.canvas.create_line(start_line + i, y_prices, start_line + i + 5, y_prices, fill=COLOR_PRIMARY, width=2)

        label_text = "Tu valoración:" if self.current_step == "VIEWING" else "Valora este producto:"
        self.canvas.create_text(cx, y_card + 310, text=label_text, fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL)
        stars_cy = y_card + 350
        self._draw_stars(cx, stars_cy)

        if self.current_step == "CONFIRMING":
            self.canvas.create_text(cx + 160, stars_cy, text="✓ Valorar", fill=COLOR_PRIMARY, font=FONT_LABEL, tags="btn_valorar", anchor="w")
            self.canvas.tag_bind("btn_valorar", "<Enter>", lambda e: [self.canvas.itemconfig("btn_valorar", fill=COLOR_PRIMARY_HOVER), self.canvas.config(cursor="hand2")])
            self.canvas.tag_bind("btn_valorar", "<Leave>", lambda e: [self.canvas.itemconfig("btn_valorar", fill=COLOR_PRIMARY), self.canvas.config(cursor="")])
            self.canvas.tag_bind("btn_valorar", "<Button-1>", lambda e: self._submit_rating())
        elif self.current_step == "VIEWING":
            self.canvas.create_text(cx + 160, stars_cy, text="✎ Modificar", fill=COLOR_PRIMARY, font=FONT_LABEL, tags="btn_modificar", anchor="w")
            self.canvas.tag_bind("btn_modificar", "<Enter>", lambda e: [self.canvas.itemconfig("btn_modificar", fill=COLOR_PRIMARY_HOVER), self.canvas.config(cursor="hand2")])
            self.canvas.tag_bind("btn_modificar", "<Leave>", lambda e: [self.canvas.itemconfig("btn_modificar", fill=COLOR_PRIMARY), self.canvas.config(cursor="")])
            self.canvas.tag_bind("btn_modificar", "<Button-1>", lambda e: self._enable_edit())

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
            color = COLOR_PRIMARY if i < self.display_rating else "#333333"
            self.canvas.create_text(x, cy, text="★", fill=color, font=("Roboto", 30), tags=tag)
            self.canvas.tag_bind(tag, "<Enter>", lambda e, s=i+1: [self.canvas.config(cursor="hand2"), self._highlight_stars(s) if self.current_step == "SELECTING" else None])
            self.canvas.tag_bind(tag, "<Leave>", lambda e: [self.canvas.config(cursor=""), self._draw() if self.current_step == "SELECTING" else None])
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, r=i+1: self._select_rating(r) if self.current_step == "SELECTING" else None)

    def _highlight_stars(self, count):
        for i in range(5):
            color = COLOR_PRIMARY if i < count else "#333333"
            self.canvas.itemconfig(f"star_{i}", fill=color)

    def _select_rating(self, rating):
        self.display_rating = rating
        self.current_step = "CONFIRMING"
        self._draw()

    def _submit_rating(self):
        p_id = self.product.get("id") or self.product.get("product_id")
        self.on_rate(p_id, self.display_rating)
        self.product["user_rating"] = self.display_rating
        self.current_step = "VIEWING"
        self._draw()

    def _enable_edit(self):
        self.current_step = "SELECTING"
        self._draw()