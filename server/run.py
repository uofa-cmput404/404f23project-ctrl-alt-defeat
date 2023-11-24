from .app import create_app

def app():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    app()