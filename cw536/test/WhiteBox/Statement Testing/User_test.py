import unittest

class Film:
    def __init__(self, name, description="", cast=None, comments=None):
        self.name = name
        self.description = description
        self.cast = cast if cast else []
        self.comments = comments if comments else []

class Comment:
    def __init__(self, message):
        self.message = message
        self.user = "tester"
    def display_comment(self):
        print(f"{self.user}: {self.message}")

from object.user import User

class TestUserStatement(unittest.TestCase):

    def setUp(self):
        self.record = {
            "id": 1,
            "username": "testuser",
            "watchlist": [],
            "films_added": 2,
            "ratings": {},
            "comments": []
        }
        self.user = User(self.record)

    def test_init_and_to_dict(self):
        data = self.user.to_dict()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["watchlist"], [])
        self.assertEqual(data["films_added"], 2)
        self.assertEqual(data["ratings"], {})
        self.assertEqual(data["comments"], [])

    def test_add_to_watchList(self):
        film1 = Film("Film A")
        film2 = Film("Film B")
        self.user.add_to_watchList(film1)
        self.assertIn(film1, self.user.watchList)
        self.user.add_to_watchList(film1)
        self.assertEqual(len(self.user.watchList), 1)
        self.user.add_to_watchList(film2)
        self.assertIn(film2, self.user.watchList)

    def test_get_watch_list(self):
        film1 = Film("Film A")
        self.user.add_to_watchList(film1)
        self.assertEqual(self.user.get_watch_list(), [film1])

    def test_display_watchlist_empty(self):
        import io, sys
        captured = io.StringIO()
        sys.stdout = captured
        self.user.display_watchlist()
        sys.stdout = sys.__stdout__
        self.assertIn("currently empty", captured.getvalue())

    def test_display_watchlist_nonempty(self):
        film = Film("Film A", "Desc", cast=[], comments=[Comment("Nice!")])
        self.user.add_to_watchList(film)
        import io, sys
        captured = io.StringIO()
        sys.stdout = captured
        self.user.display_watchlist()
        sys.stdout = sys.__stdout__
        self.assertIn("Film A", captured.getvalue())
        self.assertIn("Desc", captured.getvalue())
        self.assertIn("Nice!", captured.getvalue())

    def test_add_comment(self):
        film = Film("Film A")
        comment = Comment("Great!")
        self.user.add_comment(film, comment)
        self.assertEqual(len(self.user.comments), 1)
        self.assertEqual(self.user.comments[0]["film"], "Film A")
        self.assertEqual(self.user.comments[0]["comment"], comment)

if __name__ == "__main__":
    unittest.main()