class User:
    def __init__(self, username):
        self.username = username
        self.watchList=[]

        # A dictionary associating film names with their ratings (0-10)
        self.ratings = {}

    def add_to_watchList(self, film):
        self.watchList.append(film)

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


