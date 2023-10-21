from app.posts import bp
import json
from app.db import get_db_connection
from flask import request

@bp.route('/', methods=['POST'])
def index():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        print("data")
        request_data = request.get_json()
        username = request_data['username']
                
        conn = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public
        query = f"SELECT * FROM posts " \
                f"WHERE posts.author_id in " \
                f"(SELECT author_following FROM friends WHERE author_followee= '{username}') " \
                f"OR visibility = 'public' " \
                f"ORDER by date_posted DESC"
        
        posts = conn.execute(query).fetchall()                                
        conn.commit()
        conn.close()

        data = json.dumps([dict(i) for i in posts])
    
    except Exception as e:
        print(e)
        data = str(e)

    return data # data

@bp.route('/test/')
def categories():
    return "Test route for /posts"