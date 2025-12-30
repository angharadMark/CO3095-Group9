import json

class DatabaseWriter:
    def upload(self, database, filename):
        data=[]
        for film in database.films:
            data.append(film.to_dict())
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
    
