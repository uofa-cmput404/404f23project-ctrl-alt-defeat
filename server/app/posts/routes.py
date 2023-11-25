from app.posts import bp
import json

from app.dbase import get_db_connection

from flask import request, abort
from werkzeug.exceptions import HTTPException

from requests.auth import HTTPBasicAuth

from random import randrange
import sqlite3
from datetime import datetime, timezone
import requests
import uuid

# Hard coded for now
HOST = "http://127.0.0.1:5000"

@bp.route("/posts/restricted", methods=["GET"])
def get_restricted_users():    
    post_id = request.args.get('post_id')
    
    try:
        conn = get_db_connection()   
        # print(post_id)
        query = "SELECT username " \
                "FROM post_restrictions " \
                "INNER JOIN authors on post_restrictions.restricted_author_id = authors.author_id " \
                "WHERE post_id = ?"
        
        posts = conn.execute(query, (post_id, )).fetchall()                                        

        data = json.dumps([dict(i) for i in posts])
        print(data)

        conn.commit()
        conn.close()
        
    
    except Exception as e:
        print(e)
        data = "error"

    return data # data



@bp.route("/posts/restrict", methods=["POST"])
def restrict_user():
    request_data = request.get_json()
    post_id = request_data['post_id']
    username = request_data['username']
    
    data = ""

    try:
        # print(post_id, privacy)
        conn = get_db_connection()        
        
        # Grab the username first
        query = "SELECT author_id FROM authors WHERE username = ?"

        # Use a parameterized query to insert values safely
        result = conn.execute(query,
                    (username, )).fetchall()

        if len([dict(i) for i in result]) == 0:
            print("User not exist")
            return "not_exists"
            
        author_id = [dict(i) for i in result][0]['author_id']
        
        query = "INSERT INTO post_restrictions (post_id, restricted_author_id) " \
                    "VALUES (?, ?)"
        
        # # Use a parameterized query to insert values safely
        conn.execute(query,
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


@bp.route("/posts/unrestrict/<post_id>/<username>", methods=["DELETE"])
def unrestrict_user(post_id, username):    
    print(post_id, username)
    data = ""

    try:
        query = "SELECT author_id FROM authors WHERE username = ?"
        # # print(post_id, privacy)
        conn = get_db_connection()        

        # Use a parameterized query to insert values safely
        result = conn.execute(query,
                    (username, )).fetchall()

        if len([dict(i) for i in result]) == 0:
            print("User not exist")
            return "not_exists"
            
        author_id = [dict(i) for i in result][0]['author_id']
        
        query = "DELETE FROM post_restrictions " \
                "WHERE post_id = ? AND restricted_author_id = ?"

        # Use a parameterized query to insert values safely
        result = conn.execute(query, (post_id, author_id))
        
        conn.commit()
        conn.close()                
        
    except Exception as e:        
        print(e)
        data = "error"

    return data # data

@bp.route("/posts/visibility", methods=["POST"])
def change_visibility():
    request_data = request.get_json()
    post_id = request_data['post_id']
    visibility = request_data['visibility']
    
    data = ""

    try:
        # print(post_id, privacy)
        conn = get_db_connection()
        query = "UPDATE posts " \
                "SET visibility = ? " \
                "WHERE post_id = ? "
        conn.execute(query, (visibility, post_id))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route("/posts/delete", methods=["POST"])
def delete_post():
    request_data = request.get_json()
    post_id = request_data['post_id']
    data = ""

    try:
        conn = get_db_connection()
        query = f"DELETE FROM posts " \
                f"WHERE post_id = ? "
        conn.execute(query, (post_id, ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route('/posts/manage', methods=['GET'])
def get_my_posts():
    data = ""
    try:
        # Retrieve data from the request's JSON body         
        author_id = request.args.get('author_id')           
        conn = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public
        query = "SELECT * FROM posts " \
                "WHERE posts.author_id = ? " \
                "ORDER by date_posted DESC"
        
        posts = conn.execute(query, (author_id, )).fetchall()                                
        print(posts)
        conn.commit()
        conn.close()

        data = json.dumps([dict(i) for i in posts])
        
    except Exception as e:
        print("Something went wrong")
        print(e)
        data = str(e)

    return data # data

@bp.route('/posts', methods=['GET'])
def index():
    data = ""
    try:
        # Retrieve data from the request's JSON body
        print("data")        
        author_id = request.args.get('author_id')        
        # print(author_id)
        conn = get_db_connection()
        
        # Get all the posts from people who I'm following + posts who are public + posts that are mine
        # Do not include posts that I'm restricted from
        query = "SELECT posts.author_id, username, posts.post_id, date_posted, title, content_type, content, image_id, visibility " \
                "FROM posts " \
                "INNER JOIN authors ON posts.author_id = authors.author_id " \
                "WHERE " \
                    "(posts.visibility = 'public' " \
                    "OR posts.author_id = ? " \
					 "OR(posts.visibility = 'friends-only' AND posts.author_id IN (SELECT author_followee FROM friends WHERE author_following = ?))) " \
                    "AND post_id NOT IN (SELECT post_id FROM post_restrictions WHERE restricted_author_id =  ?) " \
                "ORDER BY date_posted DESC; " 
        
        row = conn.execute(query, (author_id, author_id, author_id)).fetchall()                                
        posts = [dict(i) for i in row]

        try:
            url = "https://cmput-average-21-b54788720538.herokuapp.com/api/posts"

            # Replace 'your_username' and 'your_password' with your actual credentials
            response = requests.get(url, auth=HTTPBasicAuth('CtrlAltDefeat', 'string'))
        
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content
                res = response.json()
                print(res["results"])
                # Convert api spec to our format
                for r in res["results"]:
                    item = dict()
                    item["author_id"] = r["author"]["id"]
                    item["username"] = r["displayName"] if "displayName" in r else None
                    item["post_id"] = r["id"]
                    item["title"] = r["title"]
                    item["content_type"] = r["contentType"]
                    item["content"] = r["content"]
                    item["date_posted"] = r["published"]
                    item["visibility"] = r["visibility"]

                    posts.append(item)
            else:
                # Print an error message if the request was not successful
                print(f"Error: {response.status_code}")
        
        except Exception as e:
            print(e)
            data = str(e)

        data = posts

    except Exception as e:
        print(e)
        data = str(e)

    return data # data

# MAKE POSTS
@bp.route('/posts/new', methods=['POST'])
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

        conn = get_db_connection()

        query = "INSERT INTO posts (post_id, author_id, title, content_type, content, image_id, visibility) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?)"

        # Use a parameterized query to insert values safely
        conn.execute(query,
                     (post_id, author_id, title, content_type, content, image_id, visibility))

        conn.commit()
        conn.close()

        data = "success"

    except Exception as e:

        print(e)
        data = str(e)

    return data  # data


@bp.route('/authors/<author_id>/<post_id>/image/', methods=['GET'])
def get_image(author_id, post_id):
    conn = get_db_connection()
    final_message = "Nothing happened."
    # check if image exists
    try:
        query = "SELECT img_id, content_type from posts WHERE (post_id = ? AND img_id IS NOT NULL AND author_id = ?);"
        cursor = conn.cursor()
        conn.execute(query, (post_id, author_id))
        img_id = cursor.fetchone()
        if img_id[0] is None:
            abort(404, "The post with this image id does not exist.")
        print("Successfully found the post with this image id.")

        query = "SELECT img_url,visibility FROM image_post WHERE img_id = ?;"

        conn.execute(query, (img_id[0],))
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
    conn = get_db_connection()
    try:
        # check if the post exists
        to_find = (post_id,)
        print(f"Attempting to find post with {post_id}")
        cursor = conn.cursor()
        query = "SELECT * FROM posts WHERE post_id = ?;"
        conn.execute(query, to_find)
        exists = cursor.fetchall()
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

        query = "UPDATE posts SET title = ?, content_type = ?,content = ?, image_id = ?, visibility = ? WHERE post_id = ? AND author_id = ?;"
        conn.execute(query, (title, content_type, content, image_id, visibility, post_id, author_id))
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

@bp.route("/authors/<author_id>/posts/<post_id>", methods=["GET"])
# Gets an individual post
def get_post(author_id,post_id):    
    conn = get_db_connection()
    data = ""
    print(post_id)
    try:
        query = "SELECT * FROM posts " \
                "WHERE post_id = ? " \
                "AND (visibility = 'public' OR visibility = 'unlisted')"
        
        row = conn.execute(query, (post_id, )).fetchall()                                        
        
        post = [dict(i) for i in row][0]        

        query = "SELECT * FROM authors " \
                "WHERE author_id = ? " 
        
        row = conn.execute(query, (author_id, )).fetchone()                 

        item = dict()
        item["type"] = "post"
        item["id"] = HOST + "/authors/" + post["author_id"] + "/posts/" + post["post_id"]
        
        # No idea what these are, skip for now
        item["source"] = None
        item["origin"] = None
        item["description"] = None
        item["contentType"] = post["content_type"]        
        
        author_item = dict()
        author_item["type"] = "author"
        author_item["host"] = HOST
        author_item["id"] = HOST + row["author_id"]
        author_item["url"] = HOST + row["author_id"]
        author_item["displayName"] = row["username"]
        author_item["github"] = row["github"]
        author_item["profileImage"] = None

        item["author"] = author_item

        # We don't have these rn
        item["categories"] = None
        item["comments"] = None
        item["commentsSrc"] = None

        input_datetime = datetime.strptime(post["date_posted"], "%Y-%m-%d %H:%M:%S")
        
        # Convert datetime object to ISO 8601 format with UTC offset
        item["published"] = input_datetime.replace(tzinfo=timezone.utc).isoformat()

        item["visibility"] = post["visibility"].upper()
        item["unlisted"] = True if post["visibility"] == "unlisted" else False

        data = json.dumps(item)
        print(data)

    except IndexError as e:
        print(e)
        data = "invalid"

    except Exception as e:
        print(e)
        data = "error"
    
    return data 

@bp.route("/authors/<author_id>/posts/", methods=["GET"])
# Gets most recent post from author AUTHOR_ID
def get_posts(author_id):    
    conn = get_db_connection()
    data = ""
    try:
        query = "SELECT * FROM posts " \
                "WHERE author_id = ? " \
                "AND (visibility = 'public') " \
                "ORDER BY date_posted " \
        
        row = conn.execute(query, (author_id, )).fetchall()                                        
        
        posts = [dict(i) for i in row]    

        payload = dict()
        payload["type"] = "authors"
        payload["items"] = []

        query = "SELECT * FROM authors " \
                "WHERE author_id = ? " 
        
        author = conn.execute(query, (author_id, )).fetchone()            

        for post in posts:
            item = dict()
            item["type"] = "post"
            item["id"] = HOST + "/authors/" + post["author_id"] + "/posts/" + post["post_id"]
            
            # No idea what these are, skip for now
            item["source"] = None
            item["origin"] = None
            item["description"] = None
            item["contentType"] = post["content_type"]        
            
            author_item = dict()
            author_item["type"] = "author"
            author_item["host"] = HOST
            print(post)
            author_item["id"] = HOST + "/" + post["author_id"]
            author_item["url"] = HOST + "/" + post["author_id"]
            author_item["displayName"] = author["username"]
            author_item["github"] = HOST + "/" + author["github"]
            author_item["profileImage"] = None

            item["author"] = author_item

            # We don't have these rn
            item["categories"] = None
            item["comments"] = None
            item["commentsSrc"] = None

            input_datetime = datetime.strptime(post["date_posted"], "%Y-%m-%d %H:%M:%S")
            
            # Convert datetime object to ISO 8601 format with UTC offset
            item["published"] = input_datetime.replace(tzinfo=timezone.utc).isoformat()

            item["visibility"] = post["visibility"].upper()
            item["unlisted"] = True if post["visibility"] == "unlisted" else False

            payload["items"].append(item)

        data = json.dumps(payload)        

    except IndexError as e:
        print(e)
        data = "invalid"

    except Exception as e:
        print(e)
        data = "error"
    
    return data 
