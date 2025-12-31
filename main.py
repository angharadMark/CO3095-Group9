from object.user import User
from database.database import Database
from database.database_loader import DatabaseLoader
from database.database_writer import DatabaseWriter
from object.film import Film, searchMovies
from object.comment import Comment
from logic.watchlist_similarity import WatchlistSimilarity
from logic.messaging_system import MessagingSystem
from logic.user_registration import userExists

from logic.filter import *
from object.filter_type import FilterType

from logic.user_state import UserState
from logic.user_login import loginUser
from logic.user_registration import LoadUserById, saveUserRecord
from logic.user_download import export_data
from logic.admin_actions import add_profan, delete_profan
from settings import settingsMenu
from logic.movie_recommendations import getMovieOfTheDay, reccomend_films
from settings import settingsMenu, adminMenu
from getpass import getpass

from logic.friends_system import friends_menu
from logic.user_registration import registerUser, userExists
from logic.file_manager import exportWatchlist

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
                print(f"Removed film #{film_index+1} ({removed_film.name}) from your watchlist.")

        elif user_input == 4:
            return
        else:
            print("Input unknown. Please input a valid choice.")

    

def main():
    state=UserState()
    print("Welcome to the film recommendation system")

    # Log in / Register first
    while not state.isLoggedIn():
        print("1: Login")
        print("2: Register")
        print("3: Exit")

        choice = int( input ("Select an option:  "))
        
        #Login
        if choice==1:
            username = input("Username: ").strip()
            password = input("Password: ")

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

    imports = DatabaseLoader()
    database = imports.load("films.json")
    export = DatabaseWriter()

    user_record = LoadUserById(state.currentUser["id"])
    user = User(user_record, database)

    while state.isLoggedIn():
        print("\nWelcome to the film recommendation system!")

        print("\n--- DATABASE ---")
        print("1: Add a film to the database")
        print("2: Show popular films")
        print("3: View all films in database")
        print("4: Get films based on age rating")
        print("5: Search for a movie using a keyword")
        print("6: View actor filmography")
        print("7: Edit a film in the database")

        print("\n--- WATCHLIST ---")
        print("8: View your watchlist")
        print("9: Rate a film in your watchlist")
        print("10: Manage your watchlist")
        print("11: Save watchlist to txt file")
        print("12: Reccomendations based on watchlist")
        print("13: View similar watchlists")

        if feature_on("comments"):
            print("14: Comment on your watchlist")

        print("\n--- DISCOVER ---")
        if feature_on("movie_of_day"):
            print("15: Movie of the Day")

        print("\n--- SOCIAL ---")
        if feature_on("friends"):
            print("16: Friends System")
        print("17: Dislike films")
        print("18: Messaging")

        print("\n--- ACCOUNT ---")
        print("19: Account Settings")
        print("20: download your personal data")

        print("\n21: Exit")

        # Admin Username= admin
        # Admin Password= admins
        if state.isAdmin():
            print("100: Administrator Tools")

        while True:
            quest = input("Please select an option: ")
            if not quest.isdigit():
                print("Please select a number")
                continue

            quest = int(quest)
            break

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
            while True: 
                target = input("What actor do you want to look at? (or 'q' to exit)")
                if target.lower() == "q":
                    break
            
                results = database.search_actor(target)

                if results == False:
                    print("We couldn't find that actor, please try again.")
                    continue

                for i,actor in enumerate(results,1):
                    print(f"{i}. {actor.name}")
                
                detail = input("Choose which one you want to look at in detail (or 'q' to exit) ")
                if detail.lower() == "q":
                    break

                try:
                    detail = int(detail)
                    if 1 <= detail <= len(results):
                        (results[detail-1]).filmography()
                    else:
                        print("")
                except ValueError:
                    print("Invalid input, returning to menu.")
        elif quest == 7:
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
            result = confirm_choice(
                "Please input the film name you want to change",
                lambda choice: database.get_film(choice),
                reject_message = "Your film could not be found")
            if result == None:
                continue

            result = database.get_film(result)
            result.display_film()
            correct_check = input("Is this the correct film? Y/N : ").strip()
            if correct_check.lower() == "n":
                continue

            if result.modify_film():
                print("Film modified")
            else:
                print("Film was not modified")

        elif quest == 8:
            user.display_watchlist()
            print()

        elif quest == 9:
            rate_film_in_watchlist(user)

        elif quest == 10:
            watchlist_dialog(database, user) 

        elif quest == 11:
            exportWatchlist(user)
            if state.isLoggedIn():
                saveUserRecord(user.to_dict())

        elif quest == 12:
            recco_films = reccomend_films(user, database)

            if not recco_films:
                print("No reccomendations avaiable!")
            else:
                print("\n Recommended films: ")
                for i, film in enumerate(recco_films, 1):
                    print(f"{i}. {film.name}")

        elif quest == 13:
            # list 3 most similar user's watchlists 
            similarities = WatchlistSimilarity.find(user, database)[:3]

            for (similar_user_id, score) in similarities:
                similar_user_record = LoadUserById(similar_user_id)
                similar_user = User(similar_user_record, database)
                print(f"Similar user found: {similar_user.username}")

                similar_user.display_watchlist(displaying_other_user = True)

            if len(similarities) == 0:
                print("Found no similar users")

        elif quest==14:
            watchlist = user.get_watch_list()
            for i,film in enumerate(watchlist, 1):
                print(f"{i}. {film.name}")
            
            #need to fix, make sure input is digit
            while True:
                film_num = input("Which film do you want to comment on? or press 'q' to quit: ")
                if film_num.strip().lower() == 'q':
                    break

                if not film_num.isdigit():
                    print("Invalid input, please try again")
                    continue
                    
                film_num = int(film_num)

                if not (1 <= film_num <= len(watchlist)):
                    print("Invalid film number, please choose from the list")
                    continue

                while True:
                    anon = input("would you like it to be anonymous? 1: Y 2: N ")
                    if anon in ("1", "2"):
                        anon = int(anon)
                        break
                    print("invalid choice, please enter 1 or 2")

                message = input("Input your comment: ").strip()
                if not message:
                    print("comment cannot be empty, please try again.")
                    continue

                if anon == 1:
                    (watchlist[film_num-1]).add_comment(Comment(message))
                else:
                    (watchlist[film_num-1]).add_comment(Comment(message,user.username))

        elif quest == 15:
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

        elif quest == 16:
            if not feature_on("friends"):
                print("This feature is currently disabled by the administrator.")
            else:
                friends_menu(state.currentUser["id"])

        elif quest == 17:
            manage_dislikes(user, database)

        elif quest == 18:
            message_system(user, database)

        elif quest==19:
            settingsMenu(state)
        
        elif quest==20:
            export_data(user)
        
        elif quest == 21:
            if state.isLoggedIn():
                state.logout(user)
            break

        elif quest == 100 and state.isAdmin():
            adminMenu(state)

        export.upload(database, "films.json")

def message_system(user, database):
    while True:
        unread = user.unread_message_count()

        if unread > 0:
            print(f"You have {unread} unread messages!")
            print()

        print("1: View inbox")
        print("2: Send message")
        print("3: Exit menu")

        user_input = int(input("Please select an option: "))

        if user_input == 1:
            user_inbox = user.get_inbox()
            if len(user_inbox) == 0:
                print("You have no messages")

            for (i, message) in enumerate(reversed(user.get_inbox())):
                sender_id = message.get_sender_id()
                sender_record = LoadUserById(sender_id)

                sender = "Unknown User"
                if sender_record != None:
                    sender = sender_record.get("username", sender)
                
                message_content = message.get_message()
                message_header_suffix = " (NEW)" if not message.get_read_status() else ""
                print()
                print(f"Message #{i+1}{message_header_suffix}")
                print(f"    From: {sender}")
                print(f"    Content: {message_content}")
                message.mark_as_read()

        elif user_input == 2:
            target_username = None
            message_content = None

            while target_username == None:
                input_username = input("Who do you want to send a message to? (Enter their exact username): ")
                if not userExists(input_username):
                    print("This user could not be found.")
                    choice = input("Would you like to try again y/n : ")
                    if choice.lower() == "y":
                        continue
                    else:
                        break
                target_username = input_username

            if target_username != None:
                while message_content == None:
                    message_content = input("Write your message: ")

                    choice = input("Is this message fine? (Y to proceed, N to rewrite your message): ")
                    if choice.lower() == "n":
                        message_content = None
                        continue

            if target_username != None and message_content != None:
                if MessagingSystem.message_user(user, 
                    target_username, message_content, database):
                    print(f"Message sent to {target_username}")
                else:
                    print("Could not send this message. Try again later")

        elif user_input == 3: return

def manage_dislikes(user, database):
    while True:
        print("1: Dislike a film in your watchlist")
        print("2: Dislike a film from the database")
        print("3: Remove a dislike")
        print("4: Show disliked films")
        print("5: Exit menu")

        user_input = int(input("Please select an option: "))

        if user_input == 1:
            user_watchlist = user.get_watch_list()

            if len(user_watchlist) < 1:
                print("No films in watchlist")
                continue

            film = None

            while film == None:
                for (i, film) in enumerate(user_watchlist):
                    print(f"{i+1}: {film.name}")
                print()

                user_input = input("Select a film in your watchlist to dislike: ")

                try:
                    result = int(user_input)
                    if result < 1 or result > len(user_watchlist):
                        print(f"Film #{result} cannot be found in your watchlist")
                        raise ValueError("outside of range")

                    film = user_watchlist[result - 1]
                except ValueError:
                    choice = input("Would you like to try again y/n : ")
                    if choice.lower() == "y":
                        continue
                    else:
                        break

            if film != None:
                if user.dislike_film(film) == None:
                    print("Film already is disliked!")
                else:
                    print(f"Film '{film.name}' disliked")


        elif user_input == 2:
            film = input("Please input the film name you want to dislike: ")
            result = database.get_film(film)
            while result == False:
                print("Your film could not be found")
                choice = input("Would you like to try again y/n : ")
                if choice.lower() == "y":
                    film = input("Please input the film again: ")
                    result = database.get_film(film)
                else:
                    break

               
            if result != False:
                if user.dislike_film(result) == None:
                    print("Film already is disliked!")
                else:
                    print(f"Film '{result.name}' disliked")

        elif user_input == 3:
            for (i, film) in enumerate(user.get_dislikes()):
                print(f"{i+1}: {film.name}")
            print()

            user_input = input("Select which dislike to remove: ")

            user_dislikes = user.get_dislikes()

            film = None

            try:
                result = int(user_input)
                if result < 1 or result > len(user_dislikes):
                    print(f"Film #{result} cannot be found in your watchlist")
                    raise ValueError("outside of range")

                film = user_dislikes[result - 1]
            except ValueError:
                choice = input("Would you like to try again y/n : ")
                if choice.lower() == "y":
                    continue
                else:
                    break

            if film != None:
                user.undislike_film(film)
            
        elif user_input == 4:
            for (i, film) in enumerate(user.get_dislikes()):
                print(f"{i+1}: {film.name}")
            print()

        elif user_input == 5: return

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



if __name__ == "__main__":
    main()
