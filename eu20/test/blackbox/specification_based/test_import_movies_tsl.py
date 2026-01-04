import unittest
import tempfile
import os
import json
import io
from contextlib import redirect_stdout

from logic.admin_actions import import_movies


class TestImportMoviesTSL(unittest.TestCase):
    """
    Black-box Specification-based testing (Category Partition / TSL).
    Sprint 3 User Story: Admin can import movies from HTML into films.json.
    SUT: logic.admin_actions.import_movies(html_path, films_path)
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = self.tmp.name

        self.html_path = os.path.join(self.tmp_path, "movies.html")
        self.films_path = os.path.join(self.tmp_path, "films.json")

        # Start with an empty films.json list
        with open(self.films_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

    def tearDown(self):
        self.tmp.cleanup()

    def write_html(self, html: str):
        with open(self.html_path, "w", encoding="utf-8") as f:
            f.write(html)

    def read_films(self):
        with open(self.films_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def capture_output(self, func, *args, **kwargs) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            func(*args, **kwargs)
        return buf.getvalue()

    # --------------------------
    # TSL Partitions / Test cases
    # --------------------------

    def test_import_no_movie_blocks(self):
        """
        Partition: HTML exists but contains no div.movie blocks
        Expected: added=0, skipped=0 and message printed
        """
        self.write_html("<html><body><h1>No movies here</h1></body></html>")
        out = self.capture_output(import_movies, self.html_path, self.films_path)

        self.assertIn("No movies found in the HTML file.", out)
        self.assertEqual(self.read_films(), [])

    def test_import_missing_required_fields_skipped(self):
        """
        Partition: movie blocks exist but missing required name/year
        Expected: treated as 'no movies' after parsing -> added=0, skipped=0
        """
        self.write_html("""
        <html><body>
          <div class="movie">
            <span class="name">Film X</span>
            <!-- year missing -->
          </div>
        </body></html>
        """)
        out = self.capture_output(import_movies, self.html_path, self.films_path)

        self.assertIn("No movies found in the HTML file.", out)
        self.assertEqual(self.read_films(), [])

    def test_import_single_valid_movie_added(self):
        """
        Partition: valid single movie
        Expected: added=1, skipped=0, films.json contains the movie
        """
        self.write_html("""
        <html><body>
          <div class="movie">
            <span class="name">Film A</span>
            <span class="year">2020</span>
            <span class="producer">Prod A</span>
            <span class="director">Dir A</span>
            <ul class="genres"><li>Action</li></ul>
            <span class="age_rating">15</span>
            <p class="description">Desc</p>
            <ul class="cast"><li data-role="Lead">Actor 1</li></ul>
          </div>
        </body></html>
        """)

        added, skipped = import_movies(self.html_path, self.films_path)
        self.assertEqual((added, skipped), (1, 0))

        films = self.read_films()
        self.assertEqual(len(films), 1)
        self.assertEqual(films[0].get("name"), "Film A")
        self.assertEqual(str(films[0].get("year")), "2020")

    def test_import_duplicate_movie_skipped(self):
        """
        Partition: duplicate movie (same name+year already exists)
        Expected: added=0, skipped=1
        """
        # Seed films.json with Film A (2020)
        with open(self.films_path, "w", encoding="utf-8") as f:
            json.dump([{"name": "Film A", "year": "2020"}], f, indent=2)

        self.write_html("""
        <html><body>
          <div class="movie">
            <span class="name">Film A</span>
            <span class="year">2020</span>
          </div>
        </body></html>
        """)

        added, skipped = import_movies(self.html_path, self.films_path)
        self.assertEqual((added, skipped), (0, 1))

        films = self.read_films()
        self.assertEqual(len(films), 1)  # still only the original

    def test_import_mixed_new_and_duplicate(self):
        """
        Partition: mixture of duplicate + new
        Expected: added=1, skipped=1
        """
        with open(self.films_path, "w", encoding="utf-8") as f:
            json.dump([{"name": "Film A", "year": "2020"}], f, indent=2)

        self.write_html("""
        <html><body>
          <div class="movie">
            <span class="name">Film A</span>
            <span class="year">2020</span>
          </div>
          <div class="movie">
            <span class="name">Film B</span>
            <span class="year">2021</span>
          </div>
        </body></html>
        """)

        added, skipped = import_movies(self.html_path, self.films_path)
        self.assertEqual((added, skipped), (1, 1))

        films = self.read_films()
        self.assertEqual(len(films), 2)
        keys = {(m.get("name"), str(m.get("year"))) for m in films}
        self.assertIn(("Film A", "2020"), keys)
        self.assertIn(("Film B", "2021"), keys)


if __name__ == "__main__":
    unittest.main()
