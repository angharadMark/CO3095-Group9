import unittest
from object.actor import Actor
from object.film import Film
'''
Technique: White-Box Branch Testing (Lab 9 Task 2)
Tool used: Unittest & Coverage.py
Description: Hits all True/False paths for conditional logic in Actor/Film objects.
'''

class TestObjectBranches(unittest.TestCase):
    def test_average_rating_branches(self):
        f = Film()
        # Branch 1: if not self.ratings (TRUE)
        self.assertEqual(f.average_rating(), 0)

        # Branch 2: if not self.ratings (FALSE)
        f.ratings = [10, 5, 7]
        self.assertEqual(f.average_rating(), 7.33)

    def test_add_actor_branches(self):
        f = Film()
        a = Actor("Cillian Murphy", "Oppenheimer")

        # Branch 1: Actor not in cast (Add new)
        f.add_actor(a)
        self.assertEqual(len(f.cast), 1)

        # Branch 2: Actor already in cast (Duplicate check)
        f.add_actor(a)
        self.assertEqual(len(f.cast), 1)  # Should not increase

    def test_add_film_branches(self):
        a = Actor("Tom Hardy")
        f = Film("Mad Max")

        # Branch 1: Film not in list
        a.add_film(f)
        self.assertEqual(len(a.films), 1)

        # Branch 2: Film already in list
        a.add_film(f)
        self.assertEqual(len(a.films), 1)


if __name__ == '__main__':
    unittest.main()