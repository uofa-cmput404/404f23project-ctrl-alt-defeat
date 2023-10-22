from app.new_post import bp
import json
from app.db import get_db_connection
from flask import request
from random import randrange

@bp.route('/', methods=['POST'])
def index():
    data = ""
    try:
        # Retrieve post data from the request's JSON body
        # to get author_id, title, content, visibility
        print("NEW POST data")
        request_data = request.get_json()
        author_id = request_data["author_id"] # TODO: clarify usage of ID vs username
        title = request_data["title"]
        content = request_data["content"]
        visibility = request_data["visibility"]

        # Assign random post ID - TODO: change method of randomization
        post_id = str(randrange(0, 100000))

        # Determine type of content
        # TODO: only plain text for now, add markdown
        content_type = "text/plain"
        
        # Check for image OR image post
        # TODO: add image posting, attaching images to posts
        image_id = request_data["image_id"]
        
        if image_id == None: # JSON `null` turns into Python `None`
            image_id = "NULL" # Change for SQL syntax

        # Get date posted, i.e. current date/time
        # TODO: Check if current time is accurate
        date_posted = "DATETIME('now', 'localtime')"
                
        conn = get_db_connection()
        
        # Create a new entry into the `posts` table
        query = f"INSERT INTO posts VALUES" \
                f"( '{post_id}', '{author_id}', " \
                f"{date_posted}, '{title}', " \
                f"'{content_type}', '{content}', " \
                f"{image_id}, '{visibility}' )"
        
        conn.execute(query)
        conn.commit()
        conn.close()
    
    except Exception as e:
        print(e)
        data = str(e)

    return data # data

@bp.route('/test/')
def categories():
    return "Test route for /new_post"