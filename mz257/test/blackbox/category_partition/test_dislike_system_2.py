import unittest

from object.film import Film
from object.user import User

class BasicFilmCombined(Film):
    def __init__(self, name, genre, cast):
        self.name = name
        self.genre = genre
        self.cast = cast

class BasicActor:
    def __init__(self, name):
        self.name = name

film_1 = BasicFilmCombined("Movie1",
    ["Action"], 
    [BasicActor("Actor1")]
),

film_2 = BasicFilmCombined("Movie4",
    ["Horror"], 
    [BasicActor("Actor1")]
)

user_record = {
    "id": "1234",
    "username": "user"
}

class TestDislikes(unittest.TestCase):
    def setUp(self):
        self.user = User(user_record, None)

    def test_dislike_add_valid(self):
        result = self.user.dislike_film(film_1) 
       
        self.assertEqual(result, film_1)

        # sanity check
        self.assertEqual(len(self.user.get_dislikes()), 1)

    def test_dislike_duplicate_add(self):
        result = self.user.dislike_film(film_1)

        self.assertEqual(result, film_1)

        result = self.user.dislike_film(film_1)

        self.assertEqual(result, None)

    def test_remove_dislike_invalid(self):
        result = self.user.undislike_film(film_1)

        self.assertEqual(result, False)

    def test_remove_dislike_valid(self):
        result = self.user.dislike_film(film_1)
        self.assertEqual(result, film_1)

        result = self.user.undislike_film(film_1)
        self.assertEqual(result, True)


