import random
from database.database_loader import DatabaseLoader

def getMovieOfTheDay(fileName="films.json"):
    loader=DatabaseLoader()
    database=loader.load(fileName)

    all_films=database.get_all_films()
    if not all_films:
        return None

    movie=random.choice(all_films)
    return movie