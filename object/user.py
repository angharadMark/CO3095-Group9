class User:
    def __init__(self, username):
        self.username = username
        self.watchList=[]
        self.films_added=0
        # A dictionary associating film names with their ratings (0-10)
        self.ratings = {}

    def add_to_watchList(self, film):
        self.watchList.append(film)

    def get_watch_list(self):
        return self.watchList
    
    def get_films_added(self):
        return self.films_added

    def set_films_added(self, value):
        self.films_added = value

    def display_watchlist(self):
        if not self.watchList:
            print("\nYour watchlist is currently empty")
            return
        print("\nYour Watchlist:")
        for i, film in enumerate(self.watchList):
            print("Film Name: "f"{film.name}")
            print("Description: "f"{film.description}")
            print("Actors:")
            for actor in film.cast:
                print(f"{actor.name} as {actor.role}")
            
    def add_rating(self, film_name, rating):
        if rating < 0 or rating > 10:
            raise IndexError("Rating value not in range 0-10")
            return

        self.ratings.update({film_name: rating})

    def get_rating(self, film_name):
        if not film_name in self.ratings:
            return None
        return self.ratings[film_name]
        
    def get_watch_list(self):
        return self.watchList

