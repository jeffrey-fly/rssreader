# RSSReader

RSSReader is a lightweight desktop RSS reader built with **Python** and **PySide6**.  
This project is primarily a **hands-on learning project** for practicing Python application development, GUI programming, and basic software architecture.

The goal of this repository is not to provide a fully polished RSS client, but to incrementally build a usable application while learning and improving along the way.

---

## Features

- Desktop GUI built with **PySide6**
- Subscribe to multiple RSS/Atom feeds
- Display article lists sorted by publish time
- Open full articles using **QWebEngineView**
- Simple, readable two-pane layout (article list + content view)
- Clear separation between UI, services, and data handling

> Advanced features such as reader-mode content extraction are intentionally **not included yet** and may be explored later as part of continued learning.

---

## Project Motivation

This project is a **personal learning exercise** with the following goals:

- Learn Python beyond scripting
- Practice structuring a medium-sized application
- Understand Qt-based GUI development
- Explore real-world concerns such as networking, UI responsiveness, and modular design
- Gradually evolve a project through refactoring and iteration

Code clarity and learning value are prioritized over completeness or performance optimizations.

---

## Project Structure
```
rssreader/
├── core/ # Core logic and shared utilities
├── services/ # RSS fetching and data services
├── ui/ # Qt UI components
│ ├── main_window.py
│ └── reader_page.py
├── feeds.json # Sample feed configuration
├── app.py # Application entry point
└── README.md
```

## Requirements

- Python 3.8+
- PySide6 (with Qt WebEngine support)

---

## Installation

It is recommended to use a virtual environment.

```bash
git clone git@github.com:jeffrey-fly/rssreader.git
cd rssreader

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
