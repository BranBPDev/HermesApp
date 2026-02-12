import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def download_file(url: str, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

def download_files(urls: tuple, paths: tuple):
    if len(paths) == 1:
        if len(urls) == 1:
            download_file(urls[0], paths[0])
        else:
            with ThreadPoolExecutor() as executor:
                for url in urls:
                    executor.submit(download_file, url, paths[0])
    elif len(paths) == len(urls):
        with ThreadPoolExecutor() as executor:
            for url, path in zip(urls, paths):
                executor.submit(download_file, url, path)
    else:
        raise ValueError("Si paths no tiene tamaño 1, debe coincidir con el tamaño de urls")