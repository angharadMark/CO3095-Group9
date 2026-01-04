import unittest
from unittest.mock import patch, mock_open
from database.database_loader import DatabaseLoader

class TestDatabaseLoader(unittest.TestCase):
    def test_load_file_not_found(self):
        # Hits the 'except FileNotFoundError: pass' branch
        loader = DatabaseLoader()
        db = loader.load("non_existent_file.json")
        self.assertEqual(len(db.get_all_films()), 0)

    def test_load_corrupted_cast_data(self):
        # Hits the 'if not actor_name or not role: continue' branch
        corrupt_json = '[{"name": "Film", "cast": [{"actor": "", "role": ""}]}]'
        with patch("builtins.open", mock_open(read_data=corrupt_json)):
            loader = DatabaseLoader()
            db = loader.load("dummy.json")
            self.assertEqual(len(db.get_all_films()), 1)
            self.assertEqual(len(db.get_all_films()[0].cast), 0)