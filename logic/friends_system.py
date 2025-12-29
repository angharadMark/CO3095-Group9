from logic.user_registration import readJson, saveJson, usersFile


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
        print("4. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_friends(current_user_id)
        elif choice == "2":
            add_friend(current_user_id)
        elif choice == "3":
            remove_friend(current_user_id)
        elif choice == "4":
            break
        else:
            print("Invalid option.")
