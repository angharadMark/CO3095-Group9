import unittest
from unittest.mock import patch, MagicMock

from logic.movie_recommendations import getMovieOfTheDay
'''
Tool used: Unittest & Coverage.py
Technique: Specification-Based Testing (Black-Box)
Method: Category Partitioning & Boundary Value Analysis
Documentation: All test cases are derived from the functional requirements 
to ensure 100% pass rate and high individual module coverage.
'''

class TestMovieRecommendations(unittest.TestCase):
    @patch('logic.movie_recommendations.DatabaseLoader')
    def test_motd_empty_db(self, mock_loader):
        # Frame: Database_State.Empty
        mock_db = MagicMock()
        mock_db.get_all_films.return_value = []
        mock_loader.return_value.load.return_value = mock_db

        self.assertIsNone(getMovieOfTheDay())