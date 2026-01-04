import unittest
from object.user import User
'''
Tool used: Unittest & Coverage.py
Technique: Specification-Based Testing (Black-Box)
Method: Category Partitioning & Boundary Value Analysis
Documentation: All test cases are derived from the functional requirements 
to ensure 100% pass rate and high individual module coverage.
'''
DUMMY_USER_RECORD = {
    "id": "b9895d05-667f-44ed-8e55-474f8b643310",
    "username": "ang",
    "avatarIndex": 0,
    "favFilm": "None Set"
}

import unittest
from unittest.mock import patch, MagicMock
from logic.user_settings import saveAvatarIndex, changeAvatarMenu

class TestAvatarPersistence(unittest.TestCase):



    @patch('builtins.input', side_effect=['0']) # Selects exit option
    @patch('builtins.print')
    def test_change_avatar_menu_exit(self, mock_print, mock_input):
        # Coverage for the 'while' loop and exit branch in changeAvatarMenu
        user_mock = MagicMock()
        changeAvatarMenu(user_mock, "123")
        self.assertEqual(mock_input.call_count, 1)

class TestUserAvatar(unittest.TestCase):
    def setUp(self):
        record = {"id": "123", "username": "test_user", "avatarIndex": 0}
        self.user = User(record)

    # In_Range (Success)
    def test_avatar_valid(self):
        result = self.user.change_avatar(1)
        self.assertTrue(result)
        self.assertEqual(self.user.avatar_index, 1)

    # Out_of_Bounds (Fallback)
    def test_avatar_out_of_bounds(self):
        result = self.user.change_avatar(99)
        self.assertFalse(result)
        # Verify it didn't change from the setup value
        self.assertEqual(self.user.avatar_index, 0)

    # Negative (Error/Boundary)
    def test_avatar_negative(self):
        result = self.user.change_avatar(-1)
        self.assertFalse(result)



if __name__ == '__main__':
    unittest.main()