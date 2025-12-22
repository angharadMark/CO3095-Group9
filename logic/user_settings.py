from logic.user_registration import(
    readJson,
    saveJson,
    usersFile,
    hashPassword,
    verifyPassword,
)
from object.user import User


def changeUsername(userID:str,newUsername:str):
    newUsername=(newUsername or "").strip()
    # Checks if username is empty
    if not newUsername:
        raise ValueError("Username cannot be empty")
    
    # Checks if username exists already
    users=readJson(usersFile,{"byId":{}, "byUsername":{}})

    if newUsername in users["byUsername"]:
        raise ValueError("Username already exists. ")
    
    # Checks user exists
    user = users["byId"].get(userID)
    if not user:
        raise ValueError("User not found")
    
    oldUsername=user["username"]

    # Updates
    user["username"]=newUsername
    users["byUsername"].pop(oldUsername)
    users["byUsername"][newUsername]=userID
    
    saveJson(usersFile,users)
    return newUsername

def changePassword(userId:str,oldPassword:str,newPassword:str):
    # Checks password < 6 characters
    if not newPassword or len(newPassword)<6:
        raise ValueError("New password must be atleast 6 characters")
    
    users=readJson(usersFile,{"byId":{},"byUsername":{}})
    user=users["byId"].get(userId)

    # Checks user exists
    if not user:
        raise ValueError("User not found")
    
    # Checks password is correct
    if not verifyPassword(oldPassword,user["passwordHash"]):
        raise ValueError("Current password is incorrect")
    
    # Updates
    user["passwordHash"]=hashPassword(newPassword)
    saveJson(usersFile,users)
    
def saveAvatarIndex(userId: str, newIndex: int):
    #Saves to JSON
    users = readJson(usersFile, {"byId":{}, "byUsername":{}})
    user = users["byId"].get(userId)
    
    if user:
        user["avatarIndex"] = newIndex 
        saveJson(usersFile, users)
    else:
        print("Warning: User record not found for avatar update.")

def changeAvatarMenu(user_obj:User,user_id:str):
    while True:
        print("\n--- Change Profile Picture ---")
        print("Select a new ASCII avatar:")

        for i, avatar in enumerate(User.AVATAR_OPTIONS):
            print(f"\n--- OPTION {i+1} ---") 
            print(avatar)
        
        print("\nEnter 0 to go back to settings")
        
        choice = input("Select an option number: ")
        
        if choice == "0":
            break
            
        try:
            selection_index = int(choice) - 1
            
            if user_obj.change_avatar(selection_index):
                saveAvatarIndex(user_id, selection_index)

                print("\nProfile picture updated successfully!")
                print("Your new avatar:")
                print(user_obj.avatar_ascii)
                break
            else:
                print("Invalid option number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def saveFavFilm(userId: str, newFilm: str):
    users = readJson(usersFile, {"byId":{}, "byUsername":{}})
    user = users["byId"].get(userId) 

    if user:
        user["favFilm"] = newFilm
        saveJson(usersFile, users)
    else:
        print("Warning: User record not found for favourite film update")

def changeFavFilmMenu(user_obj: User, user_id: str):    
    print("\n--- Change Favourite Film ---")
    print(f"Current Favourite: {user_obj.favFilm}")
    
    new_film = input("Enter your new favourite film (or press Enter to cancel): ").strip()
    
    if new_film:
        user_obj.favFilm = new_film
        saveFavFilm(user_id, new_film)
        print("Favourite film updated successfully!")
    else:
        print("No changes made.")