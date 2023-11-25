from .app import create_app

def app(environ, start_response):
    # 33507 = Flask port on Heroku
    app = create_app()
    app.run(host="0.0.0.0", port=33507, debug=True)

if __name__ == '__main__':
    app("","")