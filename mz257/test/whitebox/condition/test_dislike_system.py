import unittest

from object.film import Film
from object.user import User

from database.database import Database

class BasicFilmCombined(Film):
    def __init__(self, name, genre, cast):
        self.name = name
        self.genre = genre
        self.cast = cast

class BasicActor:
    def __init__(self, name):
        self.name = name

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

def create_db(films_list):
    db = Database()
    for film in films_list:
        db.add_films(film)
    return db

class TestDislikes(unittest.TestCase):
    def test_dislike_movie_loading(self):
        user_record = {
            "id": "1234",
            "username": "user",
            "dislikes": ["Movie1"]
        }
        database = create_db(films_1)

        user_1 = User(user_record, database)
        user_2 = User(user_record, None)

        # dislikes array length should be 0 if database is None
        self.assertEqual(len(user_1.dislikes), 1)
        self.assertEqual(len(user_2.dislikes), 0)
        self.assertEqual(films_1[0], user_1.dislikes[0])
        


