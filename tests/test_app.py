"""Integration tests for the Flask app (MLH peer test-module exchange).

Runs against an in-memory SQLite DB (TESTING=true, set below before import),
so it never touches the real MySQL. Covers the pages, the timeline JSON API
(GET + POST), and — as a TDD exercise — malformed POST validation.

Run with:  python -m unittest -v tests.test_app
"""
import os
import unittest

# Must be set BEFORE importing app so the app picks the SQLite test database.
os.environ["TESTING"] = "true"

from app import app, TimeLinePost


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Start every test from a clean timeline table (shared in-memory DB).
        TimeLinePost.delete().execute()

    # --- pages -----------------------------------------------------------
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Maitreyi Pareek" in html        # name (title / profile / footer)
        assert "Student @ UCLA" in html          # tagline
        for label in ["Home", "Hobbies", "Timeline"]:   # dynamic nav
            assert label in html

    def test_hobbies(self):
        response = self.client.get("/hobbies")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        for hobby in ["Hiking", "Photography", "Hackathons"]:
            assert hobby in html

    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        assert 'id="timeline-form"' in response.get_data(as_text=True)

    # --- timeline JSON API ----------------------------------------------
    def test_timeline_get_empty(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_timeline_post_and_get(self):
        post = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": "Hello from the test!",
        })
        assert post.status_code == 200

        json = self.client.get("/api/timeline_post").get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "John Doe"
        assert json["timeline_posts"][0]["email"] == "john@example.com"
        assert json["timeline_posts"][0]["content"] == "Hello from the test!"

    # --- TDD: malformed POST should be rejected with 400 -----------------
    def test_malformed_timeline_post(self):
        # missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com",
            "content": "Hello world!",
        })
        assert response.status_code == 400
        assert "Invalid name" in response.get_data(as_text=True)

        # empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": "",
        })
        assert response.status_code == 400
        assert "Invalid content" in response.get_data(as_text=True)

        # malformed email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello world!",
        })
        assert response.status_code == 400
        assert "Invalid email" in response.get_data(as_text=True)


if __name__ == "__main__":
    unittest.main()
