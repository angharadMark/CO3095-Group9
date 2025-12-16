from logic.user_registration import(
    readJson,
    saveJson,
    usersFile,
    hashPassword,
    verifyPassword,
)

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
    