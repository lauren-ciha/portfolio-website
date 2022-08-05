import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # Testing your home/member page
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Lauren Ciha</title>" in html

        # Home Page tests

        assert "About Me" in html
        assert "Hobbies" in html
        assert "Education" in html
        assert "Experience" in html
        assert "Timeline" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        
        # Check to make sure timeline loaded and the content works
        page_response = self.client.get("/timeline")
        assert page_response.status_code == 200
        timeline_html = page_response.get_data(as_text=True)

        # Make sure the correct fields are present
        assert 'name="name"' in timeline_html
        assert 'name="email"' in timeline_html
        assert 'name="content"' in timeline_html

        # Make sure it workds when you post data
        response = self.client.post("/api/timeline_post", data = {"name": "Test", "email": "test@email.com", "content": "Hello world, I'm Test"})
        assert response.status_code == 200

        # use get requests to make sure the data was posted correctly
        json = response.get_json()
        assert json.get("name") == "Test"
        assert json.get("email") == "test@email.com"
        assert json.get("content") == "Hello world, I'm Test"

        def test_malformed_timeline_post(self):
            # POST request missing name
            response = self.client.post("/api/timeline_post", data = {"email": "john@email.com", "content": "Hello world, I'm John"})
            assert response.status_code == 400
            html = response.get_data(as_text=True)
            assert "Invalid name" in html

            # POST request with empty content
            response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@email.com", "content": ""})
            assert response.status_code == 400
            html = response.get_data(as_text=True)
            assert "Invalid content" in html

            # POST request with invalid email address format 
            response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "tricky-email", "content": "Hello world, I'm John"})
            assert response.status_code == 400
            html = response.get_data(as_text=True)
            assert "Invalid email" in html

            # POST request with empty name
            response = self.client.post("/api/timeline_post", data={"name": "", "email": "john@email.com", "content": "Hello world, I'm John"})
            assert response.status_code == 400
            html = response.get_data(as_text=True)
            assert "Invalid name" in html

            # POST request with empty email 
            response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "", "content": "Hello world, I'm John"})
            assert response.status_code == 400
            html = response.get_data(as_text=True)
            assert "Invalid email" in html

            # POST request with empty email address before the "@" sign  
            response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "@gmail.com", "content": "Hello world, I'm John"})
            assert response.status_code == 400
            html = response.get_data(as_text=True)
            assert "Invalid email" in html
