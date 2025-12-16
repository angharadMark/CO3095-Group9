from getpass import getpass
from logic.user_state import UserState
from logic.user_settings import changePassword, changeUsername
from object.user import User

def settingsMenu(state:UserState):
    if not state.isLoggedIn():
        print("You must be logged in to access settings.")
        return

    current_user_obj = User(state.currentUser["username"])

    while True:
        print("\nAccount Settings")
        print("----------------")
        print("1. View account details")
        print("2. Change username")
        print("3. Change password")
        print("4. Logout")
        print("5. Back")

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

        elif choice == "4":
            state.logout()
            print("Logged out.")
            break

        elif choice == "5":
            break

        else:
            print("Invalid option.")