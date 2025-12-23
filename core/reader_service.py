from core.extractor import extract_article
from core.reader_html import build_reader_html

class ReaderService:
    def load_reader_html(self, url: str) -> str:
        article = extract_article(url)
        if not article or not article.get("content"):
            raise RuntimeError("正文抽取失败")
        return build_reader_html(article)
