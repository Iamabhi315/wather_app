
import sys
import requests
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QLineEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer

# Replace with your OpenWeatherMap API key
API_KEY = "53801ff1a1733e6d68b669f1184410ef"

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐍 Weather App 🐍")
        self.setWindowIcon(QIcon("weather_icon.png"))
        self.resize(400, 700)         # ✅ Allows resize
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #020024, stop:0.5 #090979, stop:1 #00D4FF
                );
                color: white;
                font-family: Segoe UI;
            }
            QLineEdit {
                padding: 10px;
                font-size: 50px;
                border-radius: 15px;
                border: 2px solid white;
            }
            QPushButton {
                background-color: white;
                color: #090979;
                padding: 20px;
                font-size: 30px;
                font-weight: bold;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #00D4FF;
                color: white;
            }
            QLabel {
                color: white;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Date-Time Label
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignCenter)
        self.datetime_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.datetime_label)

        # Timer for live time
        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)
        self.update_datetime()

        # City input
        self.city_label = QLabel("🌏Enter City Name:")
        self.city_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.city_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.city_label)

        self.city_input = QLineEdit()
        self.city_input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.city_input)

        # Get weather button
        self.get_weather_btn = QPushButton("Get Weather")
        self.get_weather_btn.clicked.connect(self.get_weather)
        layout.addWidget(self.get_weather_btn)

        # Weather result area
        self.temp_label = QLabel("")
        self.temp_label.setFont(QFont("Segoe UI", 30, QFont.Bold))
        self.temp_label.setAlignment(Qt.AlignCenter)

        self.feels_like_label = QLabel("")
        self.feels_like_label.setFont(QFont("Segoe UI", 12))
        self.feels_like_label.setAlignment(Qt.AlignCenter)

        self.icon_label = QLabel("")
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.description_label = QLabel("")
        self.description_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.description_label.setAlignment(Qt.AlignCenter)

        self.humidity_label = QLabel("")
        self.humidity_label.setFont(QFont("Segoe UI", 12))
        self.humidity_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.temp_label)
        layout.addWidget(self.feels_like_label)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.humidity_label)

        self.setLayout(layout)

    def update_datetime(self):
        now = datetime.now().strftime("%b %d, %Y - %I:%M:%S %p")
        self.datetime_label.setText(now)

    def get_weather(self):
        city = self.city_input.text()
        if not city:
            self.temp_label.setText("Please enter a city!")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                self.temp_label.setText("City not found!")
                return

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"].capitalize()
            icon_code = data["weather"][0]["icon"]

            # Update UI
            self.temp_label.setText(f"{temp}°C")
            self.feels_like_label.setText(f"Feels like {feels_like}°C")
            self.description_label.setText(desc)
            self.humidity_label.setText(f"Humidity: {humidity}%")

            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(icon_url).content)
            self.icon_label.setPixmap(pixmap)
        except:
            self.temp_label.setText("Error fetching weather!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
