import unittest
from object.user import User
DUMMY_USER_RECORD = {
    "id": "b9895d05-667f-44ed-8e55-474f8b643310",
    "username": "ang",
    "avatarIndex": 0,
    "favFilm": "None Set"
}
class TestUserAvatar(unittest.TestCase):
    def setUp(self):
        record = {"id": "123", "username": "test_user", "avatarIndex": 0}
        self.user = User(record)

    # Frame 5: In_Range (Success)
    def test_avatar_valid(self):
        result = self.user.change_avatar(1)
        self.assertTrue(result)
        self.assertEqual(self.user.avatar_index, 1)

    # Frame 6: Out_of_Bounds (Fallback)
    def test_avatar_out_of_bounds(self):
        result = self.user.change_avatar(99)
        self.assertFalse(result)
        # Verify it didn't change from the setup value
        self.assertEqual(self.user.avatar_index, 0)

    # Frame 4: Negative (Error/Boundary)
    def test_avatar_negative(self):
        result = self.user.change_avatar(-1)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()