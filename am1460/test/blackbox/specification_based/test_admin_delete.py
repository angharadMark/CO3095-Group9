import unittest
from unittest.mock import patch, MagicMock
from logic.user_settings import deleteUserAccount


class TestAdminManagement(unittest.TestCase):

    @patch('logic.user_settings.readJson')
    @patch('logic.user_settings.saveJson')
    def test_delete_user_account(self, mock_save, mock_read):
        # User_ID_Status.Exists
        mock_read.return_value = {
            "byId": {"u1": {"username": "test"}},
            "byUsername": {"test": "u1"}
        }
        self.assertTrue(deleteUserAccount("u1"))

        # User_ID_Status.Non_Existent
        mock_read.return_value = {"byId": {}, "byUsername": {}}
        self.assertFalse(deleteUserAccount("u999"))