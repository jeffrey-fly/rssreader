from PySide6.QtWidgets import (
    QWidget, QListWidget, QListWidgetItem,
    QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Signal
import uuid


class SubscriptionPanel(QWidget):
    """
    订阅管理面板
    """
    feed_selected = Signal(dict)

    def __init__(self, feed_store, parent=None):
        super().__init__(parent)
        self.feed_store = feed_store
        self._init_ui()
        self._load_feeds()
        self._bind_signals()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("RSS 订阅管理")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.feed_list = QListWidget()
        layout.addWidget(self.feed_list, 1)

        # 添加订阅输入框
        add_layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Feed 名称")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Feed URL")
        self.add_btn = QPushButton("添加")

        add_layout.addWidget(self.name_input, 1)
        add_layout.addWidget(self.url_input, 2)
        add_layout.addWidget(self.add_btn, 0)
        layout.addLayout(add_layout)

    def _load_feeds(self):
        self.feed_list.clear()
        for feed in self.feed_store.all():
            item = QListWidgetItem(feed["name"])
            item.setData(0x0100, feed)  # Qt.UserRole = 0x0100
            self.feed_list.addItem(item)

    def _bind_signals(self):
        self.feed_list.itemClicked.connect(self._on_feed_clicked)
        self.add_btn.clicked.connect(self._on_add_clicked)

    def _on_feed_clicked(self, item: QListWidgetItem):
        feed = item.data(0x0100)
        self.feed_selected.emit(feed)

    def _on_add_clicked(self):
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()

        if not url:
            QMessageBox.warning(self, "错误", "Feed URL 不能为空")
            return

        feed = {
            "id": str(uuid.uuid4()),
            "name": name or url,
            "urls": [url]
        }

        self.feed_store.add(feed)
        self.name_input.clear()
        self.url_input.clear()
        self._load_feeds()
