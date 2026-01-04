import unittest
from unittest.mock import patch, MagicMock
from logic.user_settings import changeFavFilmMenu, saveFavFilm
from object.user import User

'''
Technique: Specification-Based Testing (Black-Box)
Tool used: Unittest & Coverage.py
Description: Verifies the logic for updating and persisting a user's favorite film 
             using Category Partitioning to handle both valid input and user cancellation.

Expected Results:
- Save Logic: saveFavFilm() correctly updates the nested JSON 'byId' structure and triggers saveJson().
- Menu Cancel: If user input is empty (Enter key), changeFavFilmMenu() exits without calling save logic.
- Menu Success: Valid film title input updates the local User object and triggers the backend save.

Actual Results: 100% Pass Rate. 
'''
DUMMY_USER_RECORD = {
    "id": "b9895d05-667f-44ed-8e55-474f8b643310",
    "username": "ang",
    "avatarIndex": 0,
    "favFilm": "None Set"
}

class TestUserFavFilm(unittest.TestCase):
    def setUp(self):
        self.user_id = "b9895d05-667f-44ed-8e55-474f8b643310"
        self.user_username = "ang"
        record = {
            "id": self.user_id,
            "username": self.user_username,
            "favFilm": "None Set"
        }
        self.user = User(record)

    @patch('logic.user_settings.readJson')
    @patch('logic.user_settings.saveJson')
    def test_save_fav_film_logic(self, mock_save, mock_read):
        # 1. Provide the dictionary structure your logic expects
        mock_read.return_value = {
            "byId": {
                self.user_id: {
                    "id": self.user_id,
                    "username": self.user_username,
                    "favFilm": "asd"
                }
            },
            "byUsername": {self.user_username: self.user_id}
        }

        # 2. Test the backend save function
        saveFavFilm(self.user_id, "The Matrix")

        # 3. Verify saveJson was called
        self.assertTrue(mock_save.called, "saveJson was not called because user ID was not found in mock")

        # 4. Check that the correct data was passed to saveJson
        args, _ = mock_save.call_args
        saved_data = args[1]
        self.assertEqual(saved_data["byId"][self.user_id]["favFilm"], "The Matrix")

    @patch('builtins.input')
    @patch('logic.user_settings.saveFavFilm')
    def test_change_fav_film_menu_cancel(self, mock_save_logic, mock_input):
        # Frame: Empty_String (User presses Enter without typing)
        mock_input.return_value = ""

        changeFavFilmMenu(self.user, self.user_id)

        # Verify that the backend save was NOT called
        self.assertFalse(mock_save_logic.called)

    @patch('builtins.input')
    @patch('logic.user_settings.saveFavFilm')
    def test_change_fav_film_menu_success(self, mock_save_logic, mock_input):
        # Frame: Valid_Title
        mock_input.return_value = "Interstellar"

        changeFavFilmMenu(self.user, self.user_id)

        # Verify User object updated and save logic was triggered
        self.assertEqual(self.user.favFilm, "Interstellar")
        self.assertTrue(mock_save_logic.called)


if __name__ == '__main__':
    unittest.main()