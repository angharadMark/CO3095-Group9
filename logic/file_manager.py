import os

def exportWatchlist(user):
    watchlist=user.get_watch_list()
    if not watchlist:
        print("Your watchlist is empty")
        return
    filename=f"{user.username}_watchlist.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- {user.username.upper()}'S WATCHLIST ---\n\n")
            for i, film in enumerate(watchlist, 1):
                # Accessing Film attributes directly to avoid AttributeErrors
                f.write(f"{i}. {film.name}\n")
                f.write(f"   Genre: {', '.join(film.genre) if film.genre else 'N/A'}\n")
                f.write("-" * 30 + "\n")
        
        print(f"\nSuccessfully saved to {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Error saving file: {e}")