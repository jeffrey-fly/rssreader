from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices


class ArticleContentPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # ---------- 顶部栏 ----------
        header = QHBoxLayout()

        self.title_label = QLabel("")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.open_btn = QPushButton("原文")
        self.open_btn.setEnabled(False)
        self.open_btn.clicked.connect(self._open_in_browser)

        header.addWidget(self.title_label)
        header.addStretch()
        header.addWidget(self.open_btn)

        main_layout.addLayout(header)

        # ---------- 内容 ----------
        self.webview = QWebEngineView()
        main_layout.addWidget(self.webview)

        self._current_url = None

    def display_article(self, article: dict):
        """
        article 必须包含:
        - title
        - link
        """
        self.title_label.setText(article.get("title", ""))

        url = article.get("link")
        if url:
            self._current_url = url
            self.open_btn.setEnabled(True)
            self.webview.load(QUrl(url))
        else:
            self._current_url = None
            self.open_btn.setEnabled(False)
            self.webview.setHtml("<h3>无原文链接</h3>")

    def _open_in_browser(self):
        if self._current_url:
            QDesktopServices.openUrl(QUrl(self._current_url))
