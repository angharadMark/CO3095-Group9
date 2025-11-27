class User:
    def __init__(self, username):
        self.username = username
        self.watchList=[]

    def add_to_watchList(self, film):
        self.watchList.append(film)
        



