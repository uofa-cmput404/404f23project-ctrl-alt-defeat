from app.posts import bp
import json
from app.db import get_db_connection

@bp.route('/')
def index():
    data = ""
    try:
        conn = get_db_connection()
        
        posts = conn.execute('SELECT * FROM posts').fetchall()                        

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