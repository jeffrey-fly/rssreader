from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtGui import QAction

from services.feed_store import FeedStore
from services.rss_service import RSSService

from gui.rss_reader import RSSReaderWidget
from gui.weather_page import WeatherPage
from util.app_paths import FEEDS_FILE, APP_NAME


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(str(APP_NAME))
        self.showMaximized()  # 最大化窗口，占满屏幕（保留任务栏）

        # ----------------------
        # 核心服务
        # ----------------------
        self.feed_store = FeedStore(FEEDS_FILE)
        self.rss_service = RSSService()

        # ----------------------
        # 中央堆栈页面
        # ----------------------
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 页面实例
        self.reader_page = RSSReaderWidget(feed_store=self.feed_store)
        self.weather_page = WeatherPage()

        self.stack.addWidget(self.reader_page)
        self.stack.addWidget(self.weather_page)
        self.stack.setCurrentWidget(self.reader_page)  # 默认显示阅读页

        # 初始化菜单
        self._init_menu()

    def _init_menu(self):
        menubar = self.menuBar()
        view_menu = menubar.addMenu("view")

        reader_action = QAction("read", self)
        weather_action = QAction("weather", self)

        reader_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.reader_page)
        )
        weather_action.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.weather_page)
        )

        view_menu.addAction(reader_action)
        view_menu.addAction(weather_action)
