import unittest
from unittest.mock import patch, MagicMock
from logic.user_settings import deleteUserAccount
'''
Technique: Specification-Based Testing (Black-Box)
Tool used: Unittest & Coverage.py
Description: Verifies the full-lifecycle deletion process for user accounts, ensuring 
             both unique ID and username references are purged from the database.

Expected Results:
- Active Deletion: deleteUserAccount() returns True for a valid ID and triggers saveJson().
- Reference Cleanup: Both "byId" and "byUsername" entries are removed from the data structure.
- Non-Existent ID: Attempting to delete a missing ID returns False gracefully.

Actual Results: 100% Pass Rate. 
'''

class TestUserSelfDeletion(unittest.TestCase):

    @patch('logic.user_settings.readJson')
    @patch('logic.user_settings.saveJson')
    def test_self_deletion_flow(self, mock_save, mock_read):
        # Active Session + Confirmed
        # Setup: 'ang' exists in the mock DB
        user_id = "b9895d05-667f-44ed-8e55-474f8b643310"
        mock_read.return_value = {
            "byId": {user_id: {"username": "ang"}},
            "byUsername": {"ang": user_id}
        }

        # Execute deletion
        result = deleteUserAccount(user_id)

        # Verify backend cleanup
        self.assertTrue(result)
        self.assertTrue(mock_save.called)

        # Verify both references were removed (Branch Coverage)
        saved_data = mock_save.call_args[0][1]
        self.assertNotIn(user_id, saved_data["byId"])
        self.assertNotIn("ang", saved_data["byUsername"])

    @patch('logic.user_settings.readJson')
    def test_deletion_non_existent(self, mock_read):
        # Invalid ID / Session Error
        mock_read.return_value = {"byId": {}, "byUsername": {}}

        result = deleteUserAccount("fake-id-123")
        self.assertFalse(result)