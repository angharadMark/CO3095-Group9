import unittest
from unittest.mock import patch

from logic.user_management import deleteUser

test_pass = '1234'
test_pass_hash = '$2b$12$qbAP8zNggsXDhcPYEwsc5O0ZtBY.R/pU/01/WOIgOTDsMuVHEGaCy'

def spoof_read_json(spoofed_ver):
    return lambda _, __: spoofed_ver

def set_test_content(test, content):
    test.changed_content = content

def spoof_write_json(unit_test):
    return lambda _, file_data: set_test_content(unit_test, file_data)

class TestUserRemoval(unittest.TestCase):
    def setUp(self):
        self.changed_content = ""

    # test branch on line 6
    def test_attempt_delete_user_empty_username(self):
        result = deleteUser("", test_pass)
        self.assertEqual(result, False)

    # second part of condition on line 6
    def test_attempt_delete_user_invalid_password_value(self):
        result = deleteUser("", None)
        self.assertEqual(result, False)

    # test branch on line 9
    @patch("logic.user_management.readJson", new=spoof_read_json(None))
    def test_attempt_delete_user_empty_users_file(self):
        result = deleteUser("valid_user_name", test_pass)
        self.assertEqual(result, False)

    # tests second part of condition in line 9
    @patch("logic.user_management.readJson", new=spoof_read_json({"byUsername": {}}))
    def test_attempt_delete_user_empty_by_username_section(self):
        result = deleteUser("valid_user_name", test_pass)
        self.assertEqual(result, False)

    # tests third part of condition in line 9
    @patch("logic.user_management.readJson", new=spoof_read_json(
        {"byUsername": {"user": None}, "byId": {}}))
    def test_attempt_delete_user_empty_by_id_section(self):
        result = deleteUser("valid_user_name", test_pass)
        self.assertEqual(result, False)

    # tests branch on line 13
    @patch("logic.user_management.readJson", new=spoof_read_json(
        {"byUsername": {"user": None}, "byId": {"1111": None}}))
    def test_attempt_delete_user_user_not_present_in_by_username_section(self):
        result = deleteUser("valid_user_name", test_pass)
        self.assertEqual(result, False)

    #tests branch on line 16
    @patch("logic.user_management.readJson", new=spoof_read_json(
        {"byUsername": {"valid_user_name": "1111"}, "byId": {"1112": None}}))
    def test_attempt_delete_user_user_record_not_present_in_by_id_section(self):
        result = deleteUser("valid_user_name", test_pass)
        self.assertEqual(result, False)

    # tests branch on line 18
    @patch("logic.user_management.readJson", new=spoof_read_json(
        {"byUsername": {"valid_user_name": "1111"}, 
         "byId": {"1111": 
            {"passwordHash": test_pass_hash}}}))
    def test_attempt_delete_user_password_mismatch(self):
        result = deleteUser("valid_user_name", '123456')
        self.assertEqual(result, False)

    # tests if everything is written correctly
    @patch("logic.user_management.readJson", new=spoof_read_json(
        {"byUsername": {"valid_user_name": "1111"}, 
         "byId": {"1111": 
            {"passwordHash": test_pass_hash}}}))
    def test_attempt_delete_successful(self):
        # spoofed test should write to self.changed_content
        with patch("logic.user_management.saveJson", new=spoof_write_json(self)):
            result = deleteUser("valid_user_name", test_pass)
            self.assertEqual(result, True)

            expected_dict = {
                "byUsername": {}, 
                "byId": {}
            }

            self.assertEqual(expected_dict, self.changed_content)

    @patch("logic.user_management.readJson", new=spoof_read_json(
        {"byUsername": {"valid_user_name": "1111", "other_user": "1112"}, 
         "byId": {
             "1111": {"passwordHash": test_pass_hash},
             "1112": {"passwordHash": "randomstring"}
         }
        }))
    def test_attempt_delete_successful_with_other_users(self):
        # spoofed test should write to self.changed_content
        with patch("logic.user_management.saveJson", new=spoof_write_json(self)):
            result = deleteUser("valid_user_name", test_pass)
            self.assertEqual(result, True)

            expected_dict = {
                "byUsername": {"other_user": "1112"}, 
                "byId": {"1112": {"passwordHash": "randomstring"}}
            }

            self.assertEqual(expected_dict, self.changed_content)



    

