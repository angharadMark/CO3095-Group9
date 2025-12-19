import json

class DatabaseWriter:
    def upload(self, database, filename):
        data=[]
        for film in database.films:
            cast_list=[]
            comments=[]
            for actor in film.cast:
                cast_list.append({'name': actor.name, 'role': actor.role})
            for comment in film.comments:
                comments.append({'user': comment.user, 'comment': comment.message})
            data.append({
                'name': film.name,
                'cast': cast_list,
                'producer': film.producer,
                'director': film.director,
                'genre': film.genre,
                'age_rating': film.age_rating,
                'year': film.year,
                'ratings': film.ratings,
                'description' :film.description,
                'comments':comments
            })
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
