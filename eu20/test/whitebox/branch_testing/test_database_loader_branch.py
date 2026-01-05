import json
import os
import tempfile
import unittest

from database.database_loader import DatabaseLoader

'''
Branch testing for DatabaseLoader.load()
3 tests
Coverage includes:
missing file branch
invalid JSON branch
valid JSON with mixed bad cast entries, missing actor/role, duplicate cast, bad comment entries, valid comments, and actor reuse across films
'''

class TestDatabaseLoaderBranch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "films.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_load_missing_file_returns_empty_database(self):
        db = DatabaseLoader().load(os.path.join(self.tmp.name, "does_not_exist.json"))
        self.assertIsNotNone(db)
        self.assertEqual(len(db.films), 0)

    def test_load_invalid_json_returns_empty_database(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{bad json")

        db = DatabaseLoader().load(self.path)
        self.assertIsNotNone(db)
        self.assertEqual(len(db.films), 0)

    def test_load_exercises_cast_and_comment_branches(self):
        data = [
            {
                "name": "Film A",
                "year": 2020,
                "cast": [
                    "not-a-dict",
                    {"actor": "", "role": "Lead"},
                    {"actor": "A1", "role": ""},
                    {"actor": "A1", "role": "Lead"},
                    {"actor": "A1", "role": "Lead"},
                ],
                "comments": [
                    "bad",
                    {"user": "u1"},
                    {"user": "u1", "message": "hi"}
                ],
                "genre": ["Action"],
                "age_rating": "12",
                "ratings": [5, 4],
                "description": "desc"
            },
            {
                "name": "Film B",
                "year": 2021,
                "cast": [{"actor": "A1", "role": "Lead"}],
                "comments": [],
            }
        ]
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        db = DatabaseLoader().load(self.path)
        self.assertEqual(len(db.films), 2)

        film_a = db.get_film("Film A")
        self.assertIsNotNone(film_a)
        self.assertEqual(len(film_a.cast), 1)
        self.assertEqual(film_a.cast[0].name, "A1")

        self.assertEqual(len(film_a.comments), 1)
        self.assertEqual(film_a.comments[0].user, "u1")

        actor = next((a for a in db.actors if a.name == "A1"), None)
        self.assertIsNotNone(actor)
        self.assertGreaterEqual(len(actor.films), 2)


if __name__ == "__main__":
    unittest.main()
