import unittest
import json
from object.film import Film
from object.actor import Actor
from logic.movie_recommendations import similarity_results

# JSON film data (same as before)
film_json = [
    {
        "name": "Inception",
        "director": "Christopher Nolan",
        "producer": "Emma Thomas",
        "year": 2010,
        "genre": ["Sci-Fi", "Thriller"],
        "cast": [
            {"actor": "Leonardo DiCaprio", "role": "Cobb"},
            {"actor": "Joseph Gordon-Levitt", "role": "Arthur"},
            {"actor": "Elliot Page", "role": "Ariadne"},
            {"actor": "Tom Hardy", "role": "Eames"}
        ]
    },
    {
        "name": "The Matrix",
        "director": "Lana Wachowski",
        "producer": "Joel Silver",
        "year": 1999,
        "genre": ["Sci-Fi", "Action"],
        "cast": [
            {"actor": "Keanu Reeves", "role": "Neo"},
            {"actor": "Carrie-Anne Moss", "role": "Trinity"},
            {"actor": "Laurence Fishburne", "role": "Morpheus"}
        ]
    },
    {
        "name": "Titanic",
        "director": "James Cameron",
        "producer": "James Cameron",
        "year": 1997,
        "genre": ["Romance", "Drama"],
        "cast": [
            {"actor": "Leonardo DiCaprio", "role": "Jack"},
            {"actor": "Kate Winslet", "role": "Rose"},
            {"actor": "Billy Zane", "role": "Cal"}
        ]
    }
]

def make_film(film_data):
    f = Film()
    f.name = film_data["name"]
    f.genres = film_data.get("genre", [])
    f.cast = [Actor(a["actor"]) for a in film_data.get("cast", [])]
    f.director = film_data.get("director")
    f.producer = film_data.get("producer")
    return f

class TestSimilarityResults(unittest.TestCase):

    def setUp(self):
        # Convert JSON to Film objects
        self.films = [make_film(f) for f in film_json]

    def test_identical_films(self):
        f1 = self.films[0]
        f2 = self.films[0]
        score = similarity_results(f1, f2)
        self.assertGreater(score, 0, "Identical films should have positive similarity")

    def test_partial_overlap(self):
        f1 = self.films[0]  # Inception
        f2 = self.films[1]  # The Matrix
        score = similarity_results(f1, f2)
        self.assertEqual(score, 2, "Only genres overlap by 1 ('Sci-Fi') → 2 points")

    def test_no_overlap(self):
        f1 = self.films[1]  # The Matrix
        f2 = self.films[2]  # Titanic
        score = similarity_results(f1, f2)
        self.assertEqual(score, 0, "No genre, actor, director, or producer overlap")

    def test_actor_overlap(self):
        f1 = self.films[0]  # Inception
        f2 = self.films[2]  # Titanic
        score = similarity_results(f1, f2)
        self.assertEqual(score, 1, "Leonardo DiCaprio in both → 1 point")

if __name__ == "__main__":
    unittest.main()