import unittest
from flask import Flask, request, json
import sys
from init_mock_db import init_mock_db
sys.path.append("..")
from app.__init__ import create_app
import sqlite3

class RequestorsTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        init_mock_db()
        self.app = app.test_client()

    def test_registration_success(self):
        # Test registration with a new username
        data = {
            'username': 'testuser', 
            'password': 'password'
        }
        response = self.app.post('/api/requestors/register', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)  
        self.assertEqual(data['message'], 'Registration successful')

    def test_registration_existing_user(self):
        # Test registration with an existing username
        data = {
            'username': 'philiponions',
            'password': 'password'
        }
        response = self.app.post('/api/requestors/register', json=data)
        data = json.loads(response.data) 
        self.assertEqual(data['error'], 'Username already exists')

if __name__ == '__main__':
    unittest.main()
