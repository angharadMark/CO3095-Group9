import json
from object.film import Film
from database.database import Database
from object.actor import Actor

class DatabaseLoader:
    def load(self, fileName):
        database= Database()
        try:
            with open(fileName, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for f in data:
                cast_list=[]
                for actor in f.get('cast',[]):
                    cast_list.append(Actor(
                        name = actor.get('name'),
                        role = actor.get('role')
                    ))
                film = Film(
                    name = f.get('name'),
                    cast= cast_list,
                    producer= f.get('producer'),
                    director= f.get('director'),
                    genre= f.get('genre',[]),
                    age_rating= f.get('age_rating'),
                    year = f.get('year'),
                    ratings = f.get('ratings', [])
                    description=f.get('description')
                )
                database.add_films(film)
        except FileNotFoundError:
            pass
        return database
    

