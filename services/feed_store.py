import json
from pathlib import Path

class FeedStore:
    def __init__(self, path="feeds.json"):
        self.path = Path(path)
        self.data = {"feeds": []}
        self.load()

    def load(self):
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def save(self):
        self.path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def all(self):
        return self.data["feeds"]

    def add(self, feed):
        self.data["feeds"].append({"id": feed["id"], "name": feed["name"], "urls": feed["urls"]})
        self.save()
