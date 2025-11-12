class User:
    def __init__(self, username):
        self.username = username
        self.watchList=[]
        self.films_added=0

    def add_to_watchList(self, film):
        self.watchList.append(film)
    
    def get_films_added(self):
        return self.films_added

    def set_films_added(self, value):
        self.films_added = value



