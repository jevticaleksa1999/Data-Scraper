import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.nike.com/hu/en/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; NikeScraper/1.0; +https://example.com)"
}


def fetch_page(url: str) -> str:
    """Preuzimanje HTML stranice."""
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


def parse_links(html: str):
    """Parsiranje HTML-a i izdvajanje relevantnih linkova."""
    soup = BeautifulSoup(html, "html.parser")

    all_links = soup.find_all("a", href=True)

    results = []

    for a in all_links:
        href = a["href"]
        text = a.get_text(strip=True)

        # Filtriramo samo Nike linkove, ignorišemo prazan tekst
        if not href.startswith("http"):
            href_full = "https://www.nike.com" + href
        else:
            href_full = href

        if not text:
            continue

        # Primer filtera: linkovi koji su verovatno proizvodi ili kategorije
        if "/t/" in href_full or "/w/" in href_full or "/men" in href_full or "/women" in href_full:
            results.append({
                "text": text,
                "url": href_full
            })

    return results


def save_to_csv(links, filename="nike_links.csv"):
    """Čuvanje rezultata u CSV fajl."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "url"])
        writer.writeheader()
        writer.writerows(links)

    print(f"[OK] Sačuvano {len(links)} linkova u fajl {filename}")


def main():
    print("[INFO] Preuzimam stranicu...")
    html = fetch_page(URL)

    print("[INFO] Parsiram linkove...")
    links = parse_links(html)

    # Prikažemo prvih par u konzoli
    print(f"[INFO] Pronađeno {len(links)} linkova.")
    for l in links[:10]:
        print("-", l["text"], "->", l["url"])

    save_to_csv(links)


if __name__ == "__main__":
    main()
