from pathlib import Path
from platformdirs import user_data_dir

APP_NAME = "rssreader"
APP_VERSION = "v1"
APP_AUTHOR = "Jeffrey"

DATA_DIR = Path(user_data_dir(APP_NAME))
DATA_DIR.mkdir(parents=True, exist_ok=True)

FEEDS_FILE = DATA_DIR/"feeds.json"
LOG_FILE= DATA_DIR/"rssreader.log"