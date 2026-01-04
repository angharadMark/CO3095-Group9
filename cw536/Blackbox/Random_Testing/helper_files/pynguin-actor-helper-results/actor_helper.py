"""
Pynguin-friendly version of Actor class
Removes interactive input() calls for automated test generation
"""

class DummyFilm:
    def __init__(self, name):
        self.name = name

class Actor:
    def __init__(self, name=None, role=None, films=None):
        self.name = name
        self.role = role
        self.films = films if films is not None else []

    def set_name(self, name):
        """Set actor name programmatically"""
        self.name = name

    def set_role(self, role):
        """Set actor role programmatically"""
        self.role = role

    def display_actor(self):
        """Display actor information"""
        print("Name:", self.name)
        print("Role:", self.role)

    def add_film(self, film):
        """Add a film to the actor's filmography"""
        if film not in self.films:
            self.films.append(film)
            return True
        return False

    def filmography(self):
        """Display all films the actor has been in"""
        if not self.films:
            print("No films in filmography")
            return

        print("As seen in: ")
        for film in self.films:
            print(film.name)

    def get_film_count(self):
        """Get number of films in filmography"""
        return len(self.films)

    def remove_film(self, film):
        """Remove a film from filmography"""
        if film in self.films:
            self.films.remove(film)
            return True
        return False

    def has_film(self, film):
        """Check if actor has been in a specific film"""
        return film in self.films