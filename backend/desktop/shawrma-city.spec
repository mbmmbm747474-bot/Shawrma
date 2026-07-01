# PyInstaller spec for the desktop backend.
#
# Build with (from backend/):
#   pyinstaller desktop/shawrma-city.spec --noconfirm
#
# Produces dist/shawrma-city-backend/ containing a single executable plus
# its dependencies, and a bundled copy of the built frontend
# (frontend/dist) under frontend_dist/ next to it - see
# app/desktop/server.py's _frontend_dist_dir() for how that's located at
# runtime.
#
# IMPORTANT: run `npm run build` in frontend/ BEFORE running this, so
# frontend/dist exists - this spec does not build the frontend itself.

import sys
from pathlib import Path

block_cipher = None

# SPECPATH is the directory containing THIS .spec file, i.e. backend/desktop/
# - not backend/ itself. That one-level difference was the actual bug in an
# earlier version of this file (it looked for frontend/dist inside backend/
# instead of next to it). Named explicitly here so it can't happen again.
spec_dir = Path(SPECPATH).resolve()          # .../backend/desktop
backend_dir = spec_dir.parent                 # .../backend
project_root = backend_dir.parent             # .../ (contains both backend/ and frontend/)

frontend_dist = project_root / "frontend" / "dist"

if not frontend_dist.is_dir():
    raise SystemExit(
        f"frontend/dist not found at {frontend_dist}.\n"
        "Run `npm run build` inside frontend/ before building the desktop app."
    )

datas = [
    (str(frontend_dist), "frontend_dist"),
]

a = Analysis(
    [str(backend_dir / "app" / "desktop" / "desktop_main.py")],
    pathex=[str(backend_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
        "passlib.handlers.bcrypt",
        "email_validator",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=["redis", "celery", "psycopg"],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="shawrma-city-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="shawrma-city-backend",
)
