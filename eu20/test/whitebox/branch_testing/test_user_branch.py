import unittest
from unittest.mock import patch

from object.user import User
from object.film import Film
from object.user_message import UserMessage

'''
white box testing for User to flip True/False outcomes
4 tests
Branches covered include:
rating bounds invalid (<0, >10) throws, valid rating stored, missing rating returns None
avatar change success vs fail
dislike duplicate branch (second dislike returns None)
unread message count: 0 vs 1 vs after marking read
fav film change printing path
'''

class DummyDB:
    def get_film(self, title):
        return Film(name=title, cast=[], comments=[])


class TestUserBranch(unittest.TestCase):
    def make_user(self):
        record = {
            "id": "u1",
            "username": "alice",
            "watchlist": ["A"],
            "dislikes": [],
            "inbox": [],
            "ratings": {},
            "comments": {},
            "films_added": 0,
            "avatarIndex": 0,
            "favFilm": "None Set",
        }
        return User(record, database=DummyDB())

    def test_branch_rating_bounds(self):
        u = self.make_user()

        # below range
        with self.assertRaises(IndexError):
            u.add_rating("A", -1)

        # above range
        with self.assertRaises(IndexError):
            u.add_rating("A", 11)

        # valid
        u.add_rating("A", 5)
        self.assertEqual(u.get_rating("A"), 5)

        # missing rating branch
        self.assertIsNone(u.get_rating("missing"))

    def test_branch_avatar_and_dislikes(self):
        u = self.make_user()

        # change_avatar success + fail
        self.assertTrue(u.change_avatar(0))
        self.assertFalse(u.change_avatar(9999))

        # dislike duplicate branch
        f = Film(name="Z")
        self.assertIsNotNone(u.dislike_film(f))
        self.assertIsNone(u.dislike_film(f))

        # undislike branch
        u.undislike_film(f)
        self.assertNotIn(f, u.dislikes)

    def test_branch_unread_messages(self):
        u = self.make_user()

        # 0 unread
        self.assertEqual(u.unread_message_count(), 0)

        # 1 unread
        u.send_message(UserMessage("u2", "hi", read=False))
        self.assertEqual(u.unread_message_count(), 1)

        # mark read path via to_dict/from_dict roundtrip
        d = u.inbox[0].to_dict()
        d["read"] = True
        u.inbox[0] = UserMessage.from_dict(d)
        self.assertEqual(u.unread_message_count(), 0)

    def test_branch_favfilm_printing(self):
        u = self.make_user()
        with patch("builtins.print"):
            u.change_favFilm("Interstellar")
