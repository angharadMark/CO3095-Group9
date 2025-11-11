class Database:
    def __init__(self):
        self.films=[]

    def add_films(self, film):
        self.films.append(film)

    def get_film(self, name):
        for films in self.films:
            if films.name == name:
                return films
            else:
                return False
            
    def get_all_films(self):
        return self.films

