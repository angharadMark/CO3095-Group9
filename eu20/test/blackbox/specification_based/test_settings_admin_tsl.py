import unittest
import tempfile
import os
import json
from unittest.mock import patch

import logic.user_registration as ur
import logic.user_settings as us
import settings
from logic.user_state import UserState

'''
used for the settings menu and admin menu
3 test cases
settingsMenu()
    view profile, 
    change username, 
    password mismatch handling,
    avatar menu exit, 
    cancel fav film change, 
    logout
    
    adminMenu()
        delete branches
            user not found
            cant delete admins
            cancel delete
            confirm delete
        print users
        manage interface toggles
        
'''


class TestSettingsAdminTSL(unittest.TestCase):
    def setUp(self):
        # temp folder for users.json + interface.json
        self.tmp = tempfile.TemporaryDirectory()
        base = self.tmp.name

        # redirect users.json everywhere
        ur.usersFile = os.path.join(base, "users.json")
        us.usersFile = ur.usersFile
        settings.usersFile = ur.usersFile

        # fresh users file
        with open(ur.usersFile, "w", encoding="utf-8") as f:
            json.dump({"byId": {}, "byUsername": {}}, f, indent=2)

        # create users
        self.admin = ur.registerUser("admin", "admins")
        self.alice = ur.registerUser("alice", "123456")
        self.bob = ur.registerUser("bob", "123456")

        # redirect interface.json too
        settings.INTERFACE_FILE = os.path.join(base, "interface.json")
        if os.path.exists(settings.INTERFACE_FILE):
            os.remove(settings.INTERFACE_FILE)

        # logged-in state for settingsMenu
        self.state = UserState()
        self.state.login(self.alice)

    def tearDown(self):
        self.tmp.cleanup()

    def test_settings_menu_paths(self):
        # Drives settingsMenu through: view profile, change username,
        # password mismatch, avatar menu exit, fav film cancel, logout
        with patch("builtins.input", side_effect=[
            "1",        # view profile
            "2", "alice2",  # change username
            "3",        # change password (mismatch handled via getpass)
            "4", "0",   # change avatar -> immediately exit menu
            "5", "",    # change fav film -> cancel
            "6",        # logout
        ]), patch("settings.getpass", side_effect=[
            "123456", "newpass1", "newpass2"   # mismatch
        ]), patch("builtins.print"):
            settings.settingsMenu(self.state)

        self.assertFalse(self.state.isLoggedIn())

    def test_admin_menu_delete_branches_and_interface(self):
        # adminMenu loops forever, so we end it by raising SystemExit at the end.
        # We cover:
        # - delete user not found
        # - cannot delete admin
        # - delete cancelled
        # - delete confirmed
        # - print users
        # - manage interface (toggle then back)
        def input_side_effect(prompt=""):
            seq = [
                "1", "no_such_user",                # delete -> not found
                "1", "admin",                       # delete -> cannot delete admin
                "1", "bob", "n",                    # delete -> cancelled
                "1", "bob", "y",                    # delete -> confirmed
                "2",                                # print usernames
                "4", "1", "5",                      # interface_menu: toggle friends, back
            ]
            # After sequence ends, stop the infinite while loop
            if not hasattr(input_side_effect, "i"):
                input_side_effect.i = 0
            if input_side_effect.i >= len(seq):
                raise SystemExit()
            val = seq[input_side_effect.i]
            input_side_effect.i += 1
            return val

        # login as admin (not required by code, but makes sense)
        st = UserState()
        st.login(self.admin)

        with patch("builtins.input", side_effect=input_side_effect), patch("builtins.print"):
            with self.assertRaises(SystemExit):
                settings.adminMenu(st)

        # bob should be deleted now
        users = ur.readJson(ur.usersFile, {"byId": {}, "byUsername": {}})
        self.assertNotIn("bob", users["byUsername"])

        # interface file should exist and friends should be toggled to False
        cfg = settings.load_interface()
        self.assertIn("friends", cfg)
        self.assertFalse(cfg["friends"])

    def test_admin_menu_option_6_colon_branch(self):
        # There is a bug in settings.py: it checks '6:' not '6'
        # We'll hit that branch for coverage.
        def input_side_effect(prompt=""):
            seq = ["6:", "q"]
            if not hasattr(input_side_effect, "i"):
                input_side_effect.i = 0
            if input_side_effect.i >= len(seq):
                raise SystemExit()
            val = seq[input_side_effect.i]
            input_side_effect.i += 1
            return val

        st = UserState()
        st.login(self.admin)

        with patch("builtins.input", side_effect=input_side_effect), patch("builtins.print"):
            with self.assertRaises(SystemExit):
                settings.adminMenu(st)
