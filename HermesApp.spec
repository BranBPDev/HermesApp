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
        ('.env', '.'), 
    ],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'bcrypt',
        'psycopg2',
        # UTILS
        'app.utils.json_util', 
        'app.utils.update_util', 
        'app.utils.logger_util',
        'app.utils.paths_util',
        'app.utils.crypto_util',
        # MANAGERS
        'app.managers.product_manager',
        'app.managers.app_manager',
        'app.managers.auth_manager',
        # VIEWS
        'app.views.auth_window',
        'app.views.main_window',
        'app.views.styles',
        # COMPONENTS (Los nuevos que añadimos)
        'app.components.pagination_footer',
        'app.components.product_row',
        'app.components.scrollable_list',
        'app.components.user_header'
    ],
    hookspath=[],
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
    console=False, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)