from object.user import User
from database.database import Database
from database.database_loader import DatabaseLoader
from database.database_writer import DatabaseWriter
from object.film import Film

from logic.filter import *
from object.filter_type import FilterType

def confirm_choice(dialog_message, validate_fun,
    repeat_message = None, reject_message = "Invalid input value"):
    if not repeat_message: repeat_message = dialog_message
    user_input = input(f"{dialog_message}: ")
    while not validate_fun(user_input):
        print(reject_message)
        choice = input("Would you like to try again y/n: ")
        if choice.lower() == "y":
            user_input = input(f"{repeat_message}: ")
        else:
            return None

    return user_input

def is_text_int(text):
    try:
        converted = int(text)
        return True
    except ValueError:
        return False

def filter_search_dialog(database, user):
    filters = []
    while True:
        if len(filters) > 0:
            print("Filters:")
            for (i, filter) in enumerate(filters):
                print(f"{i+1}: (filter {filter.type.name} by '{filter.content}')")
            print()

        print("Please choose:")
        print("1: Filter results by cast")
        print("2: Filter results by genre")
        print("3: Show results")
        print("4: Add results to watchlist")
        print("5: Remove filter by index")
        print("6: Clear filters")
        print("7: Exit this menu")
        print()
        user_input = int(input("Please select an option: "))

        if user_input == 1:
            filter_content = input("What cast member should the results be filtered by? ")
            filters.append(
                QueryFilter(FilterType.CAST, filter_content)
            )
        elif user_input == 2:
            filter_content = input("What genre should the results be filtered by? ")
            filters.append(
                QueryFilter(FilterType.GENRE, filter_content)
            )
        elif user_input == 3:
            results = filter_films(filters, database.get_all_films())
            if len(results) > 0:
                print("Found: ")
                for film in results:
                    print(film.name)
            else:
                print("No films found")
        elif user_input == 4:
            results = filter_films(filters, database.get_all_films())
            if len(results) == 0:
                print("No films found")
                continue

            for film in results:
                user.add_to_watchList(film)

            print(f"Added {len(results)} films to watchlist")
        elif user_input == 5:
            if len(filters) == 0: continue

            filter_index = confirm_choice("Enter the index of the filter to be removed",
                lambda choice: is_text_int(choice) 
                    and int(choice) > 0
                    and int(choice) <= len(filters)
            )

            if filter_index != None:
                filter_index = int(filter_index)
                del filters[filter_index - 1]
                print(f"Removed filter #{i}")


        elif user_input == 6:
            print("Filters cleared...")
            filters = []

        elif user_input == 7:
            return


def watchlist_dialog(database, user):
    while True:
        print("Select:")
        print("1: Add a film to your watchlist by name")
        print("2: Search for films to add to your watchlist")
        print("3: Remove a film from your watchlist")
        print("4: Exit this menu")
        print()
        user_input = int(input("Please select an option: "))

        if user_input == 1:
            result = confirm_choice(
                "Please input the film name you want to add",
                lambda choice: database.get_film(choice),
                reject_message = "Your film could not be found")
            if result != None:
                result = database.get_film(result)
                result.display_film()
                correct_check = input("Is this the correct film? Y/N : ").strip()
                if correct_check.lower() == "n":
                    print("Film not added")
                    pass
                user.add_to_watchList(result)
                print("Film added to watchlist!")
        elif user_input == 2:
            filter_search_dialog(database, user)
        elif user_input == 3:
            user.display_watchlist()
            user_watch_list = user.get_watch_list()
            if len(user_watch_list) < 1: continue
            film = confirm_choice("Please input the film index to remove",
                lambda choice: is_text_int(choice) 
                    and int(choice) > 0
                    and int(choice) <= len(user_watch_list)
                    # ensures that the chosen int is in the right range
            )

            if film:
                film_index = int(film) - 1
                removed_film = user.pop_from_watchlist(film_index);
                print(f"Removed film #{film_index} ({removed_film.name}) from your watchlist.")

        elif user_input == 4:
            return
        else:
            print("Input unknown. Please input a valid choice.")

    

def main():
    user = User("test")
    imports = DatabaseLoader()
    database = imports.load("films.json")
    export = DatabaseWriter()
    while True:
        print("\n")
        print("Welcome to the film reccomendation system!")
        print("1: Add a film to the database")
        print("2: Add/remove a film to/from your watch list")
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
            watchlist_dialog(database, user) 
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
