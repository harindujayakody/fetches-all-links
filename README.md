# ⚡ Web Link Scraper

<p align="center">
  <img src="https://img.shields.io/github/license/harindujayakody/fetches-all-links?style=for-the-badge&color=blue" alt="License" />
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/UI-Dark%20Mode-007ACC?style=for-the-badge&logo=powershell&logoColor=white" alt="UI" />
  <img src="https://img.shields.io/github/repo-size/harindujayakody/fetches-all-links?style=for-the-badge&color=brightgreen" alt="Repo Size" />
  <img src="https://img.shields.io/github/stars/harindujayakody/fetches-all-links?style=for-the-badge&color=yellow" alt="Stars" />
</p>

A modern, high-performance Python script that scrapes all links from any webpage, groups them into dedicated site folders (`output/<domain>/`), creates clean separate `.txt` files per domain, and formats raw links without prefixes.

---

## 📸 Interface Screenshots

<p align="center">
  <img src="Screenshot1.png" alt="Terminal Prompt UI" width="800" />
  <br/><br/>
  <img src="Screenshot2.png" alt="Link Scraping Output Tree" width="800" />
  <br/><br/>
  <img src="Screenshot3.png" alt="Folder Grouping & Execution Summary" width="800" />
</p>

---

## 🌟 Key Features

- 📁 **Folder Grouping per Site**: Creates a dedicated folder for each target URL scraped (e.g. `output/cocobee.lk/`).
- 📄 **Domain Files & Combined Output**:
  - `all_links.txt`: Combined file with all scraped links categorized by domain.
  - `<domain>.txt`: Individual `.txt` files containing clean raw links for each domain (e.g. `facebook.com.txt`, `cocobee.lk.txt`).
- 🔗 **Clean Link Formatting**: No `(1)`, `(2)` prefixes before links in output files.
- ⚡ **Launcher (`run.bat`)**: Starts the script after you install its dependencies.
- 🎨 **Dark Modern Terminal UI**:
  - Sleek dark theme layout using `rich`.
  - Minimalist prompt (`› Enter URL to scrape`).
  - Live progress spinner.
  - Execution summary cards with time and link metrics.
- 🧹 **Terminal Auto-Cleaning**: Automatically clears terminal logs on launch and before each new scraping session.

---

## 📋 Folder Output Structure Example

When scraping `https://www.cocobee.lk/`:

```text
output/
└── www.cocobee.lk/
    ├── all_links.txt
    ├── www.cocobee.lk.txt
    ├── facebook.com.txt
    ├── instagram.com.txt
    ├── tiktok.com.txt
    ├── youtube.com.txt
    ├── pinterest.com.txt
    └── infiax.com.txt
```

### Clean Raw Link File Example (`www.cocobee.lk.txt`)
```text
https://www.cocobee.lk/
https://www.cocobee.lk/shop
https://www.cocobee.lk/sale
https://www.cocobee.lk/new-arrivals
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/harindujayakody/fetches-all-links.git
cd fetches-all-links
```

### 2. Run via Batch Launcher (Windows)
Double-click `run.bat` or run:
```cmd
run.bat
```

Or run via Python directly:
```bash
python main.py
```
> **Setup:** Install dependencies in a virtual environment before launching, as shown below. The launcher never installs packages automatically.

---

## 📦 Dependency installation

Create and activate a virtual environment, then install dependencies explicitly via `requirements.txt`. On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

---

## 🤖 Crawler behaviour

- **Scope:** one page per URL. Enter one URL (or several, separated by spaces/commas) and the tool fetches that page and extracts all of its links. It does not crawl the discovered links.
- **robots.txt:** respected — a URL disallowed by the site's `robots.txt` is skipped with a notice.
- **User-Agent:** the tool identifies itself honestly as `fetches-all-links/2.0` instead of impersonating a browser.
- **Dependencies:** pinned in `requirements.txt`; install them into a virtual environment first — the script never installs packages itself.

---

## 👤 Author

Developed with ❤️ by **Harindu Jayakody**
- **GitHub**: [@harindujayakody](https://github.com/harindujayakody)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

