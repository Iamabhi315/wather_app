# 🌤️ Python Weather App

A clean, real-time desktop weather application built with **Python**, **PyQt5**, and the **OpenWeatherMap API**. Enter any city name to instantly fetch live weather data — temperature, feels-like, humidity, and weather icons — all displayed in a stylish dark-gradient GUI.

---

## 📸 Preview

> A gradient-themed desktop window with live clock, city search input, and weather results (temperature, icon, description, humidity).

---

## ✨ Features

- 🌡️ **Live Temperature** — Current temp in °C
- 🤔 **Feels Like** — Apparent temperature display
- 💧 **Humidity** — Relative humidity percentage
- 🖼️ **Weather Icon** — Fetched dynamically from OpenWeatherMap
- 📝 **Weather Description** — e.g., "Broken clouds", "Light rain"
- 🕒 **Live Clock** — Real-time date & time updated every second
- 🎨 **Stylish UI** — Dark gradient background with modern PyQt5 widgets

---

## 🛠️ Tech Stack

| Component     | Technology                     |
|---------------|-------------------------------|
| Language      | Python 3.x                    |
| GUI Framework | PyQt5                         |
| HTTP Requests | `requests` library            |
| Weather Data  | OpenWeatherMap API (Free Tier)|

---

## 📦 Requirements

Make sure you have **Python 3.7+** installed, then install the dependencies:

```bash
pip install PyQt5 requests
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/weather-app.git
cd weather-app
```

### 2. Get Your API Key

1. Visit [https://openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a **free account**
3. Navigate to **API Keys** in your dashboard
4. Copy your API key

### 3. Configure the API Key

Open `weather_app.py` and replace the placeholder with your actual key:

```python
# Line 10 in weather_app.py
API_KEY = "your_api_key_here"
```

> ⚠️ **Note:** New API keys may take **10–15 minutes** to activate after creation.

### 4. Run the App

```bash
python weather_app.py
```

---

## 🖥️ Usage

1. Launch the app — a desktop window will open
2. Type a **city name** in the input field (e.g., `Mumbai`, `London`, `New York`)
3. Click **"Get Weather"**
4. View the live weather data displayed on screen

---

## 📁 Project Structure

```
weather-app/
│
├── weather_app.py       # Main application file
├── weather_icon.png     # Window icon (optional)
└── README.md            # Project documentation
```

---

## ⚙️ Configuration

| Variable   | Location         | Description                          |
|------------|------------------|--------------------------------------|
| `API_KEY`  | `weather_app.py` | Your OpenWeatherMap API key          |
| `units`    | API URL string   | Change to `imperial` for °F          |
| Window Size| `self.resize()`  | Default is `400 x 700` px            |

---

## 🐛 Known Issues / Limitations

- ❌ No 5-day forecast (requires a paid/different API endpoint)
- ❌ No auto-location detection (manual city input only)
- ⚠️ Displays a generic error message on network failure — no detailed error logging
- 🖼️ `weather_icon.png` must be present in the same directory for the window icon to show

---

## 🔮 Possible Future Improvements

- [ ] Add 5-day / 7-day forecast view
- [ ] Auto-detect user location using IP geolocation
- [ ] Toggle between °C and °F
- [ ] Add wind speed and pressure data
- [ ] Save last searched city
- [ ] Add a search history dropdown
- [ ] Dark/Light mode toggle

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Made with ❤️ using Python & PyQt5.  
Feel free to fork, star ⭐, and contribute!