"""
parser.py

HTML parsing utilities that extract structured data from HTML tables.
"""

from typing import List, Dict

from bs4 import BeautifulSoup

from .config import CONFIG


def parse_transactions(html: str) -> List[Dict[str, str]]:
    """
    Parse a table of transactions from the given HTML.
    The behaviour is controlled by selectors from CONFIG.
    """
    soup = BeautifulSoup(html, "html.parser")

    table = soup.select_one(CONFIG.table_selector)
    if table is None:
        print("[WARN] No table found with selector:", CONFIG.table_selector)
        return []

    rows = table.select(CONFIG.row_selector)
    if not rows:
        print("[WARN] No rows found with selector:", CONFIG.row_selector)
        return []

    transactions: List[Dict[str, str]] = []

    for row in rows:
        cells = row.select(CONFIG.cell_selector)
        if len(cells) < len(CONFIG.columns):
            # Row does not have enough cells – skip
            continue

        record: Dict[str, str] = {}
        for index, column_name in enumerate(CONFIG.columns):
            text_value = cells[index].get_text(strip=True)
            record[column_name] = text_value

        transactions.append(record)

    return transactions
