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
        print("3: Rate a film in your watchlist")
        print("4: Show popular films")
        print("5: View your watch list")
        print("6: View all films in database")
        print("7: Get films based on age rating")
        print("8: Rate a film in your watchlist")
        print("9: Exit")
        print("\n")
        
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
            rate_film_in_watchlist(user)
        elif quest == 4:
            database.popular_films()
        elif quest == 5:
            user.display_watchlist()
            print()
        elif quest == 6:
            all_films=database.get_all_films()
            if not all_films:
                print("Database empty")
            else:
                print("\nAll films in the database:")
                for i, film in enumerate(all_films,1):
                    print(f"{i}.{film.name}")
            print()
        elif quest == 7:
            user_age = input("Please enter the minimum age rating you want the film to be: ")
            age_filtered_films = database.get_age_filtered_films(user_age)

            if not age_filtered_films:
                print("No films match that age rating.")
            else:
                print("\nAll age appropriate films in the database:")
                for i, film in enumerate(age_filtered_films, 1):
                    print(f"{i}. {film.name}")
                    
        elif quest == 8:
            rate_film_in_watchlist(user)

        elif quest == 9:
            break
        export.upload(database,"films.json")

def rate_film_in_watchlist(user):
    user_watchlist = user.get_watch_list()

        

def rate_film_in_watchlist(user):
    user_watchlist = user.get_watch_list()

    if len(user_watchlist) < 1:
        print("Your watch list is empty! Please add some films to your watch list.")
        return

    while True:
        print("Your watchlist ratings: ")
        for idx, film in enumerate(user.get_watch_list()):
            film_rating = user.get_rating(film.name)
            rating_str = f"{film_rating}/10" if film_rating != None else "No Rating"
            print(f"{idx+1}: {film.name} ({rating_str})")

        print()

        user_input = input("Please select a film to rate (write q to quit): ").strip().lower()

        if user_input == 'q':
            break

        try:
            list_idx = int(user_input) - 1
            if list_idx < 0 or list_idx >= len(user_watchlist):
                print("Unknown entry in watchlist")
                continue
        except ValueError:
            print("Unknown entry in watchlist")
            continue

        selected_film = user_watchlist[list_idx]
        print(f"Selected '{selected_film.name}'")

        while True:
            user_rating_input = input("Rate this film (0-10): ")

            try:
                user_rating = float(user_rating_input)
                user.add_rating(selected_film.name, user_rating)
                selected_film.add_ratings(user_rating)
                break
            except ValueError:
                print("Invalid value. Please try again.")
            except IndexError:
                print("Value not in range. Please try again.")

        print("Film rating applied.")

        selected_film = user_watchlist[list_idx]
        print(f"Selected '{selected_film.name}'")

        while True:
            user_rating_input = input("Rate this film (0-10): ")

            try:
                user_rating = float(user_rating_input)
                user.add_rating(selected_film.name, user_rating)
                break
            except ValueError:
                print("Invalid value. Please try again.")
            except IndexError:
                print("Value not in range. Please try again.")

        print("Film rating applied.")

if __name__ == "__main__":
    main()
