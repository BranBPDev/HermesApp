import json
import requests
from pathlib import Path
from typing import Union

def read_json_local(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"JSON no encontrado: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_json_remote(url: str) -> dict:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def read_json(source: Union[Path, str]) -> dict:
    if isinstance(source, Path):
        return read_json_local(source)
    
    if isinstance(source, str) and (source.startswith("http://") or source.startswith("https://")):
        return read_json_remote(source)
    
    raise TypeError("read_json solo acepta Path (local) o str con URL http/https (remoto)")

def save_json(file_path: Path, data: Union[dict, list]):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))