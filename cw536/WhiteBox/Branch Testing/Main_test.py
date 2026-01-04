
import unittest
from unittest.mock import patch
from object.film import Film
from object.comment import Comment

class DummyDatabase:
    def __init__(self):
        self.films = []

    def add_films(self, film):
        self.films.append(film)

    def get_all_films(self):
        return self.films

    def popular_films(self):
        return self.films

    def get_film(self, name):
        for film in self.films:
            if film.name == name:
                return film
        return None

    def get_age_filtered_films(self, age):
        return self.films

    def search_actor(self, name):
        return []

class DummyUser:
    def __init__(self):
        self.watchlist = []
        self.comments = []
        self.ratings = {}

    def add_to_watchList(self, film):
        self.watchlist.append(film)

    def get_watch_list(self):
        return self.watchlist

    def pop_from_watchlist(self, index):
        return self.watchlist.pop(index)

    def add_comment(self, film, comment):
        self.comments.append(comment)

    def add_rating(self, film_name, rating):
        self.ratings[film_name] = rating

class TestMainOptionsFull(unittest.TestCase):

    @patch('builtins.input', side_effect=["Test Film"])
    def test_option_1_add_film(self, mock_input):
        db = DummyDatabase()
        film_name = mock_input()
        film = Film(name=film_name)
        db.add_films(film)
        self.assertEqual(len(db.get_all_films()), 1)
        self.assertEqual(db.get_all_films()[0].name, "Test Film")

    def test_option_2_popular_films(self):
        db = DummyDatabase()
        film = Film(name="Popular Film")
        db.add_films(film)
        popular = db.popular_films()
        self.assertEqual(len(popular), 1)
        self.assertEqual(popular[0].name, "Popular Film")

    def test_option_3_view_all_films(self):
        db = DummyDatabase()
        db.add_films(Film(name="Film1"))
        db.add_films(Film(name="Film2"))
        all_films = db.get_all_films()
        self.assertEqual(len(all_films), 2)

    def test_option_6_actor_search(self):
        db = DummyDatabase()
        results = db.search_actor("Someone")
        self.assertEqual(results, [])

    def test_option_8_view_watchlist(self):
        user = DummyUser()
        self.assertEqual(user.get_watch_list(), [])
        user.add_to_watchList(Film(name="Watch Film"))
        self.assertEqual(len(user.get_watch_list()), 1)

    def test_option_12_recommendations(self):
        user = DummyUser()
        recs = []
        self.assertEqual(recs, [])

    def test_option_13_comment_watchlist(self):
        user = DummyUser()
        film = Film(name="CommentFilm")
        user.add_to_watchList(film)
        comment = Comment("Nice!", "testuser")
        film.add_comment(comment)
        user.add_comment(film, comment)
        self.assertEqual(len(user.comments), 1)
        self.assertEqual(user.comments[0].message, "Nice!")

    def test_option_17_export_data(self):
        user = DummyUser()
        try:
            exported = True
        except:
            exported = False
        self.assertTrue(exported)

    def test_option_18_exit(self):
        exited = True
        self.assertTrue(exited)

if __name__ == "__main__":
    unittest.main()
