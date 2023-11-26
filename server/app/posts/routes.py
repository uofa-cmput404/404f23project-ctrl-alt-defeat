from . import bp
import json

from ..dbase import get_db_connection

from flask import request, abort
from werkzeug.exceptions import HTTPException

from random import randrange
import sqlite3

from .. import basic_auth

@bp.route("/restricted", methods=["GET"])
def get_restricted_users():    
    post_id = request.args.get('post_id')
    
    try:
        conn, curr = get_db_connection()   
        # print(post_id)
        query = "SELECT username " \
                "FROM post_restrictions " \
                "INNER JOIN authors on post_restrictions.restricted_author_id = authors.author_id " \
                "WHERE post_id = %s"
        
        curr.execute(query, (post_id, ))
        posts = curr.fetchall()           
                          

        data = json.dumps([dict(i) for i in posts])
        # print(data)

        conn.commit()
        conn.close()
        
    
    except Exception as e:
        print(e)
        data = "error"

    return data # data



@bp.route("/restrict", methods=["POST"])
def restrict_user():
    request_data = request.get_json()
    post_id = request_data['post_id']
    username = request_data['username']
    
    data = ""

    try:
        # print(post_id, privacy)
        conn, curr = get_db_connection()        
        
        # Grab the username first
        query = "SELECT author_id FROM authors WHERE username = %s"

        # Use a parameterized query to insert values safely
        curr.execute(query,
                    (username, ))
        result = curr.fetchall()

        if len([dict(i) for i in result]) == 0:
            print("User not exist")
            return "not_exists"
            
        author_id = [dict(i) for i in result][0]['author_id']
        
        query = "INSERT INTO post_restrictions (post_id, restricted_author_id) " \
                    "VALUES (%s, %s)"
        
        # # Use a parameterized query to insert values safely
        curr.execute(query,
                    (post_id, author_id))

        conn.commit()
        conn.close()

        data = "success"
    except sqlite3.IntegrityError as e:
        # Handle the UNIQUE constraint failure
        print(f"UNIQUE constraint failed: {e}")
        data = "duplicate"
        # You can log the error, notify the user, or take other appropriate actions
        
    except Exception as e:        
        print(e)
        data = "error"

    return data # data


@bp.route("/unrestrict/<post_id>/<username>", methods=["DELETE"])
def unrestrict_user(post_id, username):    
    print(post_id, username)
    data = ""

    try:
        query = "SELECT author_id FROM authors WHERE username = %s"
        # # print(post_id, privacy)
        conn, curr = get_db_connection()        

        # Use a parameterized query to insert values safely
        curr.execute(query,
                    (username, ))
        result = curr.fetchall()

        if len([dict(i) for i in result]) == 0:
            print("User not exist")
            return "not_exists"
            
        author_id = [dict(i) for i in result][0]['author_id']
        
        query = "DELETE FROM post_restrictions " \
                "WHERE post_id = %s AND restricted_author_id = %s"

        # Use a parameterized query to insert values safely
        result = curr.execute(query, (post_id, author_id))
        
        conn.commit()
        conn.close()                
        
    except Exception as e:        
        print(e)
        data = "error"

    return data # data

@bp.route("/visibility", methods=["POST"])
def change_visibility():
    request_data = request.get_json()
    post_id = request_data['post_id']
    visibility = request_data['visibility']
    
    data = ""

    try:
        # print(post_id, privacy)
        conn, curr = get_db_connection()
        query = "UPDATE posts " \
                "SET visibility = %s " \
                "WHERE post_id = %s "
        curr.execute(query, (visibility, post_id))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route("/delete", methods=["POST"])
def delete_post():
    request_data = request.get_json()
    post_id = request_data['post_id']
    data = ""

    try:
        conn, curr = get_db_connection()
        query = f"DELETE FROM posts " \
                f"WHERE post_id = %s "
        curr.execute(query, (post_id, ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route('/manage', methods=['GET'])
def get_my_posts():
    data = ""
    try:
        # Retrieve data from the request's JSON body         
        author_id = request.args.get('author_id')           
        conn, curr = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public
        query = "SELECT * FROM posts " \
                "WHERE posts.author_id = %s " \
                "ORDER by date_posted DESC"
        
        curr.execute(query, (author_id, ))
        
        posts = curr.fetchall()                             

        posts = [dict(row) for row in posts]
        print(posts)       

        data = json.dumps(posts, indent=4, sort_keys=True, default=str)
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route('/', methods=['GET'])
def index():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        print("data")        
        author_id = request.args.get('author_id')        
        # print(author_id)
        conn, curr = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public + posts that are mine
        # Do not include posts that I'm restricted from
        query = "SELECT posts.author_id, username, posts.post_id, date_posted, title, content_type, content, image_id, visibility " \
                "FROM posts " \
                "INNER JOIN authors ON posts.author_id = authors.author_id " \
                "WHERE " \
                    "(posts.visibility = 'public' " \
                    "OR posts.author_id = %s " \
					 "OR(posts.visibility = 'friends-only' AND posts.author_id IN (SELECT author_followee FROM friends WHERE author_following = %s))) " \
                    "AND post_id NOT IN (SELECT post_id FROM post_restrictions WHERE restricted_author_id =  %s) " \
                "ORDER BY date_posted DESC; " 
        
        curr.execute(query, (author_id, author_id, author_id))
        posts = curr.fetchall()                             

        posts = [dict(row) for row in posts]        

        print(posts)
        data = json.dumps(posts, indent=4, sort_keys=True, default=str)

    except Exception as e:
        print(e)
        data = str(e)

    return data # data

# MAKE POSTS
@bp.route('/new', methods=['POST'])
@basic_auth.login_required
def new_post():
    data = ""
    try:
        # Retrieve post data from the request's JSON body
        # to get author_id, title, content, visibility, type
        print("NEW POST data")
        request_data = request.get_json()
        author_id = request_data["author_id"]
        title = request_data["title"]
        content = request_data["content"]
        visibility = request_data["visibility"]
        content_type = request_data["content_type"]

        # Assign random post ID - TODO: change method of randomization
        post_id = str(randrange(0, 100000))

        # validate the content_type is of the following,
        try:
            found = ["text/plain", "text/markdown", "application/base64", "image/png;base64",
                     "image/jpeg;base64"].index(content_type)
        except ValueError:
            print("Not a valid content type.")
            abort(412)

        # Check for image OR image post
        # TODO: add image posting, attaching images to posts
        image_id = request_data["image_id"]

        if image_id == None:  # JSON `null` turns into Python `None`
            image_id = "NULL"  # Change for SQL syntax

        conn, curr = get_db_connection()

        query = "INSERT INTO posts (post_id, author_id, title, content_type, content, visibility) " \
                "VALUES (%s, %s, %s, %s, %s, %s)"

        # Use a parameterized query to insert values safely
        curr.execute(query,
                     (post_id, author_id, title, content_type, content, visibility))

        conn.commit()
        conn.close()

        data = "success"

    except Exception as e:

        print(e)
        data = str(e)

    return data  # data


@bp.route('/authors/<author_id>/<post_id>/image/', methods=['GET'])
def get_image(author_id, post_id):
    conn, curr = get_db_connection()
    final_message = "Nothing happened."
    # check if image exists
    try:
        query = "SELECT img_id, content_type from posts WHERE (post_id = %s AND img_id IS NOT NULL AND author_id = %s);"
        cursor = conn.cursor()
        curr.execute(query, (post_id, author_id))
        img_id = cursor.fetchone()
        if img_id[0] is None:
            abort(404, "The post with this image id does not exist.")
        print("Successfully found the post with this image id.")

        query = "SELECT img_url,visibility FROM image_post WHERE img_id = %s;"

        curr.execute(query, (img_id[0],))
        img_visibility = cursor.fetchone()
        if img_visibility is None:
            abort(404, "The post exists, but the image it references does not exist.")
        elif img_visibility["visibility"] != "public":
            abort(403, "This post exists, but the image contained is only visible to specific users.")

        content_type = img_id["content_type"]
        content = img_visibility["img_url"]
        final_message = f"data:{content_type},{content}"
        return final_message
    except HTTPException as e:
        final_message = str(e)
        print(final_message)
    finally:
        conn.close()
        return final_message


@bp.route('/authors/<author_id>/<post_id>/edit/', methods=['POST'])
def edit_post(author_id, post_id):
    final_message = ""
    conn, curr = get_db_connection()
    try:
        # check if the post exists
        to_find = (post_id,)
        print(f"Attempting to find post with {post_id}")        
        
        query = "SELECT * FROM posts WHERE post_id = %s;"
        curr.execute(query, to_find)
        
        exists = curr.fetchall()
        if exists is None:
            abort(404, "The post_id cannot be found.")

        # Check if valid JSON.
        try:
            request_data = request.get_json()
        except Exception:
            abort(400, "No JSON in request.")

        post_id = to_find[0]
        title = request_data["title"]

        # At the moment, I am assuming the content provided is of this content_type. Some entry validation might be needed.

        # TODO: Images will need to be updated as well in the image_post table.

        content_type = request_data["content_type"]
        content = request_data["content"]
        image_id = request_data["image_id"]
        image_id = "NULL" if image_id is None else image_id
        visibility = request_data["visibility"]

        # The things that will not change:
        # - Date posted
        # - Author ID
        # - Post ID

        # Overwrite the entry with the new data.
        # TODO: Only update what has changed. Comparison with old vs. new data needed.

        query = "UPDATE posts SET title = %s, content_type = %s,content = %s, image_id = %s, visibility = %s WHERE post_id = %s AND author_id = %s;"
        curr.execute(query, (title, content_type, content, image_id, visibility, post_id, author_id))
        final_message = "Post Updated Successfully"
        conn.commit()
    except HTTPException as e:
        final_message = str(e)
    except KeyError as e:
        final_message = str(e, "There are missing keys in the received JSON.")
    except sqlite3.DatabaseError as e:
        final_message = str(e, " Post unable to update. Rolling back database changes.")
        conn.rollback()
    except Exception as e:
        final_message = str(e)
    finally:
        conn.close()
        return final_message

@bp.route('/test/')
def categories():
    return "Test route for /posts"



@bp.route("/<post_id>", methods=["GET"])
# Gets an individual post
def get_post(post_id):    
    conn, curr = get_db_connection()
    data = ""
    print(post_id)
    try:
        query = "SELECT * FROM posts " \
                "WHERE post_id = %s " \
                "AND (visibility = 'public' OR visibility = 'unlisted')"
                
        curr.execute(query, (post_id, ))
        row = curr.fetchall()
        
        post = [dict(i) for i in row][0]        

        author_id = post["author_id"]

        query = "SELECT username FROM authors " \
                "WHERE author_id = %s " 
        
        curr.execute(query, (author_id, ))
        row = curr.fetchone()

        if row is not None:
            row_values = [str(value) for value in row]
            row_string = ', '.join(row_values)
            post["username"] = row_string                                        

        data = json.dumps(post)

    except IndexError as e:
        data = "invalid"

    except Exception as e:
        print(e)
    return data 
