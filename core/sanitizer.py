# core/sanitizer.py
import bleach

ALLOWED_TAGS = [
    "p", "br", "strong", "em",
    "ul", "ol", "li",
    "h1", "h2", "h3",
    "img", "pre", "code",
    "a", "blockquote",
]

ALLOWED_ATTRS = {
    "a": ["href"],
    "img": ["src", "alt"],
}

def sanitize_html(html: str) -> str:
    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
    )
