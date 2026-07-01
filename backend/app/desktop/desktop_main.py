"""Entry point for the packaged desktop backend (built via PyInstaller,
see desktop/build.py and desktop/shawrma-city.spec).

This is NOT used by the Docker/server deployment - that still runs
`uvicorn app.main:app` directly against Postgres, exactly as before.
This file only exists for the no-Docker desktop build.

Responsibilities:
  1. Pick a writable, per-user data directory for the SQLite file
     (so the app works even if installed to a read-only Program Files /
     Applications folder).
  2. Point DATABASE_URL at that file before any app.* module that reads
     settings gets imported (config is read once, at import time).
  3. Run the first-launch bootstrap (create tables + default admin).
  4. Start uvicorn serving the API *and* the built frontend static files
     from one process on one port, so Electron only has to point a
     window at a single URL.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def get_data_dir() -> Path:
    """Per-OS standard location for app data, created if missing."""
    app_name = "ShawrmaCity"

    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    data_dir = base / app_name
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def main() -> None:
    data_dir = get_data_dir()
    db_path = data_dir / "shawrma_city.db"

    # Must happen before `from app.core.config import settings` (or anything
    # that imports it) anywhere in the process - pydantic-settings reads the
    # environment once, at Settings() construction time.
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ.setdefault("APP_ENV", "desktop")
    os.environ.setdefault("DEBUG", "false")
    os.environ.setdefault("SECRET_KEY", _get_or_create_local_secret(data_dir))

    from app.desktop.bootstrap import bootstrap

    bootstrap(data_dir)

    import uvicorn

    from app.desktop.server import build_app

    app = build_app()

    port = int(os.environ.get("SHAWRMA_PORT", "8742"))
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


def _get_or_create_local_secret(data_dir: Path) -> str:
    """A real per-install JWT secret instead of the shared CHANGE_ME
    default, persisted so tokens survive an app restart."""
    import secrets

    secret_file = data_dir / ".secret_key"
    if secret_file.exists():
        return secret_file.read_text().strip()

    secret = secrets.token_urlsafe(48)
    secret_file.write_text(secret)
    return secret


if __name__ == "__main__":
    main()
