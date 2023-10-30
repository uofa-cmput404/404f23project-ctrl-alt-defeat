import unittest
import json
import sys
sys.path.append("..")
import sqlite3

# setting path
from app.__init__ import create_app


class PostsTestcase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  # Create a Flask test app
        self.client = self.app.test_client()  # Create a test client

        connection = sqlite3.connect("database.db") # Populate test data
        with open('mock_schema.sql') as f:
            connection.executescript(f.read())

    def test_get_restricted_users(self):
        response = self.client.get('/posts/restricted?post_id=post2')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of this route

    def test_restrict_user(self):
        data = {
            'post_id': 'post2',
            'username': 'techgeek5000'
        }
        response = self.client.post('posts/restrict', json=data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of this route

    def test_unrestrict_user(self):
        response = self.client.delete('posts/unrestrict/post2/techgeek5000')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of this route

    def test_change_visibility(self):
        data = {
            'post_id': 'post1',
            'visibility': 'public'
        }
        response = self.client.post('posts/visibility', json=data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of this route

    def test_delete_post(self):
        data = {
            'post_id': 'post2'
        }
        response = self.client.post('posts/delete', json=data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of this route

    def test_get_my_posts(self):
        data = {
            'author_id': 1
        }
        response = self.client.post('posts/manage', json=data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of this route

    def test_index(self):
        data = {
            'author_id': 1
        }
        response = self.client.post('posts/', json=data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of this route

    def test_new_post(self):
        data = {
            'author_id': 1,
            'title': 'Test Post',
            'content_type': 'text/plain',
            'content': 'This is a test post',
            'visibility': 'public',
            'image_id': None
        }
        response = self.client.post('posts/new/', json=data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of this route

    # def test_get_image(self):
    #     response = self.client.get('/authors/1/1/image/')
    #     self.assertEqual(response.status_code, 200)
    #     # Add more assertions based on the expected behavior of this route

    # def test_edit_post(self):
    #     data = {
    #         'title': 'Updated Test Post',
    #         'content_type': 'text/plain',
    #         'content': 'This is an updated test post',
    #         'img_id': None,
    #         'visibility': 'public'
    #     }
    #     response = self.client.post('/authors/1/1/edit/', json=data)
    #     self.assertEqual(response.status_code, 200)
    #     # Add more assertions based on the expected behavior of this route

    # def test_categories(self):
    #     response = self.client.get('/test/')
    #     self.assertEqual(response.status_code, 200)
    #     # Add more assertions based on the expected behavior of this route

if __name__ == '__main__':
    unittest.main()
