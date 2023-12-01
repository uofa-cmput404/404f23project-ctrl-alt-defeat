from . import bp
from flask import request, g, jsonify
import sqlite3
from ..dbase import get_db_connection
import flask
import requests


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@bp.route('/follow/usersearch', methods=['GET'])
def user_search():
    search_query = request.args.get('query')
    if not search_query:
        return jsonify({'users': []})

    conn, cursor = get_db_connection()

    cursor.execute("SELECT author_id, username FROM authors WHERE username LIKE %s", ('%' + search_query + '%',))
    users = cursor.fetchall()
    users = [dict(row) for row in users]

    if users:        
        user_list = [{'id': user["author_id"], 'username': user["username"]} for user in users]
        return jsonify({'users': user_list})
    else:
        return jsonify({'users': []})
    
@bp.route('/follow/follow_request', methods=['POST'])
def follow_request():
    data = request.get_json()
    author_send = data.get('author_send')
    author_receive = data.get('author_receive')

    conn, cursor = get_db_connection()   

    cursor.execute("SELECT * FROM friends WHERE author_following = %s AND author_followee = %s", (author_send, author_receive))
    existing_friendship = cursor.fetchone()

    if existing_friendship:
        return jsonify({'message': 'Already following'})

    cursor.execute("SELECT * FROM follow_requests WHERE author_send = %s AND author_receive = %s", (author_send, author_receive))
    existing_request = cursor.fetchone()

    if existing_request:
        return jsonify({'message': 'Follow request already sent'})

    cursor.execute("INSERT INTO follow_requests (author_send, author_receive) VALUES (%s, %s)", (author_send, author_receive))
    conn.commit()
    
    return jsonify({'message': 'Follow request sent'})

def is_local_user(author_id):
    connection, cursor = get_db_connection()

    # Check if the author_id exists in the local authors table
    cursor.execute("SELECT 1 FROM authors WHERE author_id = %s LIMIT 1", (author_id,))
    exists = cursor.fetchone() is not None

    connection.close()

    return exists

def get_remote_author_info(author_id, server_url, username, password):
    auth = (username, password)
    response = requests.get(
        f'{server_url}/authors/{author_id}',
        auth=auth
    )
    if response.ok:
        return response.json()
    return None

@bp.route('/follow/show_requests', methods=['GET'])
def get_follow_requests():
    local_request = flask.request
    author_id = local_request.args.get('authorId')
    if not author_id:
        return jsonify({'followRequests': []})
    
    connection, cursor = get_db_connection()   

    cursor.execute(
        "SELECT f.author_send, f.host FROM follow_requests f "
        "WHERE f.author_receive = %s",
        (author_id,)    
    )

    follow_requests = cursor.fetchall()
    follow_requests = [dict(row) for row in follow_requests]
    print('FOLLOWS', follow_requests)

    # Fetch all usernames before closing the connection
    usernames = {}
    for request_entry in follow_requests:
        author_send = request_entry['author_send']
        cursor.execute("SELECT username FROM authors WHERE author_id = %s", (author_send,))
        local_user = cursor.fetchone()
        if local_user:
            usernames[author_send] = local_user['username']

    connection.close()

    follow_requests_list = []

    for request_entry in follow_requests:
        author_send = request_entry['author_send']
        host = request_entry['host']

        if host == 'local':
            print('local', author_send)
            username = usernames.get(author_send)
            if username:
                follow_requests_list.append({'id': author_send, 'username': username})
        elif host == 'https://cmput404-project-backend-tian-aaf1fa9b20e8.herokuapp.com/':
            print('tian', author_send)
            host = host.rstrip('/') #strip last slash
            remote_user_info = get_remote_author_info(
                author_send,
                host,
                username='cross-server',
                password='password'
            )
            if remote_user_info:
                follow_requests_list.append({
                    'id': remote_user_info['id'].split('/')[-1],
                    'username': remote_user_info['displayName']
                })
        elif host == 'https://cmput-average-21-b54788720538.herokuapp.com/api':
            print('tian', author_send)
            remote_user_info = get_remote_author_info(
                author_send,
                host,
                username='CtrlAltDefeat', 
                password='string' 
            )
            if remote_user_info:
                follow_requests_list.append({
                    'id': remote_user_info['id'].split('/')[-1],
                    'username': remote_user_info['displayName']
                })

        elif host == 'team3':
            pass

    print(follow_requests_list)
    return jsonify({'followRequests': follow_requests_list})


@bp.route('/follow/accept_request', methods=['POST'])
def accept_follow_request():
    data = request.get_json()
    author_followee = data.get('author_followee')  # The user who is accepting the request
    author_following = data.get('author_following')  # The user who sent the request

    conn, cursor = get_db_connection()

    cursor.execute("SELECT * FROM follow_requests WHERE author_send = %s AND author_receive = %s", (author_following, author_followee))
    existing_request = cursor.fetchone()

    if existing_request:
        host = existing_request["host"]  

        cursor.execute("INSERT INTO friends (author_followee, author_following, host) VALUES (%s, %s, %s)", (author_followee, author_following, host))

        cursor.execute("DELETE FROM follow_requests WHERE author_send = %s AND author_receive = %s", (author_following, author_followee))

        conn.commit()
        return jsonify({'message': 'Follow request accepted'})
    else:
        return jsonify({'message': 'Follow request not found'})


@bp.route('/follow/reject_request', methods=['POST'])
def reject_follow_request():
    data = request.get_json()
    author_followee = data.get('author_followee')  # The user who is rejecting the request
    author_following = data.get('author_following')  # The user who sent the request

    db, cursor = get_db_connection()   

    # Check if the follow request exists
    cursor.execute("SELECT * FROM follow_requests WHERE author_send = %s AND author_receive = %s", (author_following, author_followee))
    existing_request = cursor.fetchone()

    if existing_request:
        cursor.execute("DELETE FROM follow_requests WHERE author_send = %s AND author_receive = %s", (author_following, author_followee))

        db.commit()
        return jsonify({'message': 'Follow request rejected'})
    else:
        return jsonify({'message': 'Follow request not found'})

@bp.route('/follow/unfollow', methods=['POST'])
def unfollow():
    data = request.get_json()
    author_unfollow = data.get('author_unfollow')
    author_unfollower = data.get('author_unfollower')

    db, cursor = get_db_connection()   

    cursor.execute("DELETE FROM friends WHERE author_following = %s AND author_followee = %s", (author_unfollower, author_unfollow))
    db.commit()

    return jsonify({'message': 'Unfollowed successfully'})


# REMOTE
@bp.route('/authors/<string:author_id>/followers', methods=['GET'])
def get_followers(author_id):
    try:
        db, cursor = get_db_connection()        

        query = """
            SELECT A.*
            FROM authors A
            JOIN friends F ON A.author_id = F.author_following
            WHERE F.author_followee = %s;
        """
        cursor.execute(query, (author_id,))
        followers = cursor.fetchall()        
        followers_list = [
            {
                "type": "author",
                "id": follower['author_id'],
                "url": f"{request.root_url}/authors/{follower['author_id']}",
                "host": request.root_url,
                "displayName": follower['username'],
                "github": f"https://github.com/{follower['github']}" if follower['github'] is not None else None,
            }
            for follower in followers
        ]

        response_data = {"type": "followers", "items": followers_list}

        return jsonify(response_data), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        db.close()

# REMOTE
@bp.route('/authors/<string:author_id>/followers/<string:foreign_author_id>', methods=['PUT'])
def add_follower(author_id, foreign_author_id):
    db = get_db()
    cursor = db.cursor()

    # Check if the authors exist
    cursor.execute("SELECT * FROM authors WHERE author_id = ? OR author_id = ?", (author_id, foreign_author_id))
    authors_exist = cursor.fetchall()

    if len(authors_exist) != 2:
        return jsonify({'message': 'One or both authors do not exist'}), 404

    # Check if the friendship already exists
    cursor.execute("SELECT * FROM friends WHERE author_following = ? AND author_followee = ?", (foreign_author_id, author_id))
    existing_friendship = cursor.fetchone()

    if existing_friendship:
        return jsonify({'message': 'The foreign author is already a follower'}), 400

    # Insert the new friendship
    cursor.execute("INSERT INTO friends (author_following, author_followee) VALUES (?, ?)", (foreign_author_id, author_id))
    db.commit()

    return jsonify({'message': f'{foreign_author_id} is now a follower of {author_id}'}), 200

# REMOTE
@bp.route('/authors/<string:author_id>/followers/<string:foreign_author_id>', methods=['GET'])
def check_follower(author_id, foreign_author_id):
    db = get_db()
    cursor = db.cursor()

    # Check if the authors exist
    cursor.execute("SELECT * FROM authors WHERE author_id = ? OR author_id = ?", (author_id, foreign_author_id))
    authors_exist = cursor.fetchall()

    if len(authors_exist) != 2:
        return jsonify({'message': 'One or both authors do not exist'}), 404

    # Check if the friendship exists
    cursor.execute("SELECT * FROM friends WHERE author_following = ? AND author_followee = ?", (foreign_author_id, author_id))
    existing_friendship = cursor.fetchone()

    if existing_friendship:
        return jsonify({'is_follower': True}), 200
    else:
        return jsonify({'is_follower': False}), 200

@bp.route('/authors/<string:author_id>/followers/<string:foreign_author_id>', methods=['DELETE'])
def remove_follower(author_id, foreign_author_id):
    db = get_db()
    cursor = db.cursor()

    # Check if the authors exist
    cursor.execute("SELECT * FROM authors WHERE author_id = ? OR author_id = ?", (author_id, foreign_author_id))
    authors_exist = cursor.fetchall()

    if len(authors_exist) != 2:
        return jsonify({'message': 'One or both authors do not exist'}), 404

    # Check if the friendship exists
    cursor.execute("SELECT * FROM friends WHERE author_following = ? AND author_followee = ?", (foreign_author_id, author_id))
    existing_friendship = cursor.fetchone()

    if existing_friendship:
        # Remove the friendship
        cursor.execute("DELETE FROM friends WHERE author_following = ? AND author_followee = ?", (foreign_author_id, author_id))
        db.commit()

        return jsonify({'message': f'{foreign_author_id} is no longer a follower of {author_id}'}), 200
    else:
        return jsonify({'message': 'The foreign author is not a follower'}), 400