import unittest
from unittest.mock import patch
from object.actor import Actor
from object.film import Film
'''
Technique: White-Box Statement Testing (Lab 9 Task 1)
Tool used: Unittest & Coverage.py
Objects tested: object/actor.py, object/film.py
Description: Exercises every statement in the Actor class and the core 
             data-handling methods of the Film class.
'''

class TestObjectStatements(unittest.TestCase):
    def test_actor_statements(self):
        # Test __init__ and display
        a1 = Actor("Christian Bale", "Batman")
        a1.display_actor()  # Clears print statements

        # Test filmography logic
        f1 = Film(name="The Dark Knight")
        a1.add_film(f1)
        a1.filmography()  # Executes the loop and print
        self.assertIn(f1, a1.films)

    def test_film_statements(self):
        actor = Actor("Leonardo DiCaprio", "Cobb")
        film = Film(name="Inception", year=2010)

        # Test setters and getters (Statement Coverage)
        film.set_name("Inception Redux")
        film.set_producer("Emma Thomas")
        film.set_director("Chris Nolan")
        film.set_age_rating("12")
        film.set_genre(["Sci-Fi"])

        self.assertEqual(film.get_name(), "Inception Redux")
        self.assertEqual(film.get_producer(), "Emma Thomas")

        # Test data conversion
        film.add_actor(actor)
        d = film.to_dict()
        self.assertEqual(d["name"], "Inception Redux")


if __name__ == '__main__':
    unittest.main()