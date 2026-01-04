# login_CLI.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))  # ensure project root is on the path

from getpass import getpass
from logic.user_login import loginUser
from logic.user_state import UserState
from logic.user_management import deleteUser

state = UserState()

print("Welcome to the login tool\n")

username = input("Username: ").strip()
password = input("Password: ")
#password = getpass("Password: ")

user = loginUser(username, password)

if not user:
    print("\nInvalid username or password.")
    sys.exit(0)

state.login(user)

user_name = state.currentUser['username']

print(f"\nSuccessfully logged in as {user_name} (id: {state.currentUser['id']})")

print("What would you like to do? ", "")

print(f"\nLogged in as {user_name}")
print("1: Delete your account")
print("2: Log out")

while True:
    user_choice = input("\nSelect your choice: ")
    try:
        user_choice = int(user_choice)
    except ValueError:
        print("Invalid value")
        continue

    if user_choice < 0 or user_choice > 2:
        print("No such choice exists")
        continue

    if user_choice == 1:
        confirm_choice = input(f"Are you sure you want to delete your account? ({user_name}) ")
        
        confirm_choice = confirm_choice.lower().strip()
        delete_account = confirm_choice == 'y' or confirm_choice == "yes"

        if not delete_account:
            print("Your account will NOT be deleted...")
            continue

        confirm_username = input(f"Please enter the user name of the account you are going to remove: ").strip()

        if confirm_username != user_name:
            print("Username does not match the username of the account currently logged in... Account will NOT be deleted...")
            continue

        check_password = input("Confirm your password to delete your account: ")
        #check_password = getpass("Confirm your password to delete your account: ")

        # assuming that everything in the file is alright if the user
        # is logged in, so the only case where it can return False
        # is if the password wasn't verified properly.
        if not deleteUser(user_name, check_password):
            print("Password does not match! Account will NOT be deleted...")
            continue

        print("Your account was deleted succesfully. Exitting CLI...")
        sys.exit(0)

    elif user_choice == 2:
        print("Logging out...")
        break
