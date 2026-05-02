import zipfile

def unzip_file(zip_path, extract_to) -> bool:
    try:
        extract_to.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        return True
    except Exception:
        return False