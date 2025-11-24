"""
scraper.py

High-level scraping logic:
- iterate over pages
- fetch HTML
- parse records
"""

import time
from typing import List, Dict

from .config import CONFIG
from .http_client import HttpClient
from .parser import parse_transactions


class Scraper:
    """
    Main scraper class that coordinates HTTP fetching and HTML parsing.
    """

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def scrape_page(self, page: int) -> List[Dict[str, str]]:
        url = CONFIG.base_url.format(page=page)
        print(f"[INFO] Fetching page {page}: {url}")
        response = self.http_client.get(url, timeout=CONFIG.request_timeout)
        html = response.text
        records = parse_transactions(html)
        print(f"[INFO] Parsed {len(records)} records from page {page}")
        return records

    def scrape_all_pages(self) -> List[Dict[str, str]]:
        all_records: List[Dict[str, str]] = []

        for page in range(CONFIG.start_page, CONFIG.end_page + 1):
            try:
                page_records = self.scrape_page(page)
                all_records.extend(page_records)
            except Exception as exc:
                print(f"[ERROR] Failed to scrape page {page}: {exc}")

            time.sleep(CONFIG.sleep_between_requests)

        print(f"[INFO] Total records scraped: {len(all_records)}")
        return all_records
