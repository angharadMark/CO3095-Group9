import unittest
from unittest.mock import patch, mock_open
from logic.user_registration import registerUser, userExists

'''
Technique: Specification-Based Testing (Black-Box)
Tool used: Unittest & Coverage.py
Description: Employs Boundary Value Analysis (BVA) for security constraints (password length) 
             and Category Partitioning for unique identity checks during registration.

Expected Results:
- User Exists: Correctly identifies existing vs. new users via dictionary lookup.
- Empty Input: registerUser() raises ValueError when username is blank.
- Password Boundary: registerUser() raises ValueError if password length < 6 characters.
- Duplicate Check: registerUser() raises ValueError if the username is already taken.
- Successful Flow: Valid data generates a new UUID, hashes the password, and triggers saveJson().

Actual Results: 100% Pass Rate. 
'''
class TestUserRegistration(unittest.TestCase):

    @patch('logic.user_registration.readJson')
    def test_user_exists_logic(self, mock_read):
        # Hits the basic read logic and dictionary lookup
        mock_read.return_value = {"byUsername": {"existing_user": "uuid-123"}}
        self.assertTrue(userExists("existing_user"))
        self.assertFalse(userExists("new_user"))

    @patch('logic.user_registration.readJson')
    @patch('logic.user_registration.saveJson')
    def test_register_user_errors(self, mock_save, mock_read):
        # Empty Username
        with self.assertRaises(ValueError):
            registerUser("", "password123")

        # Password too short (Boundary < 6)
        with self.assertRaises(ValueError):
            registerUser("ang", "12345")

        # Duplicate User
        mock_read.return_value = {"byUsername": {"ang": "id1"}}
        with self.assertRaises(ValueError):
            registerUser("ang", "password123")

    @patch('logic.user_registration.readJson')
    @patch('logic.user_registration.saveJson')
    @patch('logic.user_registration.hashPassword')
    def test_register_success(self, mock_hash, mock_save, mock_read):
        # Hits the full flow including uuid generation and record creation
        mock_read.return_value = {"byId": {}, "byUsername": {}}
        mock_hash.return_value = "hashed_pw"

        result = registerUser("new_user", "password123")
        self.assertEqual(result["username"], "new_user")
        self.assertTrue(mock_save.called)