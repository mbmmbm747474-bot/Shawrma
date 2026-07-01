"""FastAPI app for the desktop build: same API as app.main, plus the
built React frontend served as static files from the same process/port.

Kept separate from app/main.py (used by the Docker/server deployment)
since that one deliberately does NOT serve a frontend - in that
deployment the frontend runs in its own container/dev server and talks
to the backend over CORS instead.
"""
from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.api import api_router
from app.core.config import settings


def _frontend_dist_dir() -> Path:
    """Where the built frontend (frontend/dist) lives once bundled.

    PyInstaller unpacks bundled data files next to the executable under
    sys._MEIPASS (a temp dir it creates at runtime) when frozen; when
    running unfrozen (e.g. `python -m app.desktop.desktop_main` during
    development) it's just a relative path from the repo.
    """
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)  # type: ignore[attr-defined]
        return base / "frontend_dist"
    return Path(__file__).resolve().parents[3] / "frontend" / "dist"


def build_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/health", tags=["root"])
    def health_check():
        return {"status": "ok"}

    dist_dir = _frontend_dist_dir()

    if dist_dir.is_dir():
        assets_dir = dist_dir / "assets"
        if assets_dir.is_dir():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        index_file = dist_dir / "index.html"

        @app.get("/{full_path:path}", include_in_schema=False)
        def spa_fallback(full_path: str):
            # Anything not matched by /api/* or /assets/* above falls
            # through to here. Returning index.html for every unknown
            # path is what makes React Router's client-side routes
            # (e.g. /companies, /purchase-orders) work on a hard refresh
            # instead of 404ing, since the server has no real route for them.
            requested = dist_dir / full_path
            if full_path and requested.is_file():
                return FileResponse(requested)
            return FileResponse(index_file)

    return app
