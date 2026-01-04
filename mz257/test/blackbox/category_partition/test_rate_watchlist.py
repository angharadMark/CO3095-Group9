import unittest

from object.user import User

class RateWatchlistTest(unittest.TestCase):
    def setUp(self):
        self.user = User({"id": None, "username": None})

    def test_negative_rating(self):
        self.assertRaises(IndexError, self.user.add_rating, "A Movie", -10)

    def test_valid_rating(self):
        rating_num = 7

        self.user.add_rating("A Movie", rating_num)

        self.assertEqual(self.user.get_rating("A Movie"), rating_num)

    def test_too_high_rating(self):
        self.assertRaises(IndexError, self.user.add_rating, "A Movie", 100)

    def test_retrieve_invalid_rating(self):
        self.assertEqual(self.user.get_rating("A Movie"), None)
