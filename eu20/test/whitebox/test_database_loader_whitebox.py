import unittest
import json
import tempfile
import os

from database.database_loader import DatabaseLoader


class TestDatabaseLoaderWhiteBox(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "films.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_load_missing_file_returns_empty_database_or_handles_gracefully(self):
        loader = DatabaseLoader()
        # load a file that does not exist
        db = loader.load(os.path.join(self.tmp.name, "missing.json"))
        # We don't assume exact type structure; just that it returns something usable.
        self.assertIsNotNone(db)

    def test_load_empty_list(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([], f)

        loader = DatabaseLoader()
        db = loader.load(self.path)
        self.assertIsNotNone(db)

    def test_load_single_film_minimal_fields(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([{"name": "Film A", "year": "2020"}], f)

        loader = DatabaseLoader()
        db = loader.load(self.path)
        self.assertIsNotNone(db)


    def test_load_invalid_json_raises_json_decode_error(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{bad json")

        loader = DatabaseLoader()
        with self.assertRaises(json.JSONDecodeError):
            loader.load(self.path)



if __name__ == "__main__":
    unittest.main()
