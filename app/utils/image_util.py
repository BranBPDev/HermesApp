import threading
import requests
import hashlib
from io import BytesIO
from PIL import Image
from app.utils.paths_util import ASSETS_DIR
from concurrent.futures import ThreadPoolExecutor

class ImageLoader:
    # Configuración de Directorios
    CACHE_DIR = ASSETS_DIR / "cache"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Caché en RAM: guarda el objeto Image (PIL) para convertirlo a PhotoImage en el hilo principal
    _ram_cache = {}
    # Executor para no crear hilos infinitos
    _executor = ThreadPoolExecutor(max_workers=4)
    _lock = threading.Lock()

    @staticmethod
    def get_image(url, size=(60, 60)):
        """
        Versión síncrona: Retorna el objeto Image (PIL) si está en caché.
        """
        cache_key = f"{hashlib.md5(url.encode()).hexdigest()}_{size[0]}x{size[1]}"
        with ImageLoader._lock:
            if cache_key in ImageLoader._ram_cache:
                return ImageLoader._ram_cache[cache_key]
        return None

    @staticmethod
    def load_async(url, callback, size=(60, 60)):
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
                    callback({'pil': ImageLoader._ram_cache[cache_key]})
                    return

            # 2. Comprobar Disco o Descargar
            if path.exists():
                img = Image.open(path)
                img = img.convert("RGBA")
            else:
                # CORREGIDO: User-Agent real para evitar bloqueos 403 de Mercadona, Eroski y Gadis
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                resp = requests.get(url, timeout=5, headers=headers)
                resp.raise_for_status()
                img = Image.open(BytesIO(resp.content))
                img = img.convert("RGBA")
                img.save(path, "PNG")

            # 3. Procesar versión estándar (sin crear PhotoImage aquí)
            img_resized = img.resize(size, Image.Resampling.LANCZOS)

            # 4. Guardar en RAM
            with ImageLoader._lock:
                ImageLoader._ram_cache[cache_key] = img_resized

            callback({'pil': img_resized})
            
        except Exception:
            pass