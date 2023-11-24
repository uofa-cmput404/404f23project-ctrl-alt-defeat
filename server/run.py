from .app import create_app

def app(environ, start_response):
    # 33507 = Flask port on Heroku
    app = create_app()
    app.run(port=33507, debug=True)

if __name__ == '__main__':
    app("","")