from .app import create_app

def app(environ, start_response):
    app = create_app()
    app.run(host="0.0.0.0", debug=True)

if __name__ == '__main__':
    app("","")