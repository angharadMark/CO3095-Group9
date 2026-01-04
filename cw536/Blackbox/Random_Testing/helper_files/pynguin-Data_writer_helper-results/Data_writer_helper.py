"""
Database Writer helper class for Pynguin testing
Includes all necessary classes without external dependencies
"""

import json


class DummyFilm:
    """Helper Film class"""

    def __init__(self, name, director=None, producer=None, year=None, genre=None, ratings=None, cast=None,
                 comments=None, age_rating=None, description=None):
        self.name = name
        self.director = director
        self.producer = producer
        self.year = year
        self.genre = genre if genre is not None else []
        self.ratings = ratings if ratings is not None else []
        self.cast = cast if cast is not None else []
        self.comments = comments if comments is not None else []
        self.age_rating = age_rating
        self.description = description

    def to_dict(self):
        """Convert film to dictionary"""
        return {
            "name": self.name,
            "director": self.director,
            "producer": self.producer,
            "year": self.year,
            "genre": self.genre,
            "ratings": self.ratings,
            "cast": [
                {"actor": actor.get("name", ""), "role": actor.get("role", "")}
                for actor in self.cast
            ] if isinstance(self.cast, list) else [],
            "comments": [
                {"user": comment.get("user", ""), "message": comment.get("message", "")}
                for comment in self.comments
            ] if isinstance(self.comments, list) else [],
            "age_rating": self.age_rating,
            "description": self.description
        }


class DummyDatabase:
    """Helper Database class"""

    def __init__(self):
        self.films = []
        self.actors = []
        self.users = []

    def add_films(self, film):
        """Add a film to the database"""
        self.films.append(film)
        return True

    def get_all_films(self):
        """Get all films"""
        return self.films

    def get_film_count(self):
        """Get number of films in database"""
        return len(self.films)

    def clear_films(self):
        """Clear all films from database"""
        self.films = []
        return True


class DatabaseWriter:
    """Database writer class"""

    def upload(self, database, filename):
        """Write database to JSON file"""
        data = []
        for film in database.films:
            data.append(film.to_dict())

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        return True

    def upload_with_validation(self, database, filename):
        """Write database to JSON file with validation"""
        if not database:
            raise ValueError("Database cannot be None")

        if not filename:
            raise ValueError("Filename cannot be empty")

        if not isinstance(database.films, list):
            raise TypeError("Database.films must be a list")

        data = []
        for film in database.films:
            if not hasattr(film, 'to_dict'):
                raise AttributeError("Film must have to_dict method")
            data.append(film.to_dict())

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        return len(data)

    def get_file_size(self, filename):
        """Get size of written file"""
        import os
        if os.path.exists(filename):
            return os.path.getsize(filename)
        return 0

    def verify_json(self, filename):
        """Verify that written file is valid JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                json.load(file)
            return True
        except (json.JSONDecodeError, FileNotFoundError):
            return False