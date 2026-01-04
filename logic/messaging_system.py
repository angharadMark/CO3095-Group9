from object.user import User
from object.user_message import UserMessage

from logic.user_registration import UserIdFromUsername, LoadUserById, userExists, saveUserRecord

class MessagingSystem:
    @staticmethod
    def message_user(from_user, target_username, message, database = None):
        if not userExists(target_username): return False      
        if not message: return False
        if not database: return False

        target_id = UserIdFromUsername(target_username)
        if not target_id: return False

        target_record = LoadUserById(target_id)

        if not target_record: return False

        # the user shouldn't be able to message themselves
        if from_user.id == target_record.get("id"): return False

        target_user = User(target_record, database)

        message = UserMessage(from_user.id, message)

        target_user.send_message(message)

        saveUserRecord(target_user.to_dict())

        return True
