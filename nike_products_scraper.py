import requests
from bs4 import BeautifulSoup
import csv

CATEGORY_URL = "https://www.nike.com/hu/en/w/mens-shoes-1m67gznik1zv660zy7ok"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0 Safari/537.36"
}


def fetch_page(url: str) -> str:
    """Preuzimanje HTML stranice."""
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def parse_products(html: str):
    """
    Parsira proizvode sa Nike kategorije.

    VAŽNO:
    - 'product-card' i ostale klase su pretpostavka.
    - Otvori stranicu u Chrome → desni klik na patiku → Inspect
      i proveri prave klase, pa ih ovde po potrebi izmeni.
    """
    soup = BeautifulSoup(html, "html.parser")

    # 1) Pronađi sve kartice proizvoda
    # Podesi selektor prema onome što vidiš u Inspect
    product_cards = soup.select("div.product-card")  # <-- moguće da treba promena

    products = []

    for card in product_cards:
        # Naziv proizvoda
        name_el = card.select_one(".product-card__title") or card.find("h3")
        if not name_el:
            continue
        name = name_el.get_text(strip=True)

        # Link proizvoda
        link_el = card.find("a", href=True)
        if not link_el:
            product_url = None
        else:
            href = link_el["href"]
            if href.startswith("http"):
                product_url = href
            else:
                product_url = "https://www.nike.com" + href

        # Cena – tražimo tekst koji sadrži €
        # (Nike često ima više cena: regularna + snižena)
        price_text = None

        # Probaj da nađeš element cene po klasi
        price_el = card.select_one(".product-price") or card.select_one(".product-card__price")

        if price_el:
            # Uzmi sav tekst iz elementa koji sadrži €
            for node in price_el.stripped_strings:
                if "€" in node:
                    price_text = node
                    break

        # Ako i dalje nismo našli, fallback – traži bilo gde u kartici
        if not price_text:
            for node in card.stripped_strings:
                if "€" in node:
                    price_text = node
                    break

        products.append({
            "name": name,
            "price": price_text,
            "url": product_url
        })

    return products


def save_to_csv(products, filename="nike_products.csv"):
    """Čuva proizvode u CSV fajl."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "url"])
        writer.writeheader()
        writer.writerows(products)
    print(f"[OK] Sačuvano {len(products)} proizvoda u {filename}")


def main():
    print("[INFO] Preuzimam stranicu kategorije...")
    html = fetch_page(CATEGORY_URL)

    print("[INFO] Parsiram proizvode...")
    products = parse_products(html)

    print(f"[INFO] Pronađeno proizvoda: {len(products)}")
    for p in products[:10]:
        print("-", p["name"], "|", p["price"], "|", p["url"])

    save_to_csv(products)


if __name__ == "__main__":
    main()
