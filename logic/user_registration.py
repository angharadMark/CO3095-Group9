import os,json,uuid,bcrypt




dataDir = os.path.join(os.path.dirname(__file__), "..", "data")
usersFile = os.path.join(dataDir, "users.json")



def ensureDataDir():
    #create the /data folder if it doesnt exist
    os.makedirs(dataDir, exist_ok=True)


def readJson(path, default):
    #Read JSON file or return default if missing
    ensureDataDir()
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def saveJson(path, data):
    #Save data to a JSON file. Overwrites the old file
    ensureDataDir()
    with open(path, "w", encoding = "utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



def hashPassword(password: str):
    #turn regular password input into a hash string
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    return hashed.decode("utf-8")


def verifyPassword(password:str, storedHash: str):
    #check if the password matches the hash
    return bcrypt.checkpw(password.encode("utf-8"), storedHash.encode("utf-8"))



def userExists(username:str):
    users = readJson(usersFile, {"byId":{}, "byUsername":{}})
    return username in users["byUsername"]

def registerUser(username: str, password: str):
    '''
    Register a new user
    Returns a user dictionary if successful
    ValueError for inputs that are duplicate or invalid
    '''

    username = (username or "").strip()
    if not username:
        raise ValueError("Username cannot be empty")
    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters")
    
    users = readJson(usersFile, {"byId":{}, "byUsername": {}})

    if username in users['byUsername']:
        raise ValueError("Username already exists")
    
    userId = str(uuid.uuid4())
    record = {
        "id": userId,
        "username": username,
        "passwordHash": hashPassword(password),
        "avatarIndex":0,
    }

    users["byId"][userId] = record
    users["byUsername"][username] = userId
    saveJson(usersFile, users)
    return record