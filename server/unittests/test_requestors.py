import sys
import os
import unittest
from flask import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

class RequestorsTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

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
