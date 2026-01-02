import unittest
from unittest.mock import patch
from object.film import Film

class TestAdminAddFilm(unittest.TestCase):

    @patch('builtins.input')
    def test_add_valid_film(self, mock_input):
        # Order based on your terminal output:

        mock_input.side_effect = [
            "Inception", "Chris Nolan", "Emma Thomas", "2010", "12",
            "Sci-Fi", "n", "Leo", "Cobb", "n", "y"
        ]

        film = Film()
        result = film.input_film()
        self.assertNotEqual(result, False)

    @patch('builtins.input')
    def test_add_empty_title_film(self, mock_input):
        # The test will stop as soon as input_film() returns False.
        mock_input.side_effect = [""] * 15

        film = Film()
        result = film.input_film()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()