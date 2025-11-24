"""
config.py

Central configuration for the scraping project.
You can adapt BASE_URL and the CSS selectors to match a specific target website.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScraperConfig:
    # Example paginated URL – change to real target
    base_url: str = ""

    # First and last page to scrape (inclusive)
    start_page: int = 1
    end_page: int = 5

    # Network settings
    request_timeout: int = 10
    sleep_between_requests: float = 1.5

    # HTML parsing selectors – adjust to target HTML structure
    table_selector: str = "table"         # e.g. "table.tx-table"
    row_selector: str = "tbody tr"
    cell_selector: str = "td"

    # Expected columns in each row (order matters)
    columns: tuple = (
        "tx_hash",
        "from_address",
        "to_address",
        "value",
        "timestamp",
    )


CONFIG = ScraperConfig()
