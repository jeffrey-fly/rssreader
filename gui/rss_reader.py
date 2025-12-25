from PySide6.QtWidgets import QWidget, QHBoxLayout
from gui.subscription_panel import SubscriptionPanel
from gui.article_panel import ArticlePanel
from gui.article_content_panel import ArticleContentPanel
import requests
import feedparser
import certifi


class RSSReaderWidget(QWidget):
    def __init__(self, feed_store, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        self.sub_panel = SubscriptionPanel(feed_store)
        self.article_panel = ArticlePanel()
        self.article_content_panel = ArticleContentPanel()

        # self.sub_panel.setMinimumWidth(250)
        # self.article_panel.setMinimumWidth(250)
        layout.addWidget(self.sub_panel, 1)
        layout.addWidget(self.article_panel, 1)
        layout.addWidget(self.article_content_panel, 4)

        # 信号连接
        self.sub_panel.feed_selected.connect(self._on_feed_selected)
        self.article_panel.article_selected.connect(self.article_content_panel.display_article)

    def _on_feed_selected(self, feed):
        all_articles = []
        urls = feed.get("urls", [])
        if not urls:
            return

        for url in urls:
            articles = self._fetch_articles(url)
            for a in articles:
                a["feed_id"] = feed["id"]
            all_articles.extend(articles)

        self.article_panel.load_feed(feed, all_articles)

    def _fetch_articles(self, feed_url: str):
        try:
            resp = requests.get(feed_url, headers={"User-Agent": "Mozilla/5.0"},
                                timeout=10, verify=certifi.where())
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"拉取 RSS 失败: {feed_url}\n{e}")
            return []

        d = feedparser.parse(resp.content)
        articles = []
        for entry in d.entries:
            articles.append({
                "id": entry.get("id", entry.get("link")),
                "feed_id": "",  # 在 _on_feed_selected 补上
                "title": entry.get("title", "无标题"),
                "link": entry.get("link", ""),
                "pubDate": entry.get("published", ""),
                "summary": entry.get("summary", ""),
            })
        return articles
