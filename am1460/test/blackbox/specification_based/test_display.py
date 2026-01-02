import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from object.film import Film, searchMovies
from object.user import User
from object.actor import Actor


class TestSprint1FinalPush(unittest.TestCase):
    def setUp(self):
        self.user = User("ang")
        self.film = Film(name="Inception", ratings=[9, 10])

    @patch('builtins.input')
    def test_prompt_logic(self, mock_input):
        mock_input.side_effect = ['Interstellar', 'Nolan', 'Sci-Fi', 'n']
        f = Film()
        f.prompt_name()
        f.prompt_director()
        f.prompt_genre()
        self.assertEqual(f.name, 'Interstellar')
        self.assertIn('Sci-Fi', f.genre)

    @patch('builtins.input')
    def test_prompt_cast(self, mock_input):
        mock_input.side_effect = ['Leonardo DiCaprio', 'Cobb', 'n']
        f = Film()
        f.prompt_cast()
        self.assertEqual(len(f.cast), 1)
        self.assertEqual(f.cast[0].name, 'Leonardo DiCaprio')

    def test_average_rating_logic(self):
        f_empty = Film()
        self.assertEqual(f_empty.average_rating(), 0)
        self.assertEqual(self.film.average_rating(), 9.5)

    def test_user_avatar_options(self):
        default_av = self.user.set_default_avatar()
        self.assertIn("|o  o|", default_av)
        self.assertTrue(self.user.change_avatar(2))
        self.assertFalse(self.user.change_avatar(100))

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_film_unrated(self, mock_stdout):
        f = Film(name="New Movie")
        f.display_film()
        self.assertIn("unrated", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_user_stories_display(self, mock_stdout):
        """Covers display_watchlist, display_profile, and actor display."""
        actor = Actor("Leo", "Cobb")
        self.film.description = "A dream heist."
        self.film.cast = [actor]

        self.user.add_to_watchList(self.film)
        self.user.display_watchlist()
        self.user.display_profile()

        output = mock_stdout.getvalue()
        self.assertIn("Film Name: Inception", output)
        self.assertIn("Leo as Cobb", output)

    def test_film_search_coverage(self):
        results = searchMovies([self.film], "Inception")
        self.assertEqual(len(results), 1)
        self.assertEqual(len(searchMovies([self.film], "NONEXISTENT")), 0)

    @patch('builtins.input', side_effect=['y'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_input_film_full_flow(self, mock_stdout, mock_input):
        """Covers the input_film confirmation logic and actor.display_actor."""
        test_film = Film()
        # Mocking individual prompts to avoid input conflicts
        test_film.prompt_name = MagicMock()
        test_film.prompt_producer = MagicMock()
        test_film.prompt_director = MagicMock()
        test_film.prompt_year = MagicMock()
        test_film.prompt_age_rating = MagicMock()
        test_film.prompt_genre = MagicMock()
        test_film.prompt_cast = MagicMock()

        # Manually add an actor to cover actor.py's display_actor
        test_film.cast = [Actor("Test Actor", "Test Role")]

        result = test_film.input_film()
        self.assertTrue(result)
        self.assertIn("Test Actor", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()