import unittest
import tempfile
import json
import os
from unittest.mock import patch

import logic.user_registration as ur
import logic.friends_system as fs


class TestFriendsSystemExtraTSL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = self.tmp.name

        ur.dataDir = tmp_path
        ur.usersFile = os.path.join(tmp_path, "users.json")
        fs.usersFile = ur.usersFile  # important

        with open(ur.usersFile, "w", encoding="utf-8") as f:
            json.dump({"byId": {}, "byUsername": {}}, f, indent=2)

        self.a = ur.registerUser("alice", "123456")
        self.b = ur.registerUser("bob", "123456")

        # Ensure required lists exist
        users = ur.readJson(ur.usersFile, {"byId": {}, "byUsername": {}})
        users["byId"][self.a["id"]].setdefault("friends", [])
        users["byId"][self.a["id"]].setdefault("blocked", [])
        users["byId"][self.b["id"]].setdefault("friends", [])
        users["byId"][self.b["id"]].setdefault("blocked", [])
        ur.saveJson(ur.usersFile, users)

    def test_view_friends_no_friends(self):
        with patch("builtins.print") as p:
            fs.view_friends(self.a["id"])
            p.assert_called()

    def test_add_friend_user_not_found(self):
        with patch("builtins.input", side_effect=["nobody"]), patch("builtins.print") as p:
            fs.add_friend(self.a["id"])
            p.assert_called()

    def test_add_friend_cannot_add_self(self):
        with patch("builtins.input", side_effect=["alice"]), patch("builtins.print") as p:
            fs.add_friend(self.a["id"])
            p.assert_called()

    def test_add_friend_success_mutual(self):
        with patch("builtins.input", side_effect=["bob"]):
            fs.add_friend(self.a["id"])

        users = ur.readJson(ur.usersFile, {"byId": {}, "byUsername": {}})
        self.assertIn(self.b["id"], users["byId"][self.a["id"]]["friends"])
        self.assertIn(self.a["id"], users["byId"][self.b["id"]]["friends"])

    def test_remove_friend_not_in_list(self):
        with patch("builtins.input", side_effect=["bob"]), patch("builtins.print") as p:
            fs.remove_friend(self.a["id"])
            p.assert_called()

    def test_remove_friend_success_mutual(self):
        with patch("builtins.input", side_effect=["bob"]):
            fs.add_friend(self.a["id"])

        with patch("builtins.input", side_effect=["bob"]):
            fs.remove_friend(self.a["id"])

        users = ur.readJson(ur.usersFile, {"byId": {}, "byUsername": {}})
        self.assertNotIn(self.b["id"], users["byId"][self.a["id"]]["friends"])
        self.assertNotIn(self.a["id"], users["byId"][self.b["id"]]["friends"])

    def test_block_user_quit(self):
        with patch("builtins.input", side_effect=["q"]):
            fs.block_user(self.a["id"])

    def test_unblock_user_nobody_blocked(self):
        users = ur.readJson(ur.usersFile, {"byId": {}, "byUsername": {}})
        users["byId"][self.a["id"]]["blocked"] = []
        ur.saveJson(ur.usersFile, users)

        with patch("builtins.print") as p:
            fs.unblock_user(self.a["id"])
            p.assert_called()
