import unittest
import tempfile
import os
import json
from unittest.mock import patch

import settings


class TestInterfaceTogglesTSL(unittest.TestCase):
    """
    Black-box Specification-based testing (Category Partition / TSL).
    Sprint 3 User Story: Admin can enable/disable interface features.
    SUT: settings.load_interface(), settings.save_interface(), settings.feature_on(key), settings.interface_menu()
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = self.tmp.name

        # IMPORTANT: point settings to a temp interface file
        self.interface_path = os.path.join(self.tmp_path, "interface.json")
        settings.INTERFACE_FILE = self.interface_path

    def tearDown(self):
        self.tmp.cleanup()

    # ------------------------
    # CONFIG_FILE_STATE = missing
    # ------------------------
    def test_defaults_loaded_when_config_missing(self):
        # No file exists
        cfg = settings.load_interface()
        self.assertEqual(cfg, settings.DEFAULT_INTERFACE)

        # feature_on should reflect defaults
        self.assertTrue(settings.feature_on("friends"))
        self.assertTrue(settings.feature_on("movie_of_day"))
        self.assertTrue(settings.feature_on("comments"))

    # ------------------------
    # CONFIG_FILE_STATE = valid
    # ------------------------
    def test_save_and_load_persists_config(self):
        custom = {"friends": False, "movie_of_day": True, "comments": False}
        settings.save_interface(custom)

        cfg = settings.load_interface()
        self.assertEqual(cfg, custom)

        self.assertFalse(settings.feature_on("friends"))
        self.assertTrue(settings.feature_on("movie_of_day"))
        self.assertFalse(settings.feature_on("comments"))

    def test_unknown_feature_key_defaults_true(self):
        # With missing config file, unknown key should default to True
        self.assertTrue(settings.feature_on("some_new_feature_key"))

    # ------------------------
    # CONFIG_FILE_STATE = corrupted
    # ------------------------
    def test_corrupted_config_falls_back_to_defaults(self):
        with open(self.interface_path, "w", encoding="utf-8") as f:
            f.write("{not valid json")

        cfg = settings.load_interface()
        self.assertEqual(cfg, settings.DEFAULT_INTERFACE)

    # ------------------------
    # ADMIN_ACTION partitions via interface_menu (CLI)
    # ------------------------
    def test_toggle_friends_updates_config(self):
        # Start from defaults
        cfg0 = settings.load_interface()
        self.assertTrue(cfg0["friends"])

        # In the interface menu:
        # 1 = toggle friends
        # 5 = exit
        with patch("builtins.input", side_effect=["1", "5"]):
            settings.interface_menu()

        cfg1 = settings.load_interface()
        self.assertFalse(cfg1["friends"])  # should have flipped

    def test_reset_defaults_restores_all_true(self):
        # First set a custom config
        settings.save_interface({"friends": False, "movie_of_day": False, "comments": False})

        # In the interface menu:
        # 4 = reset defaults
        # 5 = exit
        with patch("builtins.input", side_effect=["4", "5"]):
            settings.interface_menu()

        cfg = settings.load_interface()
        self.assertEqual(cfg, settings.DEFAULT_INTERFACE)


if __name__ == "__main__":
    unittest.main()
