#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

fail() {
  echo
  echo "============================================"
  echo " [FAILED] $1"
  echo " Copy the full output above (including the actual error text from"
  echo " npm/python/pyinstaller, not just this message) and send it back."
  echo "============================================"
  exit 1
}

echo "============================================"
echo " Shawrma City - Desktop build (macOS)"
echo "============================================"

echo
echo "[1/5] Installing frontend dependencies..."
cd "$ROOT/frontend" || fail "Could not find the frontend folder."
npm install || fail "npm install failed in frontend/."

echo
echo "[2/5] Building frontend..."
npm run build || fail "Frontend build failed."

if [ ! -f "$ROOT/frontend/dist/index.html" ]; then
  fail "frontend/dist/index.html was not created - the build did not actually produce output even though npm didn't report an error."
fi

echo
echo "[3/5] Setting up Python environment and building backend executable..."
cd "$ROOT/backend" || fail "Could not find the backend folder."
python3 -m venv .venv-desktop || fail "Could not create the Python virtual environment. Is Python 3 installed?"
source .venv-desktop/bin/activate || fail "Could not activate the Python virtual environment."
pip install -r requirements-desktop.txt || fail "pip install failed."
pyinstaller desktop/shawrma-city.spec --noconfirm || fail "PyInstaller failed to build the backend executable."
deactivate

if [ ! -d "$ROOT/backend/dist/shawrma-city-backend" ]; then
  fail "backend/dist/shawrma-city-backend was not created."
fi

echo
echo "[4/5] Copying backend build into desktop-app..."
cd "$ROOT/desktop-app" || fail "Could not find the desktop-app folder."
rm -rf backend-dist
cp -R "$ROOT/backend/dist/shawrma-city-backend" backend-dist || fail "Could not copy the backend build into desktop-app/backend-dist."

echo
echo "[5/5] Building the macOS app with Electron..."
npm install || fail "npm install failed in desktop-app/."
npm run dist:mac || fail "electron-builder failed."

if [ ! -d "$ROOT/desktop-app/release" ]; then
  fail "electron-builder reported success but desktop-app/release was not created."
fi

echo
echo "============================================"
echo " Done. .dmg is in desktop-app/release/"
echo "============================================"
