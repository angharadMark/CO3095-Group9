import unittest
import json
import tempfile
import os

import logic.user_registration as ur

'''
testing register user story
7 test cases
Partitions:
Empty username → rejected (ValueError)
Spaces-only username → rejected
Missing password → rejected
Too-short password (<6) → rejected
Valid registration → user stored in JSON correctly
Username trimming → " emre " becomes "emre"
Duplicate username → rejected
'''

class TestRegisterUserTSL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = self.tmp.name

        ur.dataDir = tmp_path
        ur.usersFile = os.path.join(tmp_path, "users.json")

        with open(ur.usersFile, "w", encoding="utf-8") as f:
            json.dump({"byId": {}, "byUsername": {}}, f, indent=2)

    def tearDown(self):
        self.tmp.cleanup()

    def read_users(self):
        with open(ur.usersFile, "r", encoding="utf-8") as f:
            return json.load(f)


    def test_username_empty_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            ur.registerUser("", "123456")
        self.assertEqual(str(ctx.exception), "Username cannot be empty")

    def test_username_spaces_only_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            ur.registerUser("   ", "123456")
        self.assertEqual(str(ctx.exception), "Username cannot be empty")

    def test_password_missing_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            ur.registerUser("emre", None)
        self.assertEqual(str(ctx.exception), "Password must be at least 6 characters")

    def test_password_too_short_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            ur.registerUser("emre", "12345")
        self.assertEqual(str(ctx.exception), "Password must be at least 6 characters")

    def test_register_min_length_success_updates_json(self):
        user = ur.registerUser("emre", "123456")
        self.assertEqual(user["username"], "emre")
        self.assertTrue(user["id"])
        self.assertTrue(user["passwordHash"])

        users = self.read_users()
        self.assertIn(user["id"], users["byId"])
        self.assertEqual(users["byUsername"]["emre"], user["id"])

    def test_register_trims_username(self):
        user = ur.registerUser("  emre  ", "123456")
        self.assertEqual(user["username"], "emre")

        users = self.read_users()
        self.assertIn("emre", users["byUsername"])

    def test_duplicate_username_rejected(self):
        ur.registerUser("emre", "123456")
        with self.assertRaises(ValueError) as ctx:
            ur.registerUser("emre", "abcdef")
        self.assertEqual(str(ctx.exception), "Username already exists")
