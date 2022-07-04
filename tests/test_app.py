import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Index Page</title>" in html
        
        # Checking that sections for each member is loaded on the home page
        assert "Lauren" in html

    # Testing your member page
    def test_lauren(self):
        response = self.client.get("/lauren")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Lauren</title>" in html
        
        # Checking that sections on the member page are present
        assert "About Me" in html
        assert "Hobbies" in html
        assert "Education" in html

        
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        
        # Test that timeline page loaded properly
        page_response = self.client.get("/timeline")
        assert page_response.status_code == 200
        # Testing timeline page content
        timeline_html = page_response.get_data(as_text=True)
        # Asserting correct input fields on page
        assert 'name="name"' in timeline_html
        assert 'name="email"' in timeline_html
        assert 'name="content"' in timeline_html



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
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "fake-email", "content": "Hello world, I'm John"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

        # POST request with empty name
        response = self.client.post("/api/timeline_post", data={"name": "", "email": "john@email.com", "content": "Hello world, I'm John"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty email just to be sure 
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "fake-email", "content": "Hello world, I'm John"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html