import json
from object.film import Film
from database.database import Database
from object.actor import Actor
from object.comment import Comment

class DatabaseLoader:
    def load(self, fileName):
        database=Database()
        actors_by_name = {}
        try:
            with open(fileName, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for f in data:
                cast_list = []
                comments = []

                film = Film(
                    name = f.get('name'),
                    cast=[],
                    producer= f.get('producer'),
                    director= f.get('director'),
                    genre= f.get('genre',[]),
                    age_rating= f.get('age_rating'),
                    year = f.get('year'),
                    ratings = f.get('ratings', []),
                    description=f.get('description'),
                    comments=[]
                )

                for actor_data in f.get('cast',[]):
                    actor_name = actor_data.get('name')

                    if actor_name not in actors_by_name:
                        actor = (Actor(
                            name = actor_name,
                            role = actor_data.get('role')) 
                        )
                        actors_by_name[actor_name] = actor
                        database.add_actor(actor)
                    else:
                        actor = actors_by_name[actor_name]
                    
                    actor.films.append(film)
                    cast_list.append(actor)
                
                for comment in f.get('comments',[]):
                    comments.append(Comment(
                        message = comment.get('comment'),
                        user = comment.get('user')
                    ))
                
                film.cast = cast_list
                film.comments = comments
                database.add_films(film)
                
        except FileNotFoundError:
            pass
        return database
    

