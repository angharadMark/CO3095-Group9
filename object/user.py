class User:
    def __init__(self, username):
        self.username = username
        self.watchList=[]
        self.films_added=0
        # A dictionary associating film names with their ratings (0-10)
        self.ratings = {}

    def add_to_watchList(self, film):
        self.watchList.append(film)

    def remove_from_watchlist(self, film):
        self.watchList.remove(film)

    def pop_from_watchlist(self, film_index):
        return self.watchList.pop(film_index)

    def remove_from_watchlist_by_name(self, film_name):
        return self.remove_from_watchlist_by_property(
            lambda film: self.name, film_name
        )

    def remove_from_watchlist_by_actors(self, actor_list):
        removal_list = []

        for film in self.watchList:
            can_exit = False
            #if property_getter(film) == property_value:
            #    removal_list.push(film)
            for actor in actor_list:
                for film_actor in film.cast:
                    if actor == film_actor.name:
                        removal_list.push(film)
                        can_exit = True
                        break

                if can_exit: break
                

        for film in removal_list:
            self.watchList.remove(film)

        return len(removal_list)

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
            print(f"{i+1}: {film.name}")
            print(f"  Description: {film.description}")
            print("  Actors:")
            for actor in film.cast:
                print(f"    {actor.name} as {actor.role}")
            
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

