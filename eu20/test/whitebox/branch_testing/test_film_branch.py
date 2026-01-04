"""
White-box Branch Testing for object.film.Film

Goal:
  - average_rating(): cover branch when ratings empty (return 0) and when ratings present
  - add_actor(): cover branch where duplicate actor causes early return
"""

import unittest
from object.film import Film
from object.actor import Actor


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
