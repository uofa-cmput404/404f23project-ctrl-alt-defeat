import sys
import os
import unittest
from flask import json
sys.path.append("..")
from app.__init__ import create_app

import sqlite3

class FollowTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()  # Create a Flask test app
        self.client = self.app.test_client()  # Create a test client

        connection = sqlite3.connect("database.db") # Populate test data
        with open('mock_schema.sql') as f:
            connection.executescript(f.read())


    def test_user_search_empty_query(self):
        response = self.client.get('/follow/usersearch')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['users'], [])

    def test_user_search_existing_user(self):
        query = 'jane_doe'
        response = self.client.get('/follow/usersearch?query=' + query)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertNotEqual(len(data['users']), 0)

    def test_follow_request_success(self):   # Have to clear the follow_requests/friends table each run
        data = {
            'author_send': 4,     
            'author_receive': 2  
        }
        response = self.client.post('/follow/follow_request', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Follow request sent')

    def test_follow_request_already_following(self):
        data = {
            'author_send': 3,  
            'author_receive': 2  
        }
        response = self.client.post('/follow/follow_request', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Already following')

    def test_show_requests_empty_requests(self): 
        author_id = 4
        response = self.client.get('/follow/show_requests?authorId=' + str(author_id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['followRequests'], [])

    def test_accept_follow_request_success(self): # Data has to exist in follow_requests to accept
        data = {
            'author_followee': 1,
            'author_following': 2
        }
        response = self.client.post('/follow/accept_request', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Follow request accepted')

    def test_reject_follow_request_success(self): # Data has to exist in follow_requests to reject
        data = {
            'author_followee': 2,  
            'author_following': 3 
        }
        response = self.client.post('/follow/reject_request', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Follow request rejected')

if __name__ == '__main__':
    unittest.main()
