"""
White-box Branch Testing (Lab 9 style)

Goal: Cover each decision outcome (True/False) at least once in:
  - logic.user_registration.readJson (file exists vs missing)
  - logic.user_registration.registerUser (empty username, short password, duplicate username, success)
  - logic.user_login.loginUser (missing inputs, unknown username, missing record, wrong password, success)

Notes:
  * We redirect all file I/O to a TemporaryDirectory so tests do not touch real project data.
  * This is branch testing: cases are chosen to flip every if-condition outcome.
"""

import os
import tempfile
import unittest

import logic.user_registration as user_reg
import logic.user_login as user_login


class TestUserAuthBranch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.users_path = os.path.join(self.tmp.name, "users.json")

        user_reg.dataDir = self.tmp.name
        user_reg.usersFile = self.users_path
        user_login.usersFile = self.users_path

        # Start with empty store
        if os.path.exists(self.users_path):
            os.remove(self.users_path)
        user_reg.saveJson(self.users_path, {"byId": {}, "byUsername": {}})

    def tearDown(self):
        self.tmp.cleanup()

    # ---- registerUser branches ----
    def test_registerUser_empty_username_raises(self):
        with self.assertRaises(ValueError):
            user_reg.registerUser("", "secret1")

    def test_registerUser_short_password_raises(self):
        with self.assertRaises(ValueError):
            user_reg.registerUser("bob", "123")  # < 6 chars

    def test_registerUser_duplicate_username_raises(self):
        user_reg.registerUser("bob", "secret1")
        with self.assertRaises(ValueError):
            user_reg.registerUser("bob", "secret2")

    # ---- readJson branches ----
    def test_readJson_file_exists_reads(self):
        user_reg.saveJson(self.users_path, {"hello": "world"})
        self.assertEqual(user_reg.readJson(self.users_path, {}), {"hello": "world"})

    def test_readJson_missing_file_returns_default(self):
        os.remove(self.users_path)
        self.assertEqual(user_reg.readJson(self.users_path, {"x": 1}), {"x": 1})

    # ---- loginUser branches ----
    def test_loginUser_missing_inputs_returns_none(self):
        self.assertIsNone(user_login.loginUser("", "pw"))
        self.assertIsNone(user_login.loginUser("bob", ""))

    def test_loginUser_unknown_username_returns_none(self):
        self.assertIsNone(user_login.loginUser("unknown", "secret1"))

    def test_loginUser_userId_present_but_record_missing_returns_none(self):
        users = {"byId": {}, "byUsername": {"ghost": "id-123"}}
        user_reg.saveJson(self.users_path, users)
        self.assertIsNone(user_login.loginUser("ghost", "secret1"))

    def test_loginUser_wrong_password_returns_none(self):
        user_reg.registerUser("alice", "secret1")
        self.assertIsNone(user_login.loginUser("alice", "wrongpw"))

    def test_loginUser_success_returns_record(self):
        record = user_reg.registerUser("carol", "secret1")
        got = user_login.loginUser("carol", "secret1")
        self.assertIsNotNone(got)
        self.assertEqual(got["id"], record["id"])


if __name__ == "__main__":
    unittest.main()
