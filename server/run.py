from .app import create_app

def app(environ, start_response):
    app = create_app()
    app.run(port=33507, debug=True)
    # 33507 = Flask port on Heroku

if __name__ == '__main__':
    app("","")