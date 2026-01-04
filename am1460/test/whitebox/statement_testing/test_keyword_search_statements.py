import unittest
from unittest.mock import patch, MagicMock


class TestKeywordSearchStatements(unittest.TestCase):
    """
    Technique: White-Box Statement Testing (Lab 9 Task 1)
    Tool: unittest & coverage.py
    Objective: 100% Statement Coverage for searchMovies
    """

    @patch('sys.argv', ['main.py'])  # This shields your code from the pytest error
    def test_search_movies_statements(self, mock_args):
        # LAZY IMPORT: Move the import inside the test function
        # This prevents the 'SystemExit' crash during collection
        from object.film import Film, searchMovies

        f1 = Film()
        f1.name = "The Matrix"
        f1.description = "A sci-fi action classic"
        db = [f1]

        # Statement 1: Success Title (Hits loop + if name match)
        self.assertEqual(len(searchMovies(db, "Matrix")), 1)

        # Statement 2: Success Description (Hits elif/if description match)
        self.assertEqual(len(searchMovies(db, "sci-fi")), 1)

        # Statement 3: No Match (Hits return statement after loop finish)
        self.assertEqual(len(searchMovies(db, "Romance")), 0)