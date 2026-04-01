import os, subprocess, sys, shutil, logging
from app.utils.logger_util import HermesLogger
from app.utils.json_util import read_json
from app.utils.download_util import download_files
from app.utils.zip_util import unzip_file
from app.utils.callback_util import invoke_progress
from app.utils.paths_util import VERSION_JSON, REMOTE_VERSION_JSON, LATEST_ZIP_URL, TEMP_ZIP_PATH, DOWNLOAD_FOLDER, BASE_DIR, MAIN_LOG_PATH

log = HermesLogger.get_logger("UPDATER")

def is_latest_version():
    try:
        return read_json(VERSION_JSON)["version"] == read_json(REMOTE_VERSION_JSON)["version"]
    except Exception as e:
        log.error(f"No se pudo verificar versión: {e}")
        return True

def perform_update(progress_callback=None):
    log.info("Iniciando descarga de actualización...")
    try:
        if DOWNLOAD_FOLDER.exists(): shutil.rmtree(DOWNLOAD_FOLDER)
        DOWNLOAD_FOLDER.mkdir(parents=True)
        
        download_files((LATEST_ZIP_URL,), (TEMP_ZIP_PATH,), progress_callback=progress_callback)
        
        invoke_progress(progress_callback, 0.95, "Descomprimiendo archivos...")
        unzip_file(TEMP_ZIP_PATH, DOWNLOAD_FOLDER)
        log.info("Descompresión lista. Lanzando proceso de reemplazo...")

        pid = os.getpid()
        exe_path = sys.executable
        log_path = str(MAIN_LOG_PATH)

        logging.shutdown()

        # LOGICA INTACTA.
        # Refuerzo de limpieza de entorno: Eliminamos todas las variables que empiezan por PYI o MEI
        # que son las que bloquean la carga de la DLL en el relanzamiento.
        ps_command = (
            f"(Get-Process -Id {pid} -ErrorAction SilentlyContinue).WaitForExit(); "
            f"'--- PS_UPDATER: Ejecutando limpieza ---' | Out-File '{log_path}' -Append -Encoding utf8; "
            f"Get-ChildItem -Path '{BASE_DIR}' | ForEach-Object {{ "
            f"  if ($_.Name -ne '{DOWNLOAD_FOLDER.name}' -and $_.Name -ne '{os.path.basename(TEMP_ZIP_PATH)}') {{ "
            f"    if ($_.Name -eq 'app') {{ "
            f"      Get-ChildItem -Path $_.FullName | Where-Object {{ $_.Name -ne 'logs' }} | Remove-Item -Recurse -Force "
            f"    }} else {{ Remove-Item -Path $_.FullName -Recurse -Force }} "
            f"  }} "
            f"}}; "
            f"Copy-Item -Path '{DOWNLOAD_FOLDER}\\*' -Destination '{BASE_DIR}' -Recurse -Force; "
            f"Remove-Item -Path '{DOWNLOAD_FOLDER}' -Recurse -Force; "
            f"Start-Sleep -Seconds 1; "
            f"'--- PS_UPDATER: Relanzando aplicacion ---' | Out-File '{log_path}' -Append -Encoding utf8; "
            f"Get-ChildItem Env: | Where-Object {{ $_.Name -like '*PYI*' -or $_.Name -like '*MEI*' }} | ForEach-Object {{ Remove-Item $_.PSPath }}; "
            f"Start-Process -FilePath '{exe_path}' -WorkingDirectory '{BASE_DIR}'"
        )

        subprocess.Popen(
            f'start /min powershell.exe -NoProfile -WindowStyle Hidden -Command "{ps_command}"',
            shell=True,
            creationflags=0x00000008 | 0x00000200
        )
        
        os._exit(0)

    except Exception as e:
        log.critical(f"Error fatal en el updater: {e}")