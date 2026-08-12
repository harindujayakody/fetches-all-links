# ⚡ Web Link Scraper

<p align="center">
  <img src="https://img.shields.io/github/license/harindujayakody/fetches-all-links?style=for-the-badge&color=blue" alt="License" />
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/UI-Oh%20My%20Posh%20Style-007ACC?style=for-the-badge&logo=powershell&logoColor=white" alt="UI" />
  <img src="https://img.shields.io/github/repo-size/harindujayakody/fetches-all-links?style=for-the-badge&color=brightgreen" alt="Repo Size" />
  <img src="https://img.shields.io/github/stars/harindujayakody/fetches-all-links?style=for-the-badge&color=yellow" alt="Stars" />
</p>

A modern, high-performance Python script that scrapes all links from any webpage, groups them by domain, and formats output with domain-scoped numbering `(1)`, `(2)`, `(3)`. Features an **Oh My Posh** inspired terminal UI powered by `rich`, automatic dependency management, and anti-blocking header handling.

---

## 🌟 Key Features

- 🌐 **Domain Grouping & Numbering**: Organizes extracted links by domain name with clean `(1)`, `(2)` numbering in both terminal tree views and output files.
- 🎨 **Oh My Posh Terminal UI/UX**:
  - Powerline status segment header (`⚡ LinkScraper` │ `👤 Harindu Jayakody` │ `🐍 Python 3`).
  - Styled multi-line prompt (`╭─ 🌐 LinkScraper ╰─❯`).
  - Live loading progress spinner.
  - Execution summary cards with total link metrics and time elapsed.
- ⚡ **Auto-Dependency Management**: Automatically checks and installs any missing Python packages on startup without crashing.
- 🧹 **Terminal Auto-Cleaning**: Automatically clears terminal logs on launch and before each new scraping session.
- 🛡️ **Robust HTTP Fetching**: Handles missing URL schemes (`example.com` ➔ `https://example.com`), includes browser `User-Agent` headers to prevent `403`/`503` blocking, and resolves relative URLs seamlessly.

---

## 📋 Output Preview (`links.txt`)

```text
================================================================================
🌐 LINK SCRAPER OUTPUT - TARGET: https://httpbin.org
📊 TOTAL LINKS: 4 | UNIQUE DOMAINS: 3
================================================================================

🌐 DOMAIN: github.com (2 links)
--------------------------------------------------------------------------------
  (1) https://github.com/requests/httpbin
  (2) https://github.com/rochacbruno/flasgger

🌐 DOMAIN: httpbin.org (1 links)
--------------------------------------------------------------------------------
  (1) https://httpbin.org/forms/post
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/harindujayakody/fetches-all-links.git
cd fetches-all-links
```

### 2. Run the Script
```bash
python fetch.py
```
> **Note**: Missing dependencies (`requests`, `beautifulsoup4`, `pyfiglet`, `colorama`, `rich`) will be auto-detected and installed automatically on your first run!

---

## 📦 Manual Installation (Optional)

If you prefer to install dependencies manually via `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 👤 Author

Developed with ❤️ by **Harindu Jayakody**
- **GitHub**: [@harindujayakody](https://github.com/harindujayakody)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
