import unittest
from unittest.mock import patch
'''
Technique: White-Box Branch Testing (Lab 9 Task 2)
Tool used: Unittest & Coverage.py
Assigned Story: ID 43 (Search for movies by keyword)
Description: This test suite ensures 100% Branch Coverage for searchMovies. 
             It specifically targets the True/False outcomes of the compound 
             'if keyword in title or keyword in description' decision.

Expected Results: 
- Case 1 (True Branch - Title): res1 length = 1
- Case 2 (True Branch - Description): res2 length = 1
- Case 3 (False Branch - No Match): res3 length = 0
- Case 4 (Empty DB Branch): Loop does not execute; empty list returned.

Actual Results: All branches executed successfully. 100% Branch Coverage achieved.
'''
class TestKeywordSearchBranches(unittest.TestCase):

    def test_search_movies_branches(self):
        with patch('sys.argv', ['test_script.py']):
            from object.film import Film, searchMovies

            # Setup concrete objects for testing
            f1 = Film(name="Inception", description="Dream architecture")
            db = [f1]

            # --- BRANCH 1: Loop Entry ---
            # Condition: movies list is empty
            res_empty = searchMovies([], "test")
            self.assertEqual(len(res_empty), 0)

            # --- BRANCH 2: if keyword in title (TRUE) ---
            # Condition: keyword matches title, first part of 'OR' is True
            res_title = searchMovies(db, "Inception")
            self.assertEqual(len(res_title), 1)

            # --- BRANCH 3: if keyword in description (TRUE) ---
            # Condition: keyword doesn't match title, matches description (OR second part True)
            res_desc = searchMovies(db, "Dream")
            self.assertEqual(len(res_desc), 1)

            # --- BRANCH 4: if keyword matches neither (FALSE) ---
            # Condition: both parts of 'OR' are False, item skipped
            res_none = searchMovies(db, "Horror")
            self.assertEqual(len(res_none), 0)

if __name__ == '__main__':
    unittest.main()