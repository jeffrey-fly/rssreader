import requests

city = "tianjin"
url = f"https://wttr.in/{city}?format=j1"
resp = requests.get(url)
data = resp.json()

current = data["current_condition"][0]
print(f"{city} 当前气温: {current['temp_C']}°C, 湿度: {current['humidity']}%, 天气: {current['weatherDesc'][0]['value']}")

