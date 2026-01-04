import unittest
from unittest.mock import patch

import database.database as dbmod
from object.film import Film
from object.actor import Actor

from logic.filter import string_fuzzy_match, QueryFilter, filter_films
from object.filter_type import FilterType


class TestDatabaseFilterBranch(unittest.TestCase):
    def test_filter_branches(self):
        self.assertTrue(string_fuzzy_match("  Hi ", "hi"))
        self.assertFalse(string_fuzzy_match("hi", "bye"))
        self.assertFalse(string_fuzzy_match(123, "hi"))

        f1 = Film(name="A", genre=["Action"], cast=[Actor("Tom", "Lead")])
        f2 = Film(name="B", genre="Comedy", cast=[Actor("Bob", "Side")])

        self.assertTrue(QueryFilter(FilterType.CAST, "tom").matches(f1))
        self.assertTrue(QueryFilter(FilterType.GENRE, "action").matches(f1))
        self.assertTrue(QueryFilter(FilterType.GENRE, "comedy").matches(f2))

        self.assertEqual(filter_films("bad", "bad"), [])
        self.assertEqual(filter_films([], [f1, f2]), [f1, f2])
        self.assertEqual(filter_films([QueryFilter(FilterType.GENRE, "action")], []), [])
        out = filter_films([QueryFilter(FilterType.GENRE, "action")], [f1, f2])
        self.assertEqual([x.name for x in out], ["A"])

    def test_database_branches(self):
        db = dbmod.Database()

        # add films with different age_rating formats
        db.add_films(Film(name="A", age_rating="18"))
        db.add_films(Film(name="B", age_rating="bad"))
        db.add_films(Film(name="C", age_rating=None))

        self.assertTrue(db.get_film("a"))
        self.assertFalse(db.get_film("missing"))

        # age filter bad input branch
        with patch("builtins.print"):
            self.assertEqual(db.get_age_filtered_films("notanint"), [])

        # search_actor branches + add_actor dedupe
        db.add_actor(Actor("Tom Hardy", "Role"))
        db.add_actor(Actor("Tom Hardy", "Role"))  # dedupe branch
        db.add_actor(Actor("Scarlett Johansson", "Role"))

        self.assertFalse(db.search_actor("zzzzzz", threshold=99))
        self.assertTrue(db.search_actor("tom", threshold=40))

    def test_database_popular_films_menu_branches(self):
        # popular_films is interactive -> patch input/print
        db = dbmod.Database()

        # Case 1: no popular films
        f_low = Film(name="Low")
        f_low.average_rating = lambda: 1
        db.add_films(f_low)
        with patch("builtins.print"):
            db.popular_films()

        # Case 2: has popular film -> choose Exit
        db2 = dbmod.Database()
        f_hi = Film(name="High")
        f_hi.average_rating = lambda: 10
        f_hi.display_film = lambda: None
        db2.add_films(f_hi)

        with patch("builtins.input", side_effect=["2"]), patch("builtins.print"):
            db2.popular_films()

        # Case 3: view film -> exit with 'e'
        with patch("builtins.input", side_effect=["1", "e"]), patch("builtins.print"):
            db2.popular_films()

        # Case 4: view film -> invalid -> out of range -> valid
        with patch("builtins.input", side_effect=["1", "x", "99", "1"]), patch("builtins.print"):
            db2.popular_films()
