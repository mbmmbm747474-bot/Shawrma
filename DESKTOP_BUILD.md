# Shawrma City — Desktop Build (Windows / Mac, no Docker)

This is a **single-user, local demo/testing build**. It bundles the
backend and a SQLite database into one app you can double-click — no
Postgres, no Docker, no terminal once it's built.

**This is not meant for production or for multiple restaurant locations.**
SQLite is a single file on one computer; nothing syncs, nothing is backed
up automatically, and only one person can use it at a time. For real
deployment, use the Docker/Postgres setup described in the main README.

---

## What you get after building

- One installer (`.exe` on Windows via NSIS, `.dmg` on Mac)
- Installing it puts a normal desktop app on the system — double-click
  to launch, no console window
- On first launch, it automatically creates the database and one admin
  account, and writes the generated password to a text file in the
  app's data folder (path is shown below)
- Login screen → dashboard → everything from Milestones 1 and 2
  (companies, branches, users, warehouses, products, suppliers,
  purchase orders, goods receipt)

---

## Building it yourself

You need, on the machine doing the build:
- **Node.js 20+** and **npm**
- **Python 3.11+** with `pip`
- On Windows: build for Windows. On Mac: build for Mac. (Cross-building,
  e.g. making a `.exe` from a Mac, is possible with electron-builder but
  not set up here — build on the OS you're targeting.)

From the project root:

**Windows:**
```
build-desktop-windows.bat
```

**Mac:**
```
./build-desktop-mac.sh
```

This runs, in order:
1. `npm install` + `npm run build` in `frontend/` → produces `frontend/dist`
2. A Python venv in `backend/`, installs `requirements-desktop.txt`,
   then runs PyInstaller against `backend/desktop/shawrma-city.spec` →
   produces `backend/dist/shawrma-city-backend/`
3. Copies that PyInstaller output into `desktop-app/backend-dist/` —
   electron-builder's `extraResources` doesn't reliably support paths
   outside its own project directory, so the backend build has to be
   copied in rather than referenced via `../backend/...`
4. `npm install` + `electron-builder` in `desktop-app/` → produces the
   final installer in `desktop-app/release/`

Each step depends on the one before it finishing successfully — the
scripts stop on the first error rather than continuing.

---

## ⚠️ Honest status: this has not been run end-to-end

This entire desktop build — the PyInstaller spec, the Electron wrapper,
the SQLite compatibility layer — was written without access to a
Windows or Mac machine, Node, Python, or PyInstaller to actually execute
any of it. Everything below is reasoned through carefully and checked
against documentation, but **none of it has been built and run for real.**
Treat the first build as a debugging session, not a sure thing.

### Most likely things to go wrong, and what they'd look like

**PyInstaller build fails with a missing-module error**
mentioning `cryptography`, `bcrypt`, or `jose` — these are C-extension
packages that sometimes need explicit hidden-imports PyInstaller's static
analysis misses. `requirements-desktop.txt` includes
`pyinstaller-hooks-contrib`, which should auto-handle `cryptography`, but
if you still see `ModuleNotFoundError` when running the built exe, add the
missing module name to `hiddenimports` in `backend/desktop/shawrma-city.spec`
and rebuild.

**The Electron window opens to a blank/white page**
Usually means `frontend/dist` wasn't actually bundled, or
`_frontend_dist_dir()` in `backend/app/desktop/server.py` is pointing at
the wrong place inside the PyInstaller bundle. Check that
`backend/dist/shawrma-city-backend/frontend_dist/index.html` exists after
the PyInstaller build step — if it doesn't, the spec file's `datas` entry
didn't pick it up (re-check that `frontend/dist` existed *before* you ran
PyInstaller).

**"تعذر تشغيل التطبيق" (couldn't start the app) dialog on launch**
The Electron process couldn't find or start the backend executable. Check
the path it's looking for matches where `electron-builder`'s
`extraResources` actually placed it — see `getBackendExecutablePath()` in
`desktop-app/src/main.js`. This is the single most likely path/packaging
mismatch given none of this was tested.

**App opens but every screen shows a network/login error**
The backend process probably crashed after Electron's `/health` check
passed once but failed afterward. Run the bundled backend executable
directly from a terminal (`backend/dist/shawrma-city-backend/shawrma-city-backend.exe`
on Windows) to see its actual error output instead of through Electron,
which hides it.

**Windows SmartScreen / Mac Gatekeeper blocks the installer**
Expected — this build isn't code-signed (that requires a paid certificate).
On Windows, click "More info" → "Run anyway". On Mac, right-click the app
→ Open, or allow it in System Settings → Privacy & Security.

If you hit any of these, send me the exact error text and which step it
happened on — I'll fix the spec/config directly.

---

## Where your data lives

- **Windows**: `%APPDATA%\ShawrmaCity\shawrma_city.db`
- **Mac**: `~/Library/Application Support/ShawrmaCity/shawrma_city.db`

The first-login password is written next to the database file, in
`بيانات-الدخول.txt`, the first time the app runs.

To fully reset (wipe all data and get a fresh default admin), close the
app and delete the whole `ShawrmaCity` folder at the path above, then
reopen the app.

## Uninstalling

Use the normal Windows "Add or remove programs" / drag-to-Trash on Mac.
This does **not** delete your data folder above — delete it manually if
you want a completely clean removal.

## No custom icon yet

The app currently uses Electron's default icon — no `.ico`/`.icns` file
was created for this build. To add one: create
`desktop-app/build/icon.ico` (Windows, 256x256 recommended) and
`desktop-app/build/icon.icns` (Mac), then add them back into the `win`/`mac`
sections of `desktop-app/package.json`:
```json
"win": { "target": "nsis", "icon": "build/icon.ico" },
"mac": { "target": "dmg", "icon": "build/icon.icns", "category": "public.app-category.business" }
```
