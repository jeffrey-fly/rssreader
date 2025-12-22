import requests
import feedparser
import certifi


def get_news(feed_url, limit=5):
    """
    获取 RSS 新闻条目

    参数:
        feed_url: RSS 源 URL
        limit: 返回条目数量
    返回:
        entries: list of dict, 每条 dict 包含 title 和 link
    """

    try:
        # 用 requests 先抓取 RSS 内容，显式指定证书
        resp = requests.get(feed_url, verify=certifi.where(), timeout=5)
        resp.raise_for_status()  # HTTP 错误会抛异常

    except requests.exceptions.SSLError as e:
        print(f"SSL 错误: {e}")
        return []
    except requests.exceptions.Timeout:
        print("请求超时")
        return []
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return []

    # 使用 feedparser 解析内容
    feed = feedparser.parse(resp.text)

    # 检查解析错误
    if feed.bozo:
        print(f"RSS 解析异常: {feed.bozo_exception}")

    # 检查是否有条目
    if not feed.entries:
        print("RSS 没有任何条目")
        return []

    # 构造条目列表
    entries = []
    for entry in feed.entries[:limit]:
        entries.append({
            "title": entry.title,
            "link": entry.link
        })

    return entries
