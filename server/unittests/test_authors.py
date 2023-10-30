import sys
import os
import unittest
from flask import json
sys.path.append("..")
from app.__init__ import create_app
import sqlite3

class AuthorsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  # Create a Flask test app
        self.client = self.app.test_client()  # Create a test client

        connection = sqlite3.connect("database.db") # Populate test data
        with open('mock_schema.sql') as f:
            connection.executescript(f.read())

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
