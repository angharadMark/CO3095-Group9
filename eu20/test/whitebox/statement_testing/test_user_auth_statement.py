"""
White-box Statement Testing (Lab 9 style)

Goal: Execute every statement at least once in:
  - logic.user_registration: ensureDataDir, readJson, saveJson, hashPassword, verifyPassword, userExists, registerUser
  - logic.user_login: loginUser

Notes:
  * We redirect all file I/O to a TemporaryDirectory so tests do not touch real project data.
  * This is statement testing: chosen to run each line at least once (not every branch).
"""

import os
import tempfile
import unittest

import logic.user_registration as user_reg
import logic.user_login as user_login


class TestUserAuthStatement(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.users_path = os.path.join(self.tmp.name, "users.json")

        # Patch module-level paths to point at the temp folder/file
        user_reg.dataDir = self.tmp.name
        user_reg.usersFile = self.users_path
        user_login.usersFile = self.users_path

        # Ensure a clean file for each test
        if os.path.exists(self.users_path):
            os.remove(self.users_path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_statement_coverage_happy_path_register_then_login(self):
        # ensureDataDir + saveJson + readJson executed
        user_reg.ensureDataDir()

        # registerUser executes validation, hashing, writes file
        record = user_reg.registerUser("alice", "secret1")
        self.assertEqual(record["username"], "alice")

        # userExists executes readJson and membership check
        self.assertTrue(user_reg.userExists("alice"))

        # verifyPassword executes bcrypt check
        self.assertTrue(user_reg.verifyPassword("secret1", record["passwordHash"]))

        # loginUser executes readJson + lookup + verifyPassword + return record
        logged_in = user_login.loginUser("alice", "secret1")
        self.assertIsNotNone(logged_in)
        self.assertEqual(logged_in["id"], record["id"])

    def test_readJson_returns_default_when_missing_file(self):
        default = {"byId": {}, "byUsername": {}}
        self.assertEqual(user_reg.readJson(self.users_path, default), default)


if __name__ == "__main__":
    unittest.main()
