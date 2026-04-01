import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from app.utils.callback_util import invoke_progress # <--- Nuevo

def download_file(url: str, path: Path, progress_callback=None):
    path.parent.mkdir(parents=True, exist_ok=True)

    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    
    total_size = int(r.headers.get('content-length', 0))
    downloaded = 0

    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    # Reportamos progreso de 0.0 a 0.9 (dejamos el 10% final para el unzip)
                    percent = (downloaded / total_size) * 0.9
                    invoke_progress(progress_callback, percent, "Descargando...")

def download_files(urls: tuple, paths: tuple, progress_callback=None):
    if len(paths) == 1:
        if len(urls) == 1:
            download_file(urls[0], paths[0], progress_callback)
        else:
            with ThreadPoolExecutor() as executor:
                for url in urls:
                    executor.submit(download_file, url, paths[0], progress_callback)
    elif len(paths) == len(urls):
        with ThreadPoolExecutor() as executor:
            for url, path in zip(urls, paths):
                executor.submit(download_file, url, path, progress_callback)
    else:
        raise ValueError("Si paths no tiene tamaño 1, debe coincidir con el tamaño de urls")