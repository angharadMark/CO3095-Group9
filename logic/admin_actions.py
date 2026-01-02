import json
from logic.scraper import load_html, parse_movies
import os
dataDir = os.path.join(os.path.dirname(__file__), "..", "data")
profanFile = os.path.join(dataDir, "en.txt")


def import_movies(html_path, films_path):

    html = load_html(str(html_path))
    new_movies = parse_movies(html)

    if not new_movies:
        print("No movies found in the HTML file.")
        return 0, 0

    # Load existing films
    with open(films_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    existing_keys = {(m.get("name"), str(m.get("year"))) for m in existing}

    added = 0
    skipped = 0

    for m in new_movies:
        key = (m.get("name"), str(m.get("year")))
        if key in existing_keys:
            skipped += 1
            continue
        existing.append(m)
        existing_keys.add(key)
        added += 1

    # Save updated films list
    with open(films_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    return added, skipped



def add_profan(word):
    with open(profanFile, "a") as f:
        f.write(word + "\n")

def delete_profan(target):
    with open(profanFile, "r") as f:
        lines = f.readlines()
    
    lines_temp = []
    for line in lines:
        if line.strip() != target.strip():
            lines_temp.append(line)
    
    if len(lines_temp) == len(lines):
        return False 
    
    with open(profanFile, "w") as f:
        for line in lines_temp:
            f.writelines(line)
