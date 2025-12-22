from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
    QTextBrowser,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, QUrl


class ReaderPage(QWidget):
    """
    RSS 阅读页：
    左侧：文章列表
    右侧：内嵌阅读
    """

    def __init__(self, feed_store, rss_service, parent=None):
        super().__init__(parent)

        self.feed_store = feed_store
        self.rss_service = rss_service

        self._init_ui()
        self._bind_signals()

    # ---------------------------
    # UI
    # ---------------------------

    def _init_ui(self):
        self.setWindowTitle("RSS Reader")

        # 左侧：文章列表
        self.article_list = QListWidget()
        self.article_list.setMinimumWidth(320)
        self.article_list.setWordWrap(True)

        # 右侧：阅读区
        self.reader = QTextBrowser()
        self.reader.setOpenExternalLinks(False)
        self.reader.setPlaceholderText("请选择一篇文章")

        # 主布局
        layout = QHBoxLayout(self)
        layout.addWidget(self.article_list, 2)
        layout.addWidget(self.reader, 5)

    def _bind_signals(self):
        self.article_list.itemClicked.connect(self._on_article_clicked)

    # ---------------------------
    # Feed 入口（由 MainWindow 调用）
    # ---------------------------

    def load_feed_by_name(self, feed_name: str):
        """
        MainWindow 调用这个方法
        """
        feed = next(
            (f for f in self.feed_store.all() if f["name"] == feed_name),
            None,
        )
        if not feed:
            self.reader.setText(f"未找到订阅：{feed_name}")
            return

        self._load_feed(feed)

    # ---------------------------
    # Feed 加载逻辑
    # ---------------------------

    def _load_feed(self, feed: dict):
        self.article_list.clear()
        self.reader.clear()

        urls = feed.get("urls", [])
        if not urls:
            self.reader.setText("该订阅未配置 URL")
            return

        all_entries = []

        for url in urls:
            try:
                entries = self.rss_service.fetch(url)
                all_entries.extend(entries)
            except Exception as e:
                print(f"[RSS] 加载失败 {url}: {e}")

        if not all_entries:
            self.reader.setText("未获取到任何文章")
            return

        # 可选：按发布时间排序（如果有）
        all_entries.sort(
            key=lambda e: e.get("published", ""),
            reverse=True,
        )

        for entry in all_entries:
            self._add_article_item(entry)

    # ---------------------------
    # Article List
    # ---------------------------

    def _add_article_item(self, entry: dict):
        title = entry.get("title", "(no title)")
        link = entry.get("link", "")
        published = entry.get("published", "")

        text = title
        if published:
            text = f"{title}\n{published}"

        item = QListWidgetItem(text)
        item.setToolTip(title)
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # 绑定业务数据
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

    # ---------------------------
    # Article Click
    # ---------------------------

    def _on_article_clicked(self, item: QListWidgetItem):
        data = item.data(Qt.UserRole)
        if not data:
            return

        link = data.get("link")
        if not link:
            self.reader.setText("该文章没有可用链接")
            return

        # 内嵌打开原文
        self.reader.setSource(QUrl(link))
