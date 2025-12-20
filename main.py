# main.py
from news.rss import get_news
from weather.wttr import get_weather

CITY = "Tianjin"
NEWS_FEED = "https://feeds.bbci.co.uk/news/world/rss.xml"

def main():
    print("=" * 50)
    print(f"📍 {CITY} 今日信息")
    print("=" * 50)

    # 天气
    weather = get_weather(CITY)
    if weather:
        print(f"🌡 当前温度: {weather['temp']}°C  💧 湿度: {weather['humidity']}%")
        print(f"☁ 天气: {weather['desc']}")
    print("-" * 50)


    news = get_news(NEWS_FEED, limit=5)

    if not news:
        print("没有获取到新闻条目")
        return

    print("今日新闻：\n")
    for i, item in enumerate(news, 1):
        # 显示标题 + 链接
        print(f"{i}. {item['title']}")
        print(f"   链接: {item['link']}\n")

if __name__ == "__main__":
    main()
