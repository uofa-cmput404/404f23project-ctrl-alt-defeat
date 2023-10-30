import sys
import os
import unittest
from flask import json
sys.path.append("..")
from app.__init__ import create_app
import sqlite3

class RequestorsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  # Create a Flask test app
        self.client = self.app.test_client()  # Create a test client

        connection = sqlite3.connect("database.db") # Populate test data
        with open('mock_schema.sql') as f:
            connection.executescript(f.read())


    def test_registration_success(self):
        # Test registration with a new username
        data = {
            'username': 'testuser2', # Change this each time
            'password': 'testpassword'
        }
        response = self.client.post('requestors/register', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)  
        self.assertEqual(data['message'], 'Registration successful')

    def test_registration_existing_user(self):
        # Test registration with an existing username
        data = {
            'username': 'jane_doe',
            'password': 'securepass456'
        }
        response = self.client.post('requestors/register', json=data)
        data = json.loads(response.data) 
        self.assertEqual(data['error'], 'Username already exists')

if __name__ == '__main__':
    unittest.main()
