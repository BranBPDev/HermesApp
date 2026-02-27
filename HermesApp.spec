# -*- mode: python ; coding: utf-8 -*-
import os
import certifi
from PyInstaller.building.build_main import Analysis, PYZ, EXE

# Obtenemos la ruta absoluta de la carpeta del proyecto
project_root = os.path.abspath(os.getcwd())

a = Analysis(
    ['main.py'],
    pathex=[project_root],  # Añadimos la raíz para que encuentre la carpeta 'app'
    binaries=[],
    datas=[
        (certifi.where(), 'certifi'), # Certificados SSL
    ],
    hiddenimports=[
        'requests',
        'certifi',
        'urllib3',
        'app.utils.json_util',
        'app.utils.update_util',
        'app.utils.download_util',
        'app.utils.paths_util',
        'app.utils.zip_util',
        'app.managers.scraper_manager',
        'app.scrapers.mercadona'
    ],
    hookspath=[],
    runtime_hooks=['pyinstaller_hooks/rthook_certifi.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HermesApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Mantenemos consola para ver el progreso de los scrapers
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)