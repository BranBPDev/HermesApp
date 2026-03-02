from pathlib import Path
import sys

# BASE DIRECTORY (Entorno ejecutable)
BASE_DIR = Path(sys.executable).parent

# LOGS
LOGS_DIR = BASE_DIR / "app" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
MAIN_LOG_PATH = LOGS_DIR / "hermesApp.log"

# DATA
DATA_DIR = BASE_DIR / "app" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

VERSION_JSON = DATA_DIR / "version.json"
MERCADONA_PRODUCTS_JSON = DATA_DIR / "mercadona_products.json"
GADIS_PRODUCTS_JSON = DATA_DIR / "gadis_products.json"
EROSKI_PRODUCTS_JSON = DATA_DIR / "eroski_products.json"

# CARPETA TEMPORAL Y DESCARGAS
DOWNLOAD_FOLDER = BASE_DIR / "temp_download"
TEMP_ZIP_PATH = DOWNLOAD_FOLDER / "update.zip"

# SCRAPERS MAPPING
PRODUCT_PATHS = {
    "mercadona": MERCADONA_PRODUCTS_JSON,
    "gadis": GADIS_PRODUCTS_JSON,
    "eroski": EROSKI_PRODUCTS_JSON
}

# GITHUB / REMOTE
LATEST_ZIP_URL = "https://github.com/BranBPDev/HermesApp/releases/latest/download/HermesApp.zip"
REMOTE_VERSION_JSON = "https://github.com/BranBPDev/HermesApp/releases/latest/download/version.json"