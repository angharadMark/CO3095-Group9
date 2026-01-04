import unittest
from unittest.mock import patch
from object.film import Film
from database.database import Database
from logic.watchlist_similarity import WatchlistSimilarity
from logic.user_registration import readJson, usersFile

class BasicFilmCombined(Film):
    def __init__(self, name, genre, cast):
        self.name = name
        self.genre = genre
        self.cast = cast

class BasicFilmGenre(Film):
    def __init__(self, genre):
        self.genre = genre

class BasicActor:
    def __init__(self, name):
        self.name = name

class BasicUser:
    def __init__(self, id, username, watchlist):
        self.id = id
        self.username = username
        self.watchList = watchlist

def spoof_read_json(spoofed_ver):
    return lambda _, __: spoofed_ver

def create_db(films_list):
    db = Database()
    for film in films_list:
        db.add_films(film)
    return db

users_1 = {
    "byId": {
        "1111": {
            "watchlist" : [
                "Movie1", "Movie2", "Movie3"
            ]
        }
    },
    "byUsername": {
        "user": "1111"
    }
}

users_2 = {
    "byId": {
        "1111": {
            "watchlist" : [
                "Movie1", "Movie2", "Movie3"
            ]
        },
        "1112": {

        },
        "1113": {
            "watchlist" : [
                "Movie1", "Movie4"
            ]
        }

    },
    "byUsername": {
        "user": "1111",
        "user2": "1112",
        "user3": "1113"
    }
}

users_3 = {
    "byId": {
        "1111": {
            "watchlist" : [
                "Movie1"
            ]
        },
        "1112": {
            "watchlist" : [
                "Movie1", "Movie2", "Movie3"
            ]
        },
        "1113": {
            "watchlist" : [
                "Movie1", "Movie4"
            ]
        }

    },
    "byUsername": {
        "user": "1111",
        "user2": "1112",
        "user3": "1113"
    }
}

films_1 = [
    BasicFilmCombined("Movie1",
        ["Action"], 
        [BasicActor("Actor1")]
    ),
    BasicFilmCombined("Movie4",
        ["Horror"], 
        [BasicActor("Actor1")]
    )
]

films_2 = []

class TestWatchlistSimilarity(unittest.TestCase):
    def test(self):
        films = [
            BasicFilmGenre(["action"]),
            BasicFilmGenre(["action"])
        ]
        assert WatchlistSimilarity.get_watchlist_genres(films) == ["action", "action"]

    # testing branch on line 26 of watchlist_similarity.py 
    @patch("logic.watchlist_similarity.readJson", new=spoof_read_json(users_1))
    def test_skip_target_user(self):
        database = create_db(films_1)
        target_user = BasicUser("1111", "user", [database.get_film("Movie1")])
        results = WatchlistSimilarity.find(target_user, database)

        # branch was taken and the user was correctly skipped if len == 0.
        self.assertEqual(len(results), 0)

    @patch("logic.watchlist_similarity.readJson", new=spoof_read_json(users_2))
    def test_user_watchlist_key_not_present(self):
        database = create_db(films_1)
        target_user = BasicUser("1111", "user", [database.get_film("Movie1")])

        # tests the if of the ternary at line 30 of watchlist_similarity.py
        # watchlist for user2 is excluded so retrieved_films is [], so final score will be 0 and thus will be
        # excluded from the list. final result is a list with 1 user, also testing the branch on line 52.


        results = WatchlistSimilarity.find(target_user, database)
        self.assertEqual(len(results), 1)

    @patch("logic.watchlist_similarity.readJson", new=spoof_read_json(users_2))
    def test_user_watchlist_movies_not_in_database(self):
        database = create_db(films_2)
        target_user = BasicUser("1111", "user", [])

        # tests the if in the list comprehension at line 30 of watchlist_similarity.py
        # results should be empty again because no movie is present in the db.
        # so score will be 0 for everyone and thus everyone will be excluded.
        results = WatchlistSimilarity.find(target_user, database)
        self.assertEqual(len(results), 0)
       
    @patch("logic.watchlist_similarity.readJson", new=spoof_read_json(users_3))
    def test_similarity_scoring(self):
        database = create_db(films_1)
        target_user = BasicUser("1111", "user", [database.get_film("Movie1")])

        # on line 34 (watchlist_similarity.py), the if statement checks if the film exists in both 
        # watchlists. the following tests that branch statement by checking both users have a score of 21.

        # also covers the branch on line 42 (hence why there's a 1 added despite user3 having 2 valid movies).
        results = WatchlistSimilarity.find(target_user, database)
        self.assertEqual(len(results), 2)
        for (user_id, score) in results:
            self.assertEqual(score, 21)
