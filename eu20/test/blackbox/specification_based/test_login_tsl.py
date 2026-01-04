import unittest
import json
import tempfile
import os

import logic.user_registration as ur
import logic.user_login as ul


class TestLoginUserTSL(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = self.tmp.name

        ur.dataDir = tmp_path
        ur.usersFile = os.path.join(tmp_path, "users.json")
        ul.dataDir = tmp_path
        ul.usersFile = ur.usersFile

        with open(ur.usersFile, "w", encoding="utf-8") as f:
            json.dump({"byId": {}, "byUsername": {}}, f, indent=2)

        self.valid_user = ur.registerUser("emre", "123456")

    def tearDown(self):
        self.tmp.cleanup()


    def test_login_empty_username(self):
        result = ul.loginUser("", "123456")
        self.assertIsNone(result)

    def test_login_username_spaces_only(self):
        result = ul.loginUser("   ", "123456")
        self.assertIsNone(result)

    def test_login_missing_password(self):
        result = ul.loginUser("emre", None)
        self.assertIsNone(result)

    def test_login_nonexistent_user(self):
        result = ul.loginUser("unknown", "123456")
        self.assertIsNone(result)

    def test_login_wrong_password(self):
        result = ul.loginUser("emre", "wrongpass")
        self.assertIsNone(result)

    def test_login_success(self):
        result = ul.loginUser("emre", "123456")
        self.assertIsNotNone(result)
        self.assertEqual(result["username"], "emre")
