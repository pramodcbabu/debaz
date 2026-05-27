import os
import requests
from pathlib import Path
import concurrent.futures
import logging

logging.basicConfig(level=logging.INFO)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url: str, dest: Path):
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Downloaded {url} to {dest}")
    except Exception as e:
        logging.error(f"Failed to download {url}: {e}")

def crawl_form20(up_to_year: int = 2027):
    """Crawl ECI Form 20 PDFs for Uttar Pradesh assembly elections up to a given year.
    This is a placeholder implementation – the real URLs should be derived from the
    Chief Electoral Officer website. For demonstration we download a couple of static
    example files.
    """
    ensure_data_dir()
    base_url = "https://example.com/eci/up/form20"
    # Example static URLs (replace with real ones)
    sample_urls = [
        f"{base_url}/UP_2022_Form20.pdf",
        f"{base_url}/UP_2017_Form20.pdf",
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for url in sample_urls:
            filename = url.split('/')[-1]
            dest = DATA_DIR / filename
            futures.append(executor.submit(download_file, url, dest))
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    crawl_form20()
