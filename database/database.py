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
    
    def get_age_filtered_films(self, user_age):
        try:
            user_age = int(user_age)
        except ValueError:
            print("Invalid age entered.")
            return []

        filtered = []

        for film in self.films:
            try:
                film_age = int(film.age_rating)
            except (ValueError, TypeError):
                continue

            if film_age >= user_age:
                filtered.append(film)

        return filtered





