from logic.user_registration import readJson, verifyPassword, usersFile, saveJson

# Returns a bool when account was deleted
def deleteUser(username: str, password: str):
    username = (username or "").strip()
    if not username or not password: return False

    userData = readJson(usersFile, None)
    if not userData or len(userData["byUsername"]) == 0 or len(userData["byId"]) == 0:
        return False

    userId = userData["byUsername"].get(username)
    if not userId: return False

    userRecord = userData["byId"].get(userId)
    if not userRecord: return False

    if not verifyPassword(password, userRecord.get("passwordHash", "")):
        return False

    # password is OK, user is selected. time to delete
    del userData["byId"][userId]
    del userData["byUsername"][username]

    saveJson(usersFile, userData)
    return True
    
    
