import unittest
from unittest.mock import patch

from logic.filter import string_fuzzy_match, QueryFilter, filter_films
from object.filter_type import FilterType
from object.film import Film
from object.actor import Actor

from database.database import Database, normalise
from object.user_message import UserMessage
from logic.user_state import UserState

import __init__ as rootpkg  # project root __init__.py


class TestMiscCoverageTSL(unittest.TestCase):
    def test_string_fuzzy_match(self):
        self.assertTrue(string_fuzzy_match("  Hi ", "hi"))
        self.assertFalse(string_fuzzy_match("hi", "bye"))
        self.assertFalse(string_fuzzy_match(123, "hi"))

    def test_query_filter_cast_and_genre(self):
        f = Film(name="X", cast=[Actor("Tom", "Lead")], genre=["Action", "Drama"])
        cast_filter = QueryFilter(FilterType.CAST, " tom ")
        genre_filter = QueryFilter(FilterType.GENRE, "action")
        self.assertTrue(cast_filter.matches(f))
        self.assertTrue(genre_filter.matches(f))

    def test_filter_films_branches(self):
        f1 = Film(name="A", genre=["Action"])
        f2 = Film(name="B", genre=["Comedy"])
        flt = [QueryFilter(FilterType.GENRE, "action")]

        self.assertEqual(filter_films("bad", "bad"), [])
        self.assertEqual(filter_films([], [f1, f2]), [f1, f2])
        self.assertEqual(filter_films(flt, []), [])
        self.assertEqual([x.name for x in filter_films(flt, [f1, f2])], ["A"])

    def test_database_get_film_and_age_filter(self):
        db = Database()
        db.add_films(Film(name="A", age_rating="18"))
        db.add_films(Film(name="B", age_rating="bad"))
        db.add_films(Film(name="C", age_rating=None))

        self.assertTrue(db.get_film("a"))
        self.assertFalse(db.get_film("missing"))

        self.assertEqual(db.get_age_filtered_films("notanint"), [])
        out = db.get_age_filtered_films("10")
        self.assertEqual([f.name for f in out], ["A"])  # matches their current logic

    def test_database_search_actor(self):
        db = Database()
        a1 = Actor("Tom Hardy", "Role")
        a2 = Actor("Scarlett Johansson", "Role")
        db.add_actor(a1)
        db.add_actor(a2)

        self.assertFalse(db.search_actor("zzzzzz", threshold=90))
        res = db.search_actor("tom", threshold=50)
        self.assertTrue(res)

    def test_root_process_filter(self):
        filters = rootpkg.process_filter(["Tom", "Brad"], FilterType.CAST)
        self.assertEqual(len(filters), 2)
        self.assertEqual(filters[0].get_type(), FilterType.CAST)

    def test_user_message_and_state(self):
        msg = UserMessage("sender", "hello", read=False)
        self.assertFalse(msg.get_read_status())
        msg.mark_as_read()
        self.assertTrue(msg.get_read_status())
        d = msg.to_dict()
        msg2 = UserMessage.from_dict(d)
        self.assertEqual(msg2.get_message(), "hello")

        st = UserState()
        self.assertFalse(st.isLoggedIn())
        st.login({"id": "1", "username": "x"})
        self.assertTrue(st.isLoggedIn())
        st.logout()
        self.assertFalse(st.isLoggedIn())

    def test_actor_add_film_and_filmography(self):
        a = Actor("A", "R")
        f = Film(name="Movie")
        a.add_film(f)
        a.add_film(f)  # dedupe
        with patch("builtins.print") as p:
            a.filmography()
            p.assert_called()
