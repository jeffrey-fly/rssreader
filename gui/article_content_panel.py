from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView


class ArticleContentPanel(QWidget):
    """
    使用 QWebEngineView 显示文章网页
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)

    def display_article(self, article):
        """
        直接加载文章的 URL
        article: dict, 包含 title, summary, link
        """
        url = article.get("link", "")
        if url:
            self.webview.load(url)
        else:
            # 没有 link 时显示摘要
            html = f"""
            <html><body>
            <h2>{article['title']}</h2>
            <div>{article.get('summary', '')}</div>
            </body></html>
            """
            self.webview.setHtml(html)
