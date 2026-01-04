import unittest

from object.film import Film
from object.user import User
from object.actor import Actor

actor_1 = Actor("Actor1", "Role") 
actor_2 = Actor("Actor2", "Role") 

film_1 = Film(name = "Movie1",
    genre = ["Action"], 
    cast = [actor_1]
)
film_2 = Film(name = "Movie2",
    genre = ["Horror"], 
    cast = [actor_1]
)
film_3 = Film(name = "Movie3",
   genre = ["Horror"], 
   cast = [actor_1]
)

class TestWatchlistRemoval(unittest.TestCase):
    def setUp(self):
        self.user = User({
            "id": "1234",
            "username": "user"
            })
        self.user.add_to_watchList(film_1)
        self.user.add_to_watchList(film_2)

    def test_remove_invalid_film(self):
        result = self.user.remove_from_watchlist(film_3)
        self.assertEqual(result, 0)

    def test_remove_valid_film(self):
        result = self.user.remove_from_watchlist(film_1)
        self.assertEqual(result, 1)

    def test_remove_valid_film_twice(self):
        result = self.user.remove_from_watchlist(film_1)
        self.assertEqual(result, 1)
        result = self.user.remove_from_watchlist(film_1)
        self.assertEqual(result, 0)

    def test_pop_valid_film(self):
        result = self.user.pop_from_watchlist(0)
        self.assertEqual(result, film_1)
        self.assertEqual(len(self.user.get_watch_list()), 1)

    def test_pop_valid_film_twice(self):
        result = self.user.pop_from_watchlist(0)
        self.assertEqual(result, film_1)
        self.assertEqual(len(self.user.get_watch_list()), 1)
        result = self.user.pop_from_watchlist(0)
        self.assertEqual(result, film_2)
        self.assertEqual(len(self.user.get_watch_list()), 0)

    def test_pop_invalid_film(self):
        self.assertRaises(IndexError, self.user.pop_from_watchlist, 2)
        self.assertEqual(len(self.user.get_watch_list()), 2)

    def test_remove_valid_film_by_name(self):
        result = self.user.remove_from_watchlist_by_name("Movie1")
        self.assertEqual(result, 1)
        self.assertEqual(len(self.user.get_watch_list()), 1)

    def test_remove_valid_film_by_name_twice(self):
        result = self.user.remove_from_watchlist_by_name("Movie1")
        self.assertEqual(result, 1)
        self.assertEqual(len(self.user.get_watch_list()), 1)
        result = self.user.remove_from_watchlist_by_name("Movie1")
        self.assertEqual(result, 0)
        self.assertEqual(len(self.user.get_watch_list()), 1)

    def test_remove_invalid_film_by_name(self):
        result = self.user.remove_from_watchlist_by_name("Movie4")
        self.assertEqual(result, 0)
        self.assertEqual(len(self.user.get_watch_list()), 2)

    def test_remove_film_by_actors(self):
        result = self.user.remove_from_watchlist_by_actors([actor_1])
        self.assertEqual(result, 2)
        self.assertEqual(len(self.user.get_watch_list()), 0)

    def test_remove_film_by_actors_twice(self):
        result = self.user.remove_from_watchlist_by_actors([actor_1])
        self.assertEqual(result, 2)
        self.assertEqual(len(self.user.get_watch_list()), 0)
        result = self.user.remove_from_watchlist_by_actors([actor_1])
        self.assertEqual(result, 0)
        self.assertEqual(len(self.user.get_watch_list()), 0)

    def test_remove_invalid_film_by_actors(self):
        result = self.user.remove_from_watchlist_by_actors([actor_2])
        self.assertEqual(result, 0)
        self.assertEqual(len(self.user.get_watch_list()), 2)

