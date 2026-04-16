import threading
import requests
import hashlib
from io import BytesIO
from PIL import Image, ImageTk
import customtkinter as ctk
from app.utils.paths_util import ASSETS_DIR
from concurrent.futures import ThreadPoolExecutor

class ImageLoader:
    # Configuración de Directorios
    CACHE_DIR = ASSETS_DIR / "cache"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Caché en RAM para evitar accesos repetitivos a disco
    _ram_cache = {}
    # Executor para no crear hilos infinitos (máximo 4 descargas simultáneas)
    _executor = ThreadPoolExecutor(max_workers=4)
    _lock = threading.Lock()

    @staticmethod
    def get_image(url, size=(60, 60), mode="pil"):
        """
        Versión síncrona: Solo usar si estás SEGURO de que ya está en caché
        o no te importa bloquear el hilo actual.
        mode: "pil" (para Canvas) o "ctk" (para Widgets)
        """
        cache_key = f"{hashlib.md5(url.encode()).hexdigest()}_{size[0]}x{size[1]}"
        
        with ImageLoader._lock:
            if cache_key in ImageLoader._ram_cache:
                return ImageLoader._ram_cache[cache_key][mode]
        return None

    @staticmethod
    def load_async(url, callback, size=(60, 60)):
        """
        Carga una imagen asíncronamente y ejecuta un callback(dict_images)
        dict_images contiene: {'pil': ImageTk, 'ctk': CTkImage}
        """
        if not url: return
        ImageLoader._executor.submit(ImageLoader._download_task, url, callback, size)

    @staticmethod
    def _download_task(url, callback, size):
        try:
            url_hash = hashlib.md5(url.encode()).hexdigest()
            cache_key = f"{url_hash}_{size[0]}x{size[1]}"
            path = ImageLoader.CACHE_DIR / f"{url_hash}.png"

            # 1. Comprobar RAM
            with ImageLoader._lock:
                if cache_key in ImageLoader._ram_cache:
                    callback(ImageLoader._ram_cache[cache_key])
                    return

            # 2. Comprobar Disco o Descargar
            if path.exists():
                img = Image.open(path)
            else:
                resp = requests.get(url, timeout=5, headers={'User-Agent': 'HermesApp/1.0'})
                resp.raise_for_status()
                img = Image.open(BytesIO(resp.content))
                img.convert("RGBA").save(path, "PNG")

            # 3. Procesar versiones
            img_resized = img.resize(size, Image.Resampling.LANCZOS)
            
            # Versión para Canvas (PIL/Tkinter)
            pil_img = ImageTk.PhotoImage(img_resized)
            # Versión para CustomTkinter
            ctk_img = ctk.CTkImage(light_image=img_resized, dark_image=img_resized, size=size)

            res = {"pil": pil_img, "ctk": ctk_img}

            # Guardar en RAM
            with ImageLoader._lock:
                ImageLoader._ram_cache[cache_key] = res

            callback(res)
        except Exception as e:
            print(f"Error loading image {url}: {e}")