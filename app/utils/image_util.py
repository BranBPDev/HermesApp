import threading
import requests
from io import BytesIO
from PIL import Image
import customtkinter as ctk
from app.utils.paths_util import ASSETS_DIR # Usamos tus rutas existentes
import hashlib

# Definir carpeta de cache dentro de assets
IMG_CACHE_DIR = ASSETS_DIR / "cache"
IMG_CACHE_DIR.mkdir(parents=True, exist_ok=True)

_RAM_CACHE = {}

def load_product_image_async(url: str, label_widget: ctk.CTkLabel, size: tuple = (60, 60)):
    """
    Carga de imágenes optimizada: RAM -> Disco -> Internet.
    """
    if not url:
        return

    # 1. Check RAM
    if url in _RAM_CACHE:
        label_widget.configure(image=_RAM_CACHE[url], text="")
        return

    def download_task():
        try:
            # Nombre único para el archivo basado en la URL
            url_hash = hashlib.md5(url.encode()).hexdigest()
            cache_path = IMG_CACHE_DIR / f"{url_hash}.png"

            # 2. Check Disco
            if cache_path.exists():
                img = Image.open(cache_path)
            else:
                # 3. Descarga (con Timeout para no bloquear el hilo)
                response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                
                # Guardar en disco para la próxima vez
                img.convert("RGBA").save(cache_path, "PNG")

            # Preparar para CustomTkinter
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
            _RAM_CACHE[url] = ctk_img

            # Actualizar UI en el hilo principal (seguro para Tkinter)
            label_widget.after(0, lambda: label_widget.configure(image=ctk_img, text="", fg_color="transparent"))
            
        except Exception as e:
            # Si falla, mostramos un emoji de caja o error
            label_widget.after(0, lambda: label_widget.configure(text="📦", font=("Roboto", 18)))

    # Lanzar en hilo separado para evitar lag en el scroll
    threading.Thread(target=download_task, daemon=True).start()