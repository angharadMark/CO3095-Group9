import unittest
from unittest.mock import patch, MagicMock

from logic.movie_recommendations import getMovieOfTheDay
'''
Technique: Specification-Based Testing (Black-Box)
Tool used: Unittest & Coverage.py
Assigned Story: ID 39 (Movie of the Day Recommendation)
Description: Uses Boundary Value Analysis to test the system's behavior when 
             the movie database is empty.

Expected Results:
- Empty Database Boundary: getMovieOfTheDay() returns None when the 
  DatabaseLoader retrieves zero films.

Actual Results: 100% Pass Rate. 
'''

class TestMovieRecommendations(unittest.TestCase):
    @patch('logic.movie_recommendations.DatabaseLoader')
    def test_motd_empty_db(self, mock_loader):
        # Frame: Database_State.Empty
        mock_db = MagicMock()
        mock_db.get_all_films.return_value = []
        mock_loader.return_value.load.return_value = mock_db

        self.assertIsNone(getMovieOfTheDay())