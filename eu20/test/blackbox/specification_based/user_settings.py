import unittest
import tempfile
import json
import os
from unittest.mock import patch

import logic.user_registration as ur
import logic.user_settings as us
from object.user import User


class TestUserSettingsTSL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = self.tmp.name

        # Redirect BOTH modules to the temp users.json
        ur.dataDir = tmp_path
        ur.usersFile = os.path.join(tmp_path, "users.json")
        us.usersFile = ur.usersFile  # important: user_settings imported usersFile

        with open(ur.usersFile, "w", encoding="utf-8") as f:
            json.dump({"byId": {}, "byUsername": {}}, f, indent=2)

        # Create two users
        self.u1 = ur.registerUser("alice", "123456")
        self.u2 = ur.registerUser("bob", "123456")

    def tearDown(self):
        self.tmp.cleanup()

    def read_users(self):
        with open(ur.usersFile, "r", encoding="utf-8") as f:
            return json.load(f)

    # -------- changeUsername --------

    def test_change_username_empty_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            us.changeUsername(self.u1["id"], "   ")
        self.assertEqual(str(ctx.exception), "Username cannot be empty")

    def test_change_username_duplicate_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            us.changeUsername(self.u1["id"], "bob")
        self.assertEqual(str(ctx.exception), "Username already exists. ")

    def test_change_username_user_not_found(self):
        with self.assertRaises(ValueError) as ctx:
            us.changeUsername("missing-id", "newname")
        self.assertEqual(str(ctx.exception), "User not found")

    def test_change_username_success_updates_json(self):
        updated = us.changeUsername(self.u1["id"], "alice2")
        self.assertEqual(updated, "alice2")

        users = self.read_users()
        self.assertIn("alice2", users["byUsername"])
        self.assertNotIn("alice", users["byUsername"])
        self.assertEqual(users["byId"][self.u1["id"]]["username"], "alice2")

    # -------- changePassword --------

    def test_change_password_too_short_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            us.changePassword(self.u1["id"], "123456", "123")
        self.assertEqual(str(ctx.exception), "New password must be atleast 6 characters")

    def test_change_password_user_not_found(self):
        with self.assertRaises(ValueError) as ctx:
            us.changePassword("missing-id", "123456", "abcdef")
        self.assertEqual(str(ctx.exception), "User not found")

    def test_change_password_wrong_current_password(self):
        with self.assertRaises(ValueError) as ctx:
            us.changePassword(self.u1["id"], "wrongpw", "abcdef")
        self.assertEqual(str(ctx.exception), "Current password is incorrect")

    def test_change_password_success_updates_hash(self):
        before = self.read_users()["byId"][self.u1["id"]]["passwordHash"]
        us.changePassword(self.u1["id"], "123456", "abcdef")
        after = self.read_users()["byId"][self.u1["id"]]["passwordHash"]
        self.assertNotEqual(before, after)

    # -------- saveAvatarIndex + deleteUserAccount --------

    def test_save_avatar_index_updates_user(self):
        us.saveAvatarIndex(self.u1["id"], 3)
        users = self.read_users()
        self.assertEqual(users["byId"][self.u1["id"]]["avatarIndex"], 3)

    def test_save_avatar_index_missing_user_prints_warning(self):
        with patch("builtins.print") as p:
            us.saveAvatarIndex("missing-id", 1)
            p.assert_called()

    def test_delete_user_account_success(self):
        ok = us.deleteUserAccount(self.u2["id"])
        self.assertTrue(ok)
        users = self.read_users()
        self.assertNotIn(self.u2["id"], users["byId"])
        self.assertNotIn("bob", users["byUsername"])

    def test_delete_user_account_missing_returns_false(self):
        self.assertFalse(us.deleteUserAccount("missing-id"))

    # -------- menu functions (cover loops without needing UI) --------

    def test_change_avatar_menu_exit_immediately(self):
        user_obj = User(self.u1)
        with patch("builtins.input", side_effect=["0"]):
            us.changeAvatarMenu(user_obj, self.u1["id"])

    def test_change_fav_film_menu_cancel(self):
        user_obj = User(self.u1)
        with patch("builtins.input", side_effect=[""]):
            us.changeFavFilmMenu(user_obj, self.u1["id"])
