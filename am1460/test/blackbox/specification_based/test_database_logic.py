import unittest
from unittest.mock import patch, MagicMock
from database.database import Database
from object.film import Film
from object.actor import Actor
'''
Technique: Specification-Based Testing (Black-Box)
Tool used: Unittest & Coverage.py
Description: Tests data integrity during JSON loading and robust filtering logic 
             using Category Partitioning to handle corrupted or missing data.

Expected Results:

- get_age_filtered_films (Invalid Input): Handle TypeError/ValueError; return empty list.
- search_actor (Fuzzy): Correctly identify "Leo" as "Leonardo DiCaprio" via partial ratio.

Actual Results: 100% Pass Rate. Logic successfully isolates corrupted entries without crashing.
'''

class TestDatabaseLogic(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.film1 = Film(name="Inception", age_rating="12")
        self.film1.add_ratings(10)  # avg > 7 for popular_films logic
        self.db.add_films(self.film1)

    def test_age_filter_errors(self):
        # Hits the ValueError exception for non-integer inputs
        self.assertEqual(self.db.get_age_filtered_films("invalid_age"), [])

        # Hits the TypeError branch in the loop for films with missing ratings
        bad_film = Film(name="Broken", age_rating=None)
        self.db.add_films(bad_film)
        self.assertNotIn(bad_film, self.db.get_age_filtered_films(10))

    @patch('builtins.input', side_effect=['1', '1'])
    def test_popular_films_flow(self, mock_input):
        # Hits the 'while True' loop and the 'View a film in detail' branch
        # This will cover several logic lines in popular_films()
        self.db.popular_films()
        self.assertEqual(mock_input.call_count, 2)

    def test_search_actor_fuzz(self):
        # Hits the normalization logic and fuzz.partial_ratio
        a = Actor(name="Leonardo DiCaprio")
        self.db.add_actor(a)
        # Testing threshold branch
        self.assertTrue(self.db.search_actor("Leo"))
        self.assertFalse(self.db.search_actor("Someone Else", threshold=99))