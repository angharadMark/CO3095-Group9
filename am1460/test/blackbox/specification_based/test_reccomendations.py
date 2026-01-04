import unittest
from unittest.mock import MagicMock
from logic.movie_recommendations import similarity_results, reccomend_films


class TestRecommendations(unittest.TestCase):
    def setUp(self):
        self.film1 = MagicMock()
        self.film1.name = "Inception"
        self.film1.get_genre.return_value = ["Sci-Fi", "Action"]
        self.film1.director = "Nolan"
        self.film1.producer = "Emma Thomas"
        actor1 = MagicMock();
        actor1.name = "Leo"
        self.film1.cast = [actor1]

        self.film2 = MagicMock()
        self.film2.name = "Interstellar"
        self.film2.get_genre.return_value = ["Sci-Fi", "Drama"]
        self.film2.director = "Nolan"
        self.film2.producer = "Emma Thomas"
        actor2 = MagicMock();
        actor2.name = "Leo"
        self.film2.cast = [actor2]

    def test_similarity_scoring(self):
        # 2 (Genre: Sci-Fi) + 1 (Actor: Leo) + 1 (Director) + 1 (Producer) = 5
        score = similarity_results(self.film1, self.film2)
        self.assertEqual(score, 5)

    def test_recommend_logic_flow(self):
        user = MagicMock()
        user.get_watch_list.return_value = [self.film1]

        db = MagicMock()
        # Must include both films so the loop can compare them
        db.get_all_films.return_value = [self.film1, self.film2]

        result = reccomend_films(user, db)
        self.assertIn(self.film2, result)