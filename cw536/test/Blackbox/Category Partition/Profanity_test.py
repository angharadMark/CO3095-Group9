import unittest
import os
import tempfile
import shutil
from unittest.mock import patch
from logic.profanity_filter import load_profan, censor


class TestProfanityFilter(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def create_profanity_file(self, words):
        profanity_file = os.path.join(self.test_dir, "en.txt")
        with open(profanity_file, 'w', encoding='utf-8') as f:
            f.write("# Test profanity file\n")
            for word in words:
                f.write(f"{word}\n")
        return profanity_file

    # Test Case 1:
    def test_case_1_empty_string(self):
        result = censor("")
        self.assertEqual(result, "")

    # Test Case 2:
    @patch('logic.profanity_filter.profanFile')
    def test_case_2_case_insensitive(self, mock_profan_file):
        profanity_file = self.create_profanity_file(['badword'])
        mock_profan_file.__str__ = lambda x: profanity_file
        mock_profan_file.__fspath__ = lambda x: profanity_file

        with patch('logic.profanity_filter.profanFile', profanity_file):
            result_lower = censor("this is badword here")
            result_upper = censor("this is BADWORD here")
            result_mixed = censor("this is BaDwOrD here")

            self.assertNotIn("badword", result_lower.lower().replace("*", ""))
            self.assertNotIn("badword", result_upper.lower().replace("*", ""))
            self.assertNotIn("badword", result_mixed.lower().replace("*", ""))
            self.assertIn("*", result_lower)
            self.assertIn("*", result_upper)
            self.assertIn("*", result_mixed)

    # Test Case 3:
    @patch('logic.profanity_filter.profanFile')
    def test_case_3_word_boundaries(self, mock_profan_file):
        profanity_file = self.create_profanity_file(['bad'])

        with patch('logic.profanity_filter.profanFile', profanity_file):
            standalone = censor("this is bad")
            substring = censor("this is badge")

            self.assertIn("*", standalone)

            self.assertIn("badge", substring.lower())

    # Test Case 4:
    @patch('logic.profanity_filter.profanFile')
    def test_case_4_file_exists_clean_text(self, mock_profan_file):
        profanity_file = self.create_profanity_file(['badword', 'offensive'])

        with patch('logic.profanity_filter.profanFile', profanity_file):
            words = load_profan()
            self.assertIsInstance(words, set)
            self.assertGreater(len(words), 0)

            clean_text = "This is a nice message"
            result = censor(clean_text)
            self.assertEqual(result, clean_text)

    # Test Case 5:
    @patch('logic.profanity_filter.profanFile')
    def test_case_5_file_exists_has_profanity(self, mock_profan_file):
        profanity_file = self.create_profanity_file(['badword', 'offensive'])

        with patch('logic.profanity_filter.profanFile', profanity_file):
            words = load_profan()
            self.assertIsInstance(words, set)
            self.assertGreater(len(words), 0)

            text_with_profanity = "This has badword in it"
            result = censor(text_with_profanity)
            self.assertNotIn("badword", result.lower().replace("*", ""))
            self.assertIn("*", result)

    # Test Case 6:
    @patch('logic.profanity_filter.profanFile')
    def test_case_6_file_not_exists_clean_text(self, mock_profan_file):
        non_existent = os.path.join(self.test_dir, "nonexistent.txt")

        with patch('logic.profanity_filter.profanFile', non_existent):
            words = load_profan()
            self.assertIsInstance(words, set)
            self.assertEqual(len(words), 0)

            clean_text = "This is a nice message"
            result = censor(clean_text)
            self.assertEqual(result, clean_text)

    # Test Case 7:
    @patch('logic.profanity_filter.profanFile')
    def test_case_7_file_not_exists_has_profanity(self, mock_profan_file):
        non_existent = os.path.join(self.test_dir, "nonexistent.txt")

        with patch('logic.profanity_filter.profanFile', non_existent):
            words = load_profan()
            self.assertIsInstance(words, set)
            self.assertEqual(len(words), 0)

            text = "This has badword in it"
            result = censor(text)
            self.assertEqual(result, text)


if __name__ == "__main__":
    unittest.main()