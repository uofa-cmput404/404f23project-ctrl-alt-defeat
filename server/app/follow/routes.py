from app.follow import bp
from flask import request, g, jsonify
import sqlite3

# Hard coded for now
HOST = "http://127.0.0.1:5000"

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

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT author_id, username FROM authors WHERE username LIKE ?", ('%' + search_query + '%',))
    users = cursor.fetchall()

    if users:
        user_list = [{'id': user[0], 'username': user[1]} for user in users]
        return jsonify({'users': user_list})
    else:
        return jsonify({'users': []})
    
@bp.route('/follow/follow_request', methods=['POST'])
def follow_request():
    data = request.get_json()
    author_send = data.get('author_send')
    author_receive = data.get('author_receive')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM friends WHERE author_following = ? AND author_followee = ?", (author_send, author_receive))
    existing_friendship = cursor.fetchone()

    if existing_friendship:
        return jsonify({'message': 'Already following'})

    cursor.execute("SELECT * FROM follow_requests WHERE author_send = ? AND author_receive = ?", (author_send, author_receive))
    existing_request = cursor.fetchone()

    if existing_request:
        return jsonify({'message': 'Follow request already sent'})

    cursor.execute("INSERT INTO follow_requests (author_send, author_receive) VALUES (?, ?)", (author_send, author_receive))
    db.commit()
    
    return jsonify({'message': 'Follow request sent'})

@bp.route('/follow/show_requests', methods=['GET'])
def get_follow_requests():
    author_id = request.args.get('authorId')
    if not author_id:
        return jsonify({'followRequests': []})
    
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT f.author_send, a.username FROM follow_requests f "
        "INNER JOIN authors a ON f.author_send = a.author_id "
        "WHERE f.author_receive = ?",
        (author_id,)
    )

    follow_requests = cursor.fetchall()
    connection.close()

    if follow_requests:
        follow_requests_list = [{'id': request[0], 'username': request[1]} for request in follow_requests]
        return jsonify({'followRequests': follow_requests_list})
    else:
        return jsonify({'followRequests': []})

@bp.route('/follow/accept_request', methods=['POST'])
def accept_follow_request():
    data = request.get_json()
    author_followee = data.get('author_followee')  # The user who is accepting the request
    author_following = data.get('author_following')  # The user who sent the request

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM follow_requests WHERE author_send = ? AND author_receive = ?", (author_following, author_followee))
    existing_request = cursor.fetchone()

    if existing_request:
        cursor.execute("INSERT INTO friends (author_followee, author_following) VALUES (?, ?)", (author_followee, author_following))

        cursor.execute("DELETE FROM follow_requests WHERE author_send = ? AND author_receive = ?", (author_following, author_followee))

        db.commit()
        return jsonify({'message': 'Follow request accepted'})
    else:
        return jsonify({'message': 'Follow request not found'})

@bp.route('/follow/reject_request', methods=['POST'])
def reject_follow_request():
    data = request.get_json()
    author_followee = data.get('author_followee')  # The user who is rejecting the request
    author_following = data.get('author_following')  # The user who sent the request

    db = get_db()
    cursor = db.cursor()

    # Check if the follow request exists
    cursor.execute("SELECT * FROM follow_requests WHERE author_send = ? AND author_receive = ?", (author_following, author_followee))
    existing_request = cursor.fetchone()

    if existing_request:
        cursor.execute("DELETE FROM follow_requests WHERE author_send = ? AND author_receive = ?", (author_following, author_followee))

        db.commit()
        return jsonify({'message': 'Follow request rejected'})
    else:
        return jsonify({'message': 'Follow request not found'})

@bp.route('/follow/unfollow', methods=['POST'])
def unfollow():
    data = request.get_json()
    author_unfollow = data.get('author_unfollow')
    author_unfollower = data.get('author_unfollower')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM friends WHERE author_following = ? AND author_followee = ?", (author_unfollower, author_unfollow))
    db.commit()

    return jsonify({'message': 'Unfollowed successfully'})


# REMOTE
@bp.route('/authors/<string:author_id>/followers', methods=['GET'])
def get_followers(author_id):
    try:
        db = get_db()
        cursor = db.cursor()

        query = """
            SELECT A.*
            FROM authors A
            JOIN friends F ON A.author_id = F.author_following
            WHERE F.author_followee = ?
        """
        followers = cursor.execute(query, (author_id,)).fetchall()

        followers_list = [
            {
                "type": "author",
                "id": follower['author_id'],
                "url": f"{HOST}/authors/{follower['author_id']}",
                "host": HOST,
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