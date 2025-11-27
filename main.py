from object.user import User
from database.database import Database
from database.database_loader import DatabaseLoader
from database.database_writer import DatabaseWriter
from object.film import Film

def main():
    user = User("test")
    imports = DatabaseLoader()
    database = imports.load("films.json")
    export = DatabaseWriter()
    while True:
        print("\n")
        print("Welcome to the film reccomendation system!")
        print("1: Add a film to the database")
        print("2: Add a film to your watch list")
        print("3: View your watch list")
        print("4: View all films in database")
        print("5: Exit")
        print()




        quest = int(input("Please select an option: "))

        if quest == 1:
            film = Film()
            if film.input_film() == False:
                del film
            else:
                database.add_films(film)

        elif quest == 2:
            film = input("Please input the film name you want to add: ")
            result = database.get_film(film)
            while result == False:
                print("Your film could not be found")
                choice = input("Would you like to try again y/n : ")
                if choice.lower() == "y":
                    film = input("Please input the film again: ")
                    result = database.get_film(film)
                else:
                    break
            result.display_film()
            correct_check = input("Is this the correct film? Y/N : ").strip()
            if correct_check.lower() == "n":
                print("Film not added")
                pass
            user.add_to_watchList(result)
            print("Film added to watchlist!")
        elif quest == 3:
            user.display_watchlist()
            print()
        elif quest == 4:
            all_films=database.get_all_films()
            if not all_films:
                print("Database empty")
            else:
                print("\nAll films in the database:")
                for i, film in enumerate(all_films,1):
                    print(f"{i}.{film.name}")
            print()
        elif quest == 5:
            break
        export.upload(database,"films.json")






if __name__ == "__main__":
    main()