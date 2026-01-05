import unittest
from object.film import Film
from object.actor import Actor

'''
Branch testing for Film object
3 tests
Branches:
average rating when ratings list is empty → returns 0
average rating when ratings exist → returns computed mean
add_actor duplicate actor → ignored (dedupe branch)
'''

class TestFilmBranch(unittest.TestCase):
    def test_average_rating_empty_returns_zero(self):
        f = Film(name="X")
        self.assertEqual(f.average_rating(), 0)

    def test_average_rating_non_empty_returns_average(self):
        f = Film(name="X", ratings=[4, 5, 3])
        self.assertEqual(f.average_rating(), 4.0)

    def test_add_actor_duplicate_is_ignored(self):
        f = Film(name="X")
        f.add_actor(Actor(name="A", role="Lead"))
        f.add_actor(Actor(name="A", role="Lead"))  # duplicate
        self.assertEqual(len(f.cast), 1)


if __name__ == "__main__":
    unittest.main()
