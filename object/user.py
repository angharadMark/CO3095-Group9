class User:
    def __init__(self, username):
        self.username = username
        self.watchList=[]

    def add_to_watchList(self, film):
        self.watchList.append(film)

    def display_watchlist(self):
        if not self.watchList:
            print("\nYour watchlist is currently empty")
            return
        print("\nYour Watchlist:")
        for i, film in enumerate(self.watchList):
            print(f"{film.name}")
        


