import unittest
from unittest.mock import patch
'''
Technique: White-Box Statement Testing (Lab 9 Task 1)
Tool used: Unittest & Coverage.py
Assigned Story: ID 43 (Search for movies by keyword)
Description: This test suite ensures 100% Statement Coverage for the searchMovies 
             function by providing inputs that exercise every executable line.

Expected Results: 
- Case 1 (Title Match): res1 length = 1 (hits title processing and append)
- Case 2 (Description Match): res2 length = 1 (hits description processing and append)
- Case 3 (No Match): res3 length = 0 (hits comparison lines without append)

Actual Results: All statements executed successfully. 100% Statement Coverage achieved.
'''
class TestKeywordSearchStatements(unittest.TestCase):

    def test_search_movies_statements(self):
        # Patch sys.argv to prevent potential issues with unittest discovery
        with patch('sys.argv', ['test_script.py']):
            from object.film import Film, searchMovies

            # Setup a film with both name and description to ensure lines
            # related to title/description processing are executed.
            f1 = Film(name="The Matrix", description="A sci-fi action classic")
            db = [f1]

            # Case 1: Execute Title Statement
            # Targets: title = (movie.name or "").lower() AND results.append(movie)
            res1 = searchMovies(db, "Matrix")
            self.assertEqual(len(res1), 1)

            # Case 2: Execute Description Statement
            # Targets: description = (getattr(movie, 'description', "") or "").lower()
            res2 = searchMovies(db, "sci-fi")
            self.assertEqual(len(res2), 1)

            # Case 3: Execute Full Iteration Without Match
            # Targets: return results (at the end of the function)
            res3 = searchMovies(db, "Romance")
            self.assertEqual(len(res3), 0)

if __name__ == '__main__':
    unittest.main()