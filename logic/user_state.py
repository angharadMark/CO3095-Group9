from logic.user_registration import saveUserRecord

class UserState:
    def __init__(self):
        self.currentUser = None  # {"id": "...", "username": "..."}

    def isLoggedIn(self) -> bool:
        return self.currentUser is not None

    def login(self, userRecord: dict):
        #Store the logged-in user (dict with id + username).
        self.currentUser = userRecord

    def logout(self, user = None):
        #Clear the current user.
        if user:
            saveUserRecord(user.to_dict())
        self.currentUser = None
    
    def isAdmin(self) -> bool:
        return self.currentUser and self.currentUser.get("isAdmin", False)
