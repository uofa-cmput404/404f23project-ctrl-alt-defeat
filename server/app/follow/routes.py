from . import bp
from flask import request, g, jsonify
import sqlite3
from ..dbase import get_db_connection

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@bp.route('/usersearch', methods=['GET'])
def user_search():
    search_query = request.args.get('query')
    if not search_query:
        return jsonify({'users': []})

    conn, cursor = get_db_connection()

    cursor.execute("SELECT author_id, username FROM authors WHERE username LIKE %s", ('%' + search_query + '%',))
    users = cursor.fetchall()
    users = [dict(row) for row in users]

    print(users)

    if users:        
        user_list = [{'id': user["author_id"], 'username': user["username"]} for user in users]
        return jsonify({'users': user_list})
    else:
        return jsonify({'users': []})
    
@bp.route('/follow_request', methods=['POST'])
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

@bp.route('/show_requests', methods=['GET'])
def get_follow_requests():
    author_id = request.args.get('authorId')
    if not author_id:
        return jsonify({'followRequests': []})
    
    connection, cursor = get_db_connection()   

    cursor.execute(
        "SELECT f.author_send, a.username FROM follow_requests f "
        "INNER JOIN authors a ON f.author_send = a.author_id "
        "WHERE f.author_receive = %s",
        (author_id,)
    )

    follow_requests = cursor.fetchall()
    follow_requests = [dict(row) for row in follow_requests]

    connection.close()

    if follow_requests:
        follow_requests_list = [{'id': request["author_send"], 'username': request["username"]} for request in follow_requests]
        return jsonify({'followRequests': follow_requests_list})
    else:
        return jsonify({'followRequests': []})

@bp.route('/accept_request', methods=['POST'])
def accept_follow_request():
    data = request.get_json()
    author_followee = data.get('author_followee')  # The user who is accepting the request
    author_following = data.get('author_following')  # The user who sent the request

    conn, cursor = get_db_connection()   

    cursor.execute("SELECT * FROM follow_requests WHERE author_send = %s AND author_receive = %s", (author_following, author_followee))
    existing_request = cursor.fetchone()

    if existing_request:
        cursor.execute("INSERT INTO friends (author_followee, author_following) VALUES (%s, %s)", (author_followee, author_following))

        cursor.execute("DELETE FROM follow_requests WHERE author_send = %s AND author_receive = %s", (author_following, author_followee))

        conn.commit()
        return jsonify({'message': 'Follow request accepted'})
    else:
        return jsonify({'message': 'Follow request not found'})

@bp.route('/reject_request', methods=['POST'])
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

@bp.route('/unfollow', methods=['POST'])
def unfollow():
    data = request.get_json()
    author_unfollow = data.get('author_unfollow')
    author_unfollower = data.get('author_unfollower')

    db, cursor = get_db_connection()   

    cursor.execute("DELETE FROM friends WHERE author_following = %s AND author_followee = %s", (author_unfollower, author_unfollow))
    db.commit()

    return jsonify({'message': 'Unfollowed successfully'})
