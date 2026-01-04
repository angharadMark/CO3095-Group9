import unittest
from object.film import Film, searchMovies
'''
Technique: Specification-Based Testing (Black-Box)
Tool used: Unittest & Coverage.py
Description: Verifies the search engine's ability to match keywords against 
             both film titles and descriptions using Category Partitioning.

Expected Results:
- Title Match: searchMovies returns list length 1 when keyword is in the name.
- Description Match: searchMovies returns list length 1 when keyword is only in description.
- No Match: searchMovies returns list length 0 for non-existent keywords.

Actual Results: 100% Pass Rate. 
'''
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