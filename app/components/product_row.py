import os
from PIL import Image
import customtkinter as ctk
from app.views.styles import COLOR_PRIMARY, FONT_REGULAR
from app.utils.image_util import load_product_image_async

class ProductRow(ctk.CTkFrame):
    def __init__(self, master, product, on_add_to_cart):
        super().__init__(master, fg_color="#1a1a1a", corner_radius=8, height=75)
        self.pack_propagate(False)
        
        full_name = product.get('name', 'Producto')
        display_name = (full_name[:45] + '...') if len(full_name) > 48 else full_name
        
        store = str(product.get('store_name', 'Tienda')).lower()
        price = f"{product.get('price', 0):.2f}€"
        price_norm = f"{product.get('price_norm', 0):.2f}€/{product.get('unit_type', 'ud')}"
        img_url = product.get('image_url')
        
        sep_style = {"text": "┊", "text_color": "#333333", "font": ("Roboto", 20)}

        # 1. IMAGEN
        self.img_lbl = ctk.CTkLabel(self, text="...", width=65, height=65, fg_color="#222222", corner_radius=6)
        self.img_lbl.pack(side="left", padx=(10, 5), pady=5)
        if img_url:
            load_product_image_async(img_url, self.img_lbl, (60, 60))
        else:
            self.img_lbl.configure(text="📦", font=("Roboto", 24))

        # 2. INFO PRODUCTO (Centrado automático)
        info_cnt = ctk.CTkFrame(self, fg_color="transparent")
        info_cnt.pack(side="left", expand=True, fill="x", padx=10)
        
        ctk.CTkLabel(info_cnt, text=display_name, font=("Roboto", 13, "bold"), anchor="center").pack(fill="x")
        ctk.CTkLabel(info_cnt, text=product.get('tag', 'otros').upper(), font=("Roboto", 10), text_color=COLOR_PRIMARY, anchor="center").pack(fill="x")

        ctk.CTkLabel(self, **sep_style).pack(side="left")

        # 3. TIENDA (Centrado)
        self.store_lbl = ctk.CTkLabel(self, text="", width=120, height=35, fg_color="#2b2b2b", corner_radius=6, anchor="center")
        self.store_lbl.pack(side="left", padx=10)
        self._load_store_logo(store, self.store_lbl, (80, 25))

        ctk.CTkLabel(self, **sep_style).pack(side="left")

        # 4. PRECIO UNITARIO (Centrado)
        ctk.CTkLabel(self, text=price_norm, font=("Roboto", 12), text_color="#aaaaaa", width=100, anchor="center").pack(side="left", padx=5)

        ctk.CTkLabel(self, **sep_style).pack(side="left")

        # 5. PRECIO TOTAL (Centrado)
        ctk.CTkLabel(self, text=price, font=("Roboto", 16, "bold"), text_color="white", width=100, anchor="center").pack(side="left", padx=5)

        # 6. BOTÓN
        ctk.CTkButton(self, text="➕", width=40, height=40, fg_color="#333333", font=("Roboto", 18),
                      hover_color=COLOR_PRIMARY, command=lambda: on_add_to_cart(product)).pack(side="left", padx=(5, 15))

    def _load_store_logo(self, store_name, label_widget, size):
        path = f"app/assets/{store_name}.png"
        if os.path.exists(path):
            try:
                img = Image.open(path)
                ctk_img = ctk.CTkImage(img, size=size)
                label_widget.configure(image=ctk_img, text="", fg_color="transparent")
                return
            except: pass
        label_widget.configure(text=store_name.upper()[:10], font=("Roboto", 11, "bold"), anchor="center")