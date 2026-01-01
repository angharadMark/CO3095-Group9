from object.user import User
from database.database import Database
from database.database_loader import DatabaseLoader
from database.database_writer import DatabaseWriter
from object.film import Film
from object.film import searchMovies
from object.comment import Comment

from logic.user_state import UserState
from logic.user_login import loginUser
from logic.movie_recommendations import getMovieOfTheDay
from settings import settingsMenu, adminMenu
from getpass import getpass

from logic.friends_system import friends_menu
from logic.user_registration import registerUser, userExists

from settings import feature_on




def register_flow():
    print("\nWelcome to the registration tool\n")

    while True:
        username = input("Enter a username: ").strip()
        if not username:
            print("Your username cannot be empty")
            continue
        if userExists(username):
            print("That username already exists")
            continue
        break

    while True:
        password = getpass("Enter a password (Min 6 chars):")
        confirm = getpass("Confirm Password: ")
        if password != confirm:
            print("Passwords do not match. \n")
            continue
        if len(password) < 6:
            print("Password too short.\n")
            continue
        break

    try:
        user = registerUser(username, password)
        print(f"\n user '{user['username']}' registered successfully!")
        print(f" User ID: {user['id']}")
        return user
    except Exception as e:
        print("Registration failed:", e)
        return None







def main():
    state=UserState()
    print("Welcome to the film reccomendation system")

    # Log in / Register first
    while not state.isLoggedIn():
        print("1: Login")
        print("2: Register")
        print("3: Exit")

        choice = int( input ("Select an option:  "))
        #Login
        if choice==1:
            username = input("Username: ").strip()
            password = getpass("Password: ")

            user = loginUser(username, password)

            if user:
                state.login(user)
                print(f"\nLogged in as {state.currentUser['username']} (id: {state.currentUser['id']})")
            else:
                print("\nInvalid username or password.")
        #Register
        if choice == 2:
            new_user = register_flow()
            if new_user:
                state.login(new_user)
                print(f"\nLogged in as {state.currentUser['username']} (id: {state.currentUser['id']})")
            continue


        #Exit
        if choice==3:
            return
    

    from object.user import User
    user=User(state.currentUser["username"], avatar_index=state.currentUser.get("avatarIndex",0))

    
    imports = DatabaseLoader()
    database = imports.load("films.json")
    export = DatabaseWriter()
    while state.isLoggedIn():
        print("\n")
        print("\nWelcome to the film recommendation system!")

        print("\n--- DATABASE ---")
        print("1: Add a film to the database")
        print("2: Show popular films")
        print("3: View all films in database")
        print("4: Get films based on age rating")
        print("5: Search for a movie using a keyword")

        print("\n--- WATCHLIST ---")
        print("6: Add a film to your watchlist")
        print("7: View your watchlist")
        print("8: Rate a film in your watchlist")
        print("9: Exit")
        print("10: Account Settings")
        print("11: Comment on your watchlist")
        print("12: View actor filmography")
        print("9: Save watchlist to txt file")
        if feature_on("comments"):
            print("10: Comment on your watchlist")

        print("\n--- DISCOVER ---")
        if feature_on("movie_of_day"):
            print("11: Movie of the Day")

        print("\n--- SOCIAL ---")
        if feature_on("friends"):
            print("12: Friends System")


        print("\n--- ACCOUNT ---")
        print("13: Account Settings")

        print("\n14: Exit")


        print("\n")

        # Admin Username= admin
        # Admin Password= admins
        if state.currentUser["username"] == "admin":
            print("100: Administrator Tools")

        
        quest = int(input("Please select an option: "))

        if quest == 1:
            film = Film()
            if film.input_film() == False:
                del film
            else:
                database.add_films(film)

        elif quest == 2:
            database.popular_films()

        elif quest == 3:
            all_films = database.get_all_films()
            if not all_films:
                print("Database empty")
            else:
                print("\nAll films in the database:")
                for i, film in enumerate(all_films, 1):
                    print(f"{i}.{film.name}")
            print()

        elif quest == 4:
            user_age = input("Please enter the minimum age rating you want the film to be: ")
            age_filtered_films = database.get_age_filtered_films(user_age)

            if not age_filtered_films:
                print("No films match that age rating.")
            else:
                print("\nAll age appropriate films in the database:")
                for i, film in enumerate(age_filtered_films, 1):
                    print(f"{i}. {film.name}")

        elif quest == 5:
            searchKeyword = input("\nEnter a Movie Title or Keyword to search: ")
            all_films = database.get_all_films()
            foundMovies = searchMovies(all_films, searchKeyword)

            if foundMovies:
                print(f"\n--- Found {len(foundMovies)} match(es) ---")
                for idx, movie in enumerate(foundMovies, 1):
                    desc = getattr(movie, 'description', "No description") or "No description"
                    print(f"{idx}. {movie.name} - {desc[:50]}...")
            else:
                print("No movies found with that keyword")

        elif quest == 6:
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

        elif quest == 7:
            user.display_watchlist()
            print()

        elif quest == 8:
            rate_film_in_watchlist(user)

        elif quest == 9:
            from logic.file_manager import exportWatchlist
            exportWatchlist(user)

        elif quest == 10:
            if not feature_on("comments"):
                print("This feature is currently disabled by the administrator.")
                continue

            for i, film in enumerate(user.get_watch_list(), 1):
                print(f"{i}. {film.name}")

            film_num = int(input("Which film do you want to comment on? : "))
            anon = int(input("would you like it to be anonymous? 1: Y 2: N "))
            message = input("Input your comment: ")

            if anon == 1:
                ((user.get_watch_list())[film_num - 1]).add_comment(Comment(message))
            else:
                ((user.get_watch_list())[film_num-1]).add_comment(Comment(message,user.username))
        elif quest==12:
            target = input("What actor do you want to look at? : ")
            results = database.search_actor(target)
            for i,actor in enumerate(results,1):
                print(f"{i}. {actor.name}")
            
            detail = int(input("Choose which one you want to look at in detail : "))
            (results[detail-1]).filmography()
                ((user.get_watch_list())[film_num - 1]).add_comment(Comment(message, user.username))


        elif quest == 11:
            if not feature_on("movie_of_day"):
                print("This feature is currently disabled by the administrator.")
                continue

            motd = getMovieOfTheDay()
            print()
            print("--- MOVIE OF THE DAY ---")
            if motd:
                print(f"Title: {motd.name}")
                print(f"Description: {motd.description}")
            else:
                print("No movies available")


        elif quest == 12:
            if not feature_on("friends"):
                print("This feature is currently disabled by the administrator.")
            else:
                friends_menu(state.currentUser["id"])

        elif quest == 13:
            settingsMenu(state)

        elif quest == 14:
            break

        elif quest == 100 and state.currentUser["username"] == "admin":
            adminMenu(state)

        export.upload(database, "films.json")


def rate_film_in_watchlist(user):
    user_watchlist = user.get_watch_list()

        export.upload(database,"films.json")

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
