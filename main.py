from object.user import User
from database.database import Database
from database.database_loader import DatabaseLoader

def main():
    user = User("test")
    imports = DatabaseLoader()
    database = imports.load("films.json")
    while True:
        print("Welcome to the film reccomendation system!")
        print("1: Add a film to the database")
        print("2: Add a film to your watch list")
        print("3: View your watch list")
        print("4: View all films in database")
        print("5: Get films based on age rating")
        print()




        quest = int(input("Please select an option: "))

        if quest == 1:
            pass
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
            user.add_to_watchList(result)
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
            user_age = input("Please enter the minimum age rating you want the film to be: ")
            age_filtered_films = database.get_age_filtered_films(user_age)

            if not age_filtered_films:
                print("No films match that age rating.")
            else:
                print("\nAll age appropriate films in the database:")
                for i, film in enumerate(age_filtered_films, 1):
                    print(f"{i}. {film.name}")




        else:
            print("Invalid option selected")





if __name__ == "__main__":
    main()