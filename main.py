import os
import sys
import time

from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser

# Reconfigure stdout/stderr to utf-8 on Windows for clean rendering
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Clean terminal screen on script load
os.system('cls' if os.name == 'nt' else 'clear')

# Base output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_BASE_DIR = os.path.join(SCRIPT_DIR, 'output')

# Required packages mapping
REQUIRED_PACKAGES = {
    "requests": "requests",
    "bs4": "beautifulsoup4",
    "pyfiglet": "pyfiglet",
    "colorama": "colorama",
    "rich": "rich"
}

def check_dependencies():
    """Report missing dependencies without modifying the Python environment."""
    missing = []
    for module_name, package_name in REQUIRED_PACKAGES.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
    if missing:
        print(f"Missing required packages: {', '.join(missing)}")
        print("Activate your virtual environment and run: python -m pip install -r requirements.txt")
        sys.exit(1)

check_dependencies()

import requests
from bs4 import BeautifulSoup
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.text import Text
from rich import box

console = Console()

def render_header():
    """Renders a sleek, dark, modern terminal header."""
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        figlet_text = pyfiglet.figlet_format("Link Scraper", font="slant")
        console.print(f"[bold bright_cyan]{figlet_text}[/bold bright_cyan]")
    except Exception:
        pass

    header_text = Text()
    header_text.append("⚡ ", style="bold yellow")
    header_text.append("LINK SCRAPER ", style="bold bright_white")
    header_text.append("v2.0 ", style="bold bright_cyan")
    header_text.append("│ ", style="grey39")
    header_text.append("Web Link Crawler & Categorizer\n", style="grey70")
    header_text.append("👤 Author: ", style="bold grey54")
    header_text.append("Harindu Jayakody  ", style="bold magenta")
    header_text.append("│ ", style="grey39")
    header_text.append("🔗 Repo: ", style="bold grey54")
    header_text.append("github.com/harindujayakody/fetches-all-links", style="underline cyan")

    banner_panel = Panel(
        header_text,
        box=box.ROUNDED,
        border_style="grey35",
        padding=(0, 2)
    )
    console.print(banner_panel)
    console.print()

def sanitize_folder_name(name):
    """Sanitizes domain string to make it a safe directory name."""
    return "".join(c for c in name if c.isalnum() or c in ('-', '_', '.')).strip('.')

def allowed_by_robots(url, user_agent):
    """True unless the site's robots.txt disallows fetching `url`."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception:
        return True  # robots.txt unreachable: fail open
    try:
        return rp.can_fetch(user_agent, url)
    except Exception:
        return True


def fetch_links_and_save(url):
    url = url.strip()
    if not url:
        console.print("[bold red]❌ Error: No URL provided.[/bold red]")
        return

    # Automatically add scheme if missing (e.g., 'example.com' -> 'https://example.com')
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Identify the tool honestly instead of spoofing a Chrome browser.
    # Some sites serve different (or no) content to scrapers; identifying
    # ourselves keeps the tool's behaviour transparent.
    headers = {
        'User-Agent': 'fetches-all-links/2.0 (+https://github.com/harindujayakody/fetches-all-links)'
    }

    # Respect robots.txt: skip the URL if the site disallows this crawler.
    # A robots.txt that cannot be fetched (404/network error) is treated as
    # "no restrictions", per the standard's fail-open convention.
    if not allowed_by_robots(url, headers['User-Agent']):
        console.print(
            Panel(
                f"[bold yellow]Skipped:[/bold yellow] {url} is disallowed by the site's robots.txt.",
                title="[bold yellow]⚠ ROBOTS.TXT[/bold yellow]",
                box=box.ROUNDED,
                border_style="yellow",
            )
        )
        return

    start_time = time.time()

    try:
        with Progress(
            SpinnerColumn("dots", style="bold bright_cyan"),
            TextColumn("[bold bright_cyan]Scraping webpage & analyzing links...[/bold bright_cyan]"),
            transient=True
        ) as progress:
            progress.add_task("scrape", total=None)
            response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)

            target_domain = urlparse(url).netloc or "scraped_site"
            site_folder_name = sanitize_folder_name(target_domain)
            target_output_dir = os.path.join(OUTPUT_BASE_DIR, site_folder_name)
            os.makedirs(target_output_dir, exist_ok=True)

            link_groups = {}
            for link in links:
                href = link['href'].strip()
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                    continue

                full_url = urljoin(url, href)
                parsed = urlparse(full_url)
                domain = parsed.netloc if parsed.netloc else 'Other'

                if domain not in link_groups:
                    link_groups[domain] = []
                
                # Deduplicate links preserving insertion order
                if full_url not in link_groups[domain]:
                    link_groups[domain].append(full_url)

            total_links = sum(len(domain_links) for domain_links in link_groups.values())
            elapsed_time = round(time.time() - start_time, 2)

            # 1. Save combined all_links.txt inside the website result folder (clean raw links without (1) numbers)
            main_output_file = os.path.join(target_output_dir, 'all_links.txt')
            with open(main_output_file, 'w', encoding='utf-8') as file:
                file.write("================================================================================\n")
                file.write(f"🌐 LINK SCRAPER OUTPUT - TARGET: {url}\n")
                file.write(f"📊 TOTAL UNIQUE LINKS: {total_links} | UNIQUE DOMAINS: {len(link_groups)}\n")
                file.write("================================================================================\n\n")

                for domain, domain_links in link_groups.items():
                    file.write(f"🌐 DOMAIN: {domain} ({len(domain_links)} links)\n")
                    file.write("-" * 80 + "\n")
                    for l in domain_links:
                        file.write(f"{l}\n")
                    file.write("\n")

            # 2. Save individual domain .txt files inside the website result folder (clean raw links)
            for domain, domain_links in link_groups.items():
                domain_filename = sanitize_folder_name(domain) + ".txt"
                domain_filepath = os.path.join(target_output_dir, domain_filename)
                with open(domain_filepath, 'w', encoding='utf-8') as df:
                    for l in domain_links:
                        df.write(f"{l}\n")

            # Sleek modern tree output (clean raw links without (1) prefixes)
            tree = Tree(
                f"[bold bright_cyan]🌐 Scraped Output for:[/] [bold underline white]{url}[/]\n"
                f"[bold grey70]📁 Folder:[/] [bold green]{target_output_dir}[/]",
                guide_style="grey35"
            )
            
            for domain, domain_links in link_groups.items():
                domain_node = tree.add(
                    f"[bold yellow]📂 {domain}[/] [dim magenta]({len(domain_links)} links)[/]"
                )
                for l in domain_links:
                    domain_node.add(f"[grey85]{l}[/grey85]")

            console.print()
            console.print(tree)
            console.print()

            # Sleek Dark Summary Card
            summary_table = Table.grid(padding=(0, 2))
            summary_table.add_column(style="bold bright_cyan", justify="right")
            summary_table.add_column(style="white")

            summary_table.add_row("🎯 Target URL:", f"[bold white]{url}[/bold white]")
            summary_table.add_row("📊 Total Unique Links:", f"[bold spring_green3]{total_links}[/bold spring_green3]")
            summary_table.add_row("🌐 Unique Domains:", f"[bold yellow]{len(link_groups)}[/bold yellow]")
            summary_table.add_row("⏱️ Execution Time:", f"[bold magenta]{elapsed_time}s[/bold magenta]")
            summary_table.add_row("📁 Result Folder:", f"[bold underline green]{target_output_dir}[/bold underline green]")
            summary_table.add_row("💾 Combined File:", f"[underline cyan]{main_output_file}[/underline cyan]")

            console.print(
                Panel(
                    summary_table,
                    title="[bold spring_green3]✔ SCRAPE COMPLETE[/bold spring_green3]",
                    box=box.ROUNDED,
                    border_style="spring_green3",
                    padding=(1, 2)
                )
            )

        else:
            console.print(
                Panel(
                    f"[bold red]Failed to retrieve webpage. Status Code: {response.status_code}[/bold red]",
                    title="[bold red]✖ HTTP ERROR[/bold red]",
                    box=box.ROUNDED,
                    border_style="red"
                )
            )
    except requests.exceptions.RequestException as e:
        console.print(
            Panel(
                f"[bold red]Network error occurred:\n{e}[/bold red]",
                title="[bold red]✖ NETWORK ERROR[/bold red]",
                box=box.ROUNDED,
                border_style="red"
            )
        )
    except Exception as e:
        console.print(
            Panel(
                f"[bold red]An unexpected error occurred:\n{e}[/bold red]",
                title="[bold red]✖ ERROR[/bold red]",
                box=box.ROUNDED,
                border_style="red"
            )
        )

def main():
    while True:
        render_header()

        url_input = Prompt.ask("[bold bright_cyan]›[/bold bright_cyan] [bold white]Enter URL(s) to scrape (separate multiple URLs with a space or comma)[/bold white]").strip()

        # One page per URL: each URL is fetched and all links on that page
        # are extracted. Separate several URLs with spaces and/or commas.
        urls = [u for u in url_input.replace(",", " ").split() if u]
        if not urls:
            console.print("[bold red]❌ Error: No URL provided.[/bold red]")
        for url in urls:
            fetch_links_and_save(url)

        console.print()
        choice = Prompt.ask(
            "[bold bright_cyan]›[/bold bright_cyan] [bold white]Retry (r) or Close (c)?[/bold white]",
            choices=["r", "c", "R", "C"],
            default="r"
        ).strip().lower()

        if choice == 'c':
            console.print("\n[bold dim cyan]👋 Goodbye![/bold dim cyan]\n")
            break

if __name__ == "__main__":
    main()
