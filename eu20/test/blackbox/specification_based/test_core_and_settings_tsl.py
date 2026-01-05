import unittest
import tempfile
import os
import json
import argparse
from unittest.mock import patch

import logic.user_registration as ur
import logic.friends_system as fs
import database.database as dbmod


from logic.filter import string_fuzzy_match, QueryFilter, filter_films
from object.filter_type import FilterType
from object.film import Film
from object.actor import Actor

import importlib.util
from pathlib import Path

'''
Used to test the settings section and the core functionalities within the program
'''


def load_rootpkg():
    here = Path(__file__).resolve()
    for parent in [here] + list(here.parents):
        candidate = parent / "__init__.py"
        if candidate.exists():
            try:
                txt = candidate.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if "def main" in txt:
                spec = importlib.util.spec_from_file_location("rootpkg", str(candidate))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
    raise RuntimeError("Could not find root __init__.py containing def main()")

rootpkg = load_rootpkg()



class TestCoreBoostTSL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = self.tmp.name

        # temp users.json for friends_system
        ur.usersFile = os.path.join(base, "users.json")
        fs.usersFile = ur.usersFile  # friends_system imported its own usersFile

        with open(ur.usersFile, "w", encoding="utf-8") as f:
            json.dump({"byId": {}, "byUsername": {}}, f, indent=2)

        # make 2 users with the minimal fields friends_system expects
        users = ur.readJson(ur.usersFile, {"byId": {}, "byUsername": {}})

        self.a_id = "A"
        self.b_id = "B"

        users["byId"][self.a_id] = {
            "id": self.a_id, "username": "alice",
            "friends": [], "blocked": []
        }
        users["byId"][self.b_id] = {
            "id": self.b_id, "username": "bob",
            "friends": [], "blocked": []
        }
        users["byUsername"]["alice"] = self.a_id
        users["byUsername"]["bob"] = self.b_id
        ur.saveJson(ur.usersFile, users)

    def tearDown(self):
        self.tmp.cleanup()


    def test_root_main_with_patched_args(self):
        class FakeDB:
            def get_all_films(self):
                return [Film(name="FilmA"), Film(name="FilmB")]

        with patch("database.database_loader.DatabaseLoader.load", return_value=FakeDB()), \
             patch("logic.filter.filter_films", return_value=[]), \
             patch("argparse.ArgumentParser.parse_args",
                   return_value=argparse.Namespace(filter_cast=["Tom"], filter_genre=["Action"])), \
             patch("builtins.print"):
            rootpkg.main()

        out = rootpkg.process_filter(["X", "Y"], FilterType.CAST)
        self.assertEqual(len(out), 2)


    def test_filter_module_branches(self):
        self.assertTrue(string_fuzzy_match("  Hi ", "hi"))
        self.assertFalse(string_fuzzy_match("hi", "bye"))
        self.assertFalse(string_fuzzy_match(123, "hi"))

        f1 = Film(name="A", genre=["Action"], cast=[Actor("Tom", "Lead")])
        f2 = Film(name="B", genre="Comedy", cast=[Actor("Bob", "Side")])

        cast_filter = QueryFilter(FilterType.CAST, "tom")
        genre_filter_list = QueryFilter(FilterType.GENRE, "action")
        genre_filter_str = QueryFilter(FilterType.GENRE, "comedy")

        self.assertTrue(cast_filter.matches(f1))
        self.assertTrue(genre_filter_list.matches(f1))
        self.assertTrue(genre_filter_str.matches(f2))

        self.assertEqual(filter_films("bad", "bad"), [])
        self.assertEqual(filter_films([], [f1, f2]), [f1, f2])
        self.assertEqual(filter_films([genre_filter_list], []), [])
        self.assertEqual([f.name for f in filter_films([genre_filter_list], [f1, f2])], ["A"])


    def test_database_basic_and_age_and_actor_search(self):
        db = dbmod.Database()

        db.add_films(Film(name="A", age_rating="18"))
        db.add_films(Film(name="B", age_rating="bad"))
        db.add_films(Film(name="C", age_rating=None))

        self.assertTrue(db.get_film("a"))
        self.assertFalse(db.get_film("missing"))

        with patch("builtins.print"):
            self.assertEqual(db.get_age_filtered_films("notanint"), [])

        res = db.get_age_filtered_films("10")
        self.assertTrue(any(f.name == "A" for f in res))

        a1 = Actor("Tom Hardy", "Role")
        a2 = Actor("Scarlett Johansson", "Role")
        db.add_actor(a1)
        db.add_actor(a1)
        db.add_actor(a2)

        self.assertFalse(db.search_actor("zzzzzz", threshold=99))
        self.assertTrue(db.search_actor("tom", threshold=40))

    def test_database_popular_films_branches(self):
        db = dbmod.Database()

        # Case 1: no popular films
        f_low = Film(name="Low")
        f_low.average_rating = lambda: 1
        db.add_films(f_low)
        with patch("builtins.print"):
            db.popular_films()

        # Case 2: popular exists, choose Exit
        f_hi = Film(name="High")
        f_hi.average_rating = lambda: 10
        f_hi.display_film = lambda: None
        db2 = dbmod.Database()
        db2.add_films(f_hi)

        with patch("builtins.input", side_effect=["2"]), patch("builtins.print"):
            db2.popular_films()

        # Case 3: view film -> exit with 'e'
        with patch("builtins.input", side_effect=["1", "e"]), patch("builtins.print"):
            db2.popular_films()

        # Case 4: view film -> bad input -> out of range -> valid
        with patch("builtins.input", side_effect=["1", "x", "99", "1"]), patch("builtins.print"):
            db2.popular_films()


    def test_friends_system_paths(self):
        # add friend success
        with patch("builtins.input", side_effect=["bob"]), patch("builtins.print"):
            fs.add_friend(self.a_id)

        # view friends list
        with patch("builtins.print"):
            fs.view_friends(self.a_id)

        # remove friend success
        with patch("builtins.input", side_effect=["bob"]), patch("builtins.print"):
            fs.remove_friend(self.a_id)

        # add friend -> then block user (removes friendship and blocks)
        with patch("builtins.input", side_effect=["bob"]), patch("builtins.print"):
            fs.add_friend(self.a_id)

        with patch("builtins.input", side_effect=["bob"]), patch("builtins.print"):
            fs.block_user(self.a_id)

        # unblock flow: show list -> wrong -> then correct
        with patch("builtins.input", side_effect=["nope", "bob"]), patch("builtins.print"):
            fs.unblock_user(self.a_id)

    def test_friends_menu_invalid_then_back(self):
        # hit invalid option then back
        with patch("builtins.input", side_effect=["x", "7"]), patch("builtins.print"):
            fs.friends_menu(self.a_id)
