from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
)
from PySide6.QtCore import Signal


class SubscriptionPanel(QWidget):
    """
    RSS 订阅管理页
    """

    feed_selected = Signal(str)

    def __init__(self, feed_store, parent=None):
        super().__init__(parent)

        self.feed_store = feed_store

        self._init_ui()
        self._load_feeds()
        self._bind_signals()

    # ---------------------
    # UI
    # ---------------------

    def _init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("RSS 订阅管理")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.feed_list = QListWidget()
        layout.addWidget(self.feed_list)

        # 添加订阅
        add_layout = QHBoxLayout()
        self.feed_input = QLineEdit()
        self.feed_input.setPlaceholderText("Feed 名称（如：BBC）")

        self.add_btn = QPushButton("添加")

        add_layout.addWidget(self.feed_input, 1)
        add_layout.addWidget(self.add_btn, 0)

        layout.addLayout(add_layout)

    # ---------------------
    # Data
    # ---------------------

    def _load_feeds(self):
        self.feed_list.clear()
        for feed in self.feed_store.all():
            self.feed_list.addItem(feed["name"])

    # ---------------------
    # Signals
    # ---------------------

    def _bind_signals(self):
        self.feed_list.itemClicked.connect(self._on_feed_clicked)
        self.add_btn.clicked.connect(self._on_add_clicked)

    def _on_feed_clicked(self, item: QListWidgetItem):
        self.feed_selected.emit(item.text())

    def _on_add_clicked(self):
        name = self.feed_input.text().strip()
        if not name:
            return

        # 简化版：只加空 feed
        self.feed_store.add({
            "name": name,
            "urls": [],
        })

        self.feed_input.clear()
        self._load_feeds()
