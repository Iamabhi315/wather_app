import sys
import os
import requests
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QLineEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

# Load API key from environment variable (set OPENWEATHER_API_KEY in your system)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "53801ff1a10ef")


# ─────────────────────────────────────────────
# Worker thread to fetch weather without blocking UI
# ─────────────────────────────────────────────
class WeatherWorker(QThread):
    result_ready = pyqtSignal(dict)   # emits parsed data dict on success
    error_occurred = pyqtSignal(str)  # emits error message string on failure

    def __init__(self, city):
        super().__init__()
        self.city = city

    def run(self):
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={self.city}&appid={API_KEY}&units=metric"
        )
        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get("cod") != 200:
                self.error_occurred.emit("City not found!")
                return

            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_data = requests.get(icon_url, timeout=10).content

            self.result_ready.emit({
                "temp":       data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity":   data["main"]["humidity"],
                "wind":       data["wind"]["speed"],
                "desc":       data["weather"][0]["description"].capitalize(),
                "icon_data":  icon_data,
            })

        except requests.exceptions.ConnectionError:
            self.error_occurred.emit("No internet connection!")
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Request timed out!")
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Network error: {e}")
        except Exception as e:
            self.error_occurred.emit(f"Unexpected error: {e}")


# ─────────────────────────────────────────────
# Main Weather App Window
# ─────────────────────────────────────────────
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("weather_icon.png"))
        self.resize(400, 700)
        self.worker = None  # holds reference to current worker thread

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
                font-size: 20px;
                border-radius: 15px;
                border: 2px solid white;
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
            }
            QPushButton {
                background-color: white;
                color: #090979;
                padding: 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #00D4FF;
                color: white;
            }
            QPushButton:disabled {
                background-color: #aaaaaa;
                color: #555555;
            }
            QLabel {
                color: white;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # ── Live date-time label ──
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignCenter)
        self.datetime_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.datetime_label)

        # Store timer as instance variable so it isn't garbage-collected
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

        # ── City input ──
        self.city_label = QLabel("🌏 Enter City Name:")
        self.city_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.city_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.city_label)

        self.city_input = QLineEdit()
        self.city_input.setAlignment(Qt.AlignCenter)
        self.city_input.setPlaceholderText("e.g. London, Tokyo, New York")
        # Allow pressing Enter to fetch weather
        self.city_input.returnPressed.connect(self.get_weather)
        layout.addWidget(self.city_input)

        # ── Fetch button ──
        self.get_weather_btn = QPushButton("Get Weather")
        self.get_weather_btn.clicked.connect(self.get_weather)
        layout.addWidget(self.get_weather_btn)

        # ── Result labels ──
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

        self.wind_label = QLabel("")
        self.wind_label.setFont(QFont("Segoe UI", 12))
        self.wind_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.temp_label)
        layout.addWidget(self.feels_like_label)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.humidity_label)
        layout.addWidget(self.wind_label)

        self.setLayout(layout)

    # ── Helpers ──────────────────────────────

    def update_datetime(self):
        now = datetime.now().strftime("%b %d, %Y  -  %I:%M:%S %p")
        self.datetime_label.setText(now)

    def set_ui_loading(self, loading: bool):
        """Disable/enable controls while a fetch is in progress."""
        self.get_weather_btn.setEnabled(not loading)
        self.city_input.setEnabled(not loading)
        if loading:
            self.get_weather_btn.setText("Fetching…")
            self.temp_label.setText("")
            self.feels_like_label.setText("")
            self.description_label.setText("")
            self.humidity_label.setText("")
            self.wind_label.setText("")
            self.icon_label.clear()
        else:
            self.get_weather_btn.setText("Get Weather")

    # ── Weather fetch ─────────────────────────

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.temp_label.setText("Please enter a city!")
            return

        self.set_ui_loading(True)

        # Create and connect the background worker
        self.worker = WeatherWorker(city)
        self.worker.result_ready.connect(self.on_weather_received)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.start()

    def on_weather_received(self, data: dict):
        self.set_ui_loading(False)

        self.temp_label.setText(f"{data['temp']}°C")
        self.feels_like_label.setText(f"Feels like {data['feels_like']}°C")
        self.description_label.setText(data["desc"])
        self.humidity_label.setText(f"💧 Humidity: {data['humidity']}%")
        self.wind_label.setText(f"💨 Wind: {data['wind']} m/s")

        pixmap = QPixmap()
        pixmap.loadFromData(data["icon_data"])
        self.icon_label.setPixmap(pixmap)

    def on_error(self, message: str):
        self.set_ui_loading(False)
        self.temp_label.setText(message)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
