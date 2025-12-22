from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
)
from PySide6.QtGui import QAction

from services.feed_store import FeedStore
from services.rss_service import RSSService

from gui.reader_page import ReaderPage
from gui.subscription_panel import SubscriptionPanel
from gui.weather_page import WeatherPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RSS Reader")
        self.resize(1200, 800)

        # =====================
        # Core services (单例)
        # =====================
        self.feed_store = FeedStore("feeds.json")
        self.rss_service = RSSService()

        # =====================
        # Central stack
        # =====================
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # =====================
        # Pages
        # =====================
        self.reader_page = ReaderPage(
            feed_store=self.feed_store,
            rss_service=self.rss_service,
        )
        self.sub_page = SubscriptionPanel(
            feed_store=self.feed_store
        )
        self.weather_page = WeatherPage()

        self.stack.addWidget(self.reader_page)
        self.stack.addWidget(self.sub_page)
        self.stack.addWidget(self.weather_page)

        # 默认页
        self.stack.setCurrentWidget(self.reader_page)

        # =====================
        # Menu
        # =====================
        self._init_menu()

        # =====================
        # Signals
        # =====================
        self._bind_signals()

    # ---------------------
    # Menu
    # ---------------------

    def _init_menu(self):
        menubar = self.menuBar()

        view_menu = menubar.addMenu("视图")

        self.reader_action = QAction("阅读", self)
        self.sub_action = QAction("订阅管理", self)
        self.weather_action = QAction("天气", self)

        self.reader_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.reader_page)
        )
        self.sub_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.sub_page)
        )
        self.weather_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.weather_page)
        )

        view_menu.addAction(self.reader_action)
        view_menu.addAction(self.sub_action)
        view_menu.addAction(self.weather_action)

    # ---------------------
    # Cross-page wiring
    # ---------------------

    def _bind_signals(self):
        """
        页面之间的通信统一在 MainWindow 处理
        """

        # 订阅页：选中 feed → 阅读页加载
        self.sub_page.feed_selected.connect(
            self._on_feed_selected
        )

    def _on_feed_selected(self, feed_name: str):
        self.reader_page.load_feed_by_name(feed_name)
        self.stack.setCurrentWidget(self.reader_page)
