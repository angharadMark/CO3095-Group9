class Actor:
    def __init__(self, name=None, role=None, films=None):
        self.name = name
        self.role = role
        self.films = films if films is not None else []

    def set_name(self):
        self.name = input("input the name of the actor")
    
    def set_role(self):
        self.role = input("input the role of the actor")

    def display_actor(self):
        print("Name:",self.name)
        print("Role:",self.role)
    
    def add_film(self, film):
        if film not in self.films:
            self.films.append(film)
    
    def filmography(self):
        print("As seen in: ")
        for film in self.films:
            print(film.name)
