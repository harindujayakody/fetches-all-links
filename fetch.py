import os
import sys
import time
import subprocess
from urllib.parse import urlparse, urljoin

# Reconfigure stdout/stderr to utf-8 on Windows to handle rich unicode & emojis cleanly
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

# Required packages mapping: module_name -> pip package_name
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

# Perform dependency auto-check before importing third-party libraries
check_and_install_dependencies()

# Import third-party libraries after verification
import requests
from bs4 import BeautifulSoup
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

console = Console()

def render_oh_my_posh_header():
    """Renders a modern Oh My Posh styled terminal header."""
    os.system('cls' if os.name == 'nt' else 'clear')

    # Figlet ASCII Banner
    try:
        figlet_text = pyfiglet.figlet_format("Link Scraper", font="slant")
        console.print(f"[bold magenta]{figlet_text}[/bold magenta]")
    except Exception:
        console.print("[bold cyan]=== LINK SCRAPER ===[/bold cyan]\n")

    # Oh My Posh Styled Status Header Panel
    posh_panel = Panel(
        "[bold black on cyan] ⚡ LinkScraper Core [/bold black on cyan]  │  "
        "[bold white on magenta] 👤 Harindu Jayakody [/bold white on magenta]  │  "
        "[bold black on yellow] 🐍 Python 3 [/bold black on yellow]  │  "
        "[bold white on green] 🩷 github.com/harindujayakody/fetches-all-links [/bold white on green]",
        title="[bold bright_blue]── Oh My Posh Terminal UI ──[/bold bright_blue]",
        border_style="bright_blue",
        padding=(0, 1)
    )
    console.print(posh_panel)
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
            SpinnerColumn("dots", style="bold cyan"),
            TextColumn("[bold cyan]Connecting to webpage & scraping links...[/bold cyan]"),
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

            # Save grouped links with (1), (2) numbering under each domain header
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

            # Display Oh My Posh styled output tree in Terminal with (1), (2)... domain link numbering
            tree = Tree(f"[bold bright_green]🌐 Scraped Output for:[/] [bold underline cyan]{url}[/]")
            
            for domain, domain_links in link_groups.items():
                domain_node = tree.add(f"[bold yellow]📂 {domain}[/] [bold magenta]({len(domain_links)} links)[/]")
                for index, l in enumerate(domain_links, start=1):
                    domain_node.add(f"[bold dim cyan]({index})[/bold dim cyan] [white]{l}[/white]")

            console.print()
            console.print(tree)
            console.print()

            # Oh My Posh Summary Card Panel
            summary_table = Table.grid(padding=(0, 2))
            summary_table.add_column(style="bold cyan", justify="right")
            summary_table.add_column(style="bold white")
            summary_table.add_row("🔗 Target URL:", url)
            summary_table.add_row("📊 Total Links Saved:", f"[bold green]{total_links}[/bold green]")
            summary_table.add_row("🌐 Unique Domains:", f"[bold yellow]{len(link_groups)}[/bold yellow]")
            summary_table.add_row("⏱️ Execution Time:", f"[bold magenta]{elapsed_time}s[/bold magenta]")
            summary_table.add_row("💾 Saved File Location:", f"[bold underline green]{OUTPUT_FILE}[/bold underline green]")

            console.print(
                Panel(
                    summary_table,
                    title="[bold green]✔ SCRAPING COMPLETED SUCCESSFULLY[/bold green]",
                    border_style="green",
                    padding=(1, 2)
                )
            )

        else:
            console.print(
                Panel(
                    f"[bold red]Failed to retrieve webpage. Status Code: {response.status_code}[/bold red]",
                    title="[bold red]✖ HTTP ERROR[/bold red]",
                    border_style="red"
                )
            )
    except requests.exceptions.RequestException as e:
        console.print(
            Panel(
                f"[bold red]Network error occurred:\n{e}[/bold red]",
                title="[bold red]✖ NETWORK FAILURE[/bold red]",
                border_style="red"
            )
        )
    except Exception as e:
        console.print(
            Panel(
                f"[bold red]An unexpected error occurred:\n{e}[/bold red]",
                title="[bold red]✖ ERROR[/bold red]",
                border_style="red"
            )
        )

def main():
    while True:
        render_oh_my_posh_header()

        # Oh My Posh Styled Segment Prompt
        console.print("[bold bright_blue]╭─[/bold bright_blue] [bold black on cyan] 🌐 LinkScraper [/bold black on cyan] [bold yellow]Enter Webpage URL:[/bold yellow]")
        url_input = Prompt.ask("[bold bright_blue]╰─❯[/bold bright_blue] ").strip()

        # Clean previous file data
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
            file.write('')

        fetch_links_and_save(url_input)

        console.print()
        console.print("[bold bright_blue]╭─[/bold bright_blue] [bold white on magenta] 🔄 Action Required [/bold white on magenta] [bold cyan]Retry or Close?[/bold cyan]")
        choice = Prompt.ask(
            "[bold bright_blue]╰─❯[/bold bright_blue] [bold green](R)etry[/bold green] or [bold red](C)lose[/bold red]",
            choices=["r", "c", "R", "C"],
            default="r"
        ).strip().lower()

        if choice == 'c':
            console.print("\n[bold cyan]👋 Thank you for using Link Scraper! Goodbye.[/bold cyan]\n")
            break

if __name__ == "__main__":
    main()