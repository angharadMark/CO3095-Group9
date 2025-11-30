
class UserState:
    def __init__(self):
        self.currentUser = None  # {"id": "...", "username": "..."}

    def isLoggedIn(self) -> bool:
        return self.currentUser is not None

    def login(self, userRecord: dict):
        #Store the logged-in user (dict with id + username).
        self.currentUser = userRecord

    def logout(self):
        #Clear the current user.
        self.currentUser = None
