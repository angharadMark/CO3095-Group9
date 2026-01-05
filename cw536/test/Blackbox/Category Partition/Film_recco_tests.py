import unittest
from unittest.mock import Mock, MagicMock
from logic.movie_recommendations import similarity_results, reccomend_films
from object.film import Film
from object.user import User
from object.actor import Actor
from database.database import Database


class TestMovieRecommendations(unittest.TestCase):

    def setUp(self):
        self.film1 = Mock(spec=Film)
        self.film1.name = "Film 1"
        self.film1.get_genre = Mock(return_value=["Action", "Thriller"])
        actor1 = Mock(spec=Actor)
        actor1.name = "Actor 1"
        actor2 = Mock(spec=Actor)
        actor2.name = "Actor 2"
        self.film1.cast = [actor1, actor2]
        self.film1.director = "Director X"
        self.film1.producer = "Producer Y"

        self.film2 = Mock(spec=Film)
        self.film2.name = "Film 2"

        self.user = Mock(spec=User)

        self.database = Mock(spec=Database)

    # Test Cases 1:
    def test_case_1_all_match_empty_watchlist_found_similar(self):
        self.user.get_watch_list = Mock(return_value=[])

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])

    # Test Case 2:
    def test_case_2_all_match_empty_watchlist_no_similar(self):
        self.user.get_watch_list = Mock(return_value=[])

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])

    # Test Cases 3:
    def test_case_3_all_match_has_watchlist_found_similar(self):
        actor_a = Mock(spec=Actor)
        actor_a.name = "Actor A"
        actor_b = Mock(spec=Actor)
        actor_b.name = "Actor B"

        film_watchlist = Mock(spec=Film)
        film_watchlist.name = "Watchlist Film"
        film_watchlist.get_genre = Mock(return_value=["Action", "Thriller"])
        film_watchlist.cast = [actor_a, actor_b]
        film_watchlist.director = "Director X"
        film_watchlist.producer = "Producer Y"

        actor_a2 = Mock(spec=Actor)
        actor_a2.name = "Actor A"
        actor_c = Mock(spec=Actor)
        actor_c.name = "Actor C"

        film_similar = Mock(spec=Film)
        film_similar.name = "Similar Film"
        film_similar.get_genre = Mock(return_value=["Action", "Thriller"])
        film_similar.cast = [actor_a2, actor_c]
        film_similar.director = "Director X"
        film_similar.producer = "Producer Y"

        self.user.get_watch_list = Mock(return_value=[film_watchlist])
        self.database.get_all_films = Mock(return_value=[film_similar])

        result = reccomend_films(self.user, self.database)

        self.assertIsInstance(result, list)

    # Test Case 4:
    def test_case_4_all_match_has_watchlist_no_similar(self):
        film_watchlist = Mock(spec=Film)
        film_watchlist.name = "Watchlist Film"
        film_watchlist.get_genre = Mock(return_value=["Action"])
        film_watchlist.cast = []
        film_watchlist.director = "Director X"
        film_watchlist.producer = "Producer Y"

        film_different = Mock(spec=Film)
        film_different.name = "Different Film"
        film_different.get_genre = Mock(return_value=["Comedy"])
        film_different.cast = []
        film_different.director = "Director Z"
        film_different.producer = "Producer A"

        self.user.get_watch_list = Mock(return_value=[film_watchlist])
        self.database.get_all_films = Mock(return_value=[film_different])

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])

    # Test Cases 5:
    def test_case_5_partial_match_empty_watchlist_found_similar(self):
        self.user.get_watch_list = Mock(return_value=[])

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])

    # Test Case 6:
    def test_case_6_partial_match_empty_watchlist_no_similar(self):
        self.user.get_watch_list = Mock(return_value=[])

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])

    # Test Cases 7:
    def test_case_7_partial_match_has_watchlist_found_similar(self):
        actor_a1 = Mock(spec=Actor)
        actor_a1.name = "Actor A"

        film1 = Mock(spec=Film)
        film1.name = "Film 1"
        film1.get_genre = Mock(return_value=["Action", "Drama"])
        film1.cast = [actor_a1]
        film1.director = "Director X"
        film1.producer = "Producer Y"

        actor_a2 = Mock(spec=Actor)
        actor_a2.name = "Actor A"

        film2 = Mock(spec=Film)
        film2.name = "Film 2"
        film2.get_genre = Mock(return_value=["Action", "Comedy"])
        film2.cast = [actor_a2]
        film2.director = "Director Z"
        film2.producer = "Producer Y"

        self.user.get_watch_list = Mock(return_value=[film1])
        self.database.get_all_films = Mock(return_value=[film2])

        result = reccomend_films(self.user, self.database)

        self.assertIsInstance(result, list)

    # Test Case 8:
    def test_case_8_partial_match_has_watchlist_no_similar(self):
        film1 = Mock(spec=Film)
        film1.name = "Film 1"
        film1.get_genre = Mock(return_value=["Action"])
        film1.cast = []
        film1.director = "Director X"
        film1.producer = "Producer Y"

        film2 = Mock(spec=Film)
        film2.name = "Film 2"
        film2.get_genre = Mock(return_value=["Comedy"])
        film2.cast = []
        film2.director = "Director Z"
        film2.producer = "Producer A"

        self.user.get_watch_list = Mock(return_value=[film1])
        self.database.get_all_films = Mock(return_value=[film2])

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])

    # Test Cases 9:
    def test_case_9_no_match_empty_watchlist_found_similar(self):

        self.user.get_watch_list = Mock(return_value=[])

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])

    # Test Case 10:
    def test_case_10_no_match_empty_watchlist_no_similar(self):
        self.user.get_watch_list = Mock(return_value=[])

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])

    # Test Case 12:
    def test_case_11_no_match_has_watchlist_found_similar(self):
        film1 = Mock(spec=Film)
        film1.name = "Film 1"
        film1.get_genre = Mock(return_value=["Action"])
        film1.cast = []
        film1.director = "Director X"
        film1.producer = "Producer Y"

        film2 = Mock(spec=Film)
        film2.name = "Film 2"
        film2.get_genre = Mock(return_value=["Comedy"])
        film2.cast = []
        film2.director = "Director Z"
        film2.producer = "Producer A"

        self.user.get_watch_list = Mock(return_value=[film1])
        self.database.get_all_films = Mock(return_value=[film2])

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])

    # Test Case 12:
    def test_case_12_no_match_has_watchlist_no_similar(self):
        film1 = Mock(spec=Film)
        film1.name = "Film 1"
        film1.get_genre = Mock(return_value=["Action"])
        film1.cast = []
        film1.director = "Director X"
        film1.producer = "Producer Y"

        film2 = Mock(spec=Film)
        film2.name = "Film 2"
        film2.get_genre = Mock(return_value=["Comedy"])
        film2.cast = []
        film2.director = "Director Z"
        film2.producer = "Producer A"

        self.user.get_watch_list = Mock(return_value=[film1])
        self.database.get_all_films = Mock(return_value=[film2])

        score = similarity_results(film1, film2)

        self.assertEqual(score, 0)

        result = reccomend_films(self.user, self.database)

        self.assertEqual(result, [])


class TestSimilarityResults(unittest.TestCase):


    def test_all_match_similarity(self):

        actor_a1 = Mock(spec=Actor)
        actor_a1.name = "Actor A"
        actor_b1 = Mock(spec=Actor)
        actor_b1.name = "Actor B"

        film1 = Mock(spec=Film)
        film1.get_genre = Mock(return_value=["Action", "Thriller"])
        film1.cast = [actor_a1, actor_b1]
        film1.director = "Director X"
        film1.producer = "Producer Y"

        actor_a2 = Mock(spec=Actor)
        actor_a2.name = "Actor A"
        actor_b2 = Mock(spec=Actor)
        actor_b2.name = "Actor B"

        film2 = Mock(spec=Film)
        film2.get_genre = Mock(return_value=["Action", "Thriller"])
        film2.cast = [actor_a2, actor_b2]
        film2.director = "Director X"
        film2.producer = "Producer Y"

        score = similarity_results(film1, film2)

        self.assertEqual(score, 8)

    def test_no_match_similarity(self):
        film1 = Mock(spec=Film)
        film1.get_genre = Mock(return_value=["Action"])
        film1.cast = []
        film1.director = "Director X"
        film1.producer = "Producer Y"

        film2 = Mock(spec=Film)
        film2.get_genre = Mock(return_value=["Comedy"])
        film2.cast = []
        film2.director = "Director Z"
        film2.producer = "Producer A"

        score = similarity_results(film1, film2)

        self.assertEqual(score, 0)

    def test_no_match_similarity(self):
        film1 = Mock(spec=Film)
        film1.get_genre = Mock(return_value=["Action"])
        film1.cast = []
        film1.director = "Director X"
        film1.producer = "Producer Y"

        film2 = Mock(spec=Film)
        film2.get_genre = Mock(return_value=["Comedy"])
        film2.cast = []
        film2.director = "Director Z"
        film2.producer = "Producer A"

        score = similarity_results(film1, film2)

        self.assertEqual(score, 0)


if __name__ == "__main__":
    unittest.main()