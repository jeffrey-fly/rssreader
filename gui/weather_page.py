import requests
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Qt

from services.weather_service import WeatherService


def get_location_by_ip():
    resp = requests.get("https://ipapi.co/json/", timeout=5)
    data = resp.json()
    return {
        "city": data.get("city"),
        "lat": data.get("latitude"),
        "lon": data.get("longitude"),
    }

class WeatherPage(QWidget):
    def __init__(self, city="Tokyo"):
        super().__init__()
        loc = get_location_by_ip()
        self.city = loc.get("city")
        self.service = WeatherService()

        self.city_label = QLabel()
        self.temp_label = QLabel()
        self.desc_label = QLabel()
        self.humidity_label = QLabel()

        for label in (
            self.city_label,
            self.temp_label,
            self.desc_label,
            self.humidity_label,
        ):
            label.setAlignment(Qt.AlignCenter)

        self.refresh_btn = QPushButton("刷新天气")
        self.refresh_btn.clicked.connect(self.load_weather)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.city_label)
        layout.addWidget(self.temp_label)
        layout.addWidget(self.desc_label)
        layout.addWidget(self.humidity_label)
        layout.addWidget(self.refresh_btn)
        layout.addStretch()

        self.setLayout(layout)

        self.load_weather()

    def load_weather(self):
        data = self.service.get_weather(self.city)

        if not data:
            self.city_label.setText("天气获取失败")
            return

        self.city_label.setText(data["city"])
        self.temp_label.setText(f"{data['temp']} °C")
        self.desc_label.setText(data["desc"])
        self.humidity_label.setText(f"Humidity: {data['humidity']}%")
