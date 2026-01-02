import unittest
from unittest.mock import patch, MagicMock

from logic.movie_recommendations import getMovieOfTheDay


class TestMovieRecommendations(unittest.TestCase):
    @patch('logic.movie_recommendations.DatabaseLoader')
    def test_motd_empty_db(self, mock_loader):
        # Frame: Database_State.Empty
        mock_db = MagicMock()
        mock_db.get_all_films.return_value = []
        mock_loader.return_value.load.return_value = mock_db

        self.assertIsNone(getMovieOfTheDay())