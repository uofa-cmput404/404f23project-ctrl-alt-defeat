from pymongo import MongoClient
import os
from dotenv import load_dotenv
import os

load_dotenv()

def init_mongo():

    uri = os.environ.get('URI')

    try:
        client = MongoClient(uri)
        print("Connection successful")
    except Exception as e:
        print(e)
    
    # app.mongo = client.socialdist
    return client
