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

        init_mock_db()

        self.app = app.test_client()

    def tearDown(self):
        # Clean up resources if needed
        pass

    def test_get_authors(self):

        # Mock execute method on the cursor
        expected = {'items': [
                        {'displayName': 'maven', 
                         'github': None, 
                         'host': 'http://localhost/', 
                         'id': 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002', 
                         'profileImage': None, 
                         'type': 'author', 
                         'url': 'http://localhost/api/authors/0ca265e4-9572-11ee-b9d1-0242ac120002'}, 
                         {'displayName': 'coolguy456', 
                          'github': None, 
                          'host': 'http://localhost/', 
                          'id': 'http://localhost/api/authors/0d3aa4cb-b17d-4090-923f-8ac14185fae6', 
                          'profileImage': None, 
                          'type': 'author', 
                          'url': 'http://localhost/api/authors/0d3aa4cb-b17d-4090-923f-8ac14185fae6'}, 
                          {'displayName': 'mark', 
                           'github': 'https://github.com/mark8m', 
                           'host': 'http://localhost/', 
                           'id': 'http://localhost/api/authors/2179aff4-9572-11ee-b9d1-0242ac120002', 
                           'profileImage': None, 
                           'type': 'author', 
                           'url': 'http://localhost/api/authors/2179aff4-9572-11ee-b9d1-0242ac120002'}, 
                          {'displayName': 'philiponions', 
                           'github': 'https://github.com/philiponions', 
                           'host': 'http://localhost/', 
                           'id': 'http://localhost/api/authors/f2d79922-9571-11ee-b9d1-0242ac120002', 
                           'profileImage': None, 
                           'type': 'author', 
                           'url': 'http://localhost/api/authors/f2d79922-9571-11ee-b9d1-0242ac120002'}], 'type': 'authors'}

        # Make a request to the endpoint
        response = self.app.get('/api/authors/')

        # Assertions
        data = response.get_json()
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["type"], "authors")
        self.assertEqual(len(data["items"]), 4)
        self.assertEqual(data, expected)
        # Add more assertions based on your expected response
    
    def test_get_author(self):
        expected =  {'displayName': 'mark', 
                     'github': 'http://github.com/mark8m', 
                     'host': 'http://localhost/', 
                     'id': 'http://localhost/api/authors/2179aff4-9572-11ee-b9d1-0242ac120002', 
                     'profileImage': None, 
                     'type': 'author', 
                     'url': 'http://localhost/api/authors/2179aff4-9572-11ee-b9d1-0242ac120002'}
        
        # Make a request to the endpoint
        response = self.app.get('/api/authors/2179aff4-9572-11ee-b9d1-0242ac120002/')

        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertEqual(data["type"], "author")
        self.assertEqual(data["id"], "http://localhost/api/authors/2179aff4-9572-11ee-b9d1-0242ac120002")
        self.assertEqual(data, expected)        

   
    def test_login(self):        
        # Make a request to the endpoint
        response = self.app.post('/api/authors/login', json={"username": "coolguy456", "password": "password"})

        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Login successful")        
    

if __name__ == '__main__':
    unittest.main()