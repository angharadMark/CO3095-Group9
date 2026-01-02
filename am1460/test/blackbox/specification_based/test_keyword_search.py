import unittest
from object.film import Film, searchMovies

class TestSprint4(unittest.TestCase):
    def setUp(self):
        self.f1 = Film()
        self.f1.name = "The Matrix"
        self.f1.description = "A sci-fi action classic"
        self.db = [self.f1]

    def test_keyword_search(self):
        # Test Case: Title Match
        self.assertEqual(len(searchMovies(self.db, "Matrix")), 1)
        # Test Case: Description Match
        self.assertEqual(len(searchMovies(self.db, "sci-fi")), 1)
        # Test Case: No Match
        self.assertEqual(len(searchMovies(self.db, "Romance")), 0)