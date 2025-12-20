import requests
from requests.exceptions import RequestException, Timeout

def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"

    resp = requests.get(url)
    data = resp.json()
    current = data["current_condition"][0]

    return {
        "temp": current["temp_C"],
        "humidity": current["humidity"],
        "desc": current["weatherDesc"][0]["value"],
    }