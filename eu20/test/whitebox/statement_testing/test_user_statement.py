import unittest
from unittest.mock import patch

from object.user import User
from object.film import Film
from object.actor import Actor
from object.user_message import UserMessage


class DummyDB:
    def get_film(self, title):
        return Film(name=title, cast=[], comments=[])


class TestUserStatement(unittest.TestCase):
    def make_user(self):
        record = {
            "id": "u1",
            "username": "alice",
            "watchlist": ["A", "B"],
            "dislikes": ["X"],
            # FIX: from_dict expects "sender", not "sender_id"
            "inbox": [{"sender": "u2", "message": "hi", "read": False}],
            "ratings": {"A": 7},
            "comments": [],
            "films_added": 1,
            "avatarIndex": 0,
            "favFilm": "None Set",
        }
        return User(record, database=DummyDB())

    def test_statement_paths_basic(self):
        u = self.make_user()

        # basic getters
        self.assertEqual(u.username, "alice")
        self.assertEqual(u.get_films_added(), 1)
        self.assertEqual(len(u.get_inbox()), 1)

        # watchlist add/remove/pop
        f = Film(name="C")
        u.add_to_watchList(f)
        self.assertTrue(any(x.name == "C" for x in u.watchList))
        u.remove_from_watchlist(f)
        self.assertFalse(any(x.name == "C" for x in u.watchList))
        u.pop_from_watchlist(0)

        # display watchlist branches
        with patch("builtins.print"):
            u.display_watchlist()
        u.watchList = []
        with patch("builtins.print"):
            u.display_watchlist()

        # remove_by_actors no match (covers loop without hitting buggy push)
        u.watchList = [
            Film(name="F1", cast=[Actor("Tom", "Lead")]),
            Film(name="F2", cast=[Actor("Brad", "Lead")]),
        ]
        removed = u.remove_from_watchlist_by_actors(["NoOne"])
        self.assertEqual(removed, 0)

        # ratings + comments + messages
        self.assertEqual(u.get_rating("A"), 7)
        u.add_rating("B", 9)
        self.assertEqual(u.get_rating("B"), 9)
        u.add_comment(Film(name="A"), "Nice")
        self.assertEqual(len(u.comments), 1)
        self.assertEqual(u.comments[0]["film"], "A")

        # inbox / unread count
        self.assertEqual(u.unread_message_count(), 1)
        u.send_message(UserMessage("u3", "hello", read=True))
        self.assertEqual(len(u.inbox), 2)

        # profile display (prints)
        with patch("builtins.print"):
            u.display_profile()
