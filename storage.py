"""
storage.py

Simple helpers for storing scraped data as CSV and JSON.
"""

import csv
import json
from pathlib import Path
from typing import List, Dict

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def save_to_csv(records: List[Dict[str, str]], filename: str = "transactions.csv") -> Path:
    if not records:
        print("[INFO] No records to save to CSV.")
        return DATA_DIR / filename

    path = DATA_DIR / filename
    fieldnames = list(records[0].keys())

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[OK] Saved CSV file: {path}")
    return path


def save_to_json(records: List[Dict[str, str]], filename: str = "transactions.json") -> Path:
    path = DATA_DIR / filename

    with path.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"[OK] Saved JSON file: {path}")
    return path
