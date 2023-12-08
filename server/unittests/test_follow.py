import unittest
from flask import Flask, request, json
import sys
from init_mock_db import init_mock_db
sys.path.append("..")
from app.__init__ import create_app
import sqlite3

class FollowTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        init_mock_db()
        self.app = app.test_client()

    def test_user_search_empty_query(self):
        response = self.app.get('/api/follow/usersearch')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['users'], [])

    def test_user_search_existing_user(self):
        query = 'philiponions'
        response = self.app.get('/api/follow/usersearch?query=' + query)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertNotEqual(len(data['users']), 0)

    def test_follow_request_success(self):   # Have to clear the follow_requests/friends table each run
        data = {
            'author_send': '0d3aa4cb-b17d-4090-923f-8ac14185fae6',     
            'author_receive': '0ca265e4-9572-11ee-b9d1-0242ac120002'  
        }
        response = self.app.post('/api/follow/follow_request', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Follow request sent')

    def test_follow_request_already_following(self):
        data = {
            'author_send': '2179aff4-9572-11ee-b9d1-0242ac120002',
            'author_receive': 'f2d79922-9571-11ee-b9d1-0242ac120002' 
        }
        response = self.app.post('/api/follow/follow_request', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Already following')

    def test_show_requests_empty_requests(self): 
        author_id = 'f2d79922-9571-11ee-b9d1-0242ac120002'
        response = self.app.get('/api/follow/show_requests?authorId=' + str(author_id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['followRequests'], [])

    def test_accept_follow_request_success(self): # Data has to exist in follow_requests to accept
        data = {
            'author_followee': '0d3aa4cb-b17d-4090-923f-8ac14185fae6',
            'author_following': 'f2d79922-9571-11ee-b9d1-0242ac120002'
        }
        response = self.app.post('/api/follow/accept_request', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Follow request accepted')

    def test_check_follower_existing_friendship(self):
        author_id = 'f2d79922-9571-11ee-b9d1-0242ac120002'
        foreign_author_id = '2179aff4-9572-11ee-b9d1-0242ac120002'

        response = self.app.get(f'/api/authors/{author_id}/followers/{foreign_author_id}')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['is_follower'])

    def test_get_followers_success(self):
        author_id = 'f2d79922-9571-11ee-b9d1-0242ac120002'

        response = self.app.get(f'/api/authors/{author_id}/followers')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['items']), 1)

if __name__ == '__main__':
    unittest.main()
