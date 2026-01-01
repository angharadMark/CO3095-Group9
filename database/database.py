from object.film import Film
from object.actor import Actor
from fuzzywuzzy import fuzz
import re

def normalise(text):
    return re.sub(r'\s+', ' ', text.lower().strip())

class Database:
    def __init__(self):
        self.films=[]
        self.actors=[]

    def add_films(self, film):
        self.films.append(film)
    
    def add_actor(self,actor):
        self.actors.append(actor)

    def get_film(self, name):
        target = name.strip().lower()
        for film in self.films:
            if film.name.strip().lower() == target:
                return film
            
        return False
    
    def popular_films(self):
        popular = []
        for film in self.films:
            if film.average_rating() > 7:
                popular.append(film)

        while True:
            if len(popular) == 0:
                print("No popular films")
                break
            else:
                for i in range(len(popular)):
                    print(i+1,popular[i].name)
            
            print("\n")
            print("1: View a film in detail")
            print("2: Exit")

            user_inp = int(input("What would you like to do? : "))

            if user_inp == 1:
                detail = int(input("Pick the number of the film: "))
                film = popular[detail-1]
                film.display_film()

                print("\n")
                return False
            else:
                break
            
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
    
    def search_actor(self,target, threshold=60):
        target = normalise(target)
        result=[]

        for actor in self.actors:
            name = normalise(actor.name)

            score = max(
                fuzz.partial_ratio(target, name),
                fuzz.partial_ratio(target, " ".join(name.split()[::1]))
            )

            if score >= threshold:
                result.append(actor)
        
        return result






