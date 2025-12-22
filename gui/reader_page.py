from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView


class ReaderPage(QWidget):
    """
    RSS 阅读页（QWebEngineView 版）

    左侧：文章列表
    右侧：内嵌网页阅读
    """

    def __init__(self, feed_store, rss_service, parent=None):
        super().__init__(parent)

        self.feed_store = feed_store
        self.rss_service = rss_service

        self._init_ui()
        self._bind_signals()
        self._show_message("请选择一个订阅")

    # ---------------------
    # UI
    # ---------------------

    def _init_ui(self):
        # 左侧：文章列表
        self.article_list = QListWidget()
        self.article_list.setMinimumWidth(360)
        self.article_list.setWordWrap(True)

        # 右侧：WebEngine
        self.web_view = QWebEngineView()

        layout = QHBoxLayout(self)
        layout.addWidget(self.article_list, 2)
        layout.addWidget(self.web_view, 5)

    def _bind_signals(self):
        self.article_list.itemClicked.connect(self._on_article_clicked)

    # ---------------------
    # Public API (MainWindow 调用)
    # ---------------------

    def load_feed_by_name(self, feed_name: str):
        """
        由 MainWindow 调用，根据 feed 名称加载文章
        """
        feed = next(
            (f for f in self.feed_store.all() if f["name"] == feed_name),
            None,
        )
        if not feed:
            self._show_message(f"未找到订阅：{feed_name}")
            return

        self._load_feed(feed)

    # ---------------------
    # Feed loading
    # ---------------------

    def _load_feed(self, feed: dict):
        self.article_list.clear()

        urls = feed.get("urls", [])
        if not urls:
            self._show_message("该订阅未配置任何 RSS URL")
            return

        all_entries = []

        for url in urls:
            try:
                entries = self.rss_service.fetch(url)
                all_entries.extend(entries)
            except Exception as e:
                print(f"[RSS] 加载失败 {url}: {e}")

        if not all_entries:
            self._show_message("未获取到任何文章")
            return

        # 按发布时间排序（字符串排序，够用）
        all_entries.sort(
            key=lambda e: e.get("published", ""),
            reverse=True,
        )

        for entry in all_entries:
            self._add_article_item(entry)

        self._show_message("请选择一篇文章")

    # ---------------------
    # Article list
    # ---------------------

    def _add_article_item(self, entry: dict):
        title = entry.get("title", "(no title)")
        link = entry.get("link", "")
        published = entry.get("published", "")

        text = title
        if published:
            text = f"{title}\n{published}"

        item = QListWidgetItem(text)
        item.setToolTip(title)

        item.setData(
            Qt.UserRole,
            {
                "title": title,
                "link": link,
                "published": published,
                "entry": entry,
            },
        )

        self.article_list.addItem(item)

    # ---------------------
    # Article click
    # ---------------------

    def _on_article_clicked(self, item: QListWidgetItem):
        data = item.data(Qt.UserRole)
        if not data:
            return

        link = data.get("link")
        if not link:
            self._show_message("该文章没有可用链接")
            return

        self.web_view.load(QUrl(link))

    # ---------------------
    # Helper
    # ---------------------

    def _show_message(self, msg: str):
        """
        在 WebEngine 中显示提示信息（代替 QTextBrowser.setText）
        """
        html = f"""
        <html>
          <body style="
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            padding: 24px;
            color: #444;
          ">
            <h3>{msg}</h3>
          </body>
        </html>
        """
        self.web_view.setHtml(html)
