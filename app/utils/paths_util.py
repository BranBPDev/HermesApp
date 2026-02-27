from pathlib import Path
import sys

BASE_DIR = Path(sys.executable).parent
DATA_DIR = BASE_DIR / "app" / "data"

# Solo lo que usamos
VERSION_JSON = DATA_DIR / "version.json"
MERCADONA_PRODUCTS_JSON = DATA_DIR / "mercadona_products.json"
LIDL_PRODUCTS_JSON = DATA_DIR / "lidl_products.json"
GADIS_PRODUCTS_JSON = DATA_DIR / "gadis_products.json"
EROSKI_PRODUCTS_JSON = DATA_DIR / "eroski_products.json"

DOWNLOAD_FOLDER = BASE_DIR / "temp_download"
TEMP_ZIP_PATH = DOWNLOAD_FOLDER / "update.zip"

LATEST_ZIP_URL = "https://github.com/BranBPDev/HermesApp/releases/latest/download/HermesApp.zip"
REMOTE_VERSION_JSON = "https://github.com/BranBPDev/HermesApp/releases/latest/download/version.json"