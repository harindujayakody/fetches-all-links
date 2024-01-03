import os
import requests
from bs4 import BeautifulSoup
import pyfiglet
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Function to fetch links from a webpage, count them, and save them to a text file grouped by domain
def fetch_links_and_save(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all the anchor tags (<a>) in the page
            links = soup.find_all('a', href=True)
            
            # Extract the links and group them by domain
            link_groups = {}
            for link in links:
                href = link['href']
                domain = href.split('/')[2] if href.startswith('http') else 'Other'
                if domain not in link_groups:
                    link_groups[domain] = []
                link_groups[domain].append(href)

            # Save the grouped links to a text file
            with open('links.txt', 'w') as file:
                for domain, domain_links in link_groups.items():
                    file.write(f"{domain} Links:\n")
                    for link in domain_links:
                        file.write(link + '\n')
            
            print(Fore.GREEN + f'Total {len(links)} links saved to links.txt, grouped by domain')
        else:
            print(Fore.RED + f'Failed to retrieve the webpage. Status code: {response.status_code}')
    except Exception as e:
        print(Fore.RED + f'An error occurred: {e}')

# Function to ask the user for retry or close options
def ask_for_retry_or_close():
    while True:
        choice = input(Fore.CYAN + "Do you want to retry (R) or close (C)? ").strip().lower()
        if choice == 'r':
            return True
        elif choice == 'c':
            return False
        else:
            print(Fore.YELLOW + "Invalid choice. Please enter 'R' to retry or 'C' to close.")

if __name__ == "__main__":
    # Create an ASCII art heading using pyfiglet
    heading = pyfiglet.figlet_format("Link Scraper", font="slant")
    
    while True:
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + heading)
        
        # Hero section with credits and GitHub link
        print(Fore.MAGENTA + "Author: Harindu Jayakody")
        print(Fore.MAGENTA + "GitHub Repo 🩷: https://github.com/harindujayakody/fetches-all-links\n")
        
        url = input(Fore.YELLOW + "Enter the URL of the webpage: ")
        
        # Clean previous data by overwriting the file
        with open('links.txt', 'w') as file:
            file.write('')
        
        fetch_links_and_save(url)
        
        retry = ask_for_retry_or_close()
        if not retry:
            break