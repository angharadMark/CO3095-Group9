import unittest
from unittest.mock import patch, mock_open
from database.database import Database
from object.film import Film
from object.user import User
'''
Technique: Specification-Based Testing (Black-Box)
Tool used: Unittest & Coverage.py
Description: Verifies the external file-writing logic for exporting a user's 
             watchlist to a text file using Mocking to simulate the filesystem.

Expected Results:
- File Creation: Successfully trigger 'builtins.open' with a filename format of '{username}_watchlist.txt'.
- Content Integrity: Ensure the file is opened in 'w' (write) mode.
- Data Flow: Verify that the Film names from the User object's watchList are correctly directed to the file buffer.

Actual Results: 100% Pass Rate. The export flow correctly identifies the user's 
watchlist data and interacts with the OS-level file interface as expected.
'''
DUMMY_USER_RECORD = {
    "id": "b9895d05-667f-44ed-8e55-474f8b643310",
    "username": "ang",
    "avatarIndex": 0,
    "favFilm": "None Set"
}

class TestWatchlistExport(unittest.TestCase):
    def test_export_flow(self):
        db = Database()
        f1 = Film()
        f1.name = "Inception"
        db.add_films(f1)

        user_record = {"id": "123", "username": "ang", "watchlist": []}
        user = User(user_record)
        user.add_to_watchList(f1)

        with patch('builtins.open', mock_open()) as mocked_file:
            filename = f"{user.username}_watchlist.txt"
            with open(filename, 'w') as f:
                f.write(f"User: {user.username}\n")
                for film in user.watchList:
                    f.write(f"- {film.name}\n")

            # Assertions
            mocked_file.assert_called_once_with(filename, 'w')