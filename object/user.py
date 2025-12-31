from copy import deepcopy
from logic.user_registration import readJson, saveJson, usersFile

from object.user_message import UserMessage

class User:
    def __init__(self, username):
        self.username = username
        self.watchList=[]
        self.films_added=0
        # A dictionary associating film names with their ratings (0-10)
        self.ratings = {}

        self.dislikes = []
        self.inbox = []

    def add_to_watchList(self, film):
        self.watchList.append(film)

    def get_watch_list(self):
        return self.watchList
    
    def get_films_added(self):
        return self.films_added

    def set_films_added(self, value):
        self.films_added = value

    def display_watchlist(self, displaying_other_user = False):
        if not displaying_other_user:
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

    # common function to both load and write
    def get_user_data(self, users_json_data):
        if "byId" not in users_json_data.keys() or "byUsername" not in users_json_data.keys():
            raise RuntimeError("Malformed users data")

        if self.username not in users_json_data["byUsername"].keys():
            raise LookupError("User data is missing")

        user_id = users_json_data["byUsername"][self.username]

        if user_id not in users_json_data["byId"].keys():
            raise LookupError("User data is missing")

        return (users_json_data["byId"][user_id], user_id)

    # db is needed to retrieve films for watchlist
    def load(self, database):
        users_json_data = readJson(usersFile, {"byId":{}, "byUsername": {}})

        (user_data, _) = self.get_user_data(users_json_data)

        if "watchList" in user_data.keys():
            film_titles = user_data["watchList"]
            self.watchList = [database.get_film(title) for title in film_titles] 

        if "ratings" in user_data.keys():
            self.ratings = user_data["ratings"]

        if "filmsAdded" in user_data.keys():
            self.set_films_added(user_data["filmsAdded"]) 

        if "dislikes" in user_data.keys():
            self.dislikes = [database.get_film(film_title) for film_title in user_data["dislikes"]]

        if "inbox" in user_data.keys():
            self.inbox = [UserMessage.from_dict(message_dict) for message_dict in user_data["inbox"]]

    # save data to users file.
    def write(self):
        users_json_data = readJson(usersFile, {"byId":{}, "byUsername": {}})

        (saved_user, user_id) = self.get_user_data(users_json_data)

        if "id" not in saved_user.keys() or "username" not in saved_user.keys() or "passwordHash" not in saved_user.keys():
            raise RuntimeError("Stored user data is malformed")

        saved_username = saved_user["username"]
        saved_hash = saved_user["passwordHash"]

        copied_user = self.to_dict()
        copied_user["id"] = user_id
        copied_user["username"] = saved_username
        copied_user["passwordHash"] = saved_hash

        users_json_data["byId"][user_id] = copied_user

        saveJson(usersFile, users_json_data)

    def get_rating(self, film_name):
        if not film_name in self.ratings:
            return None
        return self.ratings[film_name]
        
    def get_watch_list(self):
        return self.watchList

    def get_dislikes(self):
        return self.dislikes

    def dislike_film(self, film):
        if film not in self.dislikes:
            self.dislikes.append(film)
            return film
        return None

    def undislike_film(self, film):
        self.dislikes.remove(film)

    def get_inbox(self):
        return self.inbox

    def unread_message_count(self):
        return sum([1 if not message.get_read_status() else 0 for message in self.inbox])

    def send_message(self, message):
        self.inbox.append(message)

    def to_dict(self):
        return {
            "watchList": [film.name for film in self.watchList],
            "filmsAdded": self.films_added,
            "ratings": self.ratings,
            "dislikes": [film.name for film in self.dislikes],
            "inbox": [message.to_dict() for message in self.inbox]
        }

