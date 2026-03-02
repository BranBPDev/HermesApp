import os, subprocess, sys, shutil
from app.utils.logger_util import HermesLogger
from app.utils.json_util import read_json
from app.utils.download_util import download_files
from app.utils.zip_util import unzip_file
from app.utils.paths_util import VERSION_JSON, REMOTE_VERSION_JSON, LATEST_ZIP_URL, TEMP_ZIP_PATH, DOWNLOAD_FOLDER, BASE_DIR

log = HermesLogger.get_logger("UPDATER")

def is_latest_version():
    try:
        return read_json(VERSION_JSON)["version"] == read_json(REMOTE_VERSION_JSON)["version"]
    except Exception as e:
        log.error(f"No se pudo verificar versión: {e}")
        return True

def perform_update():
    log.info("Iniciando descarga de actualización...")
    try:
        if DOWNLOAD_FOLDER.exists(): shutil.rmtree(DOWNLOAD_FOLDER)
        DOWNLOAD_FOLDER.mkdir(parents=True)
        
        download_files((LATEST_ZIP_URL,), (TEMP_ZIP_PATH,))
        unzip_file(TEMP_ZIP_PATH, DOWNLOAD_FOLDER)

        pid = os.getpid()
        exe = os.path.basename(sys.executable)
        
        cmd = (f'title Actualizador && :loop && tasklist /fi "pid eq {pid}" | findstr {pid} >nul && '
               f'(timeout /t 1 /nobreak >nul & goto loop) || '
               f'(for /d %x in ("{BASE_DIR}\\*") do (if /i not "%~nx"=="{DOWNLOAD_FOLDER.name}" rd /s /q "%x")) && '
               f'xcopy /e /y /h "{DOWNLOAD_FOLDER}\\*" "{BASE_DIR}\\" >nul && rd /s /q "{DOWNLOAD_FOLDER}" && '
               f'start "" "{BASE_DIR}\\{exe}"')

        subprocess.Popen(f'cmd.exe /c "{cmd}"', creationflags=0x08000000, shell=True)
        sys.exit()
    except Exception as e:
        log.critical(f"Fallo en actualización: {e}")