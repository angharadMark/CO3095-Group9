import unittest
from object.film import Film
from object.actor import Actor

class TestFilm(unittest.TestCase):

    def setUp(self):
        self.actor = Actor("John Doe", "Lead")
        self.film = Film(
            name="My Movie",
            cast=[self.actor],
            producer="Producer A",
            director="Director B",
            genre=["Action"],
            age_rating="PG-13",
            year=2020
        )

    # Test getters
    def test_getters(self):
        self.assertEqual(self.film.get_name(), "My Movie")
        self.assertEqual(self.film.get_producer(), "Producer A")
        self.assertEqual(self.film.get_director(), "Director B")
        self.assertEqual(self.film.get_year(), 2020)
        self.assertEqual(self.film.get_age_rating(), "PG-13")
        self.assertEqual(self.film.get_genre(), ["Action"])
        self.assertEqual(self.film.get_cast(), [self.actor])

    # Test setters
    def test_setters(self):
        self.film.set_name("New Name")
        self.assertEqual(self.film.get_name(), "New Name")
        self.film.set_producer("New Producer")
        self.assertEqual(self.film.get_producer(), "New Producer")
        self.film.set_director("New Director")
        self.assertEqual(self.film.get_director(), "New Director")
        self.film.set_year(1999)
        self.assertEqual(self.film.get_year(), 1999)
        self.film.set_age_rating("R")
        self.assertEqual(self.film.get_age_rating(), "R")
        self.film.set_genre(["Comedy"])
        self.assertEqual(self.film.get_genre(), ["Comedy"])
        new_actor = Actor("Jane Doe", "Supporting")
        self.film.set_cast([new_actor])
        self.assertEqual(self.film.get_cast(), [new_actor])


if __name__ == "__main__":
    unittest.main()
