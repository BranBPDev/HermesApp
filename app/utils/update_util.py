import os
import shutil
import subprocess
import sys
import ctypes
from ctypes import wintypes

from app.utils.json_util import read_json
from app.utils.download_util import download_files
from app.utils.zip_util import unzip_file
from app.utils.paths_util import (
    VERSION_JSON,
    REMOTE_VERSION_JSON,
    LATEST_ZIP_URL,
    TEMP_ZIP_PATH,
    DOWNLOAD_FOLDER,
    EXECUTABLE_PATH,
    BASE_DIR
)

def is_latest_version() -> bool:
    return read_json(VERSION_JSON)["version"] == read_json(REMOTE_VERSION_JSON)["version"]

def perform_update():
    DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    download_files(urls=(LATEST_ZIP_URL,), paths=(TEMP_ZIP_PATH,))

    unzip_file(TEMP_ZIP_PATH, DOWNLOAD_FOLDER)

    subprocess.Popen([sys.executable, "-c", "from app.utils.update_util import _update_subprocess; _update_subprocess(%d)" % os.getpid()], shell=False)

    sys.exit()

def _wait_process_windows(pid: int):
    SYNCHRONIZE = 0x00100000
    INFINITE = 0xFFFFFFFF

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    handle = kernel32.OpenProcess(SYNCHRONIZE, False, pid)
    if not handle:
        return
    
    kernel32.WaitForSingleObject(handle, INFINITE)
    kernel32.CloseHandle(handle)

def _update_subprocess(main_pid: int):

    _wait_process_windows(main_pid)

    for item in EXECUTABLE_PATH.parent.iterdir():
        if item == DOWNLOAD_FOLDER:
            continue
        item.unlink() if item.is_file() else shutil.rmtree(item)

    for item in DOWNLOAD_FOLDER.iterdir():
        if item.is_file():
            shutil.copy2(item, EXECUTABLE_PATH.parent / item.name)
        else:
            shutil.copytree(item, EXECUTABLE_PATH.parent / item.name)

    shutil.rmtree(DOWNLOAD_FOLDER, ignore_errors=True)

    subprocess.Popen([str(EXECUTABLE_PATH)], shell=False)
    sys.exit()