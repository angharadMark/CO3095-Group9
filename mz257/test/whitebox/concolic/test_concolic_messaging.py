import unittest
from unittest.mock import patch

from object.user import User

from database.database import Database
from logic.messaging_system import MessagingSystem
from logic.user_registration import LoadUserById

# allows for blanking out the saveUserRecord function
# to prevent writes to users.json
spoof_save_fun_blank = lambda _: None

def spoof_read_json(spoofed_ver):
    return lambda _, __: spoofed_ver

users_data = {
    "byId": {
        "1001": {
            "id": "1001",
            "username": "user1"
        },
        "1002": {
            "id": "1002",
            "username": "user2"
        }
    },
    "byUsername": {
        "user1": "1001",
        "user2": "1002"
    }
}

class ConcolicMessagingTest(unittest.TestCase):
    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_fun_blank)
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_data))
    def test_case_1(self):
        result = MessagingSystem.message_user(None, "username_that_does_not_exist", None, None)
        self.assertEqual(result, False)

    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_fun_blank)
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_data))
    def test_case_2(self):
        user = User(LoadUserById("1001"), None)
        result = MessagingSystem.message_user(user, "user2", None, None)
        self.assertEqual(result, False)

    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_fun_blank)
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_data))
    def test_case_3(self):
        user = User(LoadUserById("1001"), None)
        result = MessagingSystem.message_user(user, "user2", "", None)
        self.assertEqual(result, False)

    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_fun_blank)
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_data))
    def test_case_4(self):
        user = User(LoadUserById("1001"), None)
        result = MessagingSystem.message_user(user, "user2", "Message", None)
        self.assertEqual(result, False)

    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_fun_blank)
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_data))
    def test_case_5(self):
        database = Database()
        user = User(LoadUserById("1001"), database)
        result = MessagingSystem.message_user(user, "user1", "Message", database)
        self.assertEqual(result, False)

    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_fun_blank)
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_data))
    def test_case_6(self):
        database = Database()
        user = User(LoadUserById("1001"), database)
        result = MessagingSystem.message_user(user, "user2", "Message", database)
        self.assertEqual(result, True)
        

