from object.film import Film

class Database:
    def __init__(self):
        self.films=[]

    def add_films(self, film):
        self.films.append(film)

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

        

