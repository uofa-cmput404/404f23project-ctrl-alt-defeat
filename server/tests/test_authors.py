import sys
import os
import unittest
from flask import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

class AuthorsTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_login_success(self):
        data = {
            'username': 'jane_doe',
            'password': 'securepass456'
        }
        response = self.client.post('/authors/login', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Login successful')
        self.assertTrue('author_id' in data)

    def test_login_wrong_password(self):
        data = {
            'username': 'jane_doe',
            'password': 'wrongPassword'
        }
        response = self.client.post('/authors/login', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Wrong Password')

    def test_login_user_not_found(self):
        data = {
            'username': 'nonExistentAuthor',
            'password': 'somePassword'
        }
        response = self.client.post('/authors/login', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User not found')

    def test_update_username_success(self):
        data = {
            'new_username': 'new_username', # Change this each time
            'authorId': 3  
        }
        response = self.client.post('/authors/update_username', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Username updated successfully')

    def test_update_username_existing_username(self):
        data = {
            'new_username': 'jane_doe',
            'authorId': 4  
        }
        response = self.client.post('/authors/update_username', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Username already exists')

    def test_update_password_success(self):
        data = {
            'new_password': 'new_password',
            'authorId': 3  
        }
        response = self.client.post('/authors/update_password', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Password updated successfully')

if __name__ == '__main__':
    unittest.main()
