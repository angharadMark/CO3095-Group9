import unittest
import json

from logic.filter import *
from object.filter_type import *

class BasicFilmWithCast:
    def __init__(self, cast):
        self.cast = cast

class BasicFilmWithGenre:
    def __init__(self, genre):
        self.genre = genre

class BasicActor:
    def __init__(self, name):
        self.name = name

class BasicFilterTest(unittest.TestCase):
    def test_cast_filter(self):
        filters = [QueryFilter(FilterType.CAST, "Actor Name")]

        films = [
            BasicFilmWithCast([
                BasicActor("Actor Name"),
                BasicActor("Second Actor")
            ]),
            BasicFilmWithCast([
                BasicActor("Second Actor")
            ])
        ]

        filtered = filter_films(filters, films)

        self.assertEqual(len(filtered), 1)

    def test_genre_filter(self):
        filters = [QueryFilter(FilterType.GENRE, "Action")]

        films = [
            BasicFilmWithGenre("action"),
            BasicFilmWithGenre("comedy")
        ]

        filtered = filter_films(filters, films)

        self.assertEqual(len(filtered), 1)

if __name__ == '__main__':
    unittest.main()
