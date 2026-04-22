from pathlib import Path
import sys
import os

if getattr(sys, 'frozen', False):
    cert_path = os.path.join(sys._MEIPASS, 'certifi', 'cacert.pem')
    os.environ['REQUESTS_CA_BUNDLE'] = cert_path
    os.environ['SSL_CERT_FILE'] = cert_path
    
# BASE DIRECTORY (Donde está el .exe físicamente)
BASE_DIR = Path(sys.executable).parent

# INTERNAL DIRECTORY (Dentro del .exe empaquetado)
# PyInstaller extrae los archivos internos en sys._MEIPASS
INTERNAL_DIR = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(__file__).parent.parent.parent

# CONFIGURATION - Miramos DENTRO del .exe para el .env
ENV_PATH = INTERNAL_DIR / ".env"

# LOGS
LOGS_DIR = BASE_DIR / "app" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
MAIN_LOG_PATH = LOGS_DIR / "hermesApp.log"

# CARPETA TEMPORAL Y DESCARGAS
DOWNLOAD_FOLDER = BASE_DIR / "temp_download"
TEMP_ZIP_PATH = DOWNLOAD_FOLDER / "update.zip"

# ASSETS
ASSETS_DIR = BASE_DIR / "app" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

IMG_CACHE_DIR = ASSETS_DIR / "cache"
IMG_CACHE_DIR.mkdir(parents=True, exist_ok=True)

LOGO_PNG = ASSETS_DIR / "logo.png"
LOGO_ICO = ASSETS_DIR / "logo.ico"
def get_store_logo_path(store_name): return ASSETS_DIR / f"{store_name}.png"

# DATA
DATA_DIR = BASE_DIR / "app" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

VERSION_JSON = DATA_DIR / "version.json"
SESSION_JSON = DATA_DIR / "session.json"

# SCRAPERS
SCRAPERS_DIR = DATA_DIR / "scrapers"
SCRAPERS_DIR.mkdir(parents=True, exist_ok=True)

# SCRAPERS MAPPING
PRODUCT_PATHS = {
    "mercadona": SCRAPERS_DIR / "mercadona_products",
    "gadis": SCRAPERS_DIR / "gadis_products",
    "eroski": SCRAPERS_DIR / "eroski_products"
}

# GITHUB / REMOTE
LATEST_ZIP_URL = "https://github.com/BranBPDev/HermesApp/releases/latest/download/HermesApp.zip"
REMOTE_VERSION_JSON = "https://github.com/BranBPDev/HermesApp/releases/latest/download/version.json"