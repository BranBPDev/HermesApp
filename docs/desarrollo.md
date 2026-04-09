
# 👨‍💻 Desarrollo desde cero (Build Manual)

## Clonar el repositorio
```bash
git clone https://github.com/BranBPDev/HermesApp.git
```

## Moverse a la carpeta del proyecto
```bash
cd HermesApp
```

## Crear entorno virtual (Python 3.11.9)
```bash
py -3.11 -m venv venv
```

## Activar entorno virtual
```bash
.\venv\Scripts\activate
```

## Actualizar herramientas de Python
```bash
python -m pip install --upgrade pip setuptools wheel
```

## Instalar dependencias necesarias
```bash
pip install certifi requests urllib3 pyinstaller httpx h2 psycopg2-binary bcrypt python-dotenv customtkinter Pillow
```

## Limpiar compilaciones previas
```bash
rmdir /s /q dist build 2>nul
```

## Generar ejecutable con PyInstaller
```bash
pyinstaller HermesApp.spec
```

## Salir del entorno virtual
```bash
deactivate
```  

> ⚠️ Es importante que el `.exe` use el archivo `app/data/version.json` correspondiente, pero no junto con el código fuente, para evitar conflictos.

```text
{
    "name": "HermesApp",
    "description": "La forma más rápida e inteligente de comparar precios entre supermercados en España y ahorrar en cada compra.",
    "version": "0.0.0",
    "releaseDate": "2026-02-20",
    "author": "BranBP",
    "repository": "https://github.com/BranBPDev/HermesApp"
}
```