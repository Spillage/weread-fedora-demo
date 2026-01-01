const { contextBridge } = require("electron");

// 这里暂时不暴露任何危险 API，仅占位
contextBridge.exposeInMainWorld("wereadClient", {
  version: "0.1.0"
});
