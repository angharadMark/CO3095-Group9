# login_CLI.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))  # ensure project root is on the path

from getpass import getpass
from logic.user_login import loginUser
from logic.user_state import UserState

state = UserState()

print("Welcome to the login tool\n")

username = input("Username: ").strip()
password = getpass("Password: ")

user = loginUser(username, password)

if user:
    state.login(user)
    print(f"\nLogged in as {state.currentUser['username']} (id: {state.currentUser['id']})")
else:
    print("\nInvalid username or password.")
