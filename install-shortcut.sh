#!/usr/bin/env bash
set -euo pipefail

# 1) 项目目录：默认取脚本所在目录（最稳）
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 2) Electron 可执行文件：优先用本项目 node_modules/.bin/electron
ELECTRON_BIN="$PROJECT_DIR/node_modules/.bin/electron"
if [[ ! -x "$ELECTRON_BIN" ]]; then
  echo "找不到 Electron：$ELECTRON_BIN"
  echo "请先在项目目录执行：npm i -D electron"
  exit 1
fi

# 3) desktop 文件路径
APP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$APP_DIR/weread-electron.desktop"
mkdir -p "$APP_DIR"

# 4) （可选）图标：如果你在项目目录放了 icon.png 就会自动用它
#    建议 256x256 或更大 PNG
ICON_VALUE="internet-web-browser"
if [[ -f "$PROJECT_DIR/icon.png" ]]; then
  ICON_VALUE="$PROJECT_DIR/icon.png"
fi

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=微信读书
Comment=微信读书 Electron 客户端（网页版）
Exec=$ELECTRON_BIN --no-sandbox --disable-setuid-sandbox $PROJECT_DIR
Icon=$ICON_VALUE
Terminal=false
Categories=Office;Education;Network;
StartupNotify=true
EOF

chmod +x "$DESKTOP_FILE"

# 更新 desktop 数据库（有就更好，没有也不致命）
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APP_DIR" >/dev/null 2>&1 || true
fi

echo "✅ 已创建启动器：$DESKTOP_FILE"
echo "现在按 Super 键，搜索“微信读书”即可启动（也可以右键固定到 Dock）。"
echo
echo "可选：把图标放到项目目录：$PROJECT_DIR/icon.png  (PNG)"
