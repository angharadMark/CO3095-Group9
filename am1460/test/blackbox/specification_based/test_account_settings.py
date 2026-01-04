import unittest
from unittest.mock import patch, MagicMock
from logic.user_settings import changeUsername, changePassword

class TestAccountSettings(unittest.TestCase):

    @patch('logic.user_settings.readJson')
    @patch('logic.user_settings.saveJson')
    def test_username_logic(self, mock_save, mock_read):
        mock_read.return_value = {
            "byId": {"user123": {"username": "current_user"}},
            "byUsername": {"current_user": "user123", "taken_name": "user456"}
        }

        # Already_Exists (Error)
        with self.assertRaises(ValueError) as cm:
            changeUsername("user123", "taken_name")
        self.assertEqual(str(cm.exception), "Username already exists. ")

        # Empty (Error)
        with self.assertRaises(ValueError) as cm:
            changeUsername("user123", "")
        self.assertEqual(str(cm.exception), "Username cannot be empty")

        # NonExistent User ID
        with self.assertRaises(ValueError) as cm:
            changeUsername("user9999", "new_name")
        self.assertEqual(str(cm.exception), "User not found")

        # Valid_Unique (Success)
        result = changeUsername("user123", "new_unique_name")
        self.assertEqual(result, "new_unique_name")
        self.assertTrue(mock_save.called)

    @patch('logic.user_settings.readJson')
    @patch('logic.user_settings.verifyPassword')
    def test_password_logic(self, mock_verify, mock_read):
        # Too_Short (Error)
        with self.assertRaises(ValueError) as cm:
            changePassword("user123", "oldPass", "123")  # Only 3 chars
        self.assertIn("atleast 6 characters", str(cm.exception))

        # Exactly 6 Characters (Length Partition Success)
        # By setting verifyPassword to False, it proves the code got past the length check
        # and reached the "Current password is incorrect" branch.
        mock_read.return_value = {"byId": {"user123": {"passwordHash": "dummy_hash"}}}
        mock_verify.return_value = False

        with self.assertRaises(ValueError) as cm:
            changePassword("user123", "wrong_old", "123456")
        self.assertIn("incorrect", str(cm.exception))


if __name__ == '__main__':
    unittest.main()