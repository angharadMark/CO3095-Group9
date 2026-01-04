import json
from object.film import Film
from database.database import Database
from object.actor import Actor
from object.comment import Comment

class DatabaseLoader:
    def load(self, fileName):
        database = Database()
        actors_by_name = {}

        try:
            with open(fileName, 'r', encoding='utf-8') as file:
                data = json.load(file)

            for f in data:
                cast_list = []
                comments = []

                # Create Film object
                film = Film(
                    name=f.get('name'),
                    cast=[],
                    producer=f.get('producer'),
                    director=f.get('director'),
                    genre=f.get('genre', []),
                    age_rating=f.get('age_rating'),
                    year=f.get('year'),
                    ratings=f.get('ratings', []),
                    description=f.get('description'),
                    comments=[]
                )
                seen_cast = set()
                for actor_data in f.get("cast", []):
                    if isinstance(actor_data, dict):
                        actor_name = actor_data.get("actor")
                        role = actor_data.get("role")
                    else:
                        continue

                    if not actor_name or not role:
                        continue

                    key = (actor_name, role)
                    if key in seen_cast:
                        continue
                    seen_cast.add(key)

                    if actor_name not in actors_by_name:
                        actors_by_name[actor_name] = Actor(name=actor_name, role=role)

                    actor = actors_by_name[actor_name]
                    actor.add_film(film)
                    film.add_actor(actor)
                    database.add_actor(actor)

                for c in f.get("comments", []):
                    if isinstance(c, dict) and "user" in c and "message" in c:
                        comments.append(Comment(user=c["user"], message=c["message"]))

                film.comments = comments
                database.add_films(film)


        except (FileNotFoundError, json.JSONDecodeError, PermissionError):

            return database

        return database
        
        return database
    

