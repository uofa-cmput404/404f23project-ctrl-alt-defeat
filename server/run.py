from .app import create_app

def app(environ, start_response):
    app = create_app()
    app.run()

if __name__ == '__main__':
    app("","")