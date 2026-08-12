import os
import sys
import time
import subprocess
from urllib.parse import urlparse, urljoin

# Reconfigure stdout/stderr to utf-8 on Windows for clean rendering of unicode characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Clean terminal screen on script load
os.system('cls' if os.name == 'nt' else 'clear')

# Script output file location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'links.txt')

# Required packages mapping
REQUIRED_PACKAGES = {
    "requests": "requests",
    "bs4": "beautifulsoup4",
    "pyfiglet": "pyfiglet",
    "colorama": "colorama",
    "rich": "rich"
}

def check_and_install_dependencies():
    """Auto-check missing modules when script starts and install them via pip."""
    missing = []
    for module_name, package_name in REQUIRED_PACKAGES.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
            
    if missing:
        print(f"Missing required module(s): {', '.join(missing)}")
        print("Installing missing modules automatically via pip...\n")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("\nDependencies installed successfully!\n")
        except Exception as e:
            print(f"Error installing dependencies: {e}")
            sys.exit(1)

check_and_install_dependencies()

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
    """Renders a sleek, dark, modern terminal header without buggy powerline backgrounds."""
    os.system('cls' if os.name == 'nt' else 'clear')

    # Figlet header in dark neon cyan
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

def fetch_links_and_save(url):
    url = url.strip()
    if not url:
        console.print("[bold red]❌ Error: No URL provided.[/bold red]")
        return

    # Automatically add scheme if missing (e.g., 'example.com' -> 'https://example.com')
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

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
                link_groups[domain].append(full_url)

            total_links = sum(len(domain_links) for domain_links in link_groups.values())
            elapsed_time = round(time.time() - start_time, 2)

            # Save grouped links with (1), (2) numbering under each domain header to links.txt
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
                file.write("================================================================================\n")
                file.write(f"🌐 LINK SCRAPER OUTPUT - TARGET: {url}\n")
                file.write(f"📊 TOTAL LINKS: {total_links} | UNIQUE DOMAINS: {len(link_groups)}\n")
                file.write("================================================================================\n\n")

                for domain, domain_links in link_groups.items():
                    file.write(f"🌐 DOMAIN: {domain} ({len(domain_links)} links)\n")
                    file.write("-" * 80 + "\n")
                    for index, l in enumerate(domain_links, start=1):
                        file.write(f"  ({index}) {l}\n")
                    file.write("\n")

            # Sleek modern tree output
            tree = Tree(
                f"[bold bright_cyan]🌐 Target Webpage:[/] [bold underline white]{url}[/]",
                guide_style="grey35"
            )
            
            for domain, domain_links in link_groups.items():
                domain_node = tree.add(
                    f"[bold yellow]📂 {domain}[/] [dim magenta]({len(domain_links)} links)[/]"
                )
                for index, l in enumerate(domain_links, start=1):
                    domain_node.add(
                        f"[bold bright_cyan]({index})[/bold bright_cyan] [grey85]{l}[/grey85]"
                    )

            console.print()
            console.print(tree)
            console.print()

            # Sleek Dark Summary Card
            summary_table = Table.grid(padding=(0, 2))
            summary_table.add_column(style="bold bright_cyan", justify="right")
            summary_table.add_column(style="white")

            summary_table.add_row("🎯 Target URL:", f"[bold white]{url}[/bold white]")
            summary_table.add_row("📊 Total Links Extracted:", f"[bold spring_green3]{total_links}[/bold spring_green3]")
            summary_table.add_row("🌐 Unique Domains:", f"[bold yellow]{len(link_groups)}[/bold yellow]")
            summary_table.add_row("⏱️ Execution Time:", f"[bold magenta]{elapsed_time}s[/bold magenta]")
            summary_table.add_row("💾 Saved File:", f"[underline spring_green3]{OUTPUT_FILE}[/underline spring_green3]")

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

        # Modern minimalist input prompt
        url_input = Prompt.ask("[bold bright_cyan]›[/bold bright_cyan] [bold white]Enter URL to scrape[/bold white]").strip()

        # Clean previous file data
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
            file.write('')

        fetch_links_and_save(url_input)

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