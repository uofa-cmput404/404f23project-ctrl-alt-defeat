from app.posts import bp
import json
from app.db import get_db_connection
from flask import request

@bp.route("/delete", methods=["POST"])
def delete_post():
    request_data = request.get_json()
    post_id = request_data['post_id']
    data = ""

    try:
        conn = get_db_connection()
        query = f"DELETE FROM posts " \
                f"WHERE post_id = '{post_id}'"
        conn.execute(query)
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route('/manage', methods=['POST'])
def get_my_posts():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        print("manage")
        request_data = request.get_json()
        author_id = request_data['author_id']
                    
        conn = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public
        query = f"SELECT * FROM posts " \
                f"WHERE posts.author_id = '{author_id}' " \
                f"ORDER by date_posted DESC"
        
        posts = conn.execute(query).fetchall()                                
        print(posts)
        conn.commit()
        conn.close()

        data = json.dumps([dict(i) for i in posts])
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route('/', methods=['POST'])
def index():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        print("data")
        request_data = request.get_json()

        # TODO: change from username to author_id
        username = request_data['username']
                
        conn = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public
        query = f"SELECT * FROM posts " \
                f"WHERE posts.author_id in " \
                f"(SELECT author_following FROM friends WHERE author_followee= '{username}') " \
                f"OR visibility = 'public' OR posts.author_id = '{username}'" \
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