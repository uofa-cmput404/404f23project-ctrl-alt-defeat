from . import bp
import json

from ..dbase import get_db_connection

from flask import request, abort, send_file, Response, jsonify
from werkzeug.exceptions import HTTPException

from requests.auth import HTTPBasicAuth

from random import randrange
import sqlite3
from datetime import datetime, timezone
import requests
import uuid
import io,base64
from .. import basic_auth
import app.utils.remote_funcs as rf

@bp.route("/posts/restricted", methods=["GET"])
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
                          

        # data = json.dumps([dict(i) for i in posts])
        # print(data)

        data = posts

        conn.commit()
        conn.close()
        
    
    except Exception as e:
        print(e)
        data = "error"

    return jsonify(data) # data



@bp.route("/posts/restrict", methods=["POST"])
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

    return jsonify(data) # data


@bp.route("/posts/unrestrict/<post_id>/<username>", methods=["DELETE"])
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

    return jsonify(data) # data

@bp.route("/posts/visibility", methods=["POST"])
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

    return jsonify(data) # data

@bp.route("/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id):    
    data = ""

    try:
        conn, curr = get_db_connection()

        # Delete likes *in inbox table* associated with this post
        ## Get like IDs associated with this post
        like_query = "SELECT like_id FROM likes " \
                     "WHERE post_id = %s"
        curr.execute(like_query, (post_id,))
        likes = curr.fetchall()
        likes = [dict(i) for i in likes]

        ## Delete all like ids from inbox associated with post
        for like in likes:
            inbox_query = "DELETE FROM inbox_items " \
                        "WHERE object_id = %s"
            curr.execute(inbox_query, (like["like_id"],))

        # Delete actual post
        # Note that likes associated w/post are automatically deleted by cascade
        query = f"DELETE FROM posts " \
                f"WHERE post_id = %s "
        curr.execute(query, (post_id, ))

        
        conn.commit()
        conn.close()
        data = "Delete success"
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return jsonify(data) # data

@bp.route('/posts/manage', methods=['GET'])
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
        #print(posts)       

        data = posts
        # data = json.dumps(posts, indent=4, sort_keys=True, default=str)
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return jsonify(data) # data

# Grabs posts that were sent from an author's inbox
@bp.route('/posts', methods=['GET'])
@basic_auth.login_required
def index():
    print("index")
    data = []
    try:
        # Retrieve data from the request's JSON body
        author_id = request.args.get('author_id')        
        print(author_id)
        conn, curr = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public + posts that are mine
        # Do not include posts that I'm restricted from
        query = "SELECT * FROM inbox_items " \
                "WHERE recipient_id = %s " \
                "AND type = 'post' "
        
        curr.execute(query, (author_id,))
        row = curr.fetchall()                                
        posts = [dict(i) for i in row]        
        
        payload = list()        

        # posts.author_id, username, posts.post_id, date_posted, title, content_type, content, image_id, visibility
        for post in posts:
            if post['sender_host'] == 'https://cmput-average-21-b54788720538.herokuapp.com/':
                try:                    
                    new_item = rf.get_post('https://cmput-average-21-b54788720538.herokuapp.com/api/', post['sender_id'], post['object_id'], 'CtrlAltDefeat', 'string')
                    payload.append(new_item)

                except Exception as e:
                    print("Api call error")
                    print(e)
                    pass # Skip if it somehow does not work

            elif post['sender_host'] == 'https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/':
                try:                    
                    new_item = rf.get_post('https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/', post['sender_id'], post['object_id'], 'cross-server', 'password')                    
                    payload.append(new_item)

                except Exception as e:
                    print("Api call error")
                    print(e)
                    pass # Skip if it somehow does not work
            
            elif post['sender_host'] == 'https://chimp-chat-1e0cca1cc8ce.herokuapp.com/':
                try:                    
                    new_item = rf.get_post('https://chimp-chat-1e0cca1cc8ce.herokuapp.com/api/', post['sender_id'], post['object_id'], 'cross-server', 'password')                    
                    payload.append(new_item)

                except Exception as e:
                    print("Api call error")
                    print(e)
                    pass # Skip if it somehow does not work

            else:                          
                query = "SELECT posts.*, username FROM posts " \
                        "JOIN authors " \
                        "on posts.author_id = authors.author_id " \
                        "AND post_id NOT IN (SELECT post_id FROM post_restrictions WHERE restricted_author_id =  %s) " \
                        f"WHERE post_id = %s"

                print("checking", post["object_id"])
                curr.execute(query, (post["recipient_id"], post["object_id"] ))

                row = curr.fetchone()        
                print(row)        

                # If we can't find it anywhere else then the post has been deleted
                if row is None:
                    query = "DELETE FROM inbox_items " \
                            "WHERE object_id = %s"
                    print("deleting",post["object_id"])
                    curr.execute(query, (post["object_id"],))
                    conn.commit()
                else: 
                    local_result = dict(row)                    
                    payload.append(local_result)

        data = payload        

    except Exception as e:
        print(e)
        data = str(e)

    return jsonify(data) # data

# @bp.route('/posts', methods=['GET'])
# @basic_auth.login_required
# def index():
#     data = ""
#     try:
#         # Retrieve data from the request's JSON body
#         print("data")        
#         author_id = request.args.get('author_id')        
#         # print(author_id)
#         conn, curr = get_db_connection()
        
#         # Get all the posts from people who I'm following + posts who are public + posts that are mine
#         # Do not include posts that I'm restricted from
#         query = "SELECT posts.author_id, username, posts.post_id, date_posted, title, content_type, content, image_id, visibility " \
#                 "FROM posts " \
#                 "INNER JOIN authors ON posts.author_id = authors.author_id " \
#                 "WHERE " \
#                     "(posts.visibility = 'public' " \
#                     "OR posts.author_id = %s " \
# 					 "OR(posts.visibility = 'friends-only' AND posts.author_id IN (SELECT author_followee FROM friends WHERE author_following = %s))) " \
#                     "AND post_id NOT IN (SELECT post_id FROM post_restrictions WHERE restricted_author_id =  %s) " \
#                 "ORDER BY date_posted DESC; " 
        
#         curr.execute(query, (author_id, author_id, author_id))
#         row = curr.fetchall()                                
#         posts = [dict(i) for i in row]        

#         data = posts
#         # data = json.dumps(posts, indent=4, sort_keys=True, default=str)

#     except Exception as e:
#         print(e)
#         data = str(e)

#     return jsonify(data) # data

# MAKE POSTS
@bp.route('/posts/new', methods=['POST'])
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

        post_id = str(uuid.uuid4()) # Changed it so its a uuid instead

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

    return jsonify(data)  # data

# (REMOTE) 
@bp.route('/authors/<author_id>/posts/<post_id>/image', methods=['GET'])
def get_image(author_id, post_id):
    conn, curr = get_db_connection()
    final_message = Response(500,"Nothing happened.")
    try:
        query = "SELECT content, content_type,visibility from posts WHERE post_id = %s AND author_id = %s"
        curr.execute(query, (post_id, author_id))
        row = curr.fetchone()
        if row is None:
            abort(404, "The post with this post_id does not exist.")
        print("Successfully found post.")

        if row["content_type"] == "text/plain" or row["content_type"] == "text/markdown":
            abort(404, "This is not an image.")
        if row["visibility"] != "public":
            abort(403, "This post exists, but the image contained is only visible to specific users.")

        content_type = row["content_type"]
        content = row["content"]

        image_bytes = io.BytesIO(base64.b64decode(content))
        #final_message = f"data:{content_type},{content}"
        final_message = send_file(image_bytes, mimetype=content_type[:-7], max_age=30)
    except HTTPException as e:
        final_message = str(e)
        print(final_message)
    except Exception as e:
        print(e)
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

# (LOCAL) Call this instead for getting individual posts in the front end
@bp.route("/authors/<author_id>/posts/<post_id>/display", methods=["GET"])
def get_post_display(author_id, post_id):   
    print(request.root_url + "api/authors/" + author_id + "/posts/" + post_id) 
    data = requests.get(request.root_url + "api/authors/" + author_id + "/posts/" + post_id)
    
    if data.status_code == 404: # If post not found, try remote posts
        try:
            data = requests.get("https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com" + "/authors/" + author_id + "/posts/" + post_id, auth=("cross-server", "password"))
            
            if data.status_code == 200:
                return data.json()
        except Exception as e:
            print(e)
        
        try:
            data = requests.get("https://cmput-average-21-b54788720538.herokuapp.com/api" + "/authors/" + author_id + "/posts/" + post_id, auth=("CtrlAltDefeat", "string"))
            
            if data.status_code == 200:
                return data.json()
        except Exception as e:
            print(e)

    return data.json() if data.status_code == 200 else abort(404)

# (REMOTE) 
@bp.route("/authors/<author_id>/posts/<post_id>", methods=["GET"])
# Gets an individual post
def get_post(author_id, post_id):    
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
        # print(post) 

        author_id = post["author_id"]

        query = "SELECT * FROM authors " \
                "WHERE author_id = %s " 
        
        curr.execute(query, (author_id, ))
        row = curr.fetchone()            
        row = dict(row)            

        item = dict()
        item["type"] = "post"
        item["id"] = request.root_url + "api/authors/" + post["author_id"] + "/posts/" + post["post_id"]
        
        # No idea what these are, skip for now
        item["source"] = request.root_url + "api/authors/" + post["author_id"] + "/posts/" + post["post_id"]
        item["origin"] = request.root_url + "api/authors/" + post["author_id"] + "/posts/" + post["post_id"]
        item["description"] = None
        item["contentType"] = post["content_type"]   
        item["content"] = post["content"]        
        item["title"] = post["title"]        
        
        author_item = dict()
        author_item["type"] = "author"
        author_item["host"] = request.root_url
        author_item["id"] = request.root_url + "api/authors/"  + row["author_id"]
        author_item["url"] = request.root_url + "api/authors/" + row["author_id"]
        author_item["displayName"] = row["username"]
        author_item["github"] = ("https://github.com/" + row["github"]) if row["github"] != None else None
        author_item["profileImage"] = None

        item["author"] = author_item

        # We don't have these rn
        item["categories"] = []
        item["count"] = 0
        item["comments"] = request.root_url + "api/authors/" + post["author_id"] + "/posts/" + post["post_id"] + "/comments"
        item["commentsSrc"] = None

        # input_datetime = datetime.strptime(post["date_posted"], "%Y-%m-%d %H:%M:%S")
        
        # Convert datetime object to ISO 8601 format with UTC offset
        item["published"] = post["date_posted"].strftime("%Y-%m-%d %H:%M:%S") 

        visibility = post["visibility"]

        # Either public or friends only. cant be private
        if visibility == "public" or visibility == "unlisted":
            item["visibility"] = "PUBLIC" # both are technically public?
        else:
            item["visibility"] = "FRIENDS"

        item["unlisted"] = True if post["visibility"] == "unlisted" else False

       #  data = json.dumps(item, indent=2)
        data = item
        print(data)

    except IndexError as e:
        print(e)
        abort(404, "Post not found")

    except Exception as e:
        print(e)
        data = e
    
    return jsonify(data) 

# (REMOTE) 
@bp.route("/authors/<author_id>/posts/", methods=["GET"])
# Gets most recent post from author AUTHOR_ID
def get_posts(author_id):    
    conn, curr = get_db_connection()
    data = ""
    page = request.args.get('page')
    size = request.args.get('size')
    try:
        query = "SELECT * FROM posts " \
                "WHERE author_id = %s " \
                "AND visibility != 'private' " \
                "ORDER BY date_posted LIMIT %s OFFSET %s "
        
        if page is not None:
            page = int(page)
        else: page = 1 # Set default 1
        
        if size is not None:
            size = int(size)
        else: size = 20 # Set default 20

        offset = (page - 1) * size
        
        curr.execute(query, (author_id, size, offset))
        row = curr.fetchall()                                        
        posts = [dict(i) for i in row]    

        if len(posts) == 0:
            abort(404, "Post not found")

        payload = dict()
        payload["type"] = "posts"
        payload["items"] = []

        query = "SELECT * FROM authors " \
                "WHERE author_id = %s " 
        
        curr.execute(query, (author_id, ))
        author = curr.fetchone()
        # print(author)
        for post in posts:
            item = dict()
            item["type"] = "post"
            item["title"] = post["title"]
            item["id"] = request.root_url + "api/authors/" + post["author_id"] + "/posts/" + post["post_id"]
            
            # No idea what these are, skip for now
            item["source"] = request.root_url + "api/authors/" + post["author_id"] + "/posts/" + post["post_id"]
            item["origin"] = request.root_url + "api/authors/" + post["author_id"] + "/posts/" + post["post_id"]
            item["description"] = None
            item["contentType"] = post["content_type"]        
            item["content"] = post["content"]        
            
            author_item = dict()
            author_item["type"] = "author"
            author_item["host"] = request.root_url
            
            author_item["id"] = request.root_url + "api/authors/" + post["author_id"]
            author_item["url"] = request.root_url + "api/authors/" + post["author_id"]
            author_item["displayName"] = author["username"]
            author_item["github"] = ("https://github.com/" + author["github"]) if author["github"] != None else None
            author_item["profileImage"] = None

            item["author"] = author_item

            # We don't have these rn
            item["categories"] = []
            item["comments"] = request.root_url + "api/authors/" + post["author_id"] + "/posts/" + post["post_id"] + "/comments"
            item["count"] = 0
            item["commentsSrc"] = None

            # input_datetime = post["date_posted"].strptime(post["date_posted"], "%Y-%m-%d %H:%M:%S")
            
            # Convert datetime object to ISO 8601 format with UTC offset
            item["published"] = post["date_posted"].strftime("%Y-%m-%d %H:%M:%S") 

            # if item["visibility"]
            visibility = post["visibility"]

            # Either public or friends only. cant be private
            if visibility == "public" or visibility == "unlisted":
                item["visibility"] = "PUBLIC" # both are technically public?
            else:
                item["visibility"] = "FRIENDS"

            item["unlisted"] = True if post["visibility"] == "unlisted" else False

            payload["items"].append(item)

        data = payload        

    except IndexError as e:
        print(e)
        data = "invalid"

    except Exception as e:
        print(e)
        data = "error"
    
    return jsonify(data)