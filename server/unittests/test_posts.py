import unittest
from flask import Flask, request, json
import sys
from init_mock_db import init_mock_db

sys.path.append("..")

from app.__init__ import create_app

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.maxDiff = None

        init_mock_db()

        self.app = app.test_client()

    def tearDown(self):
        # Clean up resources if needed
        pass

    # Get all the liked posts that the author has liked
    def test_get_posts_author_liked(self):

        # Mock execute method on the cursor
        expected = {'items': 
                    [{'@context': None, 
                      'author': 
                        {'displayName': 'maven', 
                         'github': None, 
                         'host': 'http://localhost/', 
                         'id': 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002', 
                         'profileImage': None, 
                         'type': 'author', 
                         'url': 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002'}, 
                        'object': 'http://localhost/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/posts/77f8c164-957a-11ee-b9d1-0242ac120002', 
                        'summary': 'maven Likes your post', 
                        'type': 'Like'}, 
                        {'@context': None, 
                         'author': 
                            {'displayName': 'maven', 
                             'github': None, 
                             'host': 'http://localhost/', 
                             'id': 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002', 
                             'profileImage': None, 
                             'type': 'author', 
                             'url': 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002'}, 
                            'object': 'http://localhost/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/posts/5f3be750-957a-11ee-b9d1-0242ac120002', 
                            'summary': 'maven Likes your post', 
                            'type': 'Like'}
                        ], 'type': 'liked'}

        # Make a request to the endpoint
        response = self.app.get('/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/liked')

        # Assertions
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["type"], "liked")
        self.assertEqual(len(data["items"]), 2)
        self.assertEqual(data, expected)
        # Add more assertions based on your expected response
    
    def test_get_post(self):
    
        # Make a request to the endpoint
        response = self.app.get('/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/posts/5f3be750-957a-11ee-b9d1-0242ac120002')

        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.get_json()        
        
        self.assertEqual(data["type"], "post")
        self.assertEqual(data["id"], 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/posts/5f3be750-957a-11ee-b9d1-0242ac120002')
        self.assertEqual(data["author"]["id"], 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002')
        self.assertEqual(data["id"], "http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/posts/5f3be750-957a-11ee-b9d1-0242ac120002")        
        self.assertEqual(data["title"], 'New post')        
        self.assertEqual(data["content"], 'hello world')        
        self.assertEqual(data["visibility"], 'PUBLIC')
   
    def test_get_recent_post(self):        
        # Make a request to the endpoint
        response = self.app.get('/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/posts/')
        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.get_json()        
        
        # Check first item
        self.assertEqual(data["type"], "posts")
        self.assertEqual(data["items"][0]["id"], 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/posts/77f8c164-957a-11ee-b9d1-0242ac120002')
        self.assertEqual(data["items"][0]["author"]["id"], 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002')
        self.assertEqual(data["items"][0]["title"], "Sentence")
        self.assertEqual(data["items"][0]["content"], 'The quick brown fox jumps over the lazy dog')

        # Check second item
        self.assertEqual(data["type"], "posts")
        self.assertEqual(data["items"][1]["id"], 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/posts/5f3be750-957a-11ee-b9d1-0242ac120002')        
        self.assertEqual(data["items"][1]["author"]["id"], 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002')
        self.assertEqual(data["items"][1]["title"], "New post")
        self.assertEqual(data["items"][1]["content"], 'hello world')

    def test_get_comments(self):        
        # Make a request to the endpoint
        response = self.app.get('/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002/posts/5f3be750-957a-11ee-b9d1-0242ac120002/comments')

        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.get_json()   
        
        self.assertEqual(data["items"][0]["author"]["displayName"], "coolguy456")
        self.assertEqual(data["type"], "comments")
        self.assertEqual(data["items"][0]["comment"], "Sensational")

if __name__ == '__main__':
    unittest.main()