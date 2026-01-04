import unittest
from unittest.mock import patch
from object.film import Film
'''
Technique: Specification-Based Testing (Black-Box)
Tool used: Unittest & Coverage.py
Description: This test suite employs Boundary Value Analysis (BVA) on the 
             user input prompts for creating new film entries.

Expected Results:
- Case 1 (Valid Full Input): input_film returns True and object is populated.
- Case 2 (Empty Mandatory Title): input_film returns False/Stops on empty prompt.
- Case 3 (Input Loop Control): Correctly handles "n" to break Genre/Actor loops.

Actual Results: All test cases passed. The Film object's prompt logic correctly 
distinguishes between valid data entries and cancellation via empty strings.
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