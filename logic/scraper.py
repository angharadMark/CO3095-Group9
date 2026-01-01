from bs4 import BeautifulSoup

def load_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_movies(html):
    soup = BeautifulSoup(html, "html.parser")
    movies = []

    for block in soup.select("div.movie"):
        name_el = block.select_one(".name")
        year_el = block.select_one(".year")
        if not name_el or not year_el:
            continue

        movie = {
            "name": name_el.get_text(strip=True),
            "year": year_el.get_text(strip=True),
            "producer": (block.select_one(".producer") or {}).get_text(strip=True) if block.select_one(".producer") else "",
            "director": (block.select_one(".director") or {}).get_text(strip=True) if block.select_one(".director") else "",
            "genre": [li.get_text(strip=True) for li in block.select(".genres li")],
            "age_rating": (block.select_one(".age_rating") or {}).get_text(strip=True) if block.select_one(".age_rating") else "",
            "description": (block.select_one(".description") or {}).get_text(strip=True) if block.select_one(".description") else "",
            "ratings": [],
            "cast": [{"name": li.get_text(strip=True), "role": li.get("data-role", "")} for li in block.select(".cast li")]
        }
        movies.append(movie)

    return movies
