import unittest
from object.film import Film
from object.comment import Comment
from object.actor import Actor  # If you have this class; if not, tell me and I'll adjust.


class TestFilmWhiteBox(unittest.TestCase):
    def test_to_dict_with_no_cast_no_comments(self):
        f = Film(name="A", year="2020")
        d = f.to_dict()
        self.assertEqual(d["name"], "A")
        self.assertEqual(str(d["year"]), "2020")
        self.assertIn("cast", d)
        self.assertIn("comments", d)

    def test_add_comment_and_to_dict(self):
        f = Film(name="A", year="2020")
        f.add_comment(Comment("hello", user="emre"))
        d = f.to_dict()
        self.assertEqual(d["comments"][0]["user"], "emre")
        self.assertEqual(d["comments"][0]["message"], "hello")

    def test_add_rating_updates_ratings(self):
        f = Film(name="A", year="2020")
        f.add_ratings(5)
        f.add_ratings(1)
        self.assertIn(5, f.ratings)
        self.assertIn(1, f.ratings)

    def test_cast_to_dict_structure(self):
        f = Film(name="A", year="2020")
        f.cast = [Actor("Actor 1", "Lead")]
        d = f.to_dict()
        self.assertEqual(d["cast"][0]["actor"], "Actor 1")
        self.assertEqual(d["cast"][0]["role"], "Lead")


if __name__ == "__main__":
    unittest.main()
