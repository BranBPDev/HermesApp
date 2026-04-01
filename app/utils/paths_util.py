from pathlib import Path
import sys

# BASE DIRECTORY (Entorno ejecutable)
BASE_DIR = Path(sys.executable).parent

# CONFIGURATION
ENV_PATH = BASE_DIR / ".env"

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

LOGO_PNG = ASSETS_DIR / "logo.png"
LOGO_ICO = ASSETS_DIR / "logo.ico"

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