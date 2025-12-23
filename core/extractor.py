import trafilatura


def extract_article(url: str) -> dict:
    """
    从 URL 抽取文章正文与元信息

    返回字段：
        title
        author
        date
        content (HTML)
        source
    """

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return {}

    # 正文（HTML）
    content = trafilatura.extract(
        downloaded,
        output_format="html",
        include_images=True,
        include_links=True,
        with_metadata=True,
    )

    if not content:
        return {}

    # 元数据
    metadata = trafilatura.extract_metadata(downloaded)

    return {
        "title": metadata.title if metadata and metadata.title else "",
        "author": metadata.author if metadata and metadata.author else "",
        "date": metadata.date if metadata and metadata.date else "",
        "content": content,
        "source": url,
    }
