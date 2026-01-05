import unittest
from unittest.mock import Mock, patch, MagicMock
from database.database import Database
from object.film import Film


class TestPopularFilms(unittest.TestCase):

    def setUp(self):
        self.database = Database()

    # Test Case 1:
    @patch('builtins.input', side_effect=['2'])  # User chooses to exit
    def test_case_1_no_films_no_ratings_view_detail(self, mock_input):
        self.assertEqual(len(self.database.films), 0)

        result = self.database.popular_films()

        self.assertIsNotNone(result)

    # Test Case 2:
    @patch('builtins.input', side_effect=['2'])  # User chooses to exit
    def test_case_2_no_films_no_ratings_exit_menu(self, mock_input):
        self.assertEqual(len(self.database.films), 0)

        result = self.database.popular_films()

        self.assertIsNotNone(result)

    # Test Case 3:
    @patch('builtins.input', side_effect=['2'])
    def test_case_3_no_films_has_ratings_view_detail(self, mock_input):
        self.assertEqual(len(self.database.films), 0)

        result = self.database.popular_films()
        self.assertIsNotNone(result)

    # Test Case 4:
    @patch('builtins.input', side_effect=['2'])
    def test_case_4_no_films_has_ratings_exit_menu(self, mock_input):
        self.assertEqual(len(self.database.films), 0)

        result = self.database.popular_films()
        self.assertIsNotNone(result)

    # Test Case 5:
    @patch('builtins.input', side_effect=['2'])
    def test_case_5_below_threshold_no_ratings_view_detail(self, mock_input):
        film = Mock(spec=Film)
        film.name = "Low Rated Film"
        film.average_rating = Mock(return_value=0)
        self.database.add_films(film)

        result = self.database.popular_films()

        self.assertIsNotNone(result)

    # Test Case 6:
    @patch('builtins.input', side_effect=['2'])
    def test_case_6_below_threshold_no_ratings_exit_menu(self, mock_input):
        film = Mock(spec=Film)
        film.name = "Low Rated Film"
        film.average_rating = Mock(return_value=0)
        self.database.add_films(film)

        result = self.database.popular_films()
        self.assertIsNotNone(result)

    # Test Case 7:
    @patch('builtins.input', side_effect=['2'])
    def test_case_7_below_threshold_has_ratings_view_detail(self, mock_input):
        film = Mock(spec=Film)
        film.name = "Below Threshold Film"
        film.average_rating = Mock(return_value=6.5)
        self.database.add_films(film)

        result = self.database.popular_films()

        self.assertIsNotNone(result)

    # Test Case 8:
    @patch('builtins.input', side_effect=['2'])
    def test_case_8_below_threshold_has_ratings_exit_menu(self, mock_input):
        film = Mock(spec=Film)
        film.name = "Below Threshold Film"
        film.average_rating = Mock(return_value=6.5)
        self.database.add_films(film)

        result = self.database.popular_films()
        self.assertIsNotNone(result)

    # Test Case 9:
    @patch('builtins.input', side_effect=['2'])
    def test_case_9_above_threshold_no_ratings_view_detail(self, mock_input):
        film = Mock(spec=Film)
        film.name = "High Rated Film"
        film.average_rating = Mock(return_value=8.0)
        self.database.add_films(film)

        result = self.database.popular_films()

        self.assertIsNotNone(result)

    # Test Case 10:
    @patch('builtins.input', side_effect=['2'])
    def test_case_10_above_threshold_no_ratings_exit_menu(self, mock_input):
        film = Mock(spec=Film)
        film.name = "High Rated Film"
        film.average_rating = Mock(return_value=8.0)
        self.database.add_films(film)

        result = self.database.popular_films()
        self.assertIsNotNone(result)

    # Test Case 11:
    @patch('builtins.input', side_effect=['1', '1'])  # View detail, select film 1
    @patch('builtins.print')
    def test_case_11_above_threshold_has_ratings_view_detail(self, mock_print, mock_input):
        film = Mock(spec=Film)
        film.name = "Popular Film"
        film.average_rating = Mock(return_value=8.5)
        film.display_film = Mock()
        self.database.add_films(film)

        result = self.database.popular_films()

        self.assertFalse(result)

    # Test Case 12:
    @patch('builtins.input', side_effect=['2'])
    def test_case_12_above_threshold_has_ratings_exit_menu(self, mock_input):
        film = Mock(spec=Film)
        film.name = "Popular Film"
        film.average_rating = Mock(return_value=8.5)
        self.database.add_films(film)

        result = self.database.popular_films()
        self.assertIsNotNone(result)

    # Test Case 13:
    @patch('builtins.input', side_effect=['2'])
    def test_case_13_mixed_ratings_no_ratings_view_detail(self, mock_input):
        film1 = Mock(spec=Film)
        film1.name = "High Film"
        film1.average_rating = Mock(return_value=8.0)

        film2 = Mock(spec=Film)
        film2.name = "Low Film"
        film2.average_rating = Mock(return_value=5.0)

        self.database.add_films(film1)
        self.database.add_films(film2)

        result = self.database.popular_films()

        self.assertIsNotNone(result)

    # Test Case 14:
    @patch('builtins.input', side_effect=['2'])
    def test_case_14_mixed_ratings_no_ratings_exit_menu(self, mock_input):
        film1 = Mock(spec=Film)
        film1.name = "High Film"
        film1.average_rating = Mock(return_value=8.0)

        film2 = Mock(spec=Film)
        film2.name = "Low Film"
        film2.average_rating = Mock(return_value=5.0)

        self.database.add_films(film1)
        self.database.add_films(film2)

        result = self.database.popular_films()
        self.assertIsNotNone(result)

    # Test Case 15:
    @patch('builtins.input', side_effect=['1', '1'])  # View detail, select film 1
    @patch('builtins.print')
    def test_case_15_mixed_ratings_has_ratings_view_detail(self, mock_print, mock_input):
        film1 = Mock(spec=Film)
        film1.name = "Popular Film"
        film1.average_rating = Mock(return_value=8.5)
        film1.display_film = Mock()

        film2 = Mock(spec=Film)
        film2.name = "Unpopular Film"
        film2.average_rating = Mock(return_value=6.0)

        self.database.add_films(film1)
        self.database.add_films(film2)

        result = self.database.popular_films()

        self.assertFalse(result)

    # Test Case 16:
    @patch('builtins.input', side_effect=['2'])
    def test_case_16_mixed_ratings_has_ratings_exit_menu(self, mock_input):
        film1 = Mock(spec=Film)
        film1.name = "Popular Film"
        film1.average_rating = Mock(return_value=8.5)

        film2 = Mock(spec=Film)
        film2.name = "Unpopular Film"
        film2.average_rating = Mock(return_value=6.0)

        self.database.add_films(film1)
        self.database.add_films(film2)

        result = self.database.popular_films()
        self.assertIsNotNone(result)


class TestAverageRating(unittest.TestCase):

    def test_no_ratings_returns_zero(self):
        film = Film(name="Test Film", ratings=[])

        average = film.average_rating()

        self.assertEqual(average, 0)

    def test_has_ratings_returns_average(self):
        film = Film(name="Test Film", ratings=[8, 9, 7])

        average = film.average_rating()

        self.assertEqual(average, 8.0)


if __name__ == "__main__":
    unittest.main()