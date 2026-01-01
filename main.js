const { app, BrowserWindow, Menu, shell, dialog } = require("electron");

app.commandLine.appendSwitch("no-sandbox");
app.commandLine.appendSwitch("disable-setuid-sandbox");
const path = require("path");

const WEREAD_HOME = "https://weread.qq.com/";
const WEREAD_SHELF = "https://weread.qq.com/web/shelf";

// 单实例（避免重复开很多窗口）
const gotLock = app.requestSingleInstanceLock();
if (!gotLock) app.quit();
else {
  app.on("second-instance", () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 820,
    title: "微信读书（Electron 客户端）",
webPreferences: {
  nodeIntegration: false,
  contextIsolation: true,
  preload: path.join(__dirname, "preload.js")
}

  });

  // 让外部链接在系统浏览器打开（避免新窗口乱飞）
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });

  // 第一次加载
  mainWindow.loadURL(WEREAD_HOME);

  // 菜单
  const template = [
    {
      label: "微信读书",
      submenu: [
        { label: "首页", accelerator: "CmdOrCtrl+1", click: () => mainWindow.loadURL(WEREAD_HOME) },
        { label: "书架", accelerator: "CmdOrCtrl+2", click: () => mainWindow.loadURL(WEREAD_SHELF) },
        { type: "separator" },
        { label: "后退", accelerator: "Alt+Left", click: () => mainWindow.webContents.goBack() },
        { label: "前进", accelerator: "Alt+Right", click: () => mainWindow.webContents.goForward() },
        { label: "刷新", accelerator: "CmdOrCtrl+R", click: () => mainWindow.webContents.reload() },
        { type: "separator" },
        {
          label: "清除登录态（Cookies/缓存）",
          click: async () => {
            const choice = dialog.showMessageBoxSync(mainWindow, {
              type: "warning",
              buttons: ["取消", "清除"],
              defaultId: 1,
              cancelId: 0,
              message: "将清除 Cookies / 缓存，可能需要重新扫码登录。继续？"
            });
            if (choice === 1) {
              const ses = mainWindow.webContents.session;
              await ses.clearStorageData();
              await ses.clearCache();
              mainWindow.loadURL(WEREAD_HOME);
            }
          }
        },
        { type: "separator" },
        { label: "打开开发者工具", accelerator: "CmdOrCtrl+Shift+I", click: () => mainWindow.webContents.openDevTools() },
        { type: "separator" },
        { role: "quit", label: "退出" }
      ]
    }
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));

  mainWindow.on("closed", () => (mainWindow = null));
}



app.whenReady().then(() => {
  // Electron 默认会把 session 存在 app.getPath('userData')，所以“登录态持久化”默认就有
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  // Linux 上常规：关窗即退
  if (process.platform !== "darwin") app.quit();
});
