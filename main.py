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
        print("3: Rate a film in your watchlist")

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
            rate_film_in_watchlist(user)

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
                break
            except ValueError:
                print("Invalid value. Please try again.")
            except IndexError:
                print("Value not in range. Please try again.")

        print("Film rating applied.")

if __name__ == "__main__":
    main()
