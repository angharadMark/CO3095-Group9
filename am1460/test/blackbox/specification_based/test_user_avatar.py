import unittest
from object.user import User

class TestUserAvatar(unittest.TestCase):

    def setUp(self):
        self.user = User("test_user", avatar_index=0)

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