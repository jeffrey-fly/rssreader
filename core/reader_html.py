from core.sanitizer import sanitize_html
from html import escape


READER_CSS = """
body {
    background: #fdfdfd;
}

.reader {
    max-width: 720px;
    margin: 2em auto;
    padding: 0 16px;

    font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 16px;
    line-height: 1.7;
    color: #222;
}

.reader h1 {
    font-size: 1.8em;
    margin-bottom: 0.4em;
}

.meta {
    color: #666;
    font-size: 0.9em;
    margin-bottom: 1.6em;
}

.content p {
    margin: 0.8em 0;
}

.content img {
    max-width: 100%;
    display: block;
    margin: 1em auto;
}

.content pre {
    background: #f6f8fa;
    padding: 12px;
    overflow-x: auto;
    border-radius: 6px;
    font-size: 0.9em;
}

.content code {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}
"""

def build_reader_html(article: dict) -> str:
    """
    将 article dict 转换为阅读模式 HTML
    """

    title = escape(article.get("title", ""))
    author = escape(article.get("author", ""))
    date = escape(article.get("date", ""))

    raw_content = article.get("content", "")
    content = sanitize_html(raw_content)

    meta_parts = []
    if author:
        meta_parts.append(author)
    if date:
        meta_parts.append(date)

    meta_text = " · ".join(meta_parts)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
{READER_CSS}
</style>
</head>

<body>
  <article class="reader">
    <h1>{title}</h1>

    {'<div class="meta">' + meta_text + '</div>' if meta_text else ''}

    <section class="content">
      {content}
    </section>
  </article>
</body>
</html>
"""
