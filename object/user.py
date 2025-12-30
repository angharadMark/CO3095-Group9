class User:
    def __init__(self, record):
        self.id = record["id"]
        self.username = record["username"]
        self.watchList= record.get("watchlist", [])
        self.films_added= record.get("films_added", 0)
        # A dictionary associating film names with their ratings (0-10)
        self.ratings = record.get("ratings", {})
        self.comments = record.get("comments", {})
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "watchlist": [film.to_dict() for film in self.watchList],
            "films_added": self.films_added,
            "ratings": self.ratings,
            "comments": [{
                "user": comment.user,
                "message": comment.message
                }
                for comment in self.comments
            ]
        }

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
            print("Comments:")
            for comment in film.comments:
                comment.display_comment()
            
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

    def add_comment(self,film, comment):
        self.comments.update({film,comment})

