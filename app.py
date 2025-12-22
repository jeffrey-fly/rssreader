CITY = "Tianjin"
NEWS_FEED = "https://feeds.bbci.co.uk/news/world/rss.xml"

import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
