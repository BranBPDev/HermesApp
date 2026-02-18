from pathlib import Path
import sys

BASE_DIR = Path(sys.executable).parent

VERSION_JSON = BASE_DIR / "app" / "data" / "version.json"
DOWNLOAD_FOLDER = BASE_DIR / "temp_download"
TEMP_ZIP_PATH = DOWNLOAD_FOLDER / "update.zip"

# URLs de GitHub
LATEST_ZIP_URL = "https://github.com/BranBPDev/HermesApp/releases/latest/download/HermesApp.zip"
REMOTE_VERSION_JSON = "https://github.com/BranBPDev/HermesApp/releases/latest/download/version.json"