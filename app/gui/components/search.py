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
from app.utils.logger_util import HermesLogger

# Inicializamos el logger específico para la interfaz de búsqueda
logger = HermesLogger.get_logger("SEARCH_GUI")

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
        
        # Redibujado automático al cambiar el tamaño de la ventana
        self.canvas.bind("<Configure>", lambda e: self._draw())
        self.master.winfo_toplevel().bind("<Return>", lambda e: self.execute_search())

    def execute_search(self):
        query = self.inp.get()
        if query:
            # Reseteamos paginación al buscar algo nuevo
            self.pm.search(query)
            self._draw()

    def _draw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w <= 1 or h <= 1: return 

        # 1. Buscador fijo arriba
        self.inp.draw(30, 40, w=w-200)
        self.btn.draw(w-150, 40, w=120)

        # 2. Definición de áreas
        header_y = 110
        footer_h = 75 # Un poco más alto para mejor visual del footer
        table_start_y = 150
        available_height = h - table_start_y - footer_h
        row_h = 65

        # Cálculo dinámico de items por página según el tamaño actual
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
        # Centros exactos de columnas (Alineación Real TOTAL)
        col_img = 60
        col_prod = w * 0.25
        col_super = w * 0.45
        col_price = w * 0.58
        col_unit = w * 0.70
        col_punit = w * 0.83
        col_acc = w - 50

        # Cabeceras centradas en sus columnas
        headers = [
            (col_prod, "PRODUCTO"),
            (col_super, "SUPER"),
            (col_price, "PRECIO"),
            (col_unit, "UNIDAD"),
            (col_punit, "P. UNIT")
        ]
        
        for x, title in headers:
            self.canvas.create_text(x, header_y, text=title, fill=COLOR_PRIMARY, font=FONT_LABEL, anchor="center")
        
        self.canvas.create_line(30, header_y + 15, w-30, header_y + 15, fill="#333333")

        # Dibujado de productos
        for i, p in enumerate(products):
            y = start_y + (i * row_h)
            
            # Fondo de fila
            bg_color = "#1a1a1a" if i % 2 == 0 else COLOR_BG_DARK
            ShapeDrawer.rounded_rect(self.canvas, 25, y-25, w-50, row_h-10, 8, fill=bg_color)

            # 1. Imagen (Alineada al centro de su espacio visual inicial)
            self._draw_product_img(p.get('image_url'), col_img - 20, y-20)

            # 2. Producto (Abreviado y centrado)
            raw_name = p.get('name', '???')
            name = (raw_name[:25] + "..") if len(raw_name) > 25 else raw_name
            self.canvas.create_text(col_prod, y, text=name, fill="white", font=FONT_INPUT, anchor="center")

            # 3. Super (Centrado)
            store = str(p.get('store_name', '??')).upper()
            self.canvas.create_text(col_super, y, text=store, fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")

            # 4. Precio (Centrado)
            self.canvas.create_text(col_price, y, text=f"{p['price']}€", fill=COLOR_TEXT_MAIN, font=FONT_INPUT, anchor="center")

            # 5. Unidad (Centrado)
            self.canvas.create_text(col_unit, y, text=p['unit_type'], fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")

            # 6. Precio Unitario (Centrado)
            self.canvas.create_text(col_punit, y, text=f"{p['price_norm']}€/{p['unit_type']}", fill=COLOR_TEXT_INACTIVE, font=FONT_LABEL, anchor="center")

            # 7. Botón añadir (Interactividad: Hover, Active)
            self._draw_add_button(col_acc, y, p, i)

    def _draw_add_button(self, x, y, product, index):
        tag = f"btn_add_{index}"
        
        # Elementos del botón
        rect_id = ShapeDrawer.rounded_rect(self.canvas, x-15, y-15, 30, 30, 5, fill=COLOR_PRIMARY, tags=tag)
        text_id = self.canvas.create_text(x, y, text="+", fill="white", font=FONT_INPUT, tags=tag, anchor="center")

        # Eventos
        def on_enter(e): self.canvas.itemconfig(rect_id, fill="#d4a017") # Hover
        def on_leave(e): self.canvas.itemconfig(rect_id, fill=COLOR_PRIMARY) # Normal
        def on_press(e): # Active (Efecto de hundimiento)
            self.canvas.move(tag, 1, 1)
            self.canvas.itemconfig(rect_id, fill="#b08512")
        def on_release(e):
            self.canvas.move(tag, -1, -1)
            self.canvas.itemconfig(rect_id, fill="#d4a017")
            self.on_add(product)

        self.canvas.tag_bind(tag, "<Enter>", on_enter)
        self.canvas.tag_bind(tag, "<Leave>", on_leave)
        self.canvas.tag_bind(tag, "<Button-1>", on_press)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", on_release)

    def _draw_pagination(self, w, h, footer_h):
        footer_y = h - (footer_h / 2)
        
        # Fondo visual del footer (un tono más claro que el fondo general para destacar)
        self.canvas.create_rectangle(0, h - footer_h, w, h, fill="#121212", outline="")
        self.canvas.create_line(0, h - footer_h, w, h - footer_h, fill=COLOR_PRIMARY, width=2)

        page_text = f"PÁGINA {self.pm.current_page + 1}"
        self.canvas.create_text(w/2, footer_y, text=page_text, fill="white", font=FONT_LABEL, anchor="center")
        
        if self.pm.current_page > 0:
            self._draw_nav_btn(w/2 - 120, footer_y, "< ANTERIOR", lambda: self._change_page(-1))

        if self.pm.has_more():
            self._draw_nav_btn(w/2 + 120, footer_y, "SIGUIENTE >", lambda: self._change_page(1))

    def _draw_nav_btn(self, x, y, text, command):
        tag = f"nav_{text.strip()}"
        tid = self.canvas.create_text(x, y, text=text, fill=COLOR_PRIMARY, font=FONT_LABEL, tags=tag, anchor="center")
        
        self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.itemconfig(tid, fill="white"))
        self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.itemconfig(tid, fill=COLOR_PRIMARY))
        self.canvas.tag_bind(tag, "<Button-1>", lambda e: command())

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
            resp = requests.get(url, timeout=3)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content)).resize((40, 40), Image.Resampling.LANCZOS)
            self.after(0, lambda: self._render_downloaded_image(url, img, x, y, temp_id))
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red al descargar imagen: {url} | Motivo: {e}")
        except Exception as e:
            logger.error(f"Error inesperado procesando imagen: {url} | Error: {e}")

    def _render_downloaded_image(self, url, pil_img, x, y, temp_id):
        photo = ImageTk.PhotoImage(pil_img)
        self.img_cache[url] = photo
        self.canvas.delete(temp_id)
        self.canvas.create_image(x, y, image=photo, anchor="nw")