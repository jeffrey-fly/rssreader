# ui/console.py
def show(weather, news, city):
    print("=" * 40)
    print(f"📍 {city}")
    print(f"🌡 {weather['temp']}°C  💧 {weather['humidity']}%")
    print(f"☁ {weather['desc']}")
    print("\n📰 今日新闻:")
    for i, item in enumerate(news, 1):
        print(f"{i}. {item['title']}")
    print("=" * 40)