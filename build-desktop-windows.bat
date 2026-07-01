@echo off
setlocal

echo ============================================
echo  Shawrma City - Desktop build (Windows)
echo ============================================

set ROOT=%~dp0

cd "%ROOT%frontend"
if errorlevel 1 (
  echo.
  echo [FAILED] Could not find the frontend folder.
  goto :fail
)

echo.
echo [1/5] Installing frontend dependencies...
call npm install
if errorlevel 1 (
  echo.
  echo [FAILED] npm install failed in frontend\. See the error above.
  goto :fail
)

echo.
echo [2/5] Building frontend...
call npm run build
if errorlevel 1 (
  echo.
  echo [FAILED] Frontend build failed. See the error above.
  goto :fail
)

if not exist "%ROOT%frontend\dist\index.html" (
  echo.
  echo [FAILED] frontend\dist\index.html was not created - the build did
  echo not actually produce output even though npm didn't report an error.
  goto :fail
)

cd "%ROOT%backend"
if errorlevel 1 (
  echo.
  echo [FAILED] Could not find the backend folder.
  goto :fail
)

echo.
echo [3/5] Setting up Python environment and building backend executable...
python -m venv .venv-desktop
if errorlevel 1 (
  echo.
  echo [FAILED] Could not create the Python virtual environment. Is Python installed and on PATH?
  goto :fail
)

call .venv-desktop\Scripts\activate.bat
if errorlevel 1 (
  echo.
  echo [FAILED] Could not activate the Python virtual environment.
  goto :fail
)

pip install -r requirements-desktop.txt
if errorlevel 1 (
  echo.
  echo [FAILED] pip install failed. See the error above.
  goto :fail
)

pyinstaller desktop\shawrma-city.spec --noconfirm
if errorlevel 1 (
  echo.
  echo [FAILED] PyInstaller failed to build the backend executable. See the error above.
  goto :fail
)

call deactivate

if not exist "%ROOT%backend\dist\shawrma-city-backend" (
  echo.
  echo [FAILED] backend\dist\shawrma-city-backend was not created.
  goto :fail
)

cd "%ROOT%desktop-app"
if errorlevel 1 (
  echo.
  echo [FAILED] Could not find the desktop-app folder.
  goto :fail
)

echo.
echo [4/5] Copying backend build into desktop-app...
if exist backend-dist rmdir /s /q backend-dist
xcopy "%ROOT%backend\dist\shawrma-city-backend" backend-dist /e /i /y
if errorlevel 1 (
  echo.
  echo [FAILED] Could not copy the backend build into desktop-app\backend-dist.
  goto :fail
)

echo.
echo [5/5] Building the Windows installer with Electron...
call npm install
if errorlevel 1 (
  echo.
  echo [FAILED] npm install failed in desktop-app\. See the error above.
  goto :fail
)

call npm run dist:win
if errorlevel 1 (
  echo.
  echo [FAILED] electron-builder failed. See the error above.
  goto :fail
)

if not exist "%ROOT%desktop-app\release" (
  echo.
  echo [FAILED] electron-builder reported success but desktop-app\release was not created.
  goto :fail
)

echo.
echo ============================================
echo  Done. Installer is in desktop-app\release\
echo ============================================
pause
exit /b 0

:fail
echo.
echo ============================================
echo  Build STOPPED - see the [FAILED] message above for which step broke.
echo  Copy the full output above (including the actual error text from
echo  npm/python/pyinstaller, not just this message) and send it back.
echo ============================================
pause
exit /b 1
