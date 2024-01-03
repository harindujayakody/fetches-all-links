# fetches-all-links

![image](https://github.com/harindujayakody/fetches-all-links/assets/9878813/71f881e8-2f51-4e9a-9451-e4086a78562c)

# Web Link Scraper

Web Link Scraper is a Python script that allows you to fetch all links from a given webpage and save them to a text file, grouped by domain. The script also includes a Dracula theme for the terminal interface, a hero section with credits for the author, and options to retry or close the program.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python
- Required Python libraries (`requests`, `beautifulsoup4`, `pyfiglet`, `colorama`)

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4 pyfiglet colorama
```

## How to Use

1. Clone this repository:

```bash
git clone https://github.com/harindujayakody/fetches-all-links.git
```

2. Navigate to the repository directory:

```bash
cd your-repo
```

3. Run the Python script:

```bash
python fetch.py
```

4. Follow the on-screen instructions to enter the URL of the webpage you want to scrape.

5. The script will save the links to a text file named `links.txt`, grouped by domain. You can find this file in the same directory where the script is located.

6. You'll also see a Dracula-themed terminal interface with a hero section displaying credits for the author and a link to the GitHub repository.

7. After running the script, you can choose to retry or close the program.

## Customization

You can customize the script by modifying the following sections in the `web_link_scraper.py` file:

- **Author and GitHub Repo**: Update the author's name and GitHub repository URL in the hero section.

- **ASCII Art Heading**: Customize the ASCII art heading by changing the text and font in the `pyfiglet.figlet_format` function.

- **Dracula Theme**: If you prefer a different color theme, you can modify the terminal colors in the script.

## Credits

This script is created by [Harindu Jayakody](https://github.com/harindujayakody/fetches-all-links).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

