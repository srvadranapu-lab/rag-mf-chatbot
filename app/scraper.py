import os
import csv
import requests
from bs4 import BeautifulSoup

DATA_PATH = "data/raw_docs"
CSV_PATH = "data/sources.csv"

os.makedirs(DATA_PATH, exist_ok=True)

def fetch_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())

def save_text(file_name, content):
    path = os.path.join(DATA_PATH, file_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def run_scraper():
    with open(CSV_PATH, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row["url"]
            file_name = f"{row['id']}.txt"

            print(f"Scraping: {url}")
            html = fetch_page(url)

            if html:
                text = clean_text(html)
                save_text(file_name, text)

if __name__ == "__main__":
    run_scraper()