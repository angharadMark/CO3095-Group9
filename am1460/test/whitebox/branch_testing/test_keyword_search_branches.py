import unittest
from unittest.mock import patch


class TestKeywordSearchStatements(unittest.TestCase):
    """
    Technique: White-Box Statement Testing (Lab 9 Task 1)
    Tool: unittest & coverage.py
    Goal: 100% Statement Coverage for searchMovies
    """

    def test_search_movies_statements(self):  # No @patch decorator, no mock_args
        with patch('sys.argv', ['test_script.py']):
            # Import inside the function to prevent the parser crash
            from object.film import Film, searchMovies

            f1 = Film()
            f1.name = "The Matrix"
            f1.description = "A sci-fi action classic"
            db = [f1]

            # Case 1: Title Match (Hits 'if keyword in movie.name')
            res1 = searchMovies(db, "Matrix")
            self.assertEqual(len(res1), 1)

            # Case 2: Description Match (Hits 'elif keyword in movie.description')
            res2 = searchMovies(db, "sci-fi")
            self.assertEqual(len(res2), 1)

            # Case 3: No Match (Hits the default return)
            res3 = searchMovies(db, "Romance")
            self.assertEqual(len(res3), 0)


if __name__ == '__main__':
    unittest.main()