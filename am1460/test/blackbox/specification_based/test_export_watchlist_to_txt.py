import unittest
from unittest.mock import patch, mock_open
from database.database import Database
from object.film import Film
from object.user import User


class TestWatchlistExport(unittest.TestCase):
    def test_export_flow(self):
        db = Database()
        f1 = Film()
        f1.name = "Inception"
        db.add_films(f1)

        user = User("ang")
        user.add_to_watchList(f1)

        with patch('builtins.open', mock_open()) as mocked_file:
            filename = f"{user.username}_watchlist.txt"
            with open(filename, 'w') as f:
                f.write(f"User: {user.username}\n")
                for film in user.watchList:
                    f.write(f"- {film.name}\n")

            # Assertions
            mocked_file.assert_called_once_with(filename, 'w')