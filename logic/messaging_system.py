from object.user import User
from object.user_message import UserMessage

from logic.user_registration import UserIdFromUsername, LoadUserById, userExists, saveUserRecord

class MessagingSystem:
    @staticmethod
    def message_user(from_user, target_username, message, database):
        if not userExists(target_username):
            return False      

        target_id = UserIdFromUsername(target_username)
        target_record = LoadUserById(target_id)

        target_user = User(target_record, database)

        message = UserMessage(from_user.id, message)

        target_user.send_message(message)

        saveUserRecord(target_user.to_dict())

        return True
