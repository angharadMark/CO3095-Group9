import unittest
from unittest.mock import patch

from copy import deepcopy

from object.film import Film
from object.actor import Actor

test_actor = Actor("Actor Name", "Role")

class TestEditFilms(unittest.TestCase):
    def setUp(self):
        self.film = Film("A Film",
            [test_actor], "Film Producer", "Film Director",
            ["Comedy"], "Age Rating", 2000, [], "Description", [])

    # this is a sanity test to ensure that films can be compared properly.
    def test_setup(self):
        another_film = Film("A Film",
            [test_actor], "Film Producer", "Film Director",
            ["Comedy"], "Age Rating", 2000, [], "Description", [])

        self.assertEqual(self.film.to_dict(), another_film.to_dict())

    @patch('builtins.input')
    def test_modify_film_no_changes_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # input nothing, cancel loops wherever needed and confirm and save.
        mock_input.side_effect = ["", "", "", "", "", "", "", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_no_changes_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # input nothing, cancel loops wherever needed and confirm and save.
        mock_input.side_effect = ["", "", "", "", "", "", "", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_name_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the name
        mock_input.side_effect = ["New Name", "", "", "", "", "", "", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_name("New Name")
        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_name_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the name
        mock_input.side_effect = ["New Name", "", "", "", "", "", "", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_name("New Name")
        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_producer_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the producer
        mock_input.side_effect = ["", "New Producer", "", "", "", "", "", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_producer("New Producer")
        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_producer_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the producer
        mock_input.side_effect = ["", "New Producer", "", "", "", "", "", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_producer("New Producer")
        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_director_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the director
        mock_input.side_effect = ["", "", "New Director", "", "", "", "", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_director("New Director")
        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_director_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the director
        mock_input.side_effect = ["", "", "New Director", "", "", "", "", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_director("New Director")
        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_year_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the year of production
        mock_input.side_effect = ["", "", "", "1990", "", "", "", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_year(1990)
        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_year_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the year of production
        mock_input.side_effect = ["", "", "", "1990", "", "", "", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_year("1990")
        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_age_rating_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the age rating
        mock_input.side_effect = ["", "", "", "", "Other Age Rating", "", "", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_age_rating("Other Age Rating")
        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_age_rating_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the age rating
        mock_input.side_effect = ["", "", "", "", "Other Age Rating", "", "", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_age_rating("Other Age Rating")
        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_single_genre_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the genre to a single genre
        mock_input.side_effect = ["", "", "", "", "", "Horror", "n", "", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_genre(["Horror"])
        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_single_genre_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the genre to a single genre
        mock_input.side_effect = ["", "", "", "", "", "Horror", "n", "", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_genre(["Horror"])
        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_multiple_genres_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the genre to a two genres
        mock_input.side_effect = ["", "", "", "", "", "Horror", "y", "Thriller", "n", "", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_genre(["Horror", "Thriller"])
        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_multiple_genres_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the genre to a two genres
        mock_input.side_effect = ["", "", "", "", "", "Horror", "y", "Thriller", "n", "", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_genre(["Horror", "Thriller"])
        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_single_actor_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the cast to a single actor
        mock_input.side_effect = ["", "", "", "", "", "", "Some Actor Name 1", "Some Actor Role 1", "n", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_cast([Actor("Some Actor Name 1", "Some Actor Role 1")])
        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_single_actor_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the cast to a single actor
        mock_input.side_effect = ["", "", "", "", "", "", "Some Actor Name 1", "Some Actor Role 1", "n", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_cast([Actor("Some Actor Name 1", "Some Actor Role 1")])
        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_multiple_actors_saved(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the cast to a multiple actors
        mock_input.side_effect = ["", "", "", "", "", "", "Some Actor Name 1", "Some Actor Role 1", "y", 
                                  "Some Actor Name 2", "Some Actor Role 2", "n", "y"]

        result = to_modify.modify_film()

        self.assertEqual(result, True)

        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_cast([
            Actor("Some Actor Name 1", "Some Actor Role 1"),
            Actor("Some Actor Name 2", "Some Actor Role 2")
        ])
        self.assertEqual(self.film.to_dict(), to_modify.to_dict())

    @patch('builtins.input')
    def test_modify_film_change_multiple_actors_dont_save(self, mock_input):
        to_modify = deepcopy(self.film)

        # change only the cast to a multiple actors
        mock_input.side_effect = ["", "", "", "", "", "", "Some Actor Name 1", "Some Actor Role 1", "y", 
                                  "Some Actor Name 2", "Some Actor Role 2", "n", "n"]

        result = to_modify.modify_film()

        self.assertEqual(result, False)

        self.assertEqual(self.film.to_dict(), to_modify.to_dict())
        self.film.set_cast([
            Actor("Some Actor Name 1", "Some Actor Role 1"),
            Actor("Some Actor Name 2", "Some Actor Role 2")
        ])
        self.assertNotEqual(self.film.to_dict(), to_modify.to_dict())











