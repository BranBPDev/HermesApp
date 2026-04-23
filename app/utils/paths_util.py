from pathlib import Path
import sys
import os

# --- LÓGICA DE DIRECTORIOS CRÍTICA ---
# Si ejecutamos el .exe empaquetado por PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
    INTERNAL_DIR = Path(sys._MEIPASS)
    # Certificados para que requests no falle en el EXE
    cert_path = os.path.join(sys._MEIPASS, 'certifi', 'cacert.pem')
    if os.path.exists(cert_path):
        os.environ['REQUESTS_CA_BUNDLE'] = cert_path
        os.environ['SSL_CERT_FILE'] = cert_path
else:
    # Si estamos en desarrollo (python main.py)
    # __file__ es app/utils/paths_util.py, subimos 3 niveles para llegar a la raíz
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    INTERNAL_DIR = BASE_DIR

# --- CONFIGURACIÓN (.env) ---
# En desarrollo: busca el .env en la raíz del proyecto
# En el EXE: lo busca dentro del paquete (INTERNAL_DIR)
ENV_PATH = INTERNAL_DIR / ".env"

# --- LOGS ---
# Los logs siempre van fuera, donde esté el ejecutable o el proyecto
LOGS_DIR = BASE_DIR / "app" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
MAIN_LOG_PATH = LOGS_DIR / "hermesApp.log"

# --- CARPETA TEMPORAL Y DESCARGAS ---
DOWNLOAD_FOLDER = BASE_DIR / "temp_download"
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
TEMP_ZIP_PATH = DOWNLOAD_FOLDER / "update.zip"

# --- ASSETS (Imágenes, Logos) ---
# Importante: Buscamos en INTERNAL_DIR para que use las imágenes incluidas en el código
ASSETS_DIR = INTERNAL_DIR / "app" / "assets"
if not ASSETS_DIR.exists():
    # Fallback por si acaso en desarrollo las tienes en BASE_DIR
    ASSETS_DIR = BASE_DIR / "app" / "assets"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Caché de imágenes (esta sí va en BASE_DIR para que persista fuera del EXE)
IMG_CACHE_DIR = BASE_DIR / "app" / "assets" / "cache"
IMG_CACHE_DIR.mkdir(parents=True, exist_ok=True)

LOGO_PNG = ASSETS_DIR / "logo.png"
LOGO_ICO = ASSETS_DIR / "logo.ico"

def get_store_logo_path(store_name): 
    return ASSETS_DIR / f"{store_name}.png"

# --- DATA (JSONs, Sesiones) ---
# Esto debe ir en BASE_DIR para que el usuario pueda escribir/leer datos
DATA_DIR = BASE_DIR / "app" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

VERSION_JSON = DATA_DIR / "version.json"
SESSION_JSON = DATA_DIR / "session.json"

# --- SCRAPERS ---
SCRAPERS_DIR = DATA_DIR / "scrapers"
SCRAPERS_DIR.mkdir(parents=True, exist_ok=True)

PRODUCT_PATHS = {
    "mercadona": SCRAPERS_DIR / "mercadona_products",
    "gadis": SCRAPERS_DIR / "gadis_products",
    "eroski": SCRAPERS_DIR / "eroski_products"
}

# --- GITHUB / REMOTE ---
LATEST_ZIP_URL = "https://github.com/BranBPDev/HermesApp/releases/latest/download/HermesApp.zip"
REMOTE_VERSION_JSON = "https://github.com/BranBPDev/HermesApp/releases/latest/download/version.json"