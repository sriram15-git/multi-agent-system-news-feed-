import requests

def fetch_weather(latitude: float, longitude: float, city: str) -> dict:
    """
    Fetch weather data from Open-Meteo (100% free, no API key).
    Returns a clean dict with temp, condition, rain chance, humidity, alerts.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
        ],
        "daily": [
            "precipitation_probability_max",
            "temperature_2m_max",
            "temperature_2m_min",
        ],
        "timezone": "Asia/Kolkata",
        "forecast_days": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current"]
        daily   = data["daily"]

        weather_code = current.get("weather_code", 0)
        condition    = _code_to_condition(weather_code)

        return {
            "city":          city,
            "temp_c":        current["temperature_2m"],
            "feels_like_c":  current["apparent_temperature"],
            "humidity":      current["relative_humidity_2m"],
            "wind_kmh":      current["wind_speed_10m"],
            "condition":     condition,
            "rain_chance":   daily["precipitation_probability_max"][0],
            "max_temp":      daily["temperature_2m_max"][0],
            "min_temp":      daily["temperature_2m_min"][0],
        }

    except Exception as e:
        print(f"[WeatherTool] Error: {e}")
        return {
            "city":         city,
            "temp_c":       "--",
            "feels_like_c": "--",
            "humidity":     "--",
            "wind_kmh":     "--",
            "condition":    "Unknown",
            "rain_chance":  "--",
            "max_temp":     "--",
            "min_temp":     "--",
        }


def _code_to_condition(code: int) -> str:
    """Map WMO weather code to a human-readable string."""
    if code == 0:                   return "Clear sky ☀️"
    elif code in (1, 2, 3):         return "Partly cloudy ⛅"
    elif code in (45, 48):          return "Foggy 🌫️"
    elif code in (51, 53, 55):      return "Drizzle 🌦️"
    elif code in (61, 63, 65):      return "Rainy 🌧️"
    elif code in (80, 81, 82):      return "Rain showers 🌩️"
    elif code in (95, 96, 99):      return "Thunderstorm ⛈️"
    else:                           return "Cloudy ☁️"