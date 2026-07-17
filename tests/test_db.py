"""Database tests for the TimeLinePost model (MLH peer test-module exchange).

Follows Peewee's recommended testing pattern: bind the model to a throwaway
in-memory SQLite database, create the tables in setUp and drop them in
tearDown, so each test runs isolated and never touches the real MySQL.

Run with:  python -m unittest -v tests.test_db
"""
import os
import unittest

# Import the app in test mode so importing it doesn't try to reach MySQL.
os.environ["TESTING"] = "true"

from peewee import SqliteDatabase

from app import TimeLinePost

MODELS = [TimeLinePost]

# A separate in-memory database used only by these tests.
test_db = SqliteDatabase(":memory:")


class TestTimeLinePost(unittest.TestCase):
    def setUp(self):
        # Point the model at the test DB for the duration of each test.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimeLinePost.create(
            name="John Doe",
            email="john@example.com",
            content="Hello world, I'm John!",
        )
        assert first_post.id == 1

        second_post = TimeLinePost.create(
            name="Jane Doe",
            email="jane@example.com",
            content="Hello world, I'm Jane!",
        )
        assert second_post.id == 2

        # --- completed TODO: read the posts back and assert they are correct ---
        posts = list(TimeLinePost.select().order_by(TimeLinePost.id))
        self.assertEqual(len(posts), 2)

        self.assertEqual(posts[0].name, "John Doe")
        self.assertEqual(posts[0].email, "john@example.com")
        self.assertEqual(posts[0].content, "Hello world, I'm John!")

        self.assertEqual(posts[1].name, "Jane Doe")
        self.assertEqual(posts[1].email, "jane@example.com")
        self.assertEqual(posts[1].content, "Hello world, I'm Jane!")
