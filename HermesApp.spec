# -*- mode: python ; coding: utf-8 -*-
import os
import certifi
from PyInstaller.building.build_main import Analysis, PYZ, EXE

project_root = os.path.abspath(os.getcwd())

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        (certifi.where(), 'certifi'), 
        # Eliminada la referencia a app/data para evitar el error de compilación
    ],
    hiddenimports=[
        'requests',
        'certifi',
        'urllib3',
        'httpx',
        'httpcore',
        'anyio',
        'h2',
        'hpack',
        'hyperframe',
        'app.utils.json_util',
        'app.utils.update_util',
        'app.utils.download_util',
        'app.utils.paths_util',
        'app.utils.zip_util',
        'app.utils.logger_util',
        'app.utils.configs_util',
        'app.managers.scraper_manager',
        'app.models.scraper_base',
        'app.scrapers.mercadona',
        'app.scrapers.gadis',
        'app.scrapers.eroski'
    ],
    hookspath=[],
    runtime_hooks=[],
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
    console=True, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)