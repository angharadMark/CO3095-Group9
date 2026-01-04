import unittest
import json
import tempfile
import os
from unittest.mock import patch

import logic.user_registration as ur
import logic.friends_system as fs


class TestAddFriendTSL(unittest.TestCase):
    """
    Black-box Specification-based testing (Category Partition / TSL).
    User Story: Add other users as friends.
    SUT: logic.friends_system.add_friend(current_user_id) which prompts for username.
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

    def read_users(self):
        with open(ur.usersFile, "r", encoding="utf-8") as f:
            return json.load(f)

    # -------------------------
    # TARGET_USERNAME_INPUT partitions (via patched input())
    # -------------------------

    def test_add_friend_empty_username_rejected(self):
        users_before = self.read_users()
        with patch("builtins.input", return_value=""):
            fs.add_friend(self.u1_id)
        users_after = self.read_users()
        self.assertEqual(users_after, users_before)

    def test_add_friend_spaces_only_username_rejected(self):
        users_before = self.read_users()
        with patch("builtins.input", return_value="   "):
            fs.add_friend(self.u1_id)
        users_after = self.read_users()
        self.assertEqual(users_after, users_before)

    def test_add_friend_non_existent_user_rejected(self):
        users_before = self.read_users()
        with patch("builtins.input", return_value="does_not_exist"):
            fs.add_friend(self.u1_id)
        users_after = self.read_users()
        self.assertEqual(users_after, users_before)

    # -------------------------
    # RELATIONSHIP_STATE partitions
    # -------------------------

    def test_add_friend_self_rejected(self):
        users_before = self.read_users()
        with patch("builtins.input", return_value="user1"):
            fs.add_friend(self.u1_id)
        users_after = self.read_users()
        self.assertEqual(users_after, users_before)

    def test_add_friend_success_mutual_friendship(self):
        with patch("builtins.input", return_value="user2"):
            fs.add_friend(self.u1_id)

        users = self.read_users()
        u1_record = users["byId"][self.u1_id]
        u2_record = users["byId"][self.u2_id]

        # Mutual friendship is expected from your implementation
        self.assertIn(self.u2_id, u1_record.get("friends", []))
        self.assertIn(self.u1_id, u2_record.get("friends", []))

    def test_add_friend_already_friends_no_duplicate(self):
        with patch("builtins.input", return_value="user2"):
            fs.add_friend(self.u1_id)
        with patch("builtins.input", return_value="user2"):
            fs.add_friend(self.u1_id)

        users = self.read_users()
        u1_record = users["byId"][self.u1_id]
        u2_record = users["byId"][self.u2_id]

        # Still only one entry each
        self.assertEqual(u1_record.get("friends", []).count(self.u2_id), 1)
        self.assertEqual(u2_record.get("friends", []).count(self.u1_id), 1)


if __name__ == "__main__":
    unittest.main()
