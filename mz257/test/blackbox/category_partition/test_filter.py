import unittest
import json

from logic.filter import *

from object.film import Film
from object.filter_type import *

class BasicFilmWithCast(Film):
    def __init__(self, cast):
        self.cast = cast
        self.genre = ""

class BasicFilmWithGenre(Film):
    def __init__(self, genre):
        self.genre = genre
        self.cast = []

class BasicFilmCombined(Film):
    def __init__(self, genre, cast):
        self.genre = genre
        self.cast = cast

class BasicActor:
    def __init__(self, name):
        self.name = name

films_list_1 = [
    BasicFilmWithCast([
        BasicActor("Actor Name"),
        BasicActor("Second Actor")
    ]),
    BasicFilmWithCast([
        BasicActor("Second Actor")
    ])
]

films_list_2 = [
    BasicFilmWithGenre("action"),
    BasicFilmWithGenre("comedy")
]

films_list_3 = [
    BasicFilmCombined(cast = [
        BasicActor("Actor Name"),
        BasicActor("Second Actor")
    ], genre = "action"),
    BasicFilmCombined(cast = [
        BasicActor("Second Actor")
    ], genre = "comedy")
]

class BasicFilterTest(unittest.TestCase):
    def test_cast_filter_empty_list(self):
        filters = [QueryFilter(FilterType.CAST, "Actor Name")]

        filtered = filter_films(filters, [])

        self.assertEqual(len(filtered), 0)

    def test_cast_filter_no_match(self):
        filters = [QueryFilter(FilterType.CAST, "Another Actor Name")]

        filtered = filter_films(filters, films_list_1 + films_list_2)

        self.assertEqual(len(filtered), 0)

    def test_cast_filter_match(self):
        filters = [QueryFilter(FilterType.CAST, "Actor Name")]

        filtered = filter_films(filters, films_list_1)

        self.assertEqual(len(filtered), 1)

    def test_genre_filter_empty_list(self):
        filters = [QueryFilter(FilterType.GENRE, "Action")]

        filtered = filter_films(filters, [])

        self.assertEqual(len(filtered), 0)

    def test_genre_filter_no_match(self):
        filters = [QueryFilter(FilterType.GENRE, "Horror")]

        filtered = filter_films(filters, films_list_1 + films_list_2)

        self.assertEqual(len(filtered), 0)

    def test_genre_filter_match(self):
        filters = [QueryFilter(FilterType.GENRE, "Action")]

        filtered = filter_films(filters, films_list_2)

        self.assertEqual(len(filtered), 1)

    def test_no_filter_empty_list(self):
        filtered = filter_films([], [])
        self.assertEqual(len(filtered), 0)

    def test_no_filter(self):
        filtered = filter_films([], films_list_1)
        self.assertEqual(len(filtered), len(films_list_1))

    def test_both_filters_empty_list(self):
        filters = [QueryFilter(FilterType.CAST, "Actor Name"),
                   QueryFilter(FilterType.GENRE, "Action")]

        filtered = filter_films(filters, [])

        self.assertEqual(len(filtered), 0)

    def test_both_filters_no_match(self):
        filters = [QueryFilter(FilterType.CAST, "Another Actor Name"),
                   QueryFilter(FilterType.GENRE, "Horror")]

        filtered = filter_films(filters, films_list_3)

        self.assertEqual(len(filtered), 0)

    def test_both_filters_match(self):
        filters = [QueryFilter(FilterType.CAST, "Actor Name"),
                   QueryFilter(FilterType.GENRE, "Action")]

        filtered = filter_films(filters, films_list_3)

        self.assertEqual(len(filtered), 1)

if __name__ == '__main__':
    unittest.main()
