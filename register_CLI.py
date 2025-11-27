from getpass import getpass
from logic.user_registration import registerUser, userExists


print("Welcome to the registration tool\n")

while True:
    username  = input("Enter a username: ").strip()
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
except Exception as e:
    print("Registration failed:",e)