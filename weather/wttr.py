import requests
from requests.exceptions import RequestException, Timeout

def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        resp = requests.get(url)
        data = resp.json()
        current = data["current_condition"][0]
        result = f"{city} 当前气温: {current['temp_C']}°C, 湿度: {current['humidity']}%, 天气: {current['weatherDesc'][0]['value']}"
    except Timeout:
        result = "请求天气服务超时（city={city}）"
    except RequestException as e:
        result = f"请求天气服务失败（city={city}）：{e}"
    except ValueError as e:
        result = f"天气数据解析失败（city={city}）：{e}"
    except Exception as e:
        result =f"未知错误（city={city}）：{e}"
    return result