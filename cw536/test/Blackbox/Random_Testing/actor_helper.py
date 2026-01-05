class DummyFilm:
    def __init__(self, name):
        self.name = name

class Actor:
    def __init__(self, name=None, role=None, films=None):
        self.name = name
        self.role = role
        self.films = films if films is not None else []

    def set_name(self, name):
        self.name = name

    def set_role(self, role):
        self.role = role

    def display_actor(self):
        print("Name:", self.name)
        print("Role:", self.role)

    def add_film(self, film):
        if film not in self.films:
            self.films.append(film)
            return True
        return False

    def filmography(self):
        if not self.films:
            print("No films in filmography")
            return

        print("As seen in: ")
        for film in self.films:
            print(film.name)

    def get_film_count(self):
        return len(self.films)

    def remove_film(self, film):
        if film in self.films:
            self.films.remove(film)
            return True
        return False

    def has_film(self, film):
        return film in self.films