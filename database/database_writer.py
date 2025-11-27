import json

class DatabaseWriter:
    def upload(self, database, filename):
        cast_list=[]
        for actor in film.cast:
            cast_list.append({'name': actor.name, 'role': actor.role})
        data=[]
        for film in database.films:
            data.append({
                'name': film.name,
                'cast': cast_list,
                'producer': film.producer,
                'director': film.director,
                'genre': film.genre,
                'age_rating': film.age_rating,
                'year': film.year
            })
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
