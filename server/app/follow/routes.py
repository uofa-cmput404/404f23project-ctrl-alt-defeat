from app.follow import bp
from flask import request, g, jsonify
import sqlite3

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

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT author_id, username FROM authors WHERE username LIKE ?", ('%' + search_query + '%',))
    users = cursor.fetchall()

    if users:
        user_list = [{'id': user[0], 'username': user[1]} for user in users]
        return jsonify({'users': user_list})
    else:
        return jsonify({'users': []})
    
@bp.route('/follow_request', methods=['POST'])
def follow_request():
    data = request.get_json()
    author_send = data.get('author_send')
    author_receive = data.get('author_receive')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM follow_requests WHERE author_send = ? AND author_receive = ?", (author_send, author_receive))
    existing_request = cursor.fetchone()

    if existing_request:
        return jsonify({'message': 'Follow request already sent'})

    cursor.execute("INSERT INTO follow_requests (author_send, author_receive) VALUES (?, ?)", (author_send, author_receive))
    db.commit()
    
    return jsonify({'message': 'Follow request sent'})