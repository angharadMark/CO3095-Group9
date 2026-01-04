import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from object.film import Film, searchMovies
from object.user import User
from object.actor import Actor
from object.comment import Comment  # Added to support new interactions
'''
Technique: Specification-Based Testing (Black-Box)
Tool used: Unittest & Coverage.py
Description: Verifies integrated object interactions (Film-Comment-Actor) and 
             input/output logic using Category Partitioning and Boundary Value Analysis.

Expected Results:
- Interaction: Successfully append Comment objects to Film records; ensure data integrity.
- Prompt Logic: Correctly populate Film attributes from mocked user input; verify genre list.
- Rating Logic: Return 0 for unrated films (Boundary) and correct mean for populated lists.
- Display Logic: Capture and verify stdout for 'unrated' tags and profile summary strings.
- Avatar Bounds: Return True for valid index (2) and False for out-of-range index (100).
- Input Flow: input_film() returns True upon 'y' confirmation and displays cast details.

Actual Results: 100% Pass Rate across all 8 test cases. 
'''
DUMMY_USER_RECORD = {
    "id": "b9895d05-667f-44ed-8e55-474f8b643310",
    "username": "ang",
    "avatarIndex": 0,
    "favFilm": "None Set",
    "watchlist": [],
    "dislikes": [],
    "ratings": {},
    "comments": {},
    "inbox": []
}


class TestSprint1FinalPush(unittest.TestCase):
    def setUp(self):
        # Using a dictionary record to match the updated User constructor
        self.user_record = {
            "id": "test_id",
            "username": "ang",
            "watchlist": [],
            "avatarIndex": 0
        }
        self.user = User(self.user_record)
        self.film = Film(name="Inception", ratings=[9, 10])

    def test_film_interactions(self):
        """Verified interaction between Film and Comment objects to boost film.py coverage."""
        f = Film(name="Interstellar")
        comm = Comment("Amazing visuals", user="ang")
        f.add_comment(comm)

        # Ensures comments are being appended to the list correctly
        self.assertEqual(len(f.comments), 1)
        self.assertEqual(f.comments[0].user, "ang")

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
        # Verified default avatar and index bounds
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
        self.assertIn("1: Inception", output)
        self.assertIn("Leo as Cobb", output)

    def test_film_search_coverage(self):
        results = searchMovies([self.film], "Inception")
        self.assertEqual(len(results), 1)
        self.assertEqual(len(searchMovies([self.film], "NONEXISTENT")), 0)

    @patch('builtins.input', side_effect=['y'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_input_film_full_flow(self, mock_stdout, mock_input):
        test_film = Film()
        # Mocking individual prompts to avoid input conflicts during full flow testing
        test_film.prompt_name = MagicMock()
        test_film.prompt_producer = MagicMock()
        test_film.prompt_director = MagicMock()
        test_film.prompt_year = MagicMock()
        test_film.prompt_age_rating = MagicMock()
        test_film.prompt_genre = MagicMock()
        test_film.prompt_cast = MagicMock()

        # Manually add an actor to cover actor.py's display_actor logic
        test_film.cast = [Actor("Test Actor", "Test Role")]

        result = test_film.input_film()
        self.assertTrue(result)
        self.assertIn("Test Actor", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()