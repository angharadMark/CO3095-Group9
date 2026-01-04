import unittest
from unittest.mock import patch

from object.film import Film
from object.user import User
from object.actor import Actor
from object.user_message import UserMessage

from database.database import Database
from logic.user_registration import LoadUserById
from logic.messaging_system import MessagingSystem


actor_1 = Actor("Actor1", "Role") 

films = [
    Film(name = "Movie1",
        genre = ["Action"], 
        cast = [actor_1]
    ),
    Film(name = "Movie2",
        genre = ["Horror"], 
        cast = [actor_1]
    ),
    Film(name = "Movie3",
       genre = ["Horror"], 
       cast = [actor_1]
    )
]

users_1 = {
    "byId": {
        "1111": {
            "id": "1111",
            "username": "user1"
        },
        "1112": {
            "id": "1112",
            "username": "user2"
        }
    },

    "byUsername": {
        "user1": "1111",
        "user2": "1112"
    }
}

users_2 = {
    "byId": {
        "1111": {
            "id": "1111",
            "username": "user1"
        },
        "1112": {
            "id": "1112",
            "username": "user2"
        }
    },
    "byUsername": {}
}

users_3 = {
    "byId": {
        "1111": None,
        "1112": None,
    },

    "byUsername": {
        "user1": "1111",
        "user2": "1112"
    }
}

def db_from_films(film_list):
    db = Database()
    for film in film_list:
        db.add_films(film)
    return db

def spoof_save_record_fail(_):
    raise AssertionError("This should not have reached saveUserRecord")

def spoof_user_exists(value):
    return lambda username: value

def spoof_read_json(spoofed_ver):
    return lambda _, __: spoofed_ver

def set_test_content(test, content):
    test.changed_content = content

def spoof_save_record(unit_test):
    return lambda data: set_test_content(unit_test, data)

class TestUserMessaging(unittest.TestCase):
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_1))
    # failsafe so users.json doesn't get destroyed by the tests
    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_record_fail)
    def setUp(self):
        self.db = db_from_films(films)
        self.user = User(LoadUserById("1111"), self.db)
        self.changed_content = ""

    # test branch on line 9
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_1))
    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_record_fail)
    def test_message_nonexistent_user(self):
        result = MessagingSystem.message_user(self.user, "non_existent_user", "message", self.db)
        self.assertEqual(result, False)

    # test branch on line 10
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_1))
    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_record_fail)
    def test_message_invalid_content(self):
        result = MessagingSystem.message_user(self.user, "user2", None, self.db)
        self.assertEqual(result, False)

    # test branch on line 11
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_1))
    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_record_fail)
    def test_message_invalid_database(self):
        result = MessagingSystem.message_user(self.user, "user2", "Hello World!", None)
        self.assertEqual(result, False)

    @patch("logic.user_registration.readJson", new=spoof_read_json(users_2))
    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_record_fail)
    def test_message_invalid_id_in_broken_users_file(self):
        result = MessagingSystem.message_user(self.user, "user2", "Hello World!", self.db)
        self.assertEqual(result, False)

    # test branch on line 18
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_3))
    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_record_fail)
    def test_message_invalid_record_in_broken_users_file(self):
        result = MessagingSystem.message_user(self.user, "user2", "Hello World!", self.db)
        self.assertEqual(result, False)

    # test branch on line 21
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_1))
    @patch("logic.messaging_system.saveUserRecord", new=spoof_save_record_fail)
    def test_message_sent_to_sending_user(self):
        # both from_user and target_username have the same username in this scenario
        result = MessagingSystem.message_user(self.user, "user1", "Hello World!", self.db)
        self.assertEqual(result, False)

    # additional test to ensure that the sending functionality saves everything properly too
    @patch("logic.user_registration.readJson", new=spoof_read_json(users_1))
    def test_message_sent_correctly(self):
        with patch("logic.messaging_system.saveUserRecord", new=spoof_save_record(self)):
            result = MessagingSystem.message_user(self.user, "user2", "Hello World!", self.db)
            self.assertEqual(result, True)

            set_content = self.changed_content
            self.assertEqual(len(set_content.get("inbox")), 1)

            message = UserMessage.from_dict(set_content.get("inbox")[0])

            self.assertEqual(message.get_message(), "Hello World!")
            self.assertEqual(message.get_sender_id(), "1111")
            self.assertEqual(message.get_read_status(), False)
