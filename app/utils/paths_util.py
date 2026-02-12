from pathlib import Path

BASE_DIR = Path(__file__).parent.parent  

VERSION_JSON = BASE_DIR / "data/version.json"
DOWNLOAD_FOLDER = BASE_DIR / "temp_download"
TEMP_ZIP_PATH = DOWNLOAD_FOLDER / "update.zip"
EXECUTABLE_PATH = BASE_DIR.parent / "HermesApp.exe"  


# GITHUB URLS
LATEST_ZIP_URL = "https://github.com/BranBPDev/HermesApp/releases/latest/download/HermesApp.zip"
REMOTE_VERSION_JSON = "https://github.com/BranBPDev/HermesApp/releases/latest/download/version.json"