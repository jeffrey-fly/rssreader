# services/rss_service.py
import feedparser
import requests
import certifi


class RSSService:
    def fetch(self, url: str):
        try:
            # 第一优先：feedparser 直接解析
            feed = feedparser.parse(url)
            if feed.bozo:
                raise Exception(feed.bozo_exception)

        except Exception:
            # 兜底方案：requests + certifi
            resp = requests.get(
                url,
                timeout=5,
                verify=certifi.where(),
                headers={
                    "User-Agent": "RSSReader/1.0"
                },
            )
            resp.raise_for_status()
            feed = feedparser.parse(resp.text)

        items = []
        for entry in feed.entries:
            content = ""

            if "content" in entry:
                content = entry.content[0].value
            elif "summary" in entry:
                content = entry.summary

            items.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(entry, "published", ""),
                "content": content,
            })

        return items
