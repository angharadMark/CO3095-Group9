import unittest
from unittest.mock import patch, MagicMock
from logic.user_settings import changeUsername, changePassword

class TestAccountSettings(unittest.TestCase):

    @patch('logic.user_settings.readJson')
    @patch('logic.user_settings.saveJson')
    def test_username_logic(self, mock_save, mock_read):
        # Setup mock database
        mock_read.return_value = {
            "byId": {"user123": {"username": "current_user"}},
            "byUsername": {"current_user": "user123", "taken_name": "user456"}
        }

        # Frame 1: Already_Exists (Error)
        with self.assertRaises(ValueError) as cm:
            changeUsername("user123", "taken_name")
        self.assertEqual(str(cm.exception), "Username already exists. ")

        # Frame 2: Empty (Error)
        with self.assertRaises(ValueError):
            changeUsername("user123", "")

        # Frame 5: Valid_Unique (Success)
        result = changeUsername("user123", "new_unique_name")
        self.assertEqual(result, "new_unique_name")
        self.assertTrue(mock_save.called)

    @patch('logic.user_settings.readJson')
    def test_password_logic(self, mock_read):
        # Frame 3: Too_Short (Error)
        with self.assertRaises(ValueError) as cm:
            changePassword("user123", "oldPass", "123") # Only 3 chars
        self.assertIn("atleast 6 characters", str(cm.exception))

if __name__ == '__main__':
    unittest.main()