from . import bp
import json
from flask import request, g, jsonify, abort
import sqlite3
from ..dbase import get_db_connection
from random import randrange
from flask_bcrypt import Bcrypt

from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash
import uuid
import requests
import datetime
from .. import basic_auth



# Get all authors (REMOTE)
@bp.route('/authors/', methods=['GET'])
def get_authors():    
    page = request.args.get('page')
    size = request.args.get('size')
    data = ""
    try:
        conn, cur = get_db_connection()


        query = "SELECT * " \
                "FROM authors " \
                "ORDER BY author_id " \
                "LIMIT %s OFFSET %s"
        
        if page is not None:
            page = int(page)
        else: page = 1 # Set default 1
        
        if size is not None:
            size = int(size)
        else: size = 20 # Set default 20

        offset = (page - 1) * size
        cur.execute(query, (size, offset))
        row = cur.fetchall()
                
        res = [dict(i) for i in row]        

        data = dict()
        data["type"] = "authors"
        data["items"] = []
        
        for r in res:
            item = dict()
            item["type"] = "author"
            item["id"] = request.url_root + "api/authors/" + r["author_id"] 
            item["url"] = request.url_root + "api/authors/" + r["author_id"] 
            item["host"] = request.url_root
            item["displayName"] = r["username"]
            item["github"] = ("https://github.com/" + r["github"]) if r["github"] != None else None
            item["profileImage"] = None # TODO: implement profile pics
            data["items"].append(item)
        
        

    except Exception as e:
        print("Error getting authors: ", e)
        data = "error"
        abort(500, e)
    
    print("data here")
    return jsonify(data)

# Get a specific author (REMOTE)
@bp.route('/authors/<author_id>/', methods=['GET'])
def get_author(author_id):
    data = ""
    try:
        conn, cur = get_db_connection()


        query = "SELECT * " \
                "FROM authors " \
                "WHERE author_id = %s " \
                
        cur.execute(query, (author_id,))
        row = cur.fetchall()
        print(row)
        res = [dict(i) for i in row][0]
        item = dict()
        item["type"] = "author"
        item["host"] = request.url_root
        item["id"] = request.url_root + "api/authors/" + res["author_id"]
        item["url"] = request.url_root + "api/authors/" + res["author_id"]
        item["displayName"] = res["username"]
        item["github"] = "http://github.com/" + res["github"] if res["github"] is not None else None
        item["profileImage"] = None

        data = item

    except Exception as e:
        print("Error getting authors: ", e)
        data = "error"
        abort(500, e)
    
    return jsonify(data)

@bp.route('/authors/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    conn, cur = get_db_connection()

    cur.execute("SELECT author_id, password FROM authors WHERE username = %s", (username,))
    author = cur.fetchone()
    print(author)

    if author:
        stored_password = author['password']
        if check_password_hash(stored_password, password):
            result = {'message': 'Login successful', 'author_id': author['author_id']}
        else:
            result = {'message': 'Wrong Password'}
    else:
        result = {'message': 'User not found'}

    conn.close()

    return jsonify(result)


@bp.route('/authors/update_username', methods=['POST'])
def update_username():
    data = request.get_json()
    new_username = data.get('new_username')
    author_id = data.get('authorId')

    conn, curr = get_db_connection()

    try:
        curr.execute("SELECT author_id FROM authors WHERE username = %s", (new_username,))
        existing_username = curr.fetchone()

        if existing_username:
            return jsonify({'error': 'Username already exists'})

        curr.execute("UPDATE authors SET username = %s WHERE author_id = %s", (new_username, author_id))
        conn.commit()

        return jsonify({'message': 'Username updated successfully'})
    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the username.'})
    finally:
        conn.close()


@bp.route('/authors/update_password', methods=['POST'])
def update_password():
    data = request.get_json()
    new_password = data.get('new_password')
    author_id = data.get('authorId') 

    conn, curr = get_db_connection()    

    try:
        hashed_password = generate_password_hash(new_password).decode('utf-8')
        
        curr.execute("UPDATE authors SET password = %s WHERE author_id = %s", (hashed_password, author_id))
        conn.commit()        

        return jsonify({'message': 'Password updated successfully'})
    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the password.'})
    finally:
        conn.close()


# Get posts that the logged in author has liked 
@bp.route('/authors/<author_id>/liked', methods=['GET'])
def get_posts_liked(author_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE


    data = ""
    try:
        conn, curr = get_db_connection()

        query = "SELECT username " \
                "FROM authors " \
                "WHERE author_id = %s"         
        
        curr.execute(query, (author_id,))
        author = curr.fetchone()

        if author == None:
            abort(404, "Author not found")

        query = "SELECT l.post_id, p.author_id,  a.username, a.github " \
                "FROM likes l " \
                "JOIN posts p " \
                "ON p.post_id = l.post_id " \
                "JOIN authors a " \
                "ON a.author_id = l.like_author_id " \
                "WHERE " \
                "like_author_id = %s "
        
        curr.execute(query, (author_id,))
        likes = curr.fetchall()
        likes = [dict(i) for i in likes]
        
        payload = dict()
        payload["type"] = "liked"
        payload["items"] = []

        for like in likes:
            item = dict()
            item["@context"] = None
            item["summary"] = like["username"] + " Likes your post"
            item["type"] = "Like"
            item["author"] = dict()
                                    
            item["author"]["type"] = "author"
            item["author"]["id"] = request.root_url + "api/authors/" + like["author_id"]
            item["author"]["url"] = request.root_url + "api/authors/" + like["author_id"]
            item["author"]["host"] = request.root_url
            item["author"]["displayName"] = like["username"]
            item["author"]["profileImage"] = None
            item["author"]["github"] = "http://github.com/" + like["github"] if like["github"] is not None else None

            item["object"] = request.root_url + "authors/" + like["author_id"] + "/posts/" + like["post_id"]
            payload["items"].append(item)        

        data = payload

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Re-raise the exception to propagate it
        raise

    finally:
        # Close database connection in the finally block to ensure it's closed
        if conn:
            conn.close()
    
    return jsonify(data)

# Get a list of likes from other authors on AUTHOR_ID’s post POST_ID (REMOTE)
@bp.route('/authors/<author_id>/posts/<post_id>/likes', methods=['GET'])
def get_liked_posts(author_id, post_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE

    data = ""
    try:
        conn, cur = get_db_connection()

        query = "SELECT * " \
                "FROM likes l " \
                "JOIN authors a " \
                "ON l.like_author_id = a.author_id " \
                "WHERE " \
                "l.post_id = %s"
        
        cur.execute(query, (post_id,))
        likes = cur.fetchall()        

        res = [dict(i) for i in likes]
    
        data = dict()
        data["count"] = len(res)
        data["type"] = "likes"
        data["items"] = []
        
        for r in res:
            item = dict()

            item["@context"] = None # What is this?
            item["summary"] = r["username"] + " Likes your post"
            item["type"] = "Like"
            item["author"] = dict()
            item["author"]["type"] = "author"
            item["author"]["id"] = request.root_url + "api/authors/" + r["author_id"]
            item["author"]["url"] = request.root_url + "api/authors/" + r["author_id"]
            item["author"]["host"] = request.root_url
            item["author"]["displayName"] = r["username"]
            item["author"]["profileImage"] = None
            item["author"]["github"] = "http://github.com/" + r["github"] if r["github"] is not None else None

            item["object"] = request.root_url + "api/" + author_id + "/posts/" + post_id             
            data["items"].append(item)

        # data = json.dumps(data, indent=2)

        conn.commit()
        conn.close()


    except Exception as e:
        print("Getting likes error: ", e)
        data = "error"
        abort(500, e)
    
    return jsonify(data)

# (LOCAL/REMOTE)
@bp.route('/authors/<author_id>/inbox', methods=['POST'])
def send(author_id):
    request_data = request.get_json()
    print("payload:")
    print(request_data)
    print("sending the inbox item to", author_id)

    # In case remote node sends us a payload with `{'items': {'type' : '...', ...}}`
    if 'items' in request_data:
        request_data = request_data["items"]
    
    try:
        data = ""
        message_type = request_data["type"]

        if message_type == "Like":            
            likeAuthorId = request_data["author"]["id"].split('/')[-1]            
            likeHost = request_data["author"]["host"]
            displayName = request_data["author"]["displayName"]
            likedPost = request_data["object"].split('/')[-1]

            # Check what type of like it is, if it has /comments then it is a comment like
            
            if "/comments/" in request_data["object"]:
                inboxItemId = str(uuid.uuid4())
                likeId = str(uuid.uuid4()) 

                conn, curr = get_db_connection()
                post_url = request_data["object"].split("/")
                post_index = post_url.index("posts")
                post_id = post_url[post_index + 1]
                
                comments_index = post_url.index("comments")
                comment_id = post_url[comments_index + 1]

                # Check if the like already exists
                print("SELECT * FROM comment_likes WHERE like_comment_author_id = %s AND comment_id = %s", 
                            (likeAuthorId, comment_id))
                curr.execute("SELECT * FROM comment_likes WHERE like_comment_author_id = %s AND comment_id = %s", 
                            (likeAuthorId, comment_id))
                
                like = curr.fetchone()
                print(likeAuthorId, comment_id)
                print("Resulting:", like)
                if like:
                    print("here")
                    # Like exists, so unlike it
                    curr.execute("DELETE FROM comment_likes WHERE like_comment_author_id = %s AND comment_id = %s", 
                                (likeAuthorId, comment_id))
                    
                    conn.commit()
                    conn.close()
                else:
                    print("inserting")
                    # Like doesn't exist, so add it
                    comment_like_id = str(uuid.uuid4()) 
                    curr.execute("INSERT INTO comment_likes (comment_like_id, like_comment_author_id, comment_id, time_liked) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)", 
                                (comment_like_id, likeAuthorId, comment_id))
                    
                    inbox_query = "INSERT INTO inbox_items " \
                                "(sender_id, sender_host, " \
                                "sender_display_name, recipient_id, " \
                                "inbox_item_id, object_id, type) VALUES " \
                                "(%s, %s, %s, %s, %s, %s, %s)"
                    
                    
                    curr.execute(inbox_query, (likeAuthorId, request.root_url, displayName, author_id, inboxItemId, comment_like_id, "comment_like"))

                    conn.commit()
                    conn.close()
                    
                    data = "Liked comment successfully."
            
            else:                
                likeId = str(uuid.uuid4()) 
                inboxItemId = str(uuid.uuid4())

                conn, curr = get_db_connection()

                like_query = "INSERT INTO likes " \
                        "(like_id, like_author_id, " \
                        "post_id, time_liked) " \
                        "VALUES (%s, %s, %s, " \
                        "CURRENT_TIMESTAMP)"

                curr.execute(like_query, (likeId, likeAuthorId, likedPost))

                inbox_query = "INSERT INTO inbox_items " \
                            "(sender_id, sender_host, " \
                            "sender_display_name, recipient_id, " \
                            "inbox_item_id, object_id, type) VALUES " \
                            "(%s, %s, %s, %s, %s, %s, %s)"
                
                
                curr.execute(inbox_query, (likeAuthorId, request.root_url, displayName, author_id, inboxItemId, likeId, "Like"))

                conn.commit()
                conn.close()

                data = "like success"

        elif message_type == "Follow":
            actor_host = request_data["actor"]["host"]
            receiver = request_data["object"]["id"].split("/")

            if receiver[-1] == "":
                receiver.pop()
            receiver = receiver[-1]

            sender = request_data["actor"]["id"].split("/")[-1]

            conn, curr = get_db_connection()

            # Check if already following
            curr.execute("SELECT * FROM friends WHERE author_following = %s AND author_followee = %s", (sender, receiver))
            existing_friendship = curr.fetchone()

            if existing_friendship:
                conn.close()
                return jsonify({'message': 'Already following'})

            # Check if follow request already sent
            curr.execute("SELECT * FROM follow_requests WHERE author_send = %s AND author_receive = %s", (sender, receiver))
            existing_request = curr.fetchone()

            if existing_request:
                conn.close()
                return jsonify({'message': 'Follow request already sent'})
            
            query = "INSERT INTO follow_requests " \
                    "(author_receive, author_send, host) " \
                    "VALUES (%s, %s, %s)"

            curr.execute(query, (receiver, sender, actor_host))

            conn.commit()
            conn.close()

            data = "follow sent"

        elif message_type == "post":
            conn, curr = get_db_connection()

            sender_host = request_data["author"]["host"]

            postUrlComponents = request_data["origin"].split('/')
            # Remove extra slash if there is a slash at end of url
            if postUrlComponents[-1] == "":
                postUrlComponents.pop()

            post_id = postUrlComponents[-1]
            sender_id = postUrlComponents[-3]
            sender_display_name = request_data["author"]["displayName"]

            inbox_item_id = str(uuid.uuid4())

            # Store host, sender, recipient, post url to inbox table
            # (note we are not storing post content)

            inbox_query = "INSERT INTO inbox_items " \
                        "(inbox_item_id, sender_id, " \
                        "sender_display_name, sender_host, " \
                        "recipient_id, object_id, type) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            curr.execute(inbox_query, (inbox_item_id, sender_id, sender_display_name, sender_host, author_id, post_id, message_type))

            conn.commit()
            conn.close()

        elif message_type == "comment":     
            conn, curr = get_db_connection()                               
            #Check if the authors are friends
      
            comment_author_id = request_data["author"]["id"].split("/")[-1]
          
            check_friends_query = """
                SELECT CASE 
                    WHEN EXISTS (
                        SELECT 1 FROM friends 
                        WHERE author_followee = %s AND author_following = %s
                    ) THEN 'private'
                    ELSE 'PUBLIC'
                END AS status
            """

            curr.execute(check_friends_query, (author_id, comment_author_id))
            status = dict(curr.fetchone())['status']
            
            if author_id == comment_author_id:
                status = 'private'

            comment_id = str(uuid.uuid4()) 

            query = "INSERT INTO comments " \
                "(comment_id, comment_author_id, " \
                "post_id, author_id, comment_text, status, date_commented) " \
                "VALUES (%s, %s, %s, %s, %s, %s ,CURRENT_TIMESTAMP)" 

     
            print(request_data)
      
            post_url = request_data["object"]["id"].split("/")
      
            post_index = post_url.index("posts")
      
            post_id = post_url[post_index + 1]
      
            #print(post_id)
            curr.execute(query, (comment_id, comment_author_id,  post_id, author_id, request_data["object"]["comment"], 'PUBLIC'))
  
            inbox_query = "INSERT INTO inbox_items " \
                            "(sender_id, sender_host, " \
                            "sender_display_name, recipient_id, " \
                            "inbox_item_id, object_id, type) VALUES " \
                            "(%s, %s, %s, %s, %s, %s, %s)"
         
            inboxItemId = str(uuid.uuid4())
  
            curr.execute(inbox_query, (comment_author_id,  request_data["author"]["host"], request_data["author"]["displayName"], author_id, inboxItemId, comment_id, "comment"))

            conn.commit()
            conn.close()

            data = "Successfully added comment."        

        else:
            print("Type not recognized")
            raise(Exception("'type' must be 'post', 'comment', 'Like', or 'Follow'"))

    except Exception as e:
        print("send error: ", e)
        abort(500, e)
        

    return jsonify(data)

# MAKE POSTS
@bp.route('/authors/<author_id>/inbox', methods=['GET'])
def get_inbox_items(author_id):
    data = {}

    conn, cur = get_db_connection()
    data["type"] = "inbox"
    data["author"] = request.root_url + "api/authors/" + author_id
    data["items"] = []
    
    try:
        query = "SELECT * FROM inbox_items "\
                "WHERE recipient_id = %s " \
                "AND sender_id != %s"
        
        cur.execute(query, (author_id, author_id))
        row = cur.fetchall()
        inbox_items = [dict(i) for i in row]        
        print(inbox_items)
        for item in inbox_items: 
            print(item["type"])           
            if item["type"] == "Like":
                data_item = dict()                
                data_item["type"] = item["type"]
                data_item["author"] = item["sender_id"]
                data_item["displayName"] = item["sender_display_name"]
                data_item["summary"] =  item["sender_display_name"] + " liked your post."
                data_item["date_received"] =  item["date_received"]

                query = "SELECT * FROM likes " \
                        "WHERE like_id = %s "
                
                cur.execute(query, (item["object_id"],))
                row = cur.fetchone()

                if row is not None:
                    row = dict(row)
                
                    data_item["post_id"] = row["post_id"]
                    data["items"].append(data_item)
            
            if item["type"] == "comment":
                data_item = dict()              
                data_item["type"] = item["type"]
                data_item["author"] = item["sender_id"]
                data_item["displayName"] = item["sender_display_name"]
                data_item["summary"] =  item["sender_display_name"] + " commented on your post: "
                data_item["date_received"] =  item["date_received"]

                query = "SELECT * FROM comments " \
                        "WHERE comment_id = %s "
                # print("comment", item["object_id"])
                
                cur.execute(query, (item["object_id"],))
                row = cur.fetchone()
                                
                if row is not None:
                    row = dict(row)
                
                    data_item["post_id"] = row["post_id"]
                    data_item["comment"] = row["comment_text"]
                    data["items"].append(data_item)
      
            if item["type"] == "comment_like":
                print("comment_like")
                data_item = dict()                
                data_item["type"] = item["type"]
                data_item["author"] = item["sender_id"]
                data_item["displayName"] = item["sender_display_name"]
                data_item["summary"] =  item["sender_display_name"] + " liked your comment."
                data_item["date_received"] =  item["date_received"]

                query = "SELECT * FROM comment_likes " \
                        "WHERE comment_like_id = %s "
                
                cur.execute(query, (item["object_id"],))
                row = cur.fetchone()

                if row is not None:
                    row = dict(row)
                    
                    # Grab the original post
                    query = """SELECT * FROM comments
                            JOIN posts
                            ON posts.post_id = comments.post_id
                            WHERE comment_id = %s"""
                    
                    cur.execute(query, (row["comment_id"],))
                    row = cur.fetchone()

                    if row is not None:
                        row = dict(row)
                        data_item["post_id"] = row["post_id"]
                        data["items"].append(data_item)

            if item["type"] == "share":
                print("share")
                data_item = dict()   
              
                data_item["type"] = item["type"]
          
                data_item["author"] = item["sender_id"]
        
                data_item["displayName"] = item["sender_display_name"]
          
                data_item["summary"] =  item["sender_display_name"] + " share a post to you."
          
                data_item["date_received"] =  item["date_received"]
                

                data_item["post_id"] = item["object_id"]
          
                data["items"].append(data_item)
           
                
      
            data["items"] = sorted(data["items"], key=lambda x: x['date_received'], reverse=True)            

    except Exception as e:
        print(e)
        abort(500, e)        

    return jsonify(data)  # data

@bp.route('/authors/<author_id>/inbox/unlike', methods=['DELETE'])
# DELETE LIKE ON A POST
def delete_like(author_id):
    request_data = request.get_json()
    likeAuthorId = request_data["author"]["id"].split('/')[-1]
    likeHost = request_data["author"]["host"]
    likedPost = request_data["object"].split('/')[-1]

    
    data = ""
    try:
        conn, curr = get_db_connection()

        get_like_id_query = "SELECT like_id FROM likes " \
                            "WHERE like_author_id = %s " \
                            "AND post_id = %s"
        
        curr.execute(get_like_id_query, (likeAuthorId, likedPost))
        likeId = curr.fetchone()["like_id"]
        print("likeid",likeId)

        like_query = "DELETE FROM likes " \
                "WHERE like_author_id = %s AND post_id = %s"
        
        curr.execute(like_query, (likeAuthorId, likedPost))

        inbox_query = "DELETE FROM inbox_items " \
                    "WHERE type = 'Like' AND sender_id = %s " \
                    "AND sender_host = %s AND object_id = %s"
        curr.execute(inbox_query, (likeAuthorId, likeHost, likeId))

        data = "success"

        conn.commit()
        conn.close()
    except Exception as e:
        print("liked error: ", e)
        data = "error"
    return jsonify(data)



# REMOTE
@bp.route('/authors/<author_id>/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(author_id, post_id):    
    comment_author_id = request.args.get('comment_author_id')
    page = request.args.get('page')
    size = request.args.get('size')

    if not comment_author_id:
        comment_author_id = author_id

    try:
        
        conn, cursor = get_db_connection()
        print("author:", comment_author_id)

        query = """

            SELECT DISTINCT i.sender_display_name, c.comment_text,c.comment_author_id, c.comment_id, c.date_commented, a.github,
                EXISTS (
                    SELECT 1 FROM comment_likes cl 
                    WHERE cl.comment_id = c.comment_id 
                    AND cl.like_comment_author_id = %s
                ) AS isLikedByCurrentUser
            FROM comments c
            INNER JOIN inbox_items i ON c.comment_author_id = i.sender_id
            LEFT JOIN authors a ON c.comment_author_id = a.author_id
            WHERE c.post_id = %s
            AND c.author_id = %s
            AND (
                (c.status = 'PUBLIC') OR
                (c.status = 'private' AND c.comment_author_id = %s) OR
                (c.status = 'private' AND c.author_id = %s)
            )
            LIMIT %s OFFSET %s
        """

        if page is not None:
            page = int(page)
        else: page = 1 # Set default 1
        
        if size is not None:
            size = int(size)
        else: size = 20 # Set default 20

        offset = (page - 1) * size
        cursor.execute(query, (comment_author_id, post_id, author_id, comment_author_id, comment_author_id, size, offset))
        comment_info = cursor.fetchall()
        
        comment_info = [dict(i) for i in comment_info]
        print(comment_info)
        conn.close()


        comments_list = [
            {
                "type":"comment",
                "author":{
                    "type":"author",
                    # ID of the Author (UUID)
                    "id":comment['comment_author_id'],
                    # url to the authors information
                    "url":request.url_root + 'api/authors/' + author_id,
                    "host":request.url_root,
                    "displayName":comment['sender_display_name'],
                    # HATEOS url for Github API
                    "github": comment['github'],
                    #set profileImage to None
                    "profileImage": None
                },
                'comment': comment['comment_text'], 
                "contentType":"text/markdown",
                "published":comment['date_commented'], 
                'id': comment['comment_id'],
                'isLikedByCurrentUser': comment['islikedbycurrentuser']
            } for comment in comment_info
        ]
        comments_total = {"type":"comments","page":page, "size":size, "post":request.url_root+'api/authors/' + author_id+'/posts/' + post_id, "id": post_id, 'items': comments_list}
        return jsonify(comments_total)

    except Exception as e:
        print("Getting comments error: ", e)
        return jsonify({'error': str(e)}), 500



@bp.route('/authors/<author_id>/posts/<post_id>/comments', methods=['POST'])
def send_comments(author_id, post_id):
    # Get attributes from HTTP body

    request_data = request.get_json()
    comment_author_id = request_data["comment_author_id"]
    comment_text = request_data["comment_text"]


    # Create comment_id ID with uuid
    
    comment_id = str(uuid.uuid4()) 

    data = ""
    try:
        conn, cur = get_db_connection()

        #Check if the authors are friends
        check_friends_query = """
            SELECT CASE 
                WHEN EXISTS (
                    SELECT 1 FROM friends 
                    WHERE author_followee = %s AND author_following = %s
                ) THEN 'private'
                ELSE 'PUBLIC'
            END AS status
        """

        cur.execute(check_friends_query, (author_id, comment_author_id))
        status = dict(cur.fetchone())['status']
        
        # print(status)
        query = "INSERT INTO comments " \
                "(comment_id, comment_author_id, " \
                "post_id, author_id, comment_text, status, date_commented) " \
                "VALUES (%s, %s, %s, %s, %s, %s ,CURRENT_TIMESTAMP)" 
        cur.execute(query, (comment_id, comment_author_id, post_id, author_id, comment_text, status))


        data = "success"

        conn.commit()

        conn.close()

    except Exception as e:
        print("comment error: ", e)
        data = "error"
    
    return data

@bp.route('/authors/<author_id>/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_comment(author_id, post_id, comment_id):
    try:
        conn, cur = get_db_connection()

        # SQL query to delete all likes associated with the comment
        delete_likes_query = "DELETE FROM comment_likes WHERE comment_id = %s"
        cur.execute(delete_likes_query, (comment_id,))

        # SQL query to delete the comment
        delete_comment_query = "DELETE FROM comments WHERE comment_id = %s AND author_id = %s AND post_id = %s"
        cur.execute(delete_comment_query, (comment_id, author_id, post_id))

        # Commit the changes
        conn.commit()
        conn.close()
        return {"status": "success"}, 200
    except Exception as e:
        # Roll back the transaction in case of error
        if conn:
            conn.rollback()
        print("Error deleting comment: ", e)
        return {"status": "error", "message": str(e)}, 500





# Get Github username of author
@bp.route('/authors/github/<author_id>', methods=['GET'])
def get_github(author_id):
    # TODO: Check specification regarding private posts, right now the spec specifies "public things AUTHOR_ID liked"
    # Currently, this function pulls ALL post_id's of the posts that AUTHOR_ID has liked 
    # POSSIBLE SECURITY ISSUE

    data = ""
    try:
        conn, curr = get_db_connection()

        query = "SELECT github " \
                "FROM authors WHERE " \
                "author_id = %s"
        
        curr.execute(query, (author_id,))
        row = curr.fetchone()
        
        # row = [dict(row) for row in row]

        # data = json.dumps(row, indent=4, sort_keys=True, default=str)
        # print(data)
        data = row
        # if row is not None:
        #     row_values = [str(value) for value in row]
        #     row_string = ', '.join(row_values)
        #     data = row_string

    except Exception as e:
        print("Getting github username error: ", e)
        data = "error"
    
    return jsonify(data)


@bp.route('/authors/github', methods=['POST'])
# Set Github username
def update_github():
    request_data = request.get_json()    
    github = request_data["github"]
    author_id = request_data["author_id"]
    
    data = ""
    try:
        conn, curr = get_db_connection()        
        query = "UPDATE authors SET github = %s " \
                "WHERE author_id = %s"
        
        curr.execute(query, (github,author_id))

        data = "success"

        conn.commit()
        conn.close()
    except Exception as e:
        print("Error trying to update github username: ", e)
        data = "error"
    return jsonify(data)    


@bp.route('/authors/<author_id>/posts/<post_id>/comments/<comment_id>/toggle-like', methods=['POST'])
def toggle_like(author_id, post_id, comment_id):
    request_data = request.get_json()
    like_comment_author_id = request_data["like_comment_author_id"]

    try:
        conn, cursor = get_db_connection()


        # Check if the like already exists
        cursor.execute("SELECT * FROM comment_likes WHERE like_comment_author_id = %s AND comment_id = %s", 
                       (like_comment_author_id, comment_id))
        
        like = cursor.fetchone()
        

        if like:
            # Like exists, so unlike it
            cursor.execute("DELETE FROM comment_likes WHERE like_comment_author_id = %s AND comment_id = %s", 
                           (like_comment_author_id, comment_id))
        else:
            # Like doesn't exist, so add it
            cursor.execute("INSERT INTO comment_likes (like_comment_author_id, comment_id, time_liked) VALUES (%s, %s, CURRENT_TIMESTAMP)", 
                           (like_comment_author_id, comment_id))

        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Error toggling like: ", e)
        return jsonify({"error": str(e)}), 500




@bp.route('/authors/<author_id>/posts/<post_id>/comments/<comment_id>/likes', methods=['GET'])


def get_comments_likes(comment_id):
    try:
        conn, cursor = get_db_connection()
        
        query = """
            SELECT a.username, c.time_liked
            FROM comment_likes c
            INNER JOIN authors a ON c.like_comment_author_id = a.author_id
            WHERE c.comment_id = %s
        """

        cursor.execute(query, (comment_id ))
        comment_info = cursor.fetchall()
        conn.close()

        comment_likes_list = [{'like_comment_author_id':comment[0],'time_liked': comment[1]} for comment in comment_info]
        return jsonify({'comment_likes': comment_likes_list})

    except Exception as e:
        print("Getting comments error: ", e)
        return jsonify({'error': str(e)}), 500
    
@bp.route('/authors/<author_id>/posts/<post_id>/likes/count', methods=['GET'])
def get_post_likes_count(author_id, post_id):
    try:
        conn, curr = get_db_connection()

        # First, check the visibility of the post
        visibility_query = "SELECT visibility FROM posts WHERE post_id = %s"
        curr.execute(visibility_query, (post_id,))
        visibility_result = curr.fetchone()
        print("this is visibility_result")
        print(visibility_result)
        if not visibility_result:
            return jsonify({"error": "Post not found"}), 404

        if visibility_result['visibility'] == 'FRIENDS':
            # If visibility is 'FRIENDS', count the likes
            likes_query = "SELECT COUNT(*) as count FROM likes WHERE post_id = %s"
            curr.execute(likes_query, (post_id,))
            likes_count = curr.fetchone()['count']

            return jsonify({"numLikes": likes_count})
        else:
            # If visibility is not 'FRIENDS', return null
            return jsonify({"numLikes": None})

    except Exception as e:
        print("Error getting post likes count: ", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


@bp.route('/posts/<post_id>/share', methods=['POST'])
def share_post(post_id):
    try:
        loginUser_id = request.args.get('loginUser_id')
        request_data = request.get_json()
        share_option = request_data.get('share_option')  # 'PUBLIC' or 'FRIENDS'

        if not loginUser_id:
            return jsonify({"error": "Login user ID is required"}), 400

        conn, curr = get_db_connection()

      
        # Fetch the sender's display name
        curr.execute("SELECT username FROM authors WHERE author_id = %s", (loginUser_id,))
        sender = curr.fetchone()
        if not sender:
            return jsonify({"error": "Sender not found"}), 404
        sender_display_name = sender['username']
      
        # Determine recipients based on share_option
        if share_option == 'PUBLIC':
            # Fetch all authors
            curr.execute("SELECT author_id FROM authors")
            recipients = curr.fetchall()
        else:
            # Fetch only friends
            curr.execute("SELECT author_following FROM friends WHERE author_followee = %s AND host = 'local'", (loginUser_id,))
            recipients = curr.fetchall()

        # Insert into inbox_items for each recipient
        for recipient in recipients:
            recipient_id = recipient['author_following'] if share_option == 'FRIENDS' else recipient['author_id']
            inbox_item_id = str(uuid.uuid4())
            curr.execute("""
                INSERT INTO inbox_items (inbox_item_id, sender_id, sender_display_name, sender_host, recipient_id, object_id, type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (inbox_item_id, loginUser_id, sender_display_name, request.url_root, recipient_id, post_id, 'share'))

        conn.commit()

        return jsonify({"message": "Post shared successfully", "post_id": post_id}), 201

    except Exception as e:
        print("Error sharing post: ", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
