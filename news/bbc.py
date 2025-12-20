
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def fetch_bbc_international_news():
    url = "https://www.bbc.com/news/world"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        # 确保编码正确
        resp.encoding = resp.apparent_encoding
        html = resp.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")

    # 多个候选选择器（按优先级）
    selectors = [
        "a.gs-c-promo-heading",        # 旧式常见选择器
        "div.gs-c-promo a",            # 更宽松的 promo 捕获
        "h3 a",                        # 标题下的 a
        "a[href^='/news/']",           # 任何 /news/ 开头的链接
        "a[data-entityid]",            # 有些版面会加 data-entityid 的标识
    ]

    candidates = []
    for sel in selectors:
        found = soup.select(sel)
        if found:
            candidates.extend(found)
        # 小延迟：在某些动态站点上，先试多个选择器比较安全
        time.sleep(0.01)

    # 回退：如果完全没有找到候选，尝试查找所有 href 中包含 /news/ 的 a 标签
    if not candidates:
        candidates = [a for a in soup.find_all("a", href=True) if "/news/" in a["href"]]

    articles = []
    seen = set()
    for a in candidates:
        # title 优先取 aria-label，再取 text
        title = (a.get("aria-label") or a.get_text(strip=True) or "").strip()
        href = a.get("href", "").strip()
        if not href:
            continue
        # 把锚点/查询/片段部分也做清理（可选）
        href = href.split("#")[0]
        href = href.split("?")[0]

        # 补全相对路径
        if not href.startswith("http"):
            href = urljoin("https://www.bbc.com", href)

        # 只关心新闻文章（可根据需要放宽/收窄）
        if "/news/" not in href:
            continue

        if href in seen:
            continue
        seen.add(href)

        # 如果没有显式 title，再尝试取 <h3> 或 img alt
        if not title:
            # 尝试附近的 h3
            parent_h3 = a.find_parent("h3")
            if parent_h3:
                title = parent_h3.get_text(strip=True)
            else:
                # 查找 img alt
                img = a.find("img")
                if img and img.get("alt"):
                    title = img.get("alt").strip()

        articles.append({"title": title or "(no title)", "url": href})

    # 如果仍然空，保存页面方便你在浏览器里检查
    if not articles:
        with open("debug_bbc_world.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("⚠️ 未提取到任何文章。页面已保存为 debug_bbc_world.html，打开检查实际 DOM。")

    return articles


if __name__ == "__main__":
    news = fetch_bbc_international_news()
    for article in news:
        print(article["title"])
        print(article["url"])
        print("-" * 40)