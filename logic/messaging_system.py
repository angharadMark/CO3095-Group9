from object.user import User
from object.user_message import UserMessage

from logic.user_registration import readJson, saveJson, usersFile, userExists

class MessagingSystem:
    @staticmethod
    def message_user(from_user, target_username, message, database):
        if not userExists(target_username):
            return False

        target_user = User(target_username)
        target_user.load(database)

        message = UserMessage(from_user.username, message)

        target_user.send_message(message)

        target_user.write()

        return True
