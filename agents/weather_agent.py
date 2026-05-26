from tools.weather_tool import fetch_weather
from config.config      import CITY, LATITUDE, LONGITUDE


class WeatherAgent:
    """
    Fetches current weather for the configured city.
    Returns a structured dict for downstream agents.
    """

    def run(self) -> dict:
        print(f"[WeatherAgent] Fetching weather for {CITY}...")
        data = fetch_weather(LATITUDE, LONGITUDE, CITY)
        print(f"[WeatherAgent] Done. {data['temp_c']}°C, {data['condition']}")
        return data