import unittest
import json
import tempfile
import os
import io
from contextlib import redirect_stdout
from unittest.mock import patch

import logic.user_registration as ur
import logic.friends_system as fs

from object.film import Film
from object.comment import Comment


class FakeDatabase:
    def __init__(self, films):
        self.films = films


class FakeLoader:
    """Replaces DatabaseLoader inside friends_system for testing."""
    def __init__(self, database):
        self._db = database

    def load(self, _path):
        return self._db


class TestViewFriendsCommentsTSL(unittest.TestCase):
    """
    Black-box Specification-based testing (Category Partition / TSL).
    User Story: View comments made by my friends.
    SUT: logic.friends_system.view_friends_comments(current_user_id)
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = self.tmp.name

        # Patch registration storage
        ur.dataDir = tmp_path
        ur.usersFile = os.path.join(tmp_path, "users.json")

        # IMPORTANT: friends_system imported usersFile by value, so patch it too
        fs.usersFile = ur.usersFile

        # Create empty users.json
        with open(ur.usersFile, "w", encoding="utf-8") as f:
            json.dump({"byId": {}, "byUsername": {}}, f, indent=2)

        # Create two users
        self.u1 = ur.registerUser("user1", "123456")
        self.u2 = ur.registerUser("user2", "123456")

        self.u1_id = self.u1["id"]
        self.u2_id = self.u2["id"]

    def tearDown(self):
        self.tmp.cleanup()

    def _capture_output(self, func, *args, **kwargs) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            func(*args, **kwargs)
        return buf.getvalue()

    # -------------------------
    # Partitions / Test Cases
    # -------------------------

    def test_current_user_not_found(self):
        # Partition: invalid current user id
        out = self._capture_output(fs.view_friends_comments, "does_not_exist_id")
        self.assertIn("Current user not found.", out)

    def test_no_friends_added(self):
        # Partition: friends list empty
        out = self._capture_output(fs.view_friends_comments, self.u1_id)
        self.assertIn("You have no friends added.", out)

    def test_chosen_user_not_in_friends_list(self):
        # Make user2 a friend first (your add_friend uses input)
        with patch("builtins.input", return_value="user2"):
            fs.add_friend(self.u1_id)

        # Now choose a username that is NOT in friends list
        with patch("builtins.input", return_value="not_a_friend"):
            out = self._capture_output(fs.view_friends_comments, self.u1_id)

        self.assertIn("That user is not in your friends list.", out)

    def test_friend_has_no_comments(self):
        # user2 becomes friend
        with patch("builtins.input", return_value="user2"):
            fs.add_friend(self.u1_id)

        # Fake database with films but no comments by user2
        f1 = Film(name="FilmA", comments=[Comment("hello", user="someone_else")])
        fake_db = FakeDatabase([f1])

        # Patch DatabaseLoader used inside friends_system
        with patch.object(fs, "DatabaseLoader", return_value=FakeLoader(fake_db)):
            with patch("builtins.input", return_value="user2"):
                out = self._capture_output(fs.view_friends_comments, self.u1_id)

        self.assertIn("user2 has not made any comments.", out)

    def test_friend_has_comments_displayed(self):
        # user2 becomes friend
        with patch("builtins.input", return_value="user2"):
            fs.add_friend(self.u1_id)

        # Fake database with a comment by user2
        f1 = Film(name="FilmA", comments=[Comment("Great film", user="user2")])
        f2 = Film(name="FilmB", comments=[Comment("Meh", user="someone_else")])
        fake_db = FakeDatabase([f1, f2])

        with patch.object(fs, "DatabaseLoader", return_value=FakeLoader(fake_db)):
            with patch("builtins.input", return_value="user2"):
                out = self._capture_output(fs.view_friends_comments, self.u1_id)

        # Check key output markers
        self.assertIn("Comments by user2:", out)
        self.assertIn("Film: FilmA", out)
        self.assertIn("Comment:", out)


if __name__ == "__main__":
    unittest.main()
