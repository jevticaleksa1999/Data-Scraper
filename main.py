"""
main.py

Entry point for the scraping project.

Usage:
    python main.py

This will:
    - scrape data from configured pages
    - store results as CSV and JSON
    - run a basic analysis on the CSV
"""

from pathlib import Path

from src.analyze import run_basic_analysis
from src.http_client import HttpClient
from src.scraper import Scraper
from src.storage import save_to_csv, save_to_json


def main() -> None:
    http_client = HttpClient()
    scraper = Scraper(http_client=http_client)

    # 1. Scrape data
    records = scraper.scrape_all_pages()

    # 2. Store data
    csv_path: Path = save_to_csv(records, filename="transactions.csv")
    _ = save_to_json(records, filename="transactions.json")

    # 3. Run basic analysis
    run_basic_analysis(csv_path)


if __name__ == "__main__":
    main()
