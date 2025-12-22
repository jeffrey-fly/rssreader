from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QStackedWidget,
    QHBoxLayout,
)

from gui.pages.weather_page import WeatherPage
from gui.pages.rss_page import RSSPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Personal Reader")
        self.resize(1100, 650)

        self.nav = QListWidget()
        self.stack = QStackedWidget()

        self.nav.addItem("🌤 天气")
        self.nav.addItem("📰 BBC 新闻")
        self.nav.addItem("💻 技术")

        self.stack.addWidget(WeatherPage("Tianjin"))
        self.stack.addWidget(
            RSSPage(["https://feeds.bbci.co.uk/news/rss.xml"])
        )
        self.stack.addWidget(
            RSSPage(["https://hnrss.org/frontpage"])
        )

        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)

        layout = QHBoxLayout()
        layout.addWidget(self.nav, 2)
        layout.addWidget(self.stack, 8)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
