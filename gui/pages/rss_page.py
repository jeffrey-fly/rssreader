from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QTextBrowser,
    QHBoxLayout,
)
import webbrowser

from services.rss_service import RSSService


class RSSPage(QWidget):
    def __init__(self, feed_urls: list[str]):
        super().__init__()

        self.service = RSSService()
        self.items = []

        self.list_widget = QListWidget()
        self.reader = QTextBrowser()
        self.reader.setOpenExternalLinks(True)

        layout = QHBoxLayout()
        layout.addWidget(self.list_widget, 3)
        layout.addWidget(self.reader, 7)
        self.setLayout(layout)

        self.list_widget.currentRowChanged.connect(self.show_item)
        self.list_widget.itemDoubleClicked.connect(self.open_in_browser)

        for url in feed_urls:
            self.load_feed(url)

    def load_feed(self, url):
        items = self.service.fetch(url)
        for item in items:
            self.items.append(item)
            self.list_widget.addItem(item["title"])

    def show_item(self, index):
        if index < 0:
            return

        item = self.items[index]

        content = item["content"] or "<i>该订阅未提供正文内容。</i>"

        html = f"""
        <h2>{item['title']}</h2>
        <p><i>{item['published']}</i></p>
        <hr>
        {content}
        <p><a href="{item['link']}">阅读原文</a></p>
        """

        self.reader.setHtml(html)

    def open_in_browser(self, item):
        index = self.list_widget.row(item)
        webbrowser.open(self.items[index]["link"])
