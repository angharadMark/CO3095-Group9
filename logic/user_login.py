# logic/user_login.py

from logic.user_registration import readJson, verifyPassword, usersFile

def loginUser(username: str, password: str):
    """
    Try to log a user in
    Returns a dict {id, username} on success, or None if failed
    """
    username = (username or "").strip()
    if not username or not password:
        return None

    # Load user data
    users = readJson(usersFile, {"byId": {}, "byUsername": {}})

    # Look up by username
    userId = users["byUsername"].get(username)
    if not userId:
        return None

    record = users["byId"].get(userId)
    if not record:
        return None

    # Check password
    if verifyPassword(password, record.get("passwordHash", "")):
        return {"id": record["id"], "username": record["username"],"avatarIndex":record.get("avatarIndex",0)}

    return None
