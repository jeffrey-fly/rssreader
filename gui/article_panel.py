from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal


class ArticlePanel(QWidget):
    """
    文章列表面板
    """
    article_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.title = QLabel("文章列表")
        self.title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.title)

        self.article_list = QListWidget()
        self.article_list = QListWidget()
        self.article_list.setMinimumWidth(360)
        self.article_list.setWordWrap(True)

        self.article_list.setStyleSheet("""
                    QListWidget {
                        background: palette(base);
                        outline: none;
                    }

                    QListWidget::item {
                        padding: 6px;
                        border-bottom: 1px solid palette(mid);
                        color: palette(text);
                    }

                    /* 鼠标悬停 */
                    QListWidget::item:hover {
                        background: palette(alternate-base);
                    }

                    /* 选中 + 有焦点 */
                    QListWidget::item:selected:active {
                        background: palette(highlight);
                        color: palette(highlighted-text);
                    }

                    /* 选中 + 无焦点（关键，解决白底问题） */
                    QListWidget::item:selected:!active {
                        background: palette(midlight);
                        color: palette(text);
                    }

        """)
        layout.addWidget(self.article_list, 1)

        self.article_list.itemClicked.connect(self._on_item_clicked)

    def load_feed(self, feed: dict, articles: list[dict]):
        self.article_list.clear()
        self.title.setText(f"文章列表 - {feed['name']}")
        if not articles:
            return

        for article in articles:
            item = QListWidgetItem(article["title"])
            item.setData(Qt.UserRole, article)
            self.article_list.addItem(item)

    def _on_item_clicked(self, item: QListWidgetItem):
        article = item.data(Qt.UserRole)
        self.article_selected.emit(article)
