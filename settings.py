from getpass import getpass
from logic.user_state import UserState
from logic.user_settings import changePassword, changeUsername, changeAvatarMenu, changeFavFilmMenu, deleteUserAccount
from object.user import User
from logic.user_registration import readJson,usersFile
from pathlib import Path
from logic.admin_actions import add_profan, delete_profan

BASE_DIR = Path(__file__).resolve().parent
HTML_PATH = BASE_DIR / "data" / "scrape_sources" / "movies.html"
FILMS_PATH = BASE_DIR / "films.json"


import json
import os

INTERFACE_FILE = "interface.json"

DEFAULT_INTERFACE = {
    "friends": True,
    "movie_of_day": True,
    "comments": True,
}

def feature_on(key):
    cfg = load_interface()
    return cfg.get(key, True)

def load_interface():
    if not os.path.exists(INTERFACE_FILE):
        return DEFAULT_INTERFACE.copy()

    try:
        with open(INTERFACE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # merge defaults so missing keys don't break things
        cfg = DEFAULT_INTERFACE.copy()
        for k in cfg:
            if k in data:
                cfg[k] = bool(data[k])
        return cfg
    except:
        return DEFAULT_INTERFACE.copy()

def save_interface(cfg):
    with open(INTERFACE_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)



def interface_menu():
    while True:
        cfg = load_interface()

        print("\nInterface Management")
        print("-------------------")
        print("1. Toggle Friends System        :", "ON" if cfg["friends"] else "OFF")
        print("2. Toggle Movie of the Day      :", "ON" if cfg["movie_of_day"] else "OFF")
        print("3. Toggle Comments              :", "ON" if cfg["comments"] else "OFF")
        print("4. Reset to default")
        print("5. Back")

        choice = input("Select an option: ").strip()

        if choice == "1":
            cfg["friends"] = not cfg["friends"]
            save_interface(cfg)

        elif choice == "2":
            cfg["movie_of_day"] = not cfg["movie_of_day"]
            save_interface(cfg)

        elif choice == "3":
            cfg["comments"] = not cfg["comments"]
            save_interface(cfg)


        elif choice == "4":
            save_interface(DEFAULT_INTERFACE.copy())
            print("Reset complete.")

        elif choice == "5":
            return

        else:
            print("Invalid option")




def settingsMenu(state:UserState):
    if not state.isLoggedIn():
        print("You must be logged in to access settings.")
        return

    user_id=state.currentUser["id"]
    current_user_obj = User(state.currentUser)

    while True:
        print("\nAccount Settings")
        print("----------------")
        print("1. View account details")
        print("2. Change username")
        print("3. Change password")
        print("4. Change profile picture")
        print("5. Change favourite film")
        print("6. Logout")
        print("7. Delete Account")
        print("8. Back")


        choice = input("Select an option: ")

        if choice == "1":
            current_user_obj.display_profile()


        elif choice == "2":
            newUsername = input("Enter new username: ").strip()
            try:
                updated = changeUsername(state.currentUser["id"], newUsername)
                state.currentUser["username"] = updated
                print("Username updated successfully!")
            except ValueError as e:
                print("Error:", e)

        elif choice == "3":
            oldPw = getpass("Current password: ")
            newPw = getpass("New password: ")
            confirm = getpass("Confirm new password: ")

            if newPw != confirm:
                print("Passwords do not match.")
                continue

            try:
                changePassword(state.currentUser["id"], oldPw, newPw)
                print("Password updated successfully!")
            except ValueError as e:
                print("Error:", e)

        elif choice=="4":
            changeAvatarMenu(current_user_obj, user_id) 
        elif choice=="5":
            changeFavFilmMenu(current_user_obj,user_id)
        elif choice == "6":
            state.logout()
            print("Logged out.")
            break
        elif choice == "7":
            confirm=input("Are you absolutely sure? y/n   ")
            if confirm.lower()=="y":
                success=deleteUserAccount(user_id)
                if success:
                    print("Succesffully deleted account.")
                    state.logout()
                    break
                else:
                    print("Error, could not delete account. ")
            else:
                print("Delete cancelled. ")
        elif choice == "8":
            break

        else:
            print("Invalid option.")

def adminMenu(state:UserState):
    
    # Admin Username= admin
    # Admin Password= admins
    while True:
        print("\nAdministrator Settings")
        print("----------------")
        print("1. Delete user's account")
        print("2. Print out all user account's names")
        print("3. Scrape movies from HTML file")
        print("4. Manage interface")
        print("5. Add word to profanity filter")
        print("6. Delete word from profanity filter")

        adminChoice = input("Select an option: ")

        # Delete user
        if adminChoice == "1":
            target_name=input("Please enter user's name you would like to delete:  ")
            # Find entered user's id
            users=readJson(usersFile,{"byId":{},"byUsername":{}})
            target_id=users["byUsername"].get(target_name)

            if not target_id:
                print(f"User not found")
                continue
            if target_name=="admin":
                print(f"You cannot delete the administrator account")
                continue
            confirm=input("Are you absolutely sure? y/n   ")
            if confirm.lower()=="y":
                if deleteUserAccount(target_id):
                    print("Account deleted")
                else:
                    print("Account not found")
            else:
                print("Delete cancelled. ")

        # Print all usernames
        elif adminChoice=="2":
            users = readJson(usersFile, {"byId": {}, "byUsername": {}})
    
            usernames = users.get("byUsername", {}).keys()
            
            if not usernames:
                print("No users found in the database.")
                return

            print("\n--- Registered Users ---")
            for i, name in enumerate(usernames, 1):
                print(f"{i}. {name}")
            print("------------------------")

        elif adminChoice == "3":
            from logic.admin_actions import import_movies

            added, skipped = import_movies(HTML_PATH, FILMS_PATH)
            print(f"Added {added}, skipped {skipped}")

        elif adminChoice == "4":
            interface_menu()
        
        elif adminChoice == "5":
            profan = input("What profanity do you need to add: ")
            add_profan(profan)

        elif adminChoice == "6:":
            while True:
                profan = input("What profanity do you need to delete (or press 'q' to quit) ")
                if profan.lower() == 'q':
                    break
                
                if delete_profan(profan) == False:
                    print("Word could not be found.")
                    continue
            print("Your word",profan,"has been deleted from the filter")






