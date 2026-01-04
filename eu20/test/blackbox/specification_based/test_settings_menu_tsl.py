import unittest
import tempfile
import json
import os
from unittest.mock import patch

import logic.user_registration as ur
import settings
from logic.user_state import UserState


class TestSettingsMenuTSL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        tmp_path = self.tmp.name

        # redirect users.json used by registration + settings imports
        ur.dataDir = tmp_path
        ur.usersFile = os.path.join(tmp_path, "users.json")

        with open(ur.usersFile, "w", encoding="utf-8") as f:
            json.dump({"byId": {}, "byUsername": {}}, f, indent=2)

        # create a user and login
        self.user = ur.registerUser("alice", "123456")
        self.state = UserState()
        self.state.login(self.user)

        # isolate interface.json too
        settings.INTERFACE_FILE = os.path.join(tmp_path, "interface.json")
        if os.path.exists(settings.INTERFACE_FILE):
            os.remove(settings.INTERFACE_FILE)

    def tearDown(self):
        self.tmp.cleanup()

    def test_settings_menu_requires_login(self):
        state = UserState()
        with patch("builtins.print") as p:
            settings.settingsMenu(state)
            p.assert_called()

    def test_interface_menu_toggle_and_back(self):
        # 1 toggle friends, then 5 back
        with patch("builtins.input", side_effect=["1", "5"]):
            settings.interface_menu()

        cfg = settings.load_interface()
        self.assertFalse(cfg["friends"])

    def test_settings_menu_view_profile_then_back(self):
        # Choice 1 (view profile) then 8 back
        with patch("builtins.input", side_effect=["1", "8"]):
            settings.settingsMenu(self.state)

    def test_settings_menu_change_username_then_back(self):
        # Change username to alice2, then back
        with patch("builtins.input", side_effect=["2", "alice2", "8"]):
            settings.settingsMenu(self.state)
        self.assertEqual(self.state.currentUser["username"], "alice2")

    def test_settings_menu_change_password_mismatch_then_back(self):
        # choice 3 then mismatch => prints + continue, then back
        with patch("settings.getpass", side_effect=["old", "newpass1", "newpass2"]), \
             patch("builtins.input", side_effect=["3", "8"]), \
             patch("builtins.print") as p:
            settings.settingsMenu(self.state)
            # "Passwords do not match." should have been printed at least once
            self.assertTrue(any("Passwords do not match" in str(c) for c in p.call_args_list))

    def test_settings_menu_logout_path(self):
        with patch("builtins.input", side_effect=["6"]):
            settings.settingsMenu(self.state)
        self.assertFalse(self.state.isLoggedIn())

    def test_settings_menu_delete_cancel_then_back(self):
        with patch("builtins.input", side_effect=["7", "n", "8"]):
            settings.settingsMenu(self.state)

    def test_settings_menu_delete_confirm_then_exits(self):
        # confirm y => delete => logs out => breaks
        with patch("builtins.input", side_effect=["7", "y"]), \
             patch("builtins.print"):
            settings.settingsMenu(self.state)
        self.assertFalse(self.state.isLoggedIn())
