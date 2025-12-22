import requests
from requests.exceptions import RequestException, Timeout

class WeatherService:
    def get_weather(self, city: str):
        url = f"https://wttr.in/{city}?format=j1"

        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            current = data["current_condition"][0]

            return {
                "city": city,
                "temp": current["temp_C"],
                "humidity": current["humidity"],
                "desc": current["weatherDesc"][0]["value"],
            }
        except (RequestException, Timeout):
            return None
