const { app, BrowserWindow, dialog } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
const http = require("http");

const PORT = 8742;
const HEALTH_URL = `http://127.0.0.1:${PORT}/health`;

let backendProcess = null;
let mainWindow = null;

function getBackendExecutablePath() {
  // In a packaged app, extraResources land in process.resourcesPath/backend.
  // In dev (npm start, unpackaged), fall back to the PyInstaller dist/
  // output directly so `npm start` works without building an installer.
  const exeName = process.platform === "win32" ? "shawrma-city-backend.exe" : "shawrma-city-backend";

  if (app.isPackaged) {
    return path.join(process.resourcesPath, "backend", exeName);
  }
  return path.join(__dirname, "..", "..", "backend", "dist", "shawrma-city-backend", exeName);
}

function waitForBackend(retriesLeft, onReady, onFailed) {
  if (retriesLeft <= 0) {
    onFailed();
    return;
  }

  const req = http.get(HEALTH_URL, (res) => {
    if (res.statusCode === 200) {
      onReady();
    } else {
      setTimeout(() => waitForBackend(retriesLeft - 1, onReady, onFailed), 500);
    }
  });

  req.on("error", () => {
    setTimeout(() => waitForBackend(retriesLeft - 1, onReady, onFailed), 500);
  });
}

function startBackend() {
  const exePath = getBackendExecutablePath();

  backendProcess = spawn(exePath, [], {
    env: { ...process.env, SHAWRMA_PORT: String(PORT) },
    windowsHide: true,
  });

  backendProcess.on("error", (err) => {
    dialog.showErrorBox(
      "تعذر تشغيل التطبيق",
      `لم يتم العثور على ملف الخادم الداخلي أو تعذر تشغيله.\n\n${err.message}\n\nPath: ${exePath}`,
    );
    app.quit();
  });

  backendProcess.on("exit", (code) => {
    if (code !== null && code !== 0 && mainWindow) {
      dialog.showErrorBox("توقف الخادم الداخلي", `رمز الخروج: ${code}`);
    }
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 960,
    minHeight: 640,
    title: "مدينة الشاورما",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
    },
    show: false,
  });

  mainWindow.loadURL(`http://127.0.0.1:${PORT}/`);

  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startBackend();

  const splash = new BrowserWindow({
    width: 360,
    height: 240,
    frame: false,
    resizable: false,
    webPreferences: { contextIsolation: true },
  });
  splash.loadFile(path.join(__dirname, "splash.html"));

  waitForBackend(
    40, // ~20 seconds of retries before giving up
    () => {
      splash.close();
      createWindow();
    },
    () => {
      splash.close();
      dialog.showErrorBox(
        "تعذر بدء التطبيق",
        "لم يستجب الخادم الداخلي في الوقت المحدد. حاول إعادة فتح التطبيق.",
      );
      app.quit();
    },
  );
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("before-quit", () => {
  if (backendProcess) {
    backendProcess.kill();
  }
});
