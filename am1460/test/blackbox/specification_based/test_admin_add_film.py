import unittest
from unittest.mock import patch
from object.film import Film
'''
Tool used: Unittest & Coverage.py
Technique: Specification-Based Testing (Black-Box)
Method: Category Partitioning & Boundary Value Analysis
Documentation: All test cases are derived from the functional requirements 
to ensure 100% pass rate and high individual module coverage.
'''

class TestAdminAddFilm(unittest.TestCase):

    @patch('builtins.input')
    def test_add_valid_film(self, mock_input):
        # Original order: Name, Director, Producer, Year, Age, Genre, Stop Genre, Actor, Role, Stop Actor, Final Confirm
        mock_input.side_effect = [
            "Inception", "Chris Nolan", "Emma Thomas", "2010", "12",
            "Sci-Fi", "n", "Leo", "Cobb", "n", "y"
        ]

        film = Film()
        result = film.input_film()
        self.assertNotEqual(result, False)

    @patch('builtins.input')
    def test_add_empty_title_film(self, mock_input):
        # Stops as soon as prompt_name returns an empty string
        mock_input.side_effect = [""] * 15

        film = Film()
        result = film.input_film()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()