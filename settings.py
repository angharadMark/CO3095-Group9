from getpass import getpass
from logic.user_state import UserState
from logic.user_settings import changePassword, changeUsername, changeAvatarMenu, changeFavFilmMenu, deleteUserAccount
from object.user import User
from logic.user_registration import readJson,usersFile

def settingsMenu(state:UserState):
    if not state.isLoggedIn():
        print("You must be logged in to access settings.")
        return

    user_id=state.currentUser["id"]
    current_user_obj = User(state.currentUser["username"], 
                            avatar_index=state.currentUser.get("avatarIndex",0),
                            favFilm=state.currentUser.get("favFilm","None set")
                            )

    while True:
        print("\nAccount Settings")
        print("----------------")
        print("1. View account details")
        print("2. Change username")
        print("3. Change password")
        print("4. Change profile picture")
        print("5. Change favourite film")
        print("6. Logout")
        print("7. Back")

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

