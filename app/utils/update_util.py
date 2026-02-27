import os
import subprocess
import sys
import shutil
from app.utils.json_util import read_json
from app.utils.download_util import download_files
from app.utils.zip_util import unzip_file
from app.utils.paths_util import (
    VERSION_JSON, REMOTE_VERSION_JSON, LATEST_ZIP_URL, 
    TEMP_ZIP_PATH, DOWNLOAD_FOLDER, BASE_DIR
)

def is_latest_version():
    try:
        return read_json(VERSION_JSON)["version"] == read_json(REMOTE_VERSION_JSON)["version"]
    except Exception:
        return True

def perform_update():
    # 1. Limpieza preventiva
    if DOWNLOAD_FOLDER.exists():
        shutil.rmtree(DOWNLOAD_FOLDER)
    DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    # 2. Descarga solo del ZIP
    download_files((LATEST_ZIP_URL,), (TEMP_ZIP_PATH,))
    
    # 3. Descomprimir
    unzip_file(TEMP_ZIP_PATH, DOWNLOAD_FOLDER)

    exe_name = os.path.basename(sys.executable)
    pid = os.getpid()

    # 4. Comando de CMD
    # Cambiamos 'start' por una llamada directa que fuerce una nueva consola.
    # El uso de 'conhost' o 'cmd /c start' asegura que se asigne una ventana.
    cmd_chain = (
        f'title Actualizador && :loop && tasklist /fi ""pid eq {pid}"" | findstr {pid} >nul && (timeout /t 1 /nobreak >nul & goto loop) || '
        f'(for /d %x in ("{BASE_DIR}\\*") do (if /i not "%~nx"=="{DOWNLOAD_FOLDER.name}" rd /s /q "%x")) && '
        f'(for %x in ("{BASE_DIR}\\*") do (if /i not "%~nx"=="{DOWNLOAD_FOLDER.name}" del /f /q "%x")) && '
        f'xcopy /e /y /h "{DOWNLOAD_FOLDER}\\*" "{BASE_DIR}\\" >nul 2>&1 && '
        f'rd /s /q "{DOWNLOAD_FOLDER}" && '
        f'explorer.exe ""{BASE_DIR}\\{exe_name}""'
    )

    subprocess.Popen(
        f'cmd.exe /c "{cmd_chain}"',
        creationflags=0x08000000, 
        shell=True
    )
    
    sys.exit()