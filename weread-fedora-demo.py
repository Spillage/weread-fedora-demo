#!/usr/bin/env python3
import sys
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QMessageBox
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView


WEREAD_URL = "https://weread.qq.com/"


class WeReadClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("微信读书（网页版客户端）")
        self.resize(1200, 800)

        # 使用“持久化 Profile”，让登录态/缓存保存在本机（默认会放到 Qt 的标准目录）
        # 这样你扫码登录一次后，下次通常还能保持登录（取决于官方策略）
        self.profile = QWebEngineProfile("weread_profile", self)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

        self.view = QWebEngineView(self)
        self.view.setPage(self._make_page())
        self.setCentralWidget(self.view)

        self._init_toolbar()
        self._init_shortcuts()

        self.view.setUrl(QUrl(WEREAD_URL))

    def _make_page(self):
        # 给 view 绑定 profile
        from PySide6.QtWebEngineCore import QWebEnginePage
        return QWebEnginePage(self.profile, self.view)

    def _init_toolbar(self):
        tb = QToolBar("导航", self)
        tb.setMovable(False)
        self.addToolBar(tb)

        back = QAction("后退", self)
        back.triggered.connect(self.view.back)
        tb.addAction(back)

        forward = QAction("前进", self)
        forward.triggered.connect(self.view.forward)
        tb.addAction(forward)

        reload_ = QAction("刷新", self)
        reload_.triggered.connect(self.view.reload)
        tb.addAction(reload_)

        home = QAction("首页", self)
        home.triggered.connect(lambda: self.view.setUrl(QUrl(WEREAD_URL)))
        tb.addAction(home)

        shelf = QAction("书架", self)
        shelf.triggered.connect(lambda: self.view.setUrl(QUrl("https://weread.qq.com/web/shelf")))
        tb.addAction(shelf)

        logout = QAction("清除登录态", self)
        logout.triggered.connect(self.clear_session)
        tb.addAction(logout)

    def _init_shortcuts(self):
        # 常用快捷键
        QAction(self, shortcut=QKeySequence.StandardKey.Back, triggered=self.view.back)
        QAction(self, shortcut=QKeySequence.StandardKey.Forward, triggered=self.view.forward)
        QAction(self, shortcut=QKeySequence.StandardKey.Refresh, triggered=self.view.reload)
        QAction(self, shortcut=QKeySequence("Ctrl+L"), triggered=self.focus_address_hint)

        # 全屏
        fs = QAction(self)
        fs.setShortcut(QKeySequence("F11"))
        fs.triggered.connect(self.toggle_fullscreen)
        self.addAction(fs)

    def toggle_fullscreen(self):
        self.setWindowState(self.windowState() ^ Qt.WindowState.WindowFullScreen)

    def focus_address_hint(self):
        QMessageBox.information(
            self,
            "提示",
            "这是内嵌官方网页版的客户端。\n如需跳转地址，可在代码里新增地址栏（QLineEdit）。"
        )

    def clear_session(self):
        # 清 cookies / cache（相当于退出/重置）
        self.profile.cookieStore().deleteAllCookies()
        self.profile.clearHttpCache()
        QMessageBox.information(self, "已清除", "已清除 Cookies 和缓存。重新打开页面后可再次扫码登录。")
        self.view.setUrl(QUrl(WEREAD_URL))


def main():
    app = QApplication(sys.argv)
    win = WeReadClient()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
