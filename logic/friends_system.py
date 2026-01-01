from logic.user_registration import readJson, saveJson, usersFile
from database.database_loader import DatabaseLoader




def _load_users():
    return readJson(usersFile, {"byId": {}, "byUsername": {}})


def _save_users(users):
    saveJson(usersFile, users)


def _get_user_record(users, user_id):
    return users["byId"].get(user_id)


def _get_user_id_by_username(users, username):
    return users["byUsername"].get(username)


def view_friends(current_user_id):
    users = _load_users()
    current_user = _get_user_record(users, current_user_id)

    if not current_user:
        print("Current user not found.")
        return

    current_user.setdefault("friends", [])

    if len(current_user["friends"]) == 0:
        print("You have no friends added.")
        return

    print("\nYour friends:")
    for friend_id in current_user["friends"]:
        friend = _get_user_record(users, friend_id)
        if friend:
            print(f"- {friend['username']}")
        else:
            print(f"- Unknown user ({friend_id})")


def view_friends_comments(current_user_id):
    users = _load_users()
    current_user = _get_user_record(users, current_user_id)

    if not current_user:
        print("Current user not found.")
        return

    current_user.setdefault("friends", [])

    if len(current_user["friends"]) == 0:
        print("You have no friends added.")
        return

    # Build a list of friend usernames
    friend_usernames = []
    for friend_id in current_user["friends"]:
        friend = _get_user_record(users, friend_id)
        if friend and "username" in friend:
            friend_usernames.append(friend["username"])

    if len(friend_usernames) == 0:
        print("You have no friends added.")
        return

    print("\nYour friends:")
    for username in friend_usernames:
        print(f"- {username}")

    chosen_username = input("\nWhich friend's comments would you like to see? ").strip()

    if chosen_username not in friend_usernames:
        print("That user is not in your friends list.")
        return

    # Load films database
    imports = DatabaseLoader()
    database = imports.load("films.json")

    results = []
    for film in database.films:
        for comment in film.comments:
            if comment.user == chosen_username:
                results.append((film.name, comment.message))

    if len(results) == 0:
        print(f"{chosen_username} has not made any comments.")
        return

    print(f"\nComments by {chosen_username}:")
    for film_name, message in results:
        print(f"\nFilm: {film_name}")
        print(f"Comment: {message}")



def add_friend(current_user_id):
    users = _load_users()
    current_user = _get_user_record(users, current_user_id)

    if not current_user:
        print("Current user not found.")
        return

    friend_username = input("Enter friend's username: ").strip()
    friend_id = _get_user_id_by_username(users, friend_username)

    if not friend_id:
        print("User not found.")
        return

    if friend_id == current_user_id:
        print("You cannot add yourself.")
        return

    current_user.setdefault("friends", [])
    friend_user = _get_user_record(users, friend_id)
    friend_user.setdefault("friends", [])

    if friend_id in current_user["friends"]:
        print("This user is already your friend.")
        return

    # mutual friendship
    current_user["friends"].append(friend_id)
    friend_user["friends"].append(current_user_id)

    _save_users(users)
    print(f"{friend_username} added as a friend.")


def remove_friend(current_user_id):
    users = _load_users()
    current_user = _get_user_record(users, current_user_id)

    if not current_user:
        print("Current user not found.")
        return

    friend_username = input("Enter friend's username to remove: ").strip()
    friend_id = _get_user_id_by_username(users, friend_username)

    if not friend_id:
        print("User not found.")
        return

    current_user.setdefault("friends", [])
    friend_user = _get_user_record(users, friend_id)
    if friend_user:
        friend_user.setdefault("friends", [])

    if friend_id not in current_user["friends"]:
        print("This user is not in your friends list.")
        return

    # mutual removal
    current_user["friends"].remove(friend_id)
    if friend_user and current_user_id in friend_user["friends"]:
        friend_user["friends"].remove(current_user_id)

    _save_users(users)
    print(f"{friend_username} removed from friends.")


def friends_menu(current_user_id):
    while True:
        print("\n--- Friends Menu ---")
        print("1. View friends")
        print("2. Add friend")
        print("3. Remove friend")
        print("4. View friends comments")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_friends(current_user_id)
        elif choice == "2":
            add_friend(current_user_id)
        elif choice == "3":
            remove_friend(current_user_id)
        elif choice == "4":
            view_friends_comments(current_user_id)
        elif choice == "5":
            break
        else:
            print("Invalid option.")
