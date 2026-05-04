# -*- mode: python ; coding: utf-8 -*-
import os
import certifi
from PyInstaller.building.build_main import Analysis, PYZ, EXE
from PyInstaller.utils.hooks import collect_submodules

project_root = os.path.abspath(os.getcwd())

auto_hidden_imports = collect_submodules('app')
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
        *auto_hidden_imports
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
    console=False, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app/assets/logo.ico'],
)