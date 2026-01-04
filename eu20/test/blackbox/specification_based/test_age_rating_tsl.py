import unittest

from database.database import Database
from object.film import Film


class TestAgeRatingTSL(unittest.TestCase):


    def setUp(self):
        self.db = Database()

        self.f12 = Film(name="Film12", age_rating="12")
        self.f15 = Film(name="Film15", age_rating="15")
        self.f18 = Film(name="Film18", age_rating="18")

        self.fNA = Film(name="FilmNA", age_rating="N/A")
        self.fNone = Film(name="FilmNone", age_rating=None)

        self.db.add_films(self.f12)
        self.db.add_films(self.f15)
        self.db.add_films(self.f18)
        self.db.add_films(self.fNA)
        self.db.add_films(self.fNone)

   

    def test_age_empty(self):
        result = self.db.get_age_filtered_films("")
        self.assertEqual(result, [])

    def test_age_spaces_only(self):
        result = self.db.get_age_filtered_films("   ")
        self.assertEqual(result, [])

    def test_age_non_numeric(self):
        result = self.db.get_age_filtered_films("abc")
        self.assertEqual(result, [])

    def test_age_negative(self):
        result = self.db.get_age_filtered_films("-1")
        names = [f.name for f in result]
        self.assertEqual(names, ["Film12", "Film15", "Film18"])

    def test_age_valid_low(self):
        result = self.db.get_age_filtered_films("12")
        names = [f.name for f in result]
        self.assertEqual(names, ["Film12", "Film15", "Film18"])

    def test_age_valid_mid(self):
        result = self.db.get_age_filtered_films("15")
        names = [f.name for f in result]
        self.assertEqual(names, ["Film15", "Film18"])

    def test_age_valid_high(self):
        result = self.db.get_age_filtered_films("18")
        names = [f.name for f in result]
        self.assertEqual(names, ["Film18"])

    def test_age_above_all(self):
        result = self.db.get_age_filtered_films("21")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
