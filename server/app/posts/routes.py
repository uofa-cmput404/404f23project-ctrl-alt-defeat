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
from ..utils import remote_funcs as rf

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
            if post['sender_host'] == 'https://cmput-average-21-b54788720538.herokuapp.com/api':
                try:                    
                    # print("checking")
                    new_item = rf.get_post('https://cmput-average-21-b54788720538.herokuapp.com/api/', post['sender_id'], post['object_id'], 'CtrlAltDefeat', 'string')
                    new_item["date_posted"] = post["date_received"]
                    payload.append(new_item)

                except Exception as e:
                    print("Api call error")
                    print(e)
                    pass # Skip if it somehow does not work

            elif post['sender_host'] == 'https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/':
                try:                
                    new_item = rf.get_post('https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/', post['sender_id'], post['object_id'], 'cross-server', 'password')                    
                    new_item["date_posted"] = post["date_received"]
                    payload.append(new_item)

                except Exception as e:
                    print("Api call error")
                    print(e)
                    pass # Skip if it somehow does not work
            
            elif post['sender_host'] == 'https://chimp-chat-1e0cca1cc8ce.herokuapp.com/':
                try:                    
                    new_item = rf.get_post('https://chimp-chat-1e0cca1cc8ce.herokuapp.com/api/', post['sender_id'], post['object_id'], 'cross-server', 'password')                    
                    new_item["date_posted"] = post["date_received"]
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
                        "WHERE post_id = %s AND ((VISIBILITY = 'PUBLIC' OR ((VISIBILITY = 'FRIENDS') AND (posts.author_id IN (SELECT author_followee FROM friends WHERE author_following = %s) OR posts.author_id = %s))) OR (VISIBILITY = 'private' and posts.author_id = %s))"

                # print("checking", post["object_id"])
                curr.execute(query, (post["recipient_id"], post["object_id"], post["recipient_id"], post["recipient_id"], post["recipient_id"]))

                row = curr.fetchone()        
                # print(row)        

                # If we can't find it anywhere else then the post has been deleted
                if row is not None:
                    local_result = dict(row)                    
                    payload.append(local_result)

        # # Convert 'date' strings to datetime objects
        # for item in payload:
        #     item['date_posted'] = datetime.strptime(item['date_posted'], '%Y-%m-%d')

        # # Sort the list of dicts by the 'date' key
        payload = sorted(payload, key=lambda x: x['date_posted'], reverse=True)
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
        print("Sending a new post:")
        request_data = request.get_json()
        author_id = request_data["author_id"]
        title = request_data["title"]
        content = request_data["content"]
        visibility = request_data["visibility"]
        content_type = request_data["content_type"]

        post_id = str(uuid.uuid4())

        # validate the content_type is of the following
        try:
            found = ["text/plain", "text/markdown", "application/base64", "image/png;base64",
                     "image/jpeg;base64"].index(content_type)
        except ValueError:
            print("Not a valid content type.")
            abort(412)

        # Check for image OR image post
        image_id = request_data["image_id"]

        if image_id == None:  # JSON `null` turns into Python `None`
            image_id = "NULL"  # Change for SQL syntax

        conn, curr = get_db_connection()

        # Insert post into local db

        query = "INSERT INTO posts (post_id, author_id, title, content_type, content, visibility) " \
                "VALUES (%s, %s, %s, %s, %s, %s)"

        # Use a parameterized query to insert values safely
        curr.execute(query,
                     (post_id, author_id, title, content_type, content, visibility))

        author_query = "SELECT github, username FROM authors WHERE author_id = %s"
        curr.execute(author_query, (author_id,))
        author_info = curr.fetchone()

        data = "successfully posted in local db"

        author_host = request.root_url
        author_display_name = author_info["username"]

        # Depending on visibility, send to specific
        # authors of local node (i.e. Ctrl+Alt+Defeat)
        if visibility == "PUBLIC":
            # Get all authors on local node
            recipient_query = "SELECT author_id FROM authors"
            curr.execute(recipient_query)
            localRecipients = curr.fetchall()
            localRecipients = [dict(i) for i in localRecipients]
            column = "author_id"

        elif visibility == "FRIENDS":
            # Find the local authors who are following the post author
            recipient_query = "SELECT author_following FROM " \
                              "friends WHERE author_followee = %s " \
                              "AND host = %s"
            curr.execute(recipient_query, (author_id, "local"))
            localRecipients = curr.fetchall()
            localRecipients = [dict(i) for i in localRecipients]
            
            # Also add post author to list (they should receive their own post!)
            localRecipients.append({"author_following": author_id})
            column = "author_following"

        elif visibility == "private" or visibility == "unlisted":
  
            # Only send to post author's inbox
            column = "author_id"
            localRecipients = [{column: author_id}]

        else:
            raise Exception("Invalid visibility value was given by NewPost.js: accepts (for remote nodes) 'PUBLIC', 'FRIENDS'; (for local node) 'private', 'unlisted'")
        
        print(localRecipients)
        for la in localRecipients:
            for key in la:
                key_au = key
            recipient_id = la[key_au]
   
            inbox_item_id = str(uuid.uuid4())
   
            inbox_query = "INSERT INTO inbox_items " \
                        "(inbox_item_id, sender_id, " \
                        "sender_display_name, sender_host, " \
                        "recipient_id, object_id, type) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"

            curr.execute(inbox_query, (inbox_item_id, author_id, author_display_name, author_host, recipient_id, post_id, "post"))
            print("Sent to local author", recipient_id)

        conn.commit()
        conn.close()

        data = "success"

    except Exception as e:

        print(e)
        data = str(e)
        abort(500, e)

    return jsonify(data)  # data

@bp.route('/posts/new/remote', methods=['POST'])
@basic_auth.login_required
def new_post_to_remote_nodes():
    data = ""
    try:
        # Retrieve post data from the request's JSON body
        # to get author_id, title, content, visibility, type
        print("Sending a new post:")
        request_data = request.get_json()
        author_id = request_data["author_id"]
        title = request_data["title"]
        content = request_data["content"]
        visibility = request_data["visibility"]
        content_type = request_data["content_type"]

        post_id = str(uuid.uuid4())

        # validate the content_type is of the following
        try:
            found = ["text/plain", "text/markdown", "application/base64", "image/png;base64",
                     "image/jpeg;base64"].index(content_type)
        except ValueError:
            print("Not a valid content type.")
            abort(412)

        # Check for image OR image post
        image_id = request_data["image_id"]

        if image_id == None:  # JSON `null` turns into Python `None`
            image_id = "NULL"  # Change for SQL syntax

        conn, curr = get_db_connection()

        # Get `github` and `displayName`
        author_query = "SELECT github, username FROM authors WHERE author_id = %s"
        curr.execute(author_query, (author_id,))
        author_info = curr.fetchone()


        # Package the body according to spec
        send_data = dict()
        send_data["type"] = "post"
        send_data["title"] = title
        send_data["id"] = request.root_url + "authors/" + author_id + "/posts/" + post_id
        send_data["source"] = send_data["id"] 
        send_data["origin"] = send_data["id"]
        send_data["description"] = ""
        send_data["contentType"] = content_type
        send_data["content"] = content
        send_data["author"] = dict()
        send_data["author"]["type"] = "author"
        send_data["author"]["id"] = request.root_url + "authors/" + author_id
        send_data["author"]["host"] = request.root_url
        send_data["author"]["displayName"] = author_info["username"]
        send_data["author"]["url"] = send_data["author"]["id"]
        if author_info["github"] == None:
            send_data["author"]["github"] = None
        else:
            send_data["author"]["github"] = "https://github.com/" + author_info["github"]
        send_data["author"]["profileImage"] = None
        send_data["categories"] = []
        send_data["comments"] = request.root_url + "authors/" + author_id + "/posts/" + post_id + "/comments"
        #send_data["commentsSrc"] = {} # `null` for now, will send as needed
        # Count = number of comments
        send_data["count"] = 0
        send_data["published"] = str(datetime.now().astimezone().replace(microsecond=0).isoformat())
        if visibility == "unlisted":
            send_data["visibility"] = "PUBLIC" # make unlisted post public but unlisted
            send_data["unlisted"] = True
        else:
            send_data["visibility"] = visibility   
            send_data["unlisted"] = False

        # Package body into json
        body = send_data

        # If the post visiblity is public, send out to
        # to the inboxes of all authors of remote nodes
        # (i.e. Ctrl+C and Ctrl+V, 21-Average)
        if visibility == "PUBLIC":
            # Get all authors from remote nodes
            ## Ctrl+C and Ctrl+V
            remoteAuthorsUrl = "https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/authors/"
            remoteAuthorsResp = requests.get(remoteAuthorsUrl, auth = ('cross-server','password'))
            remoteAuthorsCtrlCCtrlV = dict(remoteAuthorsResp.json())["items"]

            ## 21-Average
            remoteAuthorsUrl = "https://cmput-average-21-b54788720538.herokuapp.com/api/authors"
            remoteAuthorsResp = requests.get(remoteAuthorsUrl, auth = ('CtrlAltDefeat', 'string'))
            remoteAuthors21avg = dict(remoteAuthorsResp.json())["items"]

            ## Coding Monkeys
            remoteAuthorsUrl = "https://chimp-chat-1e0cca1cc8ce.herokuapp.com/authors/"
            remoteAuthorsResp = requests.get(remoteAuthorsUrl, auth = ('node-ctrl-alt-defeat','chimpchatapi'))
            remoteAuthorsCodingMonkeys = dict(remoteAuthorsResp.json())["items"]

            # Send to all authors
            ## Ctrl+C and Ctrl+V node
            for ra in remoteAuthorsCtrlCCtrlV:
                recipient_id = ra["id"].split('/')[-1]
                remoteInboxUrl = "https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/authors/" + recipient_id + "/inbox"
                remoteInboxResp = requests.post(remoteInboxUrl, json = body, auth = ('cross-server','password'))
                #print(remoteInboxResp.request.body) # Confirmed that `None` -> `null` 
                if remoteInboxResp.status_code != 200:
                    print("ERROR: code", remoteInboxResp, "at", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
                else:
                    print("Successfully sent post to", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
            
            ## 21-Average node
            specificBody = {"items": body} # specific body for 21-average
            for ra in remoteAuthors21avg:
                recipient_id = ra["id"].split('/')[-2]
                remoteInboxUrl = "https://cmput-average-21-b54788720538.herokuapp.com/api/authors/" + recipient_id + "/inbox/"
                remoteInboxResp = requests.post(remoteInboxUrl, json = specificBody, auth = ('CtrlAltDefeat', 'string'))
                if remoteInboxResp.status_code != 201:
                    print("ERROR: code", remoteInboxResp, "at", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
                else:
                    print("Successfully sent post to", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
            
            ## Coding-Monkeys node
            body["commentsSrc"] = {} # added to fit their spec
            for ra in remoteAuthorsCodingMonkeys:
                recipient_id = ra["id"].split('/')[-1]
                remoteInboxUrl = "https://chimp-chat-1e0cca1cc8ce.herokuapp.com/authors/" + recipient_id + "/inbox/"
                remoteInboxResp = requests.post(remoteInboxUrl, json = body, auth = ('node-ctrl-alt-defeat','chimpchatapi'))
                #print(remoteInboxResp.request.body) # Confirmed that `None` -> `null` 
                if remoteInboxResp.status_code != 200:
                    print("ERROR: code", remoteInboxResp, "at", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
                else:
                    print("Successfully sent post to", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
            
        elif visibility == "FRIENDS":
            # If friends-only post, check remote followers
            # and send to node

            # CHECK friends TABLE FOR REMOTE 
            # AUTHORS WHO FOLLOW THE POST AUTHOR
            friends_query = "SELECT author_following, host FROM " \
                            "friends WHERE author_followee = %s " \
                            "AND NOT host = %s"
            curr.execute(friends_query, (author_id, "local"))

            recipients = curr.fetchall()
            recipients = [dict(i) for i in recipients]

            # For each remote follower of the post author, 
            # send to the respective follower's inbox (depending on host)
            for recipient in recipients:
                recipient_host = recipient["host"]
                recipient_id = recipient["author_following"]

                if recipient_host == "https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/":
                    remoteInboxUrl = "https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/authors/" + recipient_id + "/inbox"
                    remoteInboxResp = requests.post(remoteInboxUrl, json = body, auth = ('cross-server','password'))
                    #print(remoteInboxResp.request.body) # Confirmed that `None` -> `null` 
                    if remoteInboxResp.status_code != 200:
                        print("ERROR: code", remoteInboxResp, "at", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
                    else:
                        print("Successfully sent post to", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
                
                elif recipient_host == "https://cmput-average-21-b54788720538.herokuapp.com/api": 
                    specificBody = {"items": body} # specific body for 21-average
                    recipient_id = ra["id"].split('/')[-2]
                    remoteInboxUrl = "https://cmput-average-21-b54788720538.herokuapp.com/api/authors/" + recipient_id + "/inbox/"
                    remoteInboxResp = requests.post(remoteInboxUrl, json = specificBody, auth = ('CtrlAltDefeat', 'string'))
                    if remoteInboxResp.status_code != 201:
                        print("ERROR: code", remoteInboxResp, "at", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
                    else:
                        print("Successfully sent post to", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
                    
                elif recipient_host == "https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/":
                    body["commentsSrc"] = {} # added to fit their spec
                    remoteInboxUrl = "https://chimp-chat-1e0cca1cc8ce.herokuapp.com/authors/" + recipient_id + "/inbox/"
                    remoteInboxResp = requests.post(remoteInboxUrl, json = body, auth = ('node-ctrl-alt-defeat','chimpchatapi'))
                    #print(remoteInboxResp.request.body) # Confirmed that `None` -> `null` 
                    if remoteInboxResp.status_code != 200:
                        print("ERROR: code", remoteInboxResp, "at", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
                    else:
                        print("Successfully sent post to", remoteInboxUrl, " response:", remoteInboxResp.content, "\n")
        else:
            print("Private or unlisted post detected, not sending to remote node inboxes. \n")

        conn.commit()
        conn.close()
        data = "success"

    except Exception as e:

        print(e)
        data = str(e)
        abort(500, e)

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
        #row = curr.execute(query, (post_id, author_id)).fetchone()
        if row is None:
            abort(404, "The post with this post_id does not exist.")
        print("Successfully found post.")

        if row["content_type"] == "text/plain" or row["content_type"] == "text/markdown":
            abort(404, "This is not an image.")
        if row["visibility"] != "PUBLIC":
            abort(403, "This post exists, but the image contained is only visible to specific users.")

        content_type = row["content_type"]
        content = row["content"]

        image_bytes = io.BytesIO(base64.b64decode(content))
        #final_message = f"data:{content_type},{content}"
        final_message = send_file(image_bytes, mimetype=content_type[:-7], max_age=0)
    except HTTPException as e:
        final_message = str(e)
        print(final_message)
    except Exception as e:
        print(e)
        abort(500, e)
    finally:
        curr.close()
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
                # "AND (visibility = 'PUBLIC' OR visibility = 'unlisted')"
                
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
        if visibility == "PUBLIC" or visibility == "unlisted":
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
        abort(500, e)
    
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
            if visibility == "PUBLIC" or visibility == "unlisted":
                item["visibility"] = "PUBLIC" # both are technically public?
            else:
                item["visibility"] = "FRIENDS"

            item["unlisted"] = True if post["visibility"] == "unlisted" else False

            payload["items"].append(item)

        data = payload        

    except IndexError as e:
        print(e)
        data = "invalid"
        abort(500, e)

    except Exception as e:
        print(e)
        data = "error"
        abort(500, e)
    
    return jsonify(data)