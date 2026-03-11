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
    ],
    hiddenimports=[
        # Core & Networking
        'requests', 'certifi', 'urllib3', 'httpx', 'httpcore', 
        'anyio', 'h2', 'hpack', 'hyperframe',
        
        # App Utils
        'app.utils.json_util', 'app.utils.update_util', 
        'app.utils.download_util', 'app.utils.paths_util', 
        'app.utils.zip_util', 'app.utils.logger_util', 
        'app.utils.configs_util', 'app.utils.dates_util',
        
        # App Daos
        'app.daos.product_dao',
        
        # App Models
        'app.models.scraper_base',
        
        # App Scrapers
        'app.scrapers.mercadona', 'app.scrapers.gadis', 'app.scrapers.eroski',
        
        # App Managers
        'app.managers.scraper_manager', 
        'app.managers.product_manager', 
        'app.managers.app_manager'
    ],
    hookspath=[],
    # El hook rthook_certifi.py debe estar en la carpeta pyinstaller_hooks en la raíz
    runtime_hooks=[os.path.join('pyinstaller_hooks', 'rthook_certifi.py')],
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