"""
analyze.py

Basic data analysis on the scraped transactions using pandas.
"""

from pathlib import Path

import pandas as pd


def run_basic_analysis(csv_path: Path) -> None:
    if not csv_path.exists():
        print(f"[ERROR] CSV file not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    print("=== Basic Analysis ===")
    print(f"Total records: {len(df)}")

    # If there is a numeric 'value' column (e.g. '0.12 ETH'),
    # you can clean it like this:
    if "value" in df.columns:
        cleaned = (
            df["value"]
            .astype(str)
            .str.replace("ETH", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        # Filter out non-numeric values
        cleaned_numeric = pd.to_numeric(cleaned, errors="coerce")
        total_value = cleaned_numeric.sum(skipna=True)
        print(f"Total numeric value (approx): {total_value}")

    if "from_address" in df.columns:
        print("\nTop 5 senders (by count):")
        print(df["from_address"].value_counts().head(5))
