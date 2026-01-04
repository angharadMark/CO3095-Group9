import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import Mock
from database.database_loader import DatabaseLoader
from database.database_writer import DatabaseWriter
from database.database import Database
from object.film import Film
from object.actor import Actor


class TestDatabaseLoader(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.loader = DatabaseLoader()
        self.writer = DatabaseWriter()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    # Test Case 1:
    def test_case_1_invalid_json(self):
        invalid_json_file = os.path.join(self.test_dir, "invalid.json")
        with open(invalid_json_file, 'w') as f:
            f.write("{invalid json content")

        with self.assertRaises(json.JSONDecodeError):
            self.loader.load(invalid_json_file)

    # Test Case 2:
    @unittest.skipIf(os.name == 'nt', "Permission test not reliable on Windows")
    def test_case_2_no_permission(self):
        read_only_file = os.path.join(self.test_dir, "readonly.json")

        with open(read_only_file, 'w') as f:
            json.dump([], f)
        os.chmod(read_only_file, 0o444)

        database = Database()

        with self.assertRaises(PermissionError):
            self.writer.upload(database, read_only_file)

    # Test Case 3:
    def test_case_3_valid_json_has_films_exact_name(self):
        json_file = os.path.join(self.test_dir, "films.json")
        data = [
            {
                "name": "Test Film",
                "director": "Director A",
                "producer": "Producer A",
                "year": 2020,
                "genre": ["Action"],
                "ratings": [8, 9],
                "cast": [{"actor": "Actor X", "role": "Hero"}],
                "comments": [],
                "age_rating": "PG-13",
                "description": "A test film"
            }
        ]
        with open(json_file, 'w') as f:
            json.dump(data, f)

        database = self.loader.load(json_file)
        self.assertGreater(len(database.films), 0)

        output_file = os.path.join(self.test_dir, "output.json")
        self.writer.upload(database, output_file)
        self.assertTrue(os.path.exists(output_file))

        result = database.search_actor("Actor X")
        self.assertNotEqual(result, False)

    # Test Case 4:
    def test_case_4_valid_json_has_films_fuzzy_match(self):
        json_file = os.path.join(self.test_dir, "films.json")
        data = [
            {
                "name": "Test Film",
                "director": "Director A",
                "producer": "Producer A",
                "year": 2020,
                "genre": ["Action"],
                "ratings": [8],
                "cast": [{"actor": "Johnny Depp", "role": "Hero"}],
                "comments": [],
                "age_rating": "PG-13",
                "description": "A test film"
            }
        ]
        with open(json_file, 'w') as f:
            json.dump(data, f)

        database = self.loader.load(json_file)
        result = database.search_actor("John")
        self.assertNotEqual(result, False)

    # Test Case 5:
    def test_case_5_valid_json_has_films_no_match(self):
        json_file = os.path.join(self.test_dir, "films.json")
        data = [
            {
                "name": "Test Film",
                "director": "Director A",
                "producer": "Producer A",
                "year": 2020,
                "genre": ["Action"],
                "ratings": [8],
                "cast": [{"actor": "Actor X", "role": "Hero"}],
                "comments": [],
                "age_rating": "PG-13",
                "description": "A test film"
            }
        ]
        with open(json_file, 'w') as f:
            json.dump(data, f)

        database = self.loader.load(json_file)
        result = database.search_actor("ZZZNonExistent", threshold=90)
        self.assertEqual(result, False)

    # Test Cases 6-8:
    def test_case_6_8_valid_json_empty_database(self):
        json_file = os.path.join(self.test_dir, "empty.json")
        with open(json_file, 'w') as f:
            json.dump([], f)

        database = self.loader.load(json_file)
        self.assertEqual(len(database.films), 0)

        output_file = os.path.join(self.test_dir, "output.json")
        self.writer.upload(database, output_file)
        self.assertTrue(os.path.exists(output_file))

        # All searches return False on empty database
        self.assertEqual(database.search_actor("Actor X"), False)
        self.assertEqual(database.search_actor("Actor"), False)
        self.assertEqual(database.search_actor("NonExistent"), False)

    # Test Case 9:
    def test_case_9_empty_json_file(self):
        json_file = os.path.join(self.test_dir, "empty.json")
        with open(json_file, 'w') as f:
            f.write("")

        with self.assertRaises(json.JSONDecodeError):
            self.loader.load(json_file)

    # Test Cases 15-20:
    def test_case_15_20_file_not_found(self):
        non_existent = os.path.join(self.test_dir, "nonexistent.json")

        with self.assertRaises(FileNotFoundError):
            self.loader.load(non_existent)


class TestDatabaseWriter(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.writer = DatabaseWriter()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_write_empty_database(self):
        database = Database()
        output_file = os.path.join(self.test_dir, "empty_output.json")

        self.writer.upload(database, output_file)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            data = json.load(f)
        self.assertEqual(data, [])

    def test_write_database_with_films(self):
        database = Database()
        film = Film(name="Test Film", director="Test Director")
        database.add_films(film)

        output_file = os.path.join(self.test_dir, "films_output.json")
        self.writer.upload(database, output_file)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            data = json.load(f)
        self.assertGreater(len(data), 0)


if __name__ == "__main__":
    unittest.main()