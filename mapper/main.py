from flask import Flask
from flask_bootstrap import Bootstrap

from urls import initialize_flask_routes


def create_app():
    app = Flask(__name__,
                static_folder='./static',
                template_folder='./templates')
    initialize_flask_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
