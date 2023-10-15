from flask import render_template
from app.posts import bp
from bson.json_util import dumps, loads 
from flask import jsonify
from app.db import init_mongo

@bp.route('/')
def index():
    data = ""
    try:
        client = init_mongo()

        # Ask for the socialdist database
        db = client['socialdist']
        
        # Get the "posts" collection
        collection = db['post']

        # Grab all posts from the database
        cursor = collection.find()
        list_cur = list(cursor) 

        # Converting to the JSON 
        json_data = dumps(list_cur, indent = 2)  
        
        cursor.close() # Close cursor when done
        client.close() # Close client when done

        data = json_data
    
    except Exception as e:
        data = e

    return data # data

@bp.route('/test/')
def categories():
    return "Test route for /posts"