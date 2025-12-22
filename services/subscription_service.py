import json
from pathlib import Path


class SubscriptionService:
    def __init__(self, path="feeds.json"):
        self.path = Path(path)
        if not self.path.exists():
            self._save({})

    def load(self):
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_feed(self, key, name, url):
        data = self.load()
        if key not in data:
            data[key] = {"name": name, "urls": []}
        data[key]["urls"].append(url)
        self._save(data)

    def remove_feed(self, key):
        data = self.load()
        if key in data:
            del data[key]
            self._save(data)
